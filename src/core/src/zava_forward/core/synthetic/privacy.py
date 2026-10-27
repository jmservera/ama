"""Offline, bounded pattern/label checks; never a universal personal-data guarantee."""

import argparse
import csv
import hashlib
import json
import re
from datetime import date
from pathlib import Path

from .sensor_backfill import STOCK_VERSION

PATTERNS = {
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "uk_phone": re.compile(
        r"(?<![\w])(?:\+44[ .-]?(?:\(0\)[ .-]?)?|0)[1-9](?:[ .-]?\d){9}(?![\w])"
    ),
    "ni_number": re.compile(r"\b[A-CEGHJ-PR-TW-Z]{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?[A-D]\b", re.I),
    "uk_postcode": re.compile(r"\b[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}\b", re.I),
}
CHAT_FILES = (
    "personas",
    "threads",
    "turns",
    "ledger_events",
    "memory_state",
    "memory_items",
    "exclusion_probes",
    "isolation_cases",
    "deletion_cases",
)
PACK = Path("docs/reference/research/retrofit-synthetic-data")


def pattern_issues(value: object, *, scale_home: bool = False) -> list[str]:
    """Scan every scalar (including nested exempt metadata), without returning values."""
    if isinstance(value, dict):
        return [
            issue
            for key, item in value.items()
            for issue in pattern_issues(key)
            + (
                []
                if scale_home
                and key == "postcode"
                and isinstance(item, str)
                and re.fullmatch(r"TE[0-8] 1ST", item)
                else pattern_issues(item)
            )
        ]
    if isinstance(value, list):
        return [issue for item in value for issue in pattern_issues(item)]
    if isinstance(value, str):
        return [name for name, pattern in PATTERNS.items() if pattern.search(value)]
    return []


def record_issues(
    row: object, label_field: str = "is_synthetic", *, scale_home: bool = False
) -> list[str]:
    if not isinstance(row, dict):
        return ["record_not_object"]
    issues = pattern_issues(row, scale_home=scale_home)
    value = row.get(label_field)
    if label_field == "is_synthetic":
        valid = value is True or (isinstance(value, str) and value.lower() == "true")
    elif label_field == "contains_real_data":
        valid = value is False
    else:
        valid = value == "SYNTHETIC"
    if not valid:
        issues.append("missing_synthetic_label")
    return issues


def _declared_labels(value: object) -> list[str]:
    if isinstance(value, dict):
        issues = []
        if (
            "is_synthetic" in value
            and value["is_synthetic"] is not True
            and value["is_synthetic"] != "true"
        ):
            issues.append("missing_synthetic_label")
        if "contains_real_data" in value and value["contains_real_data"] is not False:
            issues.append("contains_real_data")
        return issues + [issue for item in value.values() for issue in _declared_labels(item)]
    if isinstance(value, list):
        return [issue for item in value for issue in _declared_labels(item)]
    return []


def source_issues(sources: list[dict[str, object]]) -> list[str]:
    issues = []
    for source in sources:
        sid = str(source["id"])
        for field in ("licence", "attribution", "url"):
            value = source.get(field)
            if not isinstance(value, str) or not value.strip():
                issues.append(f"{sid}:missing_{field}")
            elif re.search(r"expected|to confirm|wording to confirm", value, re.I):
                issues.append(f"{sid}:provisional_{field}")
        retrieved = source.get("retrieval_date")
        try:
            if (
                not isinstance(retrieved, str)
                or date.fromisoformat(retrieved).isoformat() != retrieved
            ):
                raise ValueError
        except ValueError:
            issues.append(f"{sid}:missing_or_invalid_retrieval_date")
    return issues


def _json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("JSON root must be an object")
    return value


def _csv_issues(path: Path, label: str | None, *, allow_empty: bool = False) -> list[str]:
    issues = []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
            return ["invalid_csv_header"]
        count = 0
        for count, row in enumerate(reader, 1):
            if None in row or None in row.values():
                issues.append(f"row-{count}:invalid_csv_shape")
            found = record_issues(row, label) if label else pattern_issues(row)
            issues.extend(f"row-{count}:{issue}" for issue in found)
        if not count and not allow_empty:
            issues.append("empty_dataset")
    return issues


def public_issues(root: Path, *, check_sources: bool = False) -> list[str]:
    """Only public registered payloads are opened; private locations are never read."""
    register = _json(root / PACK / "provenance-register.json")
    datasets = register["datasets"]
    if not isinstance(datasets, list):
        raise ValueError("datasets must be a list")
    issues = []
    checked: set[str] = set()
    for dataset in datasets:
        if dataset["visibility"] != "public":
            continue
        location = str(dataset["location"])
        if not (location.startswith("docs/") or re.match(r"src/[^/]+/evals/", location)):
            raise ValueError("Public location must be under docs/ or src/<project>/evals/")
        path = root / location
        paths = sorted(path.glob(dataset["files_glob"])) if "files_glob" in dataset else [path]
        if not paths:
            issues.append(f"{dataset['id']}:missing_payload")
        for path in paths:
            if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink():
                raise ValueError("Public payload escapes repository or is a symlink")
            name = path.relative_to(root).as_posix()
            checked.add(name)
            contract = dataset.get("validation", {})
            if path.suffix == ".csv":
                label = None if path.name in dataset.get("label_exempt", []) else "is_synthetic"
                found = _csv_issues(path, label)
            else:
                value = _json(path)
                found = pattern_issues(value) + _declared_labels(value)
                collection = contract.get("collection")
                if collection:
                    rows = value.get(collection)
                    if not isinstance(rows, list) or not rows:
                        found.append("missing_record_collection")
                    else:
                        for i, row in enumerate(rows, 1):
                            found.extend(
                                f"row-{i}:{issue}"
                                for issue in record_issues(
                                    row, contract.get("label", "is_synthetic")
                                )
                                if issue in {"missing_synthetic_label", "record_not_object"}
                            )
                elif contract.get("root_label"):
                    found.extend(
                        issue
                        for issue in record_issues(value)
                        if issue == "missing_synthetic_label"
                    )
                elif contract.get("marker_field"):
                    marker = value.get(contract["marker_field"])
                    if not isinstance(marker, str) or not re.search(
                        r"synthetic|constructed", marker, re.I
                    ):
                        found.append("missing_synthetic_label")
                else:
                    found.append("missing_validation_contract")
            issues.extend(f"{name}:{issue}" for issue in found)
    expected = {
        p.relative_to(root).as_posix()
        for folder in [root / PACK, *sorted((root / "src").glob("*/evals"))]
        for p in folder.iterdir()
        if p.suffix in {".csv", ".json"}
        and p.name not in {"provenance-register.json", "needs-inventory.json"}
    }
    issues.extend(f"{name}:unregistered_public_payload" for name in sorted(expected - checked))
    if check_sources:
        sources = register["sources"]
        if not isinstance(sources, list):
            raise ValueError("sources must be a list")
        issues.extend(source_issues(sources))
    return issues


def snapshot_issues(out: Path, kind: str) -> list[str]:
    """Validate an explicitly supplied snapshot, never discover private working data."""
    manifest = _json(out / "manifest.json")
    issues = pattern_issues(manifest)
    source = "SYNTHETIC-DEMO" if kind == "chat" else "SYNTHETIC"
    if manifest.get("source_type") != source:
        issues.append("manifest:missing_synthetic_label")
    if kind == "scale":
        files = ["homes.jsonl", "households.jsonl", "events.jsonl"]
    elif kind == "chat":
        files = [f"{name}.jsonl" for name in CHAT_FILES]
    elif kind == "sensor":
        shards = manifest.get("shards")
        if not isinstance(shards, list):
            raise ValueError("Sensor manifest requires shards")
        files = ["estimate.json", "sensors.csv", *(str(row["file"]) for row in shards)]
        stock_mode = manifest.get("version") in ("sensor-backfill-stock-v1", STOCK_VERSION)
        if stock_mode:
            files.append("stock-fabric.csv")
    else:
        raise ValueError("Unknown snapshot kind")
    if any(Path(name).name != name for name in files) or len(files) != len(set(files)):
        raise ValueError("Snapshot payload names must be unique basenames")
    if {p.name for p in out.iterdir()} != {"manifest.json", *files}:
        issues.append("snapshot:unexpected_or_missing_files")
    digest = hashlib.sha256()
    hashes = manifest.get("file_sha256")
    if kind != "chat" and (not isinstance(hashes, dict) or set(hashes) != set(files)):
        issues.append("manifest:missing_payload_hashes")
    for name in files:
        path = out / name
        if not path.is_file() or path.is_symlink():
            issues.append(f"{name}:missing_or_symlink_payload")
            continue
        content_hash = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
                content_hash.update(chunk)
        if isinstance(hashes, dict) and hashes.get(name) != content_hash.hexdigest():
            issues.append(f"{name}:hash_mismatch")
        if path.suffix == ".csv":
            label = "is_synthetic" if name == "stock-fabric.csv" else "source_type"
            empty_selection = (
                name == "sensors.csv"
                and stock_mode
                and manifest.get("homes_covered") == 0
                and manifest.get("rows") == 0
                and manifest.get("shards") == []
            )
            found = _csv_issues(path, label, allow_empty=empty_selection)
        elif path.suffix == ".jsonl":
            found = []
            count = 0
            with path.open(encoding="utf-8") as handle:
                for count, line in enumerate(handle, 1):
                    row = json.loads(line)
                    if kind == "scale" and name != "households.jsonl":
                        row_issues = pattern_issues(row, scale_home=name == "homes.jsonl")
                        if not isinstance(row, dict):
                            row_issues.append("record_not_object")
                    else:
                        row_issues = record_issues(row)
                    found.extend(f"row-{count}:{issue}" for issue in row_issues)
            if not count:
                found.append("empty_dataset")
        else:
            found = pattern_issues(_json(path))
        issues.extend(f"{name}:{issue}" for issue in found)
    if kind == "chat" and manifest.get("sha256") != digest.hexdigest():
        issues.append("manifest:hash_mismatch")
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--public-root", type=Path)
    mode.add_argument("--snapshot", type=Path)
    parser.add_argument("--kind", choices=("scale", "sensor", "chat"))
    parser.add_argument("--sources", action="store_true")
    args = parser.parse_args(argv)
    if args.snapshot and (not args.kind or args.sources):
        parser.error("--snapshot requires --kind and cannot use --sources")
    try:
        issues = (
            snapshot_issues(args.snapshot, args.kind)
            if args.snapshot
            else public_issues(args.public_root, check_sources=args.sources)
        )
    except (OSError, ValueError, KeyError, TypeError):
        # Parser messages intentionally omit payload content and matched personal values.
        parser.error("Unable to validate: missing, malformed or unreadable dataset/contract")
    print(json.dumps({"issues": issues, "scope": "bounded-pattern-label-check"}, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
