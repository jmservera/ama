"""Replay every in-repo synthetic generator twice and report byte identity and manifest fields.

SYNTHETIC DATA ONLY. Writes to temporary directories and never reads private data. The original
stock register generator is not in the repository; it is reported as unavailable, not passed.
"""

import argparse
import contextlib
import csv
import importlib
import io
import json
import re
import sys
import tempfile
from collections.abc import Callable, Sequence
from datetime import timedelta
from pathlib import Path

from zava_forward.core.synthetic import (
    scale_fixture,
    sensor_backfill,
    sensor_scenarios,
    stock_fabric,
)

SEED = 7
AS_OF = "2026-10-15"
# The public pack generator writes nothing unless its own validation passes; seed 7 fails it.
SEEDS = {"public-pack": 1341953496}
REVISION = re.compile(r"^sha256:(?:[0-9a-f]{16}|[0-9a-f]{64})$")
SUPPORT_GENERATOR = (
    Path(__file__).resolve().parents[6]
    / "support/synthetic-data/retrofit-flow/zava-forward-year-one/generator"
)
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


def _register(out: Path) -> Path:
    register = out.parent / (out.name + "-register.csv")
    with register.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["synthetic_home_id", "locality_theme", "building_form_osm"])
        for i in range(8):
            writer.writerow([f"AUDIT-{i:03d}", "Locality A", ""])
    return register


def _support(name: str) -> object:
    sys.path.insert(0, str(SUPPORT_GENERATOR))
    try:
        return importlib.import_module(name)
    finally:
        sys.path.remove(str(SUPPORT_GENERATOR))


def _public_pack(out: Path) -> Path:
    pack = _support("generate_pack")
    argv = ["pack", "--seed", str(SEEDS["public-pack"]), "--as-of", AS_OF]
    argv += ["--pack-dir", str(out / "pack"), "--key-dir", str(out / "key")]
    with contextlib.redirect_stdout(io.StringIO()):
        old, sys.argv = sys.argv, argv
        try:
            pack.main()  # type: ignore[attr-defined]
        finally:
            sys.argv = old
    return out / "pack" / "manifest.json"


def _stock_epc(out: Path) -> Path:
    epc = _support("zf_stock_epc")
    out.mkdir(parents=True)
    args = ["--seed", str(SEED), "--register", str(_register(out)), "--out", str(out / "epc.csv")]
    args += ["--manifest", str(out / "conflicts.csv"), "--summary", str(out / "summary.json")]
    with contextlib.redirect_stderr(io.StringIO()):
        epc.main(args)  # type: ignore[attr-defined]
    return out / "summary.json"


def _stock_fabric(out: Path) -> Path:
    register = _register(out)
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
SUPPORT_GENERATORS: dict[str, Callable[[Path], Path]] = {
    "public-pack": _public_pack,
    "stock-epc": _stock_epc,
}


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()
    }


def _window(name: str) -> dict[str, str]:
    if name == "sensor-scenarios":
        start = sensor_scenarios.START
        end = start + timedelta(days=sensor_scenarios.DAYS)
        return {
            "basis": "intrinsic",
            "start": start.date().isoformat(),
            "end": end.date().isoformat(),
        }
    return {"basis": "as_of", "as_of": AS_OF}


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
            ("seed", manifest.get("seed") == SEEDS.get(name, SEED)),
            ("version", bool(manifest.get("version"))),
            (
                "generator_revision",
                isinstance(revision, str) and bool(REVISION.fullmatch(revision)),
            ),
        )
        if not ok
    ]
    return {
        "generator": name,
        "window": _window(name),
        "status": "PASS" if identical and not missing else "FAIL",
        "byte_identical": identical,
        "manifest_missing": missing,
        "version": manifest.get("version"),
        "generator_revision": revision,
    }


def audit() -> dict[str, object]:
    runs = dict(GENERATORS)
    unavailable = dict(UNAVAILABLE)
    if SUPPORT_GENERATOR.is_dir():
        runs.update(SUPPORT_GENERATORS)
    else:
        for name in SUPPORT_GENERATORS:
            unavailable[name] = "support/ generator directory not found; not replayed."
    results = [_check(name, run) for name, run in runs.items()]
    return {
        "seed": SEED,
        "seed_overrides": dict(SEEDS),
        "as_of": AS_OF,
        "as_of_applies_to": "results with window.basis as_of; others report their own window",
        "results": results,
        "unavailable": unavailable,
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
