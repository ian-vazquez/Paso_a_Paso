#!/usr/bin/env python3
"""
Check that the two i18n files stay in step with each other and with the page.

    python scripts/check_i18n.py

Standard library only. Exit 0 if everything lines up, 1 if it does not.

Why this exists: "bilingual from the start" fails quietly. A key added to
en.json and forgotten in es.json does not crash anything — src/i18n.js falls
back to English — so a Spanish visitor just sees an English word sitting in the
middle of a Spanish page, and nobody notices until a student does. CI catching
it is cheaper than a reviewer catching it.

Checks:
  1. en.json and es.json have exactly the same set of keys
  2. no value is an empty string (an empty translation is a silent blank)
  3. {placeholders} match between the two languages for every key
  4. every data-i18n / data-i18n-attr key used in index.html actually exists

Keys beginning with "_" are metadata (see the _meta block in es.json) and are
skipped everywhere, matching how src/i18n.js treats them.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EN_FILE = REPO_ROOT / "src" / "i18n" / "en.json"
ES_FILE = REPO_ROOT / "src" / "i18n" / "es.json"
HTML_FILE = REPO_ROOT / "index.html"

PLACEHOLDER_PATTERN = re.compile(r"\{(\w+)\}")


def flatten(node, prefix: str = "") -> dict[str, str]:
    """Nested dict -> {"card.deadline": "Deadline"}. Skips _ keys."""
    flat: dict[str, str] = {}
    for key, value in node.items():
        if key.startswith("_"):
            continue
        path = f"{prefix}{key}"
        if isinstance(value, dict):
            flat.update(flatten(value, path + "."))
        else:
            flat[path] = value
    return flat


def keys_used_in_html(html: str) -> set[str]:
    """Both data-i18n="x" and data-i18n-attr="placeholder:x,title:y"."""
    used = set(re.findall(r'data-i18n="([^"]+)"', html))
    for group in re.findall(r'data-i18n-attr="([^"]+)"', html):
        for pair in group.split(","):
            _, _, key = pair.partition(":")
            if key.strip():
                used.add(key.strip())
    return used


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("Paso a Paso — i18n consistency check")

    try:
        en = flatten(json.loads(EN_FILE.read_text(encoding="utf-8")))
        es = flatten(json.loads(ES_FILE.read_text(encoding="utf-8")))
    except json.JSONDecodeError as exc:
        print(f"\nFAIL — an i18n file is not valid JSON: {exc}")
        return 1
    except FileNotFoundError as exc:
        print(f"\nFAIL — {exc}")
        return 1

    html = HTML_FILE.read_text(encoding="utf-8")
    problems: list[str] = []

    print(f"en.json: {len(en)} keys")
    print(f"es.json: {len(es)} keys")

    # 1. Key parity -------------------------------------------------------
    for key in sorted(set(en) - set(es)):
        problems.append(f"es.json is missing '{key}' (a Spanish page would show the English text)")
    for key in sorted(set(es) - set(en)):
        problems.append(f"es.json has '{key}', which does not exist in en.json")

    # 2. Empty values -----------------------------------------------------
    for name, table in (("en.json", en), ("es.json", es)):
        for key in sorted(table):
            value = table[key]
            if not isinstance(value, str):
                problems.append(f"{name}: '{key}' must be a string, got {type(value).__name__}")
            elif not value.strip():
                problems.append(f"{name}: '{key}' is empty")

    # 3. Placeholder parity ------------------------------------------------
    for key in sorted(set(en) & set(es)):
        if not (isinstance(en[key], str) and isinstance(es[key], str)):
            continue
        en_slots = set(PLACEHOLDER_PATTERN.findall(en[key]))
        es_slots = set(PLACEHOLDER_PATTERN.findall(es[key]))
        if en_slots != es_slots:
            problems.append(
                f"'{key}': placeholders differ — en has {sorted(en_slots) or 'none'}, "
                f"es has {sorted(es_slots) or 'none'}"
            )

    # 4. Keys the page actually asks for ----------------------------------
    used = keys_used_in_html(html)
    print(f"index.html uses {len(used)} key(s)")
    for key in sorted(used - set(en)):
        problems.append(f"index.html uses '{key}', which is not in en.json")

    if problems:
        print(f"\nPROBLEMS ({len(problems)})")
        for problem in problems:
            print(f"  - {problem}")
        print(f"\nFAIL — {len(problems)} problem(s).")
        return 1

    print("\nPASS — key sets match, no empty strings, placeholders agree.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
