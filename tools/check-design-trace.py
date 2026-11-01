"""Offline design traceability and review gate checker (Refs #156).

Reads the screen-feature register in the prototype profile review and checks
that every screen issue names a journey, a task flow (or its explicit gap) and
a design artefact (or an explicit NOT SUPPLIED gap). It performs no network
access and never records human review, accessibility or content acceptance.

Exit codes: 0 every screen has a supplied design, 1 gate blocked by
NOT SUPPLIED designs, 2 register malformed or links unresolved.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REGISTER = "docs/reference/research/ux/zava-forward-prototype-profile-review.md"
HEADING = "### Known screen features and exact trace or gap"
COLUMNS = 5
ISSUE_RE = re.compile(r"^\[#(\d+)\]\(https://github\.com/[^/]+/[^/]+/issues/\d+")
REF_USE_RE = re.compile(r"\[[^\]]+\]\[([^\]]+)\]")
INLINE_RE = re.compile(r"\]\((\.[^)#\s]*)(?:#[^)\s]*)?\)")
REF_DEF_RE = re.compile(r"^\[([^\]]+)\]:\s*(\S+)", re.MULTILINE)
NOT_SUPPLIED = "NOT SUPPLIED"


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def register_rows(text: str) -> list[str]:
    start = text.find(HEADING)
    if start < 0:
        return []
    section = text[start + len(HEADING) :]
    nxt = re.search(r"^#{2,3} ", section, re.MULTILINE)
    if nxt:
        section = section[: nxt.start()]
    return [ln for ln in section.splitlines() if ln.startswith("| [#")]


def link_targets(cell: str, refs: dict[str, str]) -> tuple[list[str], list[str]]:
    targets = [m.group(1) for m in INLINE_RE.finditer(cell)]
    missing = []
    for name in REF_USE_RE.findall(cell):
        if name in refs:
            targets.append(refs[name])
        else:
            missing.append(name)
    return targets, missing


def check(text: str, base: Path) -> dict:
    refs = dict(REF_DEF_RE.findall(text))
    errors: list[str] = []
    rows = []
    for line in register_rows(text):
        cells = split_row(line)
        match = ISSUE_RE.match(cells[0]) if cells else None
        if len(cells) != COLUMNS or not match:
            errors.append(f"malformed row: {line[:60]}")
            continue
        issue = int(match.group(1))
        journey, flow, design = cells[1], cells[2], cells[3]
        targets, missing = link_targets(" ".join(cells[1:4]), refs)
        for name in missing:
            errors.append(f"#{issue}: undefined link reference [{name}]")
        for target in targets:
            path = target.split("#", 1)[0]
            if path and not path.startswith("http") and not (base / path).exists():
                errors.append(f"#{issue}: missing link target {path}")
        if not (
            NOT_SUPPLIED in journey or REF_USE_RE.search(journey) or "](" in journey
        ):
            errors.append(f"#{issue}: journey names neither link nor gap")
        if not flow:
            errors.append(f"#{issue}: empty task flow cell")
        if not design:
            errors.append(f"#{issue}: empty design cell")
        rows.append({"issue": issue, "design_supplied": NOT_SUPPLIED not in design})
    issues = [r["issue"] for r in rows]
    if len(set(issues)) != len(issues):
        errors.append("duplicate issue rows")
    supplied = sum(1 for r in rows if r["design_supplied"])
    if errors or not rows:
        verdict = "malformed"
    elif supplied == len(rows):
        verdict = "pass"
    else:
        verdict = "blocked"
    return {
        "screen_issues": len(rows),
        "design_supplied": supplied,
        "design_not_supplied": len(rows) - supplied,
        "not_supplied_issues": [r["issue"] for r in rows if not r["design_supplied"]],
        "errors": errors or (["no register rows found"] if not rows else []),
        "verdict": verdict,
        "note": "Supplied design is not human, accessibility or content acceptance.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--register", type=Path, help="register Markdown file")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    register = args.register or root / REGISTER
    report = check(register.read_text(encoding="utf-8"), register.parent)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(
            f"Design gate: {report['verdict']}; {report['screen_issues']} screen "
            f"issues, {report['design_supplied']} with a supplied design, "
            f"{report['design_not_supplied']} NOT SUPPLIED"
        )
        for err in report["errors"]:
            print(f"error: {err}")
        print(report["note"])
    return {"pass": 0, "blocked": 1}.get(report["verdict"], 2)


if __name__ == "__main__":
    sys.exit(main())
