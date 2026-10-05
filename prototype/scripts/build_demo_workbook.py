import argparse
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font


HEADERS = (
    "candidate_id",
    "property_ref",
    "current_status",
    "owner",
    "locality",
    "archetype_id",
    "lead_supplier",
    "rag_status",
    "is_synthetic",
)

SAMPLE_ROWS = (
    ("CAND-DEMO-0001", "SYN-PROP-DEMO-0001", "01 Identified", "PM-01", "Locality A", "ARC-01", "SUP-F1", "Green", True),
    ("CAND-DEMO-0002", "SYN-PROP-DEMO-0002", "02 Contacting resident", "RLO-01", "Locality B", "ARC-02", "SUP-F2", "Amber", True),
    ("CAND-DEMO-0003", "SYN-PROP-DEMO-0003", "05 In design", "RC-01", "Locality C", "ARC-04", "SUP-HP", "Green", True),
)


def build_workbook(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "cases"
    sheet.append(HEADERS)
    for cell in sheet[1]:
        cell.font = Font(bold=True)
    for row in SAMPLE_ROWS:
        sheet.append(row)
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    workbook.save(path)
    workbook.close()


def main() -> None:
    default_path = Path(__file__).resolve().parents[1] / "seed" / "demo-import.xlsx"
    parser = argparse.ArgumentParser(
        description="Generate a workbook containing only the approved fictional demo fields."
    )
    parser.add_argument("--output", type=Path, default=default_path)
    args = parser.parse_args()
    build_workbook(args.output.resolve())
    print(f"Wrote {len(SAMPLE_ROWS)} fictional rows to {args.output.resolve()}")


if __name__ == "__main__":
    main()
