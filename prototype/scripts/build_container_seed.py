import argparse
import csv
from pathlib import Path


CASE_COLUMNS = (
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
HOLD_COLUMNS = ("candidate_id", "is_synthetic", "hold_status_in_tracker")


def copy_allowlisted_rows(
    source: Path,
    target: Path,
    columns: tuple[str, ...],
    preserve_source_row: bool = False,
) -> int:
    with source.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = set(columns) - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"{source.name} is missing required columns: {', '.join(sorted(missing))}")
        rows = []
        for source_row, row in enumerate(reader, start=2):
            if (row.get("is_synthetic") or "").casefold() != "true":
                continue
            selected = {column: (row.get(column) or "").strip() for column in columns}
            if preserve_source_row:
                selected["source_row"] = str(source_row)
            rows.append(selected)

    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        output_columns = (*columns, "source_row") if preserve_source_row else columns
        writer = csv.DictWriter(handle, fieldnames=output_columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def build_container_seed(source_dir: Path, output_dir: Path) -> tuple[int, int]:
    cases = copy_allowlisted_rows(
        source_dir / "candidate-lifecycle.csv",
        output_dir / "candidate-lifecycle.csv",
        CASE_COLUMNS,
        preserve_source_row=True,
    )
    holds = copy_allowlisted_rows(
        source_dir / "safety-holds.csv",
        output_dir / "safety-holds.csv",
        HOLD_COLUMNS,
    )
    if cases == 0:
        raise ValueError("No fictional synthetic cases were found in candidate-lifecycle.csv.")
    return cases, holds


def main() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(
        description="Copy only allowlisted synthetic fields into the container build seed."
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=repository_root / "docs" / "reference" / "research" / "retrofit-synthetic-data",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=repository_root / "prototype" / "seed" / "container-source",
    )
    args = parser.parse_args()
    cases, holds = build_container_seed(args.source_dir.resolve(), args.output_dir.resolve())
    print(f"Wrote {cases} synthetic cases and {holds} synthetic safety holds to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
