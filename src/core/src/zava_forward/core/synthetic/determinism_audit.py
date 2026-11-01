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
import os
import re
import subprocess
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
# Core generators record the full digest; the support generators record a 16 digit prefix.
CORE_REVISION = re.compile(r"^sha256:[0-9a-f]{64}$")
SUPPORT_REVISION = re.compile(r"^sha256:[0-9a-f]{16}$")
SUPPORT_RELATIVE = Path("support/synthetic-data/retrofit-flow/zava-forward-year-one/generator")
SUPPORT_ENV = "ZF_SUPPORT_GENERATOR"
KEY_MANIFESTS = {"public-pack": "key/ground-truth-summary.json"}


def locate_support(explicit: str | Path | None = None) -> Path:
    """Find the support generator directory from an argument, the environment or the checkout."""
    given = explicit or os.environ.get(SUPPORT_ENV)
    if given:
        return Path(given).resolve()
    for start in (Path.cwd().resolve(), Path(__file__).resolve()):
        for parent in (start, *start.parents):
            if (parent / SUPPORT_RELATIVE).is_dir():
                return parent / SUPPORT_RELATIVE
    return Path.cwd().resolve() / SUPPORT_RELATIVE


SUPPORT_GENERATOR = locate_support()
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


def _import_support(name: str, directory: Path) -> object:
    sys.path.insert(0, str(directory))
    try:
        return importlib.import_module(name)
    finally:
        sys.path.remove(str(directory))


def _write_window(out: Path, window: dict[str, str]) -> None:
    sidecar = out.parent / (out.name + "-window.json")
    sidecar.write_text(json.dumps(window), encoding="utf-8")


def _replay_public_pack(out: Path, directory: Path) -> Path:
    pack = _import_support("generate_pack", directory)
    model = _import_support("zf_model", directory)
    argv = ["pack", "--seed", str(SEEDS["public-pack"]), "--as-of", AS_OF]
    argv += ["--pack-dir", str(out / "pack"), "--key-dir", str(out / "key")]
    sys.argv = argv
    pack.main()  # type: ignore[attr-defined]
    manifest = out / "pack" / "manifest.json"
    if not manifest.is_file():
        raise RuntimeError("pack generator wrote no manifest; its own validation failed")
    _write_window(
        out,
        {
            "basis": "intrinsic",
            "start": model.SIM_START.isoformat(),  # type: ignore[attr-defined]
            "end": model.SNAP.isoformat(),  # type: ignore[attr-defined]
            "generation_label_as_of": AS_OF,
        },
    )
    return manifest


def _replay_stock_epc(out: Path, directory: Path) -> Path:
    epc = _import_support("zf_stock_epc", directory)
    out.mkdir(parents=True)
    args = ["--seed", str(SEED), "--register", str(_register(out)), "--out", str(out / "epc.csv")]
    args += ["--manifest", str(out / "conflicts.csv"), "--summary", str(out / "summary.json")]
    epc.main(args)  # type: ignore[attr-defined]
    _write_window(
        out,
        {
            "basis": "intrinsic",
            "start": epc.EPC_START.isoformat(),  # type: ignore[attr-defined]
            "end": epc.EPC_END.isoformat(),  # type: ignore[attr-defined]
            "epc_validity_as_of": epc.AS_OF.isoformat(),  # type: ignore[attr-defined]
        },
    )
    return out / "summary.json"


REPLAYS: dict[str, Callable[[Path, Path], Path]] = {
    "public-pack": _replay_public_pack,
    "stock-epc": _replay_stock_epc,
}


def _isolated(name: str) -> Callable[[Path], Path]:
    """Replay a support generator in a fresh interpreter so no module cache can mask changes."""

    def run(out: Path) -> Path:
        command = [
            sys.executable,
            "-m",
            "zava_forward.core.synthetic.determinism_audit",
            "--replay",
            name,
            str(out),
            "--support-dir",
            str(SUPPORT_GENERATOR),
        ]
        done = subprocess.run(command, capture_output=True, text=True, check=False)
        if done.returncode != 0:
            detail = (done.stderr + done.stdout).strip()[-1500:]
            raise RuntimeError(f"{name} replay failed ({done.returncode}): {detail}")
        return Path(done.stdout.strip().splitlines()[-1])

    return run


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
SUPPORT_GENERATORS = tuple(REPLAYS)


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()
    }


def _window(name: str, root: Path) -> dict[str, str]:
    sidecar = root.parent / (root.name + "-window.json")
    if sidecar.is_file():
        return dict(json.loads(sidecar.read_text(encoding="utf-8")))
    if name == "sensor-scenarios":
        start = sensor_scenarios.START
        end = start + timedelta(days=sensor_scenarios.DAYS)
        return {
            "basis": "intrinsic",
            "start": start.date().isoformat(),
            "end": end.date().isoformat(),
        }
    return {"basis": "as_of", "as_of": AS_OF}


def _missing(manifest: dict[str, object], seed: int, pattern: re.Pattern[str]) -> list[str]:
    revision = manifest.get("generator_revision")
    return [
        key
        for key, ok in (
            ("seed", manifest.get("seed") == seed),
            ("version", bool(manifest.get("version"))),
            (
                "generator_revision",
                isinstance(revision, str) and bool(pattern.fullmatch(revision)),
            ),
        )
        if not ok
    ]


def _check(
    name: str,
    run: Callable[[Path], Path],
    pattern: re.Pattern[str] = CORE_REVISION,
) -> dict[str, object]:
    seed = SEEDS.get(name, SEED)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            roots = [Path(tmp) / "one", Path(tmp) / "two"]
            manifests = [run(root) for root in roots]
            identical = _snapshot(roots[0]) == _snapshot(roots[1])
            manifest = json.loads(manifests[0].read_text(encoding="utf-8"))
            missing = _missing(manifest, seed, pattern)
            key_path = KEY_MANIFESTS.get(name)
            if key_path:
                key = json.loads((roots[0] / key_path).read_text(encoding="utf-8"))
                missing += [f"key:{field}" for field in _missing(key, seed, pattern)]
            window = _window(name, roots[0])
    except Exception as error:  # noqa: BLE001 - one failing generator must not hide the others
        return {
            "generator": name,
            "window": {"basis": "unavailable"},
            "status": "FAIL",
            "byte_identical": False,
            "manifest_missing": [],
            "error": str(error)[:1500],
        }
    return {
        "generator": name,
        "window": window,
        "status": "PASS" if identical and not missing else "FAIL",
        "byte_identical": identical,
        "manifest_missing": missing,
        "version": manifest.get("version"),
        "generator_revision": manifest.get("generator_revision"),
    }


def audit() -> dict[str, object]:
    runs: dict[str, tuple[Callable[[Path], Path], re.Pattern[str]]] = {
        name: (run, CORE_REVISION) for name, run in GENERATORS.items()
    }
    unavailable = dict(UNAVAILABLE)
    if SUPPORT_GENERATOR.is_dir():
        for name in SUPPORT_GENERATORS:
            runs[name] = (_isolated(name), SUPPORT_REVISION)
    else:
        for name in SUPPORT_GENERATORS:
            unavailable[name] = "support/ generator directory not found; not replayed."
    results = [_check(name, run, pattern) for name, (run, pattern) in runs.items()]
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
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--support-dir", help=f"support generator directory (or ${SUPPORT_ENV})")
    parser.add_argument("--replay", nargs=2, metavar=("NAME", "OUT"), help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    global SUPPORT_GENERATOR
    SUPPORT_GENERATOR = locate_support(args.support_dir)
    if args.replay:
        name, out = args.replay
        print(REPLAYS[name](Path(out), SUPPORT_GENERATOR))
        return
    report = audit()
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["all_available_pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
