"""Offline completeness check for the atlas-to-screen trace (Refs #233).

Reads the PRD profile contract, the atlas design themes and the trace document, and
reports which perspectives, themes, tensions and walkthrough stages are not traced to
a screen or a recorded deferral. It records no human, accessibility or content
acceptance. Exit codes: 0 complete, 1 gaps found, 2 source not readable.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

PRD = "docs/prds/zava-forward-retrofit-programme-demonstrator.md"
ATLAS = "docs/reference/research/ux/customer-journeys/customer-journey-atlas.md"
TRACE = "docs/reference/research/ux/atlas-screen-trace.md"
STAGES = 8
TENSIONS = ("Continuity versus disclosure", "Utilisation versus choice")
SCREEN_RE = re.compile(r"`[a-z][a-z0-9-]+`")
HOME_RE = re.compile(r"EX-HOME-\d+")
MANIFEST_RE = re.compile(r"^\| [a-z-]+ \| ([\d, ]+) \| \d+ \|", re.MULTILINE)
# Registered (asset-board) and proposed role screens; update when a screen is added or renamed.
KNOWN_SCREENS = frozenset(
    {
        "asset-board",
        "programme-queue",
        "technical-queue",
        "resident-choice",
        "safety-lead",
        "hazard-triage",
        "procurement-packages",
        "contractor-job-pack",
        "quality-queue",
        "finance-invoices",
        "finance-funding",
        "data-operator",
    }
)


def section(text: str, heading: str) -> str:
    match = re.search(rf"^#{{2,3}} {re.escape(heading)}\s*$", text, re.MULTILINE)
    if not match:
        return ""
    rest = text[match.end() :]
    nxt = re.search(r"^#{2,3} ", rest, re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def rows(block: str) -> list[list[str]]:
    result = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
            continue
        result.append(cells)
    return result[1:]


def first_column(block: str) -> list[str]:
    return [r[0] for r in rows(block) if r]


def traced(cell: str) -> bool:
    return bool(SCREEN_RE.search(cell)) or "Deferred:" in cell


def unknown_screens(cell: str) -> list[str]:
    return [s for s in (m.strip("`") for m in SCREEN_RE.findall(cell)) if s not in KNOWN_SCREENS]


def existing_homes(prd: str) -> set[str]:
    homes = set(HOME_RE.findall(prd))
    for suffixes in MANIFEST_RE.findall(prd):
        homes.update(f"EX-HOME-{n}" for n in re.findall(r"\d+", suffixes))
    return homes


def check(prd: str, atlas: str, trace: str) -> dict[str, Any]:
    gaps: list[str] = []
    perspectives = first_column(section(prd, "Profile Journey Contract for the Next Prototype"))
    themes = first_column(section(atlas, "Five design themes and tensions"))
    if len(perspectives) != 11:
        gaps.append(f"expected 11 PRD perspectives, found {len(perspectives)}")
    if len(themes) != 5:
        gaps.append(f"expected 5 atlas themes, found {len(themes)}")

    def lookup(block: str) -> dict[str, list[str]]:
        return {r[0]: r for r in rows(block) if r}

    persp_rows = lookup(section(trace, "Perspectives to screens"))
    theme_rows = lookup(section(trace, "Atlas design themes to screens"))
    for name in perspectives:
        row = persp_rows.get(name)
        if row is None or len(row) < 5 or not traced(row[1]) or not all(row[2:5]):
            gaps.append(f"perspective not traced with confirms/changes/hypothesis: {name}")
    for name in themes:
        row = theme_rows.get(name)
        if row is None or len(row) < 3 or not traced(row[1]) or not row[2]:
            gaps.append(f"theme has neither screen nor deferral: {name}")
    tension_rows = lookup(section(trace, "Tensions"))
    for name in TENSIONS:
        row = tension_rows.get(name)
        if row is None or len(row) < 4 or not traced(row[1]) or not row[2]:
            gaps.append(f"tension not resolved on a screen: {name}")

    walk_block = section(trace, "Same-home walkthrough")
    walk = rows(walk_block)
    if len(walk) != STAGES or [r[0][:1] for r in walk] != [str(i) for i in range(1, STAGES + 1)]:
        gaps.append(f"walkthrough must list stages 1 to {STAGES} in order")
    for r in walk:
        if len(r) < 4 or not traced(r[1]) or not r[2] or not r[3]:
            gaps.append(
                f"walkthrough stage lacks screen, description or boundary: {r[0] if r else '?'}"
            )
    homes = set(HOME_RE.findall(walk_block))
    existing = existing_homes(prd)
    if len(homes) != 1 or homes & existing:
        gaps.append("walkthrough must use exactly one new home id, not an existing example")
    for block_name in (
        "Perspectives to screens",
        "Atlas design themes to screens",
        "Tensions",
        "Same-home walkthrough",
    ):
        for ident in sorted(
            {
                i
                for r in rows(section(trace, block_name))
                for i in unknown_screens(r[1])
                if len(r) > 1
            }
        ):
            gaps.append(f"unknown screen id in {block_name}: {ident}")
    if "hypothes" not in section(trace, "Scope and evidence label").lower():
        gaps.append("atlas findings are not labelled hypotheses")
    return {
        "perspectives": len(perspectives),
        "themes": len(themes),
        "gaps": gaps,
        "verdict": "complete" if not gaps else "gaps",
        "note": "Trace completeness is not accessibility, content or human acceptance.",
    }


def default_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / TRACE).exists():
            return parent
    return Path.cwd()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    parser.add_argument("--root", type=Path, default=None, help="repository root")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)
    root = args.root or default_root()
    try:
        report = check(
            (root / PRD).read_text(encoding="utf-8"),
            (root / ATLAS).read_text(encoding="utf-8"),
            (root / TRACE).read_text(encoding="utf-8"),
        )
    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Atlas trace: {report['verdict']}")
        for gap in report["gaps"]:
            print(f"gap: {gap}")
        print(report["note"])
    return 0 if report["verdict"] == "complete" else 1


if __name__ == "__main__":
    sys.exit(main())
