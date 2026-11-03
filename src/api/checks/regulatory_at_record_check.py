"""Check completeness of keyboard and assistive-technology session records for regulatory alerts.

Input is a JSON list of records from the acceptance kit's record table:
{"session": "S01", "role": "repairs", "tool": "NVDA 2025.1 with Firefox", "mode": "screen-reader",
 "chat_available": false, "result": "pass", "barrier": "", "workaround": ""}
The script only checks that the record set is complete and well formed and lists the findings to
route. It does not judge conformance. Human reviewers and the owner decide; a clean result here is
not acceptance of the WCAG 2.2 AA criterion.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROLES = (
    "repairs",
    "building-safety",
    "assessor",
    "programme",
    "finance-grants",
    "data-handlers",
    "suppliers",
)
MODES = ("keyboard-only", "screen-reader")
RESULTS = ("pass", "fail", "blocked")
# Suppliers get static guidance with no chat, so no chat-unavailable run applies.
NO_CHAT_ROLES = {"suppliers"}


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def check(records: list[dict[str, Any]]) -> dict[str, Any]:
    problems: list[str] = []
    findings: list[dict[str, str]] = []
    covered: set[tuple[str, str]] = set()
    chat_off: set[str] = set()
    for record in records:
        session, role, mode = _text(record.get("session")), record.get("role"), record.get("mode")
        result = record.get("result")
        if not session or role not in ROLES or mode not in MODES or result not in RESULTS:
            problems.append(f"Unusable session, role, mode or result: {record!r}")
            continue
        if not isinstance(record.get("chat_available"), bool):
            problems.append(f"{session}: chat_available must be true or false")
            continue
        if mode == "screen-reader" and not _text(record.get("tool")):
            problems.append(f"{session}: screen-reader record needs tool and version")
            continue
        if result != "pass":
            if not _text(record.get("barrier")):
                problems.append(f"{session}: {result} result needs the barrier in words")
                continue
            findings.append(
                {
                    "session": session,
                    "role": role,
                    "result": result,
                    "barrier": _text(record.get("barrier")),
                    "workaround": _text(record.get("workaround")) or "none recorded",
                }
            )
        covered.add((role, mode))
        if record["chat_available"] is False:
            chat_off.add(role)
    missing = [f"{role}/{mode}" for role in ROLES for mode in MODES if (role, mode) not in covered]
    if missing:
        problems.append(f"No usable record for: {', '.join(missing)}")
    no_chat = [role for role in ROLES if role not in NO_CHAT_ROLES and role not in chat_off]
    if no_chat:
        problems.append(f"No chat-unavailable run for: {', '.join(no_chat)}")
    return {
        "records": len(records),
        "problems": problems,
        "findings_to_route": findings,
        "records_complete": not problems,
        "note": "Complete records are not acceptance; the human owner decides on criterion 3.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", type=Path, help="JSON file of session records")
    args = parser.parse_args(argv)
    data = json.loads(args.records.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        print("Records must be a JSON list", file=sys.stderr)
        return 2
    result = check(data)
    print(json.dumps(result, indent=2))
    return 0 if result["records_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
