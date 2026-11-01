"""Read-only gap-routing baseline for the public synthetic needs inventory."""

import argparse
import csv
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

COVERAGE = ("covered", "partial", "missing")
CLOSURE_KINDS = ("child", "delivered", "deferred")
CONVENTIONS = ("reuse_rule", "seed", "identifiers", "is_synthetic")


def _mapping(value: object, field: str) -> dict[str, object]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ValueError(f"{field}: expected an object with string keys")
    return {key: item for key, item in value.items()}


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}: expected nonblank text")
    return value.strip()


def _texts(value: object, field: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{field}: expected a list of text values")
    return [_text(item, field) for item in value]


def build_baseline(value: object) -> dict[str, object]:
    """Check route shape and consistency, not issue existence or acceptance.

    Raise ValueError for malformed metadata; report missing/deferred needs as gaps.
    """
    inventory = _mapping(value, "inventory")
    version = _text(inventory.get("version"), "version")
    review_date = _text(inventory.get("review_date"), "review_date")
    if date.fromisoformat(review_date).isoformat() != review_date:
        raise ValueError("review_date: expected an ISO YYYY-MM-DD date")
    status = _text(inventory.get("status"), "status")
    declarations = _mapping(inventory.get("generator_conventions"), "generator_conventions")
    conventions = {key: _text(declarations.get(key), key) for key in CONVENTIONS}
    open_items = _texts(inventory.get("open_items"), "open_items")
    needs = inventory.get("needs")
    if not isinstance(needs, list) or not needs:
        raise ValueError("needs: expected a nonempty list")
    rows: list[dict[str, object]] = []
    open_gaps: list[str] = []
    seen: set[str] = set()
    counts: Counter[str] = Counter()
    for item in needs:
        need = _mapping(item, "need")
        need_id = _text(need.get("id"), "need.id")
        if not re.fullmatch(r"SN-(?:0[1-9]|[1-9][0-9]+)", need_id):
            raise ValueError(f"{need_id}: expected a positive SN-nn identifier")
        if need_id in seen:
            raise ValueError(f"{need_id}: duplicate need identifier")
        seen.add(need_id)
        label = _text(need.get("need"), f"{need_id}.need")
        coverage = _text(need.get("coverage"), f"{need_id}.coverage")
        if coverage not in COVERAGE:
            raise ValueError(f"{need_id}: coverage must be one of {COVERAGE}")
        closure = _mapping(need.get("gap_closure"), f"{need_id}.gap_closure")
        kind = _text(closure.get("kind"), f"{need_id}.gap_closure.kind")
        if kind not in CLOSURE_KINDS:
            raise ValueError(f"{need_id}: closure kind must be one of {CLOSURE_KINDS}")
        note = _text(closure.get("note"), f"{need_id}.gap_closure.note")
        issues = _texts(closure.get("issues"), f"{need_id}.gap_closure.issues")
        if any(not re.fullmatch(r"#[1-9][0-9]*", issue) for issue in issues):
            raise ValueError(f"{need_id}: issue references must be positive #number values")
        if len(issues) != len(set(issues)):
            raise ValueError(f"{need_id}: duplicate closure issue references")
        if kind != "deferred" and not issues:
            raise ValueError(f"{need_id}: {kind} closure needs at least one issue")
        if coverage == "covered" and kind != "delivered":
            raise ValueError(f"{need_id}: covered coverage requires delivered closure")
        if kind == "delivered" and coverage != "covered":
            raise ValueError(f"{need_id}: partial/missing coverage cannot be delivered")
        if coverage == "missing" or kind == "deferred":
            open_gaps.append(need_id)
        counts[coverage] += 1
        rows.append(
            {
                "id": need_id,
                "need": label,
                "coverage": coverage,
                "gap_closure": {"kind": kind, "issues": sorted(issues), "note": note},
            }
        )
    return {
        "inventory_version": version,
        "review_date": review_date,
        "inventory_status": status,
        "routing_shape_validated": True,
        "issue_existence": "not-assessed",
        "open_gaps": sorted(open_gaps),
        "generator_output_conformance": "not-assessed",
        "owner_approval": "not-established",
        "application_acceptance": "not-assessed",
        "coverage_counts": {key: counts[key] for key in COVERAGE},
        "needs": sorted(rows, key=lambda row: str(row["id"])),
        "declared_generator_conventions": conventions,
        "open_items": open_items,
    }


def check_register_labels(path: Path) -> dict[str, object]:
    """Count rows whose is_synthetic value is true; never expose row content."""
    rows = labelled = 0
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        names = reader.fieldnames or []
        if len(names) != len(set(names)):
            raise ValueError("Register requires unique CSV column names")
        missing = "is_synthetic" not in names
        try:
            for row in reader:
                rows += 1
                if str(row.get("is_synthetic", "")).strip().lower() in ("true", "1"):
                    labelled += 1
        except csv.Error as error:
            raise ValueError("Register is not valid CSV") from error
    conforms = not missing and rows > 0 and labelled == rows
    return {
        "rows": rows,
        "labelled": labelled,
        "unlabelled": rows - labelled,
        "missing_column": missing,
        "conforms": conforms,
    }


def main(argv: list[str] | None = None) -> int:
    """Print deterministic JSON; fail on invalid metadata or reported open gaps."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path, help="Public needs-inventory.json, not a dataset")
    parser.add_argument(
        "--register", type=Path, help="Optional CSV to check for per-row is_synthetic=true"
    )
    args = parser.parse_args(argv)
    try:
        value: object = json.loads(args.inventory.read_text(encoding="utf-8"))
        report = build_baseline(value)
        if args.register is not None:
            register = check_register_labels(args.register)
            report["register_label_conformance"] = register
            if not register["conforms"]:
                report["open_gaps"] = [*report["open_gaps"], "register-is_synthetic"]  # type: ignore[misc]
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(1, f"coverage: {args.inventory}: {error}\n")
    sys.stdout.write(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return 1 if report["open_gaps"] else 0


if __name__ == "__main__":
    sys.exit(main())
