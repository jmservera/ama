"""Generate the synthetic demo case-list workbook for the Excel import (issues #2008, #80).

All content is invented: fictional street names, `Demo Resident NN` labels, no phone numbers or
real people. The workbook follows the declared `case-list` structure (sheet `Cases`) with
deliberate header differences, row problems and one duplicate reference, so the row-level
preview shows clean rows, mapping differences and conflicts.

Run from the repository root after `pip install -e src/core -e src/importer`:

    python3 tools/make-demo-case-list.py [--out-dir DIR]

It writes `demo-case-list.xlsx` and `demo-case-list.csv` (the Cases sheet saved as CSV, which
is what the deployed web check accepts today).
"""

import argparse
import csv
import io
from pathlib import Path

from zava_forward.importer.xlsx import write_workbook

DEFAULT_OUT = Path(__file__).resolve().parent.parent / "docs/reference/research/demo-workbook"

HEADERS = [
    "Ref",
    "Resident name",
    "Property address",
    "Post code",
    "Workflow stage",
    "Status",
    "Case owner",
    "Notes",
]

# Rows 2-7 are clean; 8-10 each have a row problem; 11 repeats the reference of row 3 (conflict).
ROWS = [
    [
        "DEMO-001",
        "Demo Resident 01",
        "1 Fictional Row, Exampletown",
        "ZZ1 1AA",
        "Survey booked",
        "Open",
        "Demo Officer A",
        "",
    ],
    [
        "DEMO-002",
        "Demo Resident 02",
        "2 Fictional Row, Exampletown",
        "ZZ1 1AB",
        "Assessment",
        "Open",
        "Demo Officer A",
        "Gas safety date missing in source",
    ],
    [
        "DEMO-003",
        "Demo Resident 03",
        "3 Fictional Row, Exampletown",
        "ZZ1 1AD",
        "Design",
        "Open",
        "Demo Officer B",
        "",
    ],
    [
        "DEMO-004",
        "Demo Resident 04",
        "4 Fictional Row, Exampletown",
        "ZZ1 1AE",
        "Install",
        "On hold",
        "Demo Officer B",
        "",
    ],
    [
        "DEMO-005",
        "Demo Resident 05",
        "5 Fictional Row, Exampletown",
        "ZZ1 1AF",
        "Handover",
        "Open",
        "Demo Officer C",
        "",
    ],
    [
        "DEMO-006",
        "Demo Resident 06",
        "6 Fictional Row, Exampletown",
        "ZZ1 1AG",
        "Survey booked",
        "Open",
        "Demo Officer C",
        "",
    ],
    [
        "DEMO-007",
        "Demo Resident 07",
        "",
        "ZZ1 1AH",
        "Assessment",
        "Open",
        "Demo Officer A",
        "Address missing",
    ],
    [
        "DEMO-008",
        "Demo Resident 08",
        "8 Fictional Row, Exampletown",
        "ZZ-18",
        "Design",
        "Open",
        "Demo Officer B",
        "Postcode typed wrongly",
    ],
    [
        "DEMO-009",
        "Demo Resident 09",
        "9 Fictional Row, Exampletown",
        "ZZ1 1AJ",
        "",
        "Open",
        "Demo Officer C",
        "Stage not filled in",
    ],
    [
        "DEMO-002",
        "Demo Resident 10",
        "10 Fictional Row, Exampletown",
        "ZZ1 1AK",
        "Install",
        "Open",
        "Demo Officer A",
        "Reuses DEMO-002",
    ],
]

ABOUT = [
    ["About this demo"],
    ["Synthetic workbook for the Zava Forward import demo (issue 2008). Every value is invented."],
    [
        "Sheet Cases follows the declared case-list structure with differently named headers, so the preview shows alias mapping."
    ],
    [
        "Rows 8 to 10 have a row problem each; row 11 repeats the reference of row 3, which is a blocking conflict."
    ],
    ["The import preview never writes to this file."],
]


def sheets() -> dict[str, list[list[str]]]:
    return {"Cases": [HEADERS, *ROWS], "About this demo": ABOUT}


def csv_text() -> str:
    out = io.StringIO()
    csv.writer(out, lineterminator="\n").writerows([HEADERS, *ROWS])
    return out.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "demo-case-list.xlsx").write_bytes(write_workbook(sheets()))
    (args.out_dir / "demo-case-list.csv").write_text(csv_text(), encoding="utf-8", newline="")


if __name__ == "__main__":
    main()
