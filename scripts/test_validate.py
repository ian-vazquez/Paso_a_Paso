#!/usr/bin/env python3
"""
Tests for scripts/validate.py. Standard library only (unittest).

    python scripts/test_validate.py

Each test writes a small fixture file to a temp directory and runs validate.py's
main() against it with an explicit --today, so the date-sensitive rules are
tested against a fixed calendar instead of whenever the test happens to run.
The real data/scholarships.json is never modified.
"""

from __future__ import annotations

import copy
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import validate  # noqa: E402

TODAY = "2026-10-15"

# A minimal entry that passes cleanly on TODAY. Individual tests copy it and
# break exactly one thing, so a failure points at one rule.
BASE_ENTRY = {
    "id": "test-entry",
    "name": "Test Entry",
    "sponsor": "Test Sponsor",
    "amount_min": 500,
    "amount_max": 2500,
    "amount_display": {"en": "$500–$2,500", "es": "$500–$2,500"},
    "renewable": False,
    "deadline": "2027-03-01",
    "cycle_status": "open",
    "opens_month": 9,
    "categories": ["merit"],
    "grade_levels": ["hs_senior"],
    "residency": "el_paso_county",
    "districts": [],
    "schools": [],
    "eligible_institutions": [],
    "degree_types": ["bachelor"],
    "gpa_min": 3.0,
    "fields_of_study": [],
    "demographics": [],
    "requirements": {
        "essay_required": True,
        "recs_needed": 2,
        "fafsa_required": True,
        "accepts_tasfa": True,
        "citizenship_required": False,
        "interview": False,
        "other": {"en": "", "es": ""},
    },
    "application_language": "en",
    "source_url": "https://example.com/source",
    "apply_url": "https://example.com/apply",
    "summary": {"en": "A test entry.", "es": "Una entrada de prueba."},
    "notes": {"en": "", "es": ""},
    "translation_reviewed": True,
    "last_verified": TODAY,
}


def entry(**overrides):
    """BASE_ENTRY with top-level fields replaced."""
    result = copy.deepcopy(BASE_ENTRY)
    result.update(overrides)
    return result


class ValidateTestCase(unittest.TestCase):
    """Runs validate.py against fixture text and captures its output."""

    def run_validator(self, content, *, today=TODAY):
        """Returns (exit_code, stdout). `content` is a list of entries or raw text."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.json"
            raw = content if isinstance(content, str) else json.dumps(content, indent=2)
            path.write_text(raw, encoding="utf-8")

            buffer = io.StringIO()
            with redirect_stdout(buffer):
                code = validate.main(["--file", str(path), "--today", today])
            return code, buffer.getvalue()

    def assertClean(self, output):
        """No ERRORS block was printed."""
        self.assertNotIn("ERRORS", output, msg=f"unexpected errors in:\n{output}")


class TestBaseFixture(ValidateTestCase):
    def test_base_entry_passes_with_no_problems(self):
        code, out = self.run_validator([entry()])
        self.assertEqual(code, 0, msg=out)
        self.assertClean(out)
        self.assertIn("PASS — 0 errors, 0 warning(s).", out)


class TestAmountRange(ValidateTestCase):
    """Rule 2: amount_min greater than amount_max is an ERROR."""

    def test_reversed_amount_range_is_an_error(self):
        code, out = self.run_validator([entry(amount_min=2500, amount_max=500)])
        self.assertEqual(code, 1, msg=out)
        self.assertIn("amount_min (2500) is greater than amount_max (500)", out)

    def test_equal_amounts_are_fine(self):
        code, out = self.run_validator([entry(amount_min=1000, amount_max=1000)])
        self.assertEqual(code, 0, msg=out)
        self.assertClean(out)

    def test_null_amounts_are_not_compared(self):
        code, out = self.run_validator([entry(amount_min=None, amount_max=None)])
        self.assertEqual(code, 0, msg=out)
        self.assertClean(out)

    def test_one_null_amount_is_not_compared(self):
        code, out = self.run_validator([entry(amount_min=2500, amount_max=None)])
        self.assertEqual(code, 0, msg=out)
        self.assertClean(out)


class TestMissingTimingFacts(ValidateTestCase):
    """Rule 3: open with no deadline, and upcoming with no opens_month, warn."""

    def test_open_without_deadline_warns(self):
        code, out = self.run_validator([entry(cycle_status="open", deadline=None)])
        self.assertEqual(code, 0, msg=out)
        self.assertClean(out)
        self.assertIn("cycle_status is 'open' but deadline is null", out)

    def test_upcoming_without_opens_month_warns(self):
        code, out = self.run_validator(
            [entry(cycle_status="upcoming", opens_month=None, deadline=None)]
        )
        self.assertEqual(code, 0, msg=out)
        self.assertClean(out)
        self.assertIn("cycle_status is 'upcoming' but opens_month is null", out)

    def test_open_with_deadline_does_not_warn(self):
        code, out = self.run_validator([entry(cycle_status="open", deadline="2027-03-01")])
        self.assertEqual(code, 0, msg=out)
        self.assertIn("PASS — 0 errors, 0 warning(s).", out)

    def test_closed_reopens_without_deadline_does_not_warn(self):
        code, out = self.run_validator([entry(cycle_status="closed_reopens", deadline=None)])
        self.assertEqual(code, 0, msg=out)
        self.assertIn("PASS — 0 errors, 0 warning(s).", out)


class TestExpiredOpenEntry(ValidateTestCase):
    """Rule 4: open with a past deadline WARNS, and must not block a deploy."""

    def test_expired_open_entry_warns_but_exits_zero(self):
        code, out = self.run_validator([entry(cycle_status="open", deadline="2026-09-01")])
        self.assertEqual(code, 0, msg=out)
        self.assertClean(out)
        self.assertIn("the deadline passed 44 day(s) ago", out)

    def test_expired_open_entry_does_not_block_a_valid_sibling(self):
        """The real point of the downgrade: one stale entry, deploy still ships."""
        code, out = self.run_validator(
            [
                entry(id="expired-entry", cycle_status="open", deadline="2026-09-01"),
                entry(id="healthy-entry"),
            ]
        )
        self.assertEqual(code, 0, msg=out)
        self.assertClean(out)

    def test_deadline_soon_warns(self):
        code, out = self.run_validator([entry(deadline="2026-10-20")])
        self.assertEqual(code, 0, msg=out)
        self.assertIn("deadline is in 5 day(s)", out)


class TestMalformedFile(ValidateTestCase):
    """Rule 1: a syntax error exits 2 with a readable message, not a traceback."""

    def test_missing_comma_exits_two(self):
        broken = '[{"id": "a" "name": "B"}]'  # missing comma after "a"
        code, out = self.run_validator(broken)
        self.assertEqual(code, 2, msg=out)
        self.assertIn("is not valid JSON", out)
        self.assertIn("Nothing was validated", out)

    def test_top_level_object_is_an_error(self):
        code, out = self.run_validator('{"id": "a"}')
        self.assertEqual(code, 1, msg=out)
        self.assertIn("top level of the file must be a list", out)


class TestRealDataFile(ValidateTestCase):
    """The committed data file must always be error-free."""

    def test_committed_data_file_has_no_errors(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = validate.main(["--today", TODAY])
        self.assertEqual(code, 0, msg=buffer.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
