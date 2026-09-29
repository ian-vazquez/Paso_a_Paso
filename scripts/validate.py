#!/usr/bin/env python3
"""
Validate data/scholarships.json against the schema in CLAUDE.md section 4.

Standard library only. Run it from anywhere:

    python scripts/validate.py
    python scripts/validate.py --file path/to/other.json
    python scripts/validate.py --today 2026-10-15   # for testing date rules

Exit codes:
    0  no errors (warnings may still have been printed)
    1  at least one error — CI fails and the deploy is blocked
    2  the file is missing or is not valid JSON

The split between errors and warnings is deliberate. Errors mean the data is
malformed, contradicts itself, or would make the site show something untrue.
Warnings mean the data is well-formed but wants a human's attention — a stale
verification, an untranslated summary, a deadline about to pass. Warnings never
block a deploy, because a stale entry that honestly shows its "last verified"
date is still better than a site that cannot ship a bug fix.

The enum sets below are the approval gate: adding a new field-of-study or
demographic tag means editing this file, which shows up in a diff for review.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_FILE = REPO_ROOT / "data" / "scholarships.json"

# Warning thresholds (CLAUDE.md section 4).
STALE_VERIFICATION_DAYS = 45
DEADLINE_SOON_DAYS = 14

# `requirements` has 7 fields: 5 yes/no flags, the numeric recs_needed, and the
# bilingual `other` prose block. Only the 6 non-prose fields carry facts we can
# count as known-or-unknown, so the "needs more research" warning looks at those
# 6 and ignores `other`.
COUNTABLE_REQUIREMENT_FIELDS = 6
MANY_NULL_REQUIREMENTS = 4  # warn at 4 or more of those 6 being null

# ---------------------------------------------------------------------------
# Allowed values. Changing any of these is a schema change: see CLAUDE.md §7.
# ---------------------------------------------------------------------------

CYCLE_STATUS = {"open", "upcoming", "closed_reopens", "rolling", "unknown"}
CATEGORIES = {"merit", "need_based", "first_gen", "regional", "demographic", "field_specific"}
GRADE_LEVELS = {"hs_junior", "hs_senior", "college"}
RESIDENCY = {"el_paso_county", "specific_districts", "specific_schools", "texas", "national"}
DEGREE_TYPES = {"associate", "bachelor", "trade_technical"}
FIELDS_OF_STUDY = {"stem", "cs", "nursing", "education", "hospitality", "business"}
DEMOGRAPHICS = {"hispanic", "first_gen", "female", "african_american", "aapi", "native_american"}
APPLICATION_LANGUAGE = {"en", "es", "both"}

ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ISO_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Every key an entry must have, in schema order. Presence is checked against
# this list; the type of each is checked by check_entry() below.
ENTRY_FIELDS = [
    "id",
    "name",
    "sponsor",
    "amount_min",
    "amount_max",
    "amount_display",
    "renewable",
    "deadline",
    "cycle_status",
    "opens_month",
    "categories",
    "grade_levels",
    "residency",
    "districts",
    "schools",
    "eligible_institutions",
    "degree_types",
    "gpa_min",
    "fields_of_study",
    "demographics",
    "requirements",
    "application_language",
    "source_url",
    "apply_url",
    "summary",
    "notes",
    "translation_reviewed",
    "last_verified",
]

REQUIREMENT_FLAGS = [
    "essay_required",
    "fafsa_required",
    "accepts_tasfa",
    "citizenship_required",
    "interview",
]
COUNTABLE_REQUIREMENTS = [*REQUIREMENT_FLAGS, "recs_needed"]
REQUIREMENT_FIELDS = [*COUNTABLE_REQUIREMENTS, "other"]

# A weighted GPA can exceed 4.0, so the ceiling is generous; it exists only to
# catch a percentage (e.g. 85) typed into a GPA field.
GPA_MAX = 5.0


class Report:
    """Collects problems keyed to the entry they came from."""

    def __init__(self) -> None:
        self.errors: list[tuple[str, str]] = []
        self.warnings: list[tuple[str, str]] = []

    def error(self, entry_id: str, message: str) -> None:
        self.errors.append((entry_id, message))

    def warn(self, entry_id: str, message: str) -> None:
        self.warnings.append((entry_id, message))


# ---------------------------------------------------------------------------
# Small field checkers. Each reports at most one problem and returns nothing;
# the caller keeps going so one bad entry produces a full list of its problems
# rather than only the first.
# ---------------------------------------------------------------------------


def type_name(value) -> str:
    if value is None:
        return "null"
    return {
        bool: "boolean",
        int: "number",
        float: "number",
        str: "string",
        list: "list",
        dict: "object",
    }.get(type(value), type(value).__name__)


def is_number(value) -> bool:
    """bool is a subclass of int in Python, so exclude it explicitly."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def check_string(report: Report, eid: str, field: str, value, *, allow_empty: bool) -> None:
    if not isinstance(value, str):
        report.error(eid, f"{field}: must be a string, got {type_name(value)}")
    elif not allow_empty and not value.strip():
        report.error(eid, f"{field}: must not be empty")


def check_bool_or_null(report: Report, eid: str, field: str, value) -> None:
    if value is not None and not isinstance(value, bool):
        report.error(eid, f"{field}: must be true, false, or null — got {type_name(value)}")


def check_number_or_null(
    report: Report, eid: str, field: str, value, *, minimum=None, maximum=None
) -> None:
    if value is None:
        return
    if not is_number(value):
        report.error(eid, f"{field}: must be a number or null — got {type_name(value)}")
        return
    if minimum is not None and value < minimum:
        report.error(eid, f"{field}: {value} is below the minimum of {minimum}")
    if maximum is not None and value > maximum:
        report.error(eid, f"{field}: {value} is above the maximum of {maximum}")


def check_int_or_null(
    report: Report, eid: str, field: str, value, *, minimum=None, maximum=None
) -> None:
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, int):
        report.error(eid, f"{field}: must be a whole number or null — got {type_name(value)}")
        return
    if minimum is not None and value < minimum:
        report.error(eid, f"{field}: {value} is below the minimum of {minimum}")
    if maximum is not None and value > maximum:
        report.error(eid, f"{field}: {value} is above the maximum of {maximum}")


def check_bilingual(report: Report, eid: str, field: str, value) -> None:
    """A {"en": str, "es": str} pair. Both keys required; empty strings allowed."""
    if not isinstance(value, dict):
        report.error(eid, f"{field}: must be an object with 'en' and 'es' — got {type_name(value)}")
        return
    for lang in ("en", "es"):
        if lang not in value:
            report.error(eid, f"{field}: missing '{lang}'")
        elif not isinstance(value[lang], str):
            report.error(eid, f"{field}.{lang}: must be a string, got {type_name(value[lang])}")
    for extra in sorted(set(value) - {"en", "es"}):
        report.error(eid, f"{field}: unexpected key '{extra}' (only 'en' and 'es' are allowed)")


def check_enum(report: Report, eid: str, field: str, value, allowed: set[str]) -> None:
    if not isinstance(value, str):
        report.error(eid, f"{field}: must be a string, got {type_name(value)}")
    elif value not in allowed:
        report.error(eid, f"{field}: '{value}' is not one of {sorted(allowed)}")


def check_enum_list(
    report: Report, eid: str, field: str, value, allowed: set[str], *, min_items: int = 0
) -> None:
    if not isinstance(value, list):
        report.error(eid, f"{field}: must be a list, got {type_name(value)}")
        return
    if len(value) < min_items:
        report.error(eid, f"{field}: needs at least {min_items} value(s)")
    for item in value:
        if not isinstance(item, str):
            report.error(eid, f"{field}: list items must be strings, got {type_name(item)}")
        elif item not in allowed:
            report.error(eid, f"{field}: '{item}' is not one of {sorted(allowed)}")
    for dup in sorted({v for v in value if isinstance(v, str) and value.count(v) > 1}):
        report.error(eid, f"{field}: '{dup}' is listed more than once")


def check_string_list(report: Report, eid: str, field: str, value) -> None:
    """A free-text list (districts, schools, eligible_institutions)."""
    if not isinstance(value, list):
        report.error(eid, f"{field}: must be a list, got {type_name(value)}")
        return
    for item in value:
        if not isinstance(item, str):
            report.error(eid, f"{field}: list items must be strings, got {type_name(item)}")
        elif not item.strip():
            report.error(eid, f"{field}: list items must not be empty strings")


def parse_date(report: Report, eid: str, field: str, value, *, allow_null: bool):
    """Returns a date, or None. Reports a problem and returns None if invalid."""
    if value is None:
        if not allow_null:
            report.error(eid, f"{field}: is required and must not be null")
        return None
    if not isinstance(value, str) or not ISO_DATE_PATTERN.match(value):
        report.error(eid, f"{field}: must be an ISO date like 2026-03-13 — got {value!r}")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        report.error(eid, f"{field}: '{value}' is not a real calendar date")
        return None


def check_https_url(report: Report, eid: str, field: str, value, *, allow_null: bool) -> None:
    if value is None:
        if not allow_null:
            report.error(eid, f"{field}: is required and must not be null")
        return
    if not isinstance(value, str):
        report.error(eid, f"{field}: must be a string, got {type_name(value)}")
    elif not value.startswith("https://"):
        report.error(eid, f"{field}: must start with https:// — got {value!r}")


# ---------------------------------------------------------------------------
# Entry validation
# ---------------------------------------------------------------------------


def check_entry(report: Report, entry, index: int, today: date) -> str | None:
    """Validates one entry. Returns its id (for duplicate detection) or None."""
    if not isinstance(entry, dict):
        report.error(f"entry #{index}", f"must be an object, got {type_name(entry)}")
        return None

    raw_id = entry.get("id")
    eid = raw_id if isinstance(raw_id, str) and raw_id.strip() else f"entry #{index} (no id)"

    for field in ENTRY_FIELDS:
        if field not in entry:
            report.error(eid, f"{field}: required field is missing")
    for extra in sorted(set(entry) - set(ENTRY_FIELDS)):
        report.error(eid, f"unexpected field '{extra}' — not in the schema")

    # --- identity and display text -----------------------------------------
    if isinstance(raw_id, str):
        if not ID_PATTERN.match(raw_id):
            report.error(
                eid,
                "id: use lowercase letters, numbers and single hyphens, e.g. 'sponsor-name-2026'",
            )
    elif "id" in entry:
        report.error(eid, f"id: must be a string, got {type_name(raw_id)}")

    check_string(report, eid, "name", entry.get("name"), allow_empty=False)
    check_string(report, eid, "sponsor", entry.get("sponsor"), allow_empty=False)

    # --- money --------------------------------------------------------------
    amount_min = entry.get("amount_min")
    amount_max = entry.get("amount_max")
    check_number_or_null(report, eid, "amount_min", amount_min, minimum=0)
    check_number_or_null(report, eid, "amount_max", amount_max, minimum=0)
    # A range that runs backwards is a contradiction in the data, not a
    # judgment call, so it is an error.
    if is_number(amount_min) and is_number(amount_max) and amount_min > amount_max:
        report.error(
            eid,
            f"amount_min ({amount_min}) is greater than amount_max ({amount_max})",
        )
    check_bilingual(report, eid, "amount_display", entry.get("amount_display"))
    check_bool_or_null(report, eid, "renewable", entry.get("renewable"))

    # --- timing -------------------------------------------------------------
    deadline = parse_date(report, eid, "deadline", entry.get("deadline"), allow_null=True)
    cycle_status = entry.get("cycle_status")
    check_enum(report, eid, "cycle_status", cycle_status, CYCLE_STATUS)
    opens_month = entry.get("opens_month")
    check_int_or_null(report, eid, "opens_month", opens_month, minimum=1, maximum=12)

    # --- who it is for ------------------------------------------------------
    check_enum_list(report, eid, "categories", entry.get("categories"), CATEGORIES, min_items=1)
    check_enum_list(report, eid, "grade_levels", entry.get("grade_levels"), GRADE_LEVELS)
    check_enum(report, eid, "residency", entry.get("residency"), RESIDENCY)
    check_string_list(report, eid, "districts", entry.get("districts"))
    check_string_list(report, eid, "schools", entry.get("schools"))
    check_string_list(report, eid, "eligible_institutions", entry.get("eligible_institutions"))
    check_enum_list(report, eid, "degree_types", entry.get("degree_types"), DEGREE_TYPES)
    check_number_or_null(report, eid, "gpa_min", entry.get("gpa_min"), minimum=0, maximum=GPA_MAX)
    check_enum_list(report, eid, "fields_of_study", entry.get("fields_of_study"), FIELDS_OF_STUDY)
    check_enum_list(report, eid, "demographics", entry.get("demographics"), DEMOGRAPHICS)

    # --- requirements -------------------------------------------------------
    requirements = entry.get("requirements")
    if not isinstance(requirements, dict):
        if "requirements" in entry:
            report.error(eid, f"requirements: must be an object, got {type_name(requirements)}")
        requirements = {}
    else:
        for field in REQUIREMENT_FIELDS:
            if field not in requirements:
                report.error(eid, f"requirements.{field}: required field is missing")
        for extra in sorted(set(requirements) - set(REQUIREMENT_FIELDS)):
            report.error(eid, f"requirements: unexpected field '{extra}' — not in the schema")
        for field in REQUIREMENT_FLAGS:
            check_bool_or_null(report, eid, f"requirements.{field}", requirements.get(field))
        check_int_or_null(
            report, eid, "requirements.recs_needed", requirements.get("recs_needed"), minimum=0
        )
        check_bilingual(report, eid, "requirements.other", requirements.get("other"))

    # --- language, links, prose --------------------------------------------
    check_enum(
        report, eid, "application_language", entry.get("application_language"), APPLICATION_LANGUAGE
    )
    check_https_url(report, eid, "source_url", entry.get("source_url"), allow_null=False)
    check_https_url(report, eid, "apply_url", entry.get("apply_url"), allow_null=True)

    summary = entry.get("summary")
    check_bilingual(report, eid, "summary", summary)
    if isinstance(summary, dict) and isinstance(summary.get("en"), str) and not summary["en"].strip():
        report.error(
            eid, "summary.en: must not be empty — the English summary is what every student sees"
        )

    check_bilingual(report, eid, "notes", entry.get("notes"))

    if not isinstance(entry.get("translation_reviewed"), bool):
        report.error(
            eid,
            "translation_reviewed: must be true or false, got "
            f"{type_name(entry.get('translation_reviewed'))}",
        )

    last_verified = parse_date(
        report, eid, "last_verified", entry.get("last_verified"), allow_null=False
    )

    # --- warnings -----------------------------------------------------------
    if isinstance(summary, dict) and isinstance(summary.get("es"), str) and not summary["es"].strip():
        report.warn(eid, "summary.es is empty — the Spanish UI will fall back to the English summary")

    if entry.get("translation_reviewed") is False:
        report.warn(eid, "translation_reviewed is false — Spanish text has not been approved yet")

    if last_verified is not None:
        age = (today - last_verified).days
        if age > STALE_VERIFICATION_DAYS:
            report.warn(
                eid,
                f"last_verified is {age} days old (over {STALE_VERIFICATION_DAYS}) — re-check the source",
            )
        elif age < 0:
            report.warn(
                eid, f"last_verified {last_verified.isoformat()} is in the future — is that right?"
            )

    # Missing timing facts: well-formed, but the one thing a student most needs.
    if cycle_status == "open" and deadline is None:
        report.warn(eid, "cycle_status is 'open' but deadline is null — students cannot tell how long they have")
    if cycle_status == "upcoming" and opens_month is None:
        report.warn(eid, "cycle_status is 'upcoming' but opens_month is null — students cannot tell when to come back")

    if deadline is not None:
        days_left = (deadline - today).days
        if 0 <= days_left <= DEADLINE_SOON_DAYS:
            report.warn(eid, f"deadline is in {days_left} day(s) — confirm it before the next deploy")
        elif days_left < 0 and cycle_status == "open":
            # A warning, not an error: an entry nobody got around to updating
            # must not block an unrelated deploy during workshop week. The
            # Phase 2 UI is responsible for not showing this as open.
            report.warn(
                eid,
                f"cycle_status is 'open' but the deadline passed {abs(days_left)} day(s) ago "
                "— update cycle_status",
            )
        elif days_left < 0 and cycle_status == "upcoming":
            report.warn(
                eid,
                f"cycle_status is 'upcoming' but the deadline passed {abs(days_left)} day(s) ago "
                "— update cycle_status",
            )

    if isinstance(requirements, dict):
        null_count = sum(1 for field in COUNTABLE_REQUIREMENTS if requirements.get(field) is None)
        if null_count >= MANY_NULL_REQUIREMENTS:
            report.warn(
                eid,
                f"{null_count} of the {COUNTABLE_REQUIREMENT_FIELDS} yes/no requirement fields are "
                "null — the entry may need more research",
            )

    if isinstance(raw_id, str) and raw_id.startswith("example-"):
        report.warn(eid, "this is a placeholder example entry — delete it before launch")

    return raw_id if isinstance(raw_id, str) else None


# ---------------------------------------------------------------------------
# Runner and output
# ---------------------------------------------------------------------------


def validate(entries, today: date) -> Report:
    report = Report()

    if not isinstance(entries, list):
        report.error(
            "file", f"the top level of the file must be a list of entries, got {type_name(entries)}"
        )
        return report

    seen: dict[str, int] = {}
    for index, entry in enumerate(entries):
        entry_id = check_entry(report, entry, index, today)
        if entry_id is not None:
            if entry_id in seen:
                report.error(entry_id, f"duplicate id — also used by entry #{seen[entry_id]}")
            else:
                seen[entry_id] = index

    return report


def print_group(title: str, problems: list[tuple[str, str]]) -> None:
    print(f"\n{title} ({len(problems)})")
    current = None
    for entry_id, message in problems:
        if entry_id != current:
            print(f"  {entry_id}")
            current = entry_id
        print(f"    - {message}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate the scholarship data file.")
    parser.add_argument(
        "--file", type=Path, default=DEFAULT_DATA_FILE, help="path to the JSON data file"
    )
    parser.add_argument(
        "--today", help="override today's date (YYYY-MM-DD) when testing the date rules"
    )
    args = parser.parse_args(argv)

    # Windows consoles default to a legacy code page, which turns em-dashes and
    # Spanish accents into mojibake. Force UTF-8 so messages that quote Spanish
    # scholarship text stay readable. StringIO (used by the tests) has no
    # reconfigure, hence the guard.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    # date.today() reads the machine's local clock. On a GitHub Actions runner
    # that clock is UTC, which is 6-7 hours ahead of El Paso, so an evening run
    # can already be "tomorrow" there. The only effect is that a deadline or
    # staleness warning may appear a day early, which is the harmless direction,
    # so this is left alone on purpose.
    today = date.fromisoformat(args.today) if args.today else date.today()

    print("Paso a Paso — scholarship data validation")
    try:
        display_path = args.file.resolve().relative_to(REPO_ROOT)
    except ValueError:
        display_path = args.file
    print(f"File:  {display_path}")
    print(f"Today: {today.isoformat()}")

    try:
        raw = args.file.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"\nFAIL — file not found: {args.file}")
        return 2
    except OSError as exc:
        print(f"\nFAIL — could not read {args.file}: {exc}")
        return 2

    try:
        entries = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"\nFAIL — {display_path} is not valid JSON.")
        print(f"       Line {exc.lineno}, column {exc.colno}: {exc.msg}")
        print("       Nothing was validated. Fix the JSON syntax and run again.")
        return 2

    report = validate(entries, today)
    print(f"Entries: {len(entries) if isinstance(entries, list) else 0}")

    if report.errors:
        print_group("ERRORS — these block the deploy", report.errors)
    if report.warnings:
        print_group("WARNINGS — these do not block the deploy", report.warnings)

    print()
    if report.errors:
        print(f"FAIL — {len(report.errors)} error(s), {len(report.warnings)} warning(s).")
        return 1

    print(f"PASS — 0 errors, {len(report.warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
