"""Replay every in-repo synthetic generator twice and report byte identity and manifest fields.

SYNTHETIC DATA ONLY. Writes to temporary directories and never reads private data. The original
stock register generator is not in the repository; it is reported as unavailable, not passed.
"""

import argparse
import contextlib
import csv
import io
import json
import sys
import tempfile
from collections.abc import Callable, Sequence
from pathlib import Path

from zava_forward.core.synthetic import (
    scale_fixture,
    sensor_backfill,
    sensor_scenarios,
    stock_fabric,
)

SEED = 7
AS_OF = "2026-10-15"
UNAVAILABLE = {
    "stock-register": (
        "Original private stock register generator and pinned OSM inputs are not in the "
        "repository; no receipt can be produced."
    )
}


def _scale(out: Path) -> Path:
    scale_fixture.write(out, n=12, per_home=3, seed=SEED, as_of=AS_OF)
    return out / "manifest.json"


def _sensor_backfill(out: Path) -> Path:
    sensor_backfill.write(out, homes=3, seed=SEED, days=2, cadence=360, as_of=AS_OF)
    return out / "manifest.json"


def _sensor_scenarios(out: Path) -> Path:
    sensor_scenarios.write(out, seed=SEED)
    return out / "truth" / "manifest.json"


def _stock_fabric(out: Path) -> Path:
    register = out.parent / (out.name + "-register.csv")
    with register.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["synthetic_home_id", "locality_theme", "building_form_osm"])
        for i in range(8):
            writer.writerow([f"AUDIT-{i:03d}", "Locality A", ""])
    with contextlib.redirect_stderr(io.StringIO()):
        stock_fabric.main(
            ["--seed", str(SEED), "--as-of", AS_OF, "--register", str(register), "--out", str(out)]
        )
    return out / "summary.json"


GENERATORS: dict[str, Callable[[Path], Path]] = {
    "scale-fixture": _scale,
    "sensor-backfill": _sensor_backfill,
    "sensor-scenarios": _sensor_scenarios,
    "stock-fabric": _stock_fabric,
}


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()
    }


def _check(name: str, run: Callable[[Path], Path]) -> dict[str, object]:
    with tempfile.TemporaryDirectory() as tmp:
        roots = [Path(tmp) / "one", Path(tmp) / "two"]
        manifests = [run(root) for root in roots]
        identical = _snapshot(roots[0]) == _snapshot(roots[1])
        manifest = json.loads(manifests[0].read_text(encoding="utf-8"))
    revision = manifest.get("generator_revision")
    missing = [
        key
        for key, ok in (
            ("seed", manifest.get("seed") == SEED),
            ("version", bool(manifest.get("version"))),
            ("generator_revision", isinstance(revision, str) and revision.startswith("sha256:")),
        )
        if not ok
    ]
    return {
        "generator": name,
        "status": "PASS" if identical and not missing else "FAIL",
        "byte_identical": identical,
        "manifest_missing": missing,
        "version": manifest.get("version"),
        "generator_revision": revision,
    }


def audit() -> dict[str, object]:
    results = [_check(name, run) for name, run in GENERATORS.items()]
    return {
        "seed": SEED,
        "as_of": AS_OF,
        "results": results,
        "unavailable": dict(UNAVAILABLE),
        "all_available_pass": all(r["status"] == "PASS" for r in results),
    }


def main(argv: Sequence[str] | None = None) -> None:
    argparse.ArgumentParser(description=__doc__.split("\n")[0]).parse_args(argv)
    report = audit()
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["all_available_pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
