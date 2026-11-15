"""Each in-repo generator is byte-identical for one (seed, as_of) under hostile ambient state.

Every replay runs in a fresh interpreter with a different PYTHONHASHSEED (exposes unordered-set
iteration) and with wall-clock and uuid sources made to raise (exposes datetime.now, date.today,
time.time and uuid4 leaks that a same-day, same-process replay cannot see).
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from zava_forward.core.synthetic import determinism_audit as da
from zava_forward.core.synthetic import scale_fixture, sensor_backfill, stock_register

GUARDED_RUN = """
import datetime as _dt, sys, time, uuid
def _banned(*a, **k):
    raise RuntimeError("wall clock or uuid used during generation")
class _D(_dt.date):
    today = classmethod(_banned)
class _T(_dt.datetime):
    now = utcnow = today = classmethod(_banned)
_dt.date, _dt.datetime = _D, _T
from pathlib import Path
from zava_forward.core.synthetic import determinism_audit as da
time.time = time.time_ns = time.localtime = time.gmtime = _banned
uuid.uuid1 = uuid.uuid4 = _banned
print(da.GENERATORS[sys.argv[1]](Path(sys.argv[2])))
"""
PREVIEW_RUN = (
    GUARDED_RUN.rsplit("print(", 1)[0]
    + """
from zava_forward.core.synthetic import resident_preview_fixture as rpf
print(rpf.build(Path(sys.argv[1]))[0])
"""
)
CORE_REVISION = re.compile(r"^sha256:[0-9a-f]{64}$")


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        for part in (str(path.relative_to(root)).encode(), path.read_bytes()):
            digest.update(len(part).to_bytes(8, "big") + part)
    return digest.hexdigest()


def replay(name: str, out: Path, hash_seed: str) -> Path:
    env = {**os.environ, "PYTHONHASHSEED": hash_seed, "PYTHONDONTWRITEBYTECODE": "1"}
    script, args = (
        (PREVIEW_RUN, [str(out)]) if name == "preview" else (GUARDED_RUN, [name, str(out)])
    )
    done = subprocess.run(
        [sys.executable, "-c", script, *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
        stdin=subprocess.DEVNULL,
    )
    if done.returncode != 0:
        raise AssertionError(f"{name} failed under guards: {done.stderr[-1500:]}")
    return Path(done.stdout.strip().splitlines()[-1])


class GeneratorDeterminismMatrixTests(unittest.TestCase):
    def test_every_generator_is_identical_across_hash_seeds_without_clock_or_uuid(self) -> None:
        for name in da.GENERATORS:
            with self.subTest(generator=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                manifests = [
                    replay(name, root / label, hash_seed)
                    for label, hash_seed in (("a", "1"), ("b", "2"), ("c", "3"))
                ]
                self.assertEqual(
                    {tree_digest(root / label) for label in "abc"}, {tree_digest(root / "a")}
                )
                manifest = json.loads(manifests[0].read_text(encoding="utf-8"))
                self.assertEqual(manifest["seed"], da.SEED)
                self.assertTrue(manifest["version"])
                self.assertRegex(manifest["generator_revision"], CORE_REVISION)

    def test_resident_preview_is_clock_free_and_records_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            datasets = [
                replay("preview", root / label, seed) for label, seed in (("a", "1"), ("b", "2"))
            ]
            self.assertEqual(tree_digest(root / "a"), tree_digest(root / "b"))
            meta = json.loads(datasets[0].read_text(encoding="utf-8"))["synthetic_preview"]
            self.assertEqual((meta["seed"], meta["as_of"]), (444, "2026-10-24"))
            self.assertTrue(meta["version"])
            self.assertRegex(meta["generator_revision"], CORE_REVISION)

    def test_stock_register_and_sensor_data_honour_as_of_without_wall_clock(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stock_register.write(root / "r1", n=20, seed=11, as_of="2026-10-15")
            stock_register.write(root / "r2", n=20, seed=11, as_of="2031-01-02")
            self.assertEqual(
                (root / "r1/stock-register.csv").read_bytes(),
                (root / "r2/stock-register.csv").read_bytes(),
            )
            manifests = [json.loads((root / f"r{i}/manifest.json").read_text()) for i in (1, 2)]
            self.assertEqual([m["as_of"] for m in manifests], ["2026-10-15", "2031-01-02"])
            for as_of in ("2026-10-15", "2026-10-16"):
                sensor_backfill.write(
                    root / f"s{as_of}", homes=2, seed=11, days=1, cadence=720, as_of=as_of
                )
            first, second = (
                json.loads((root / f"s{d}/manifest.json").read_text())
                for d in ("2026-10-15", "2026-10-16")
            )
            self.assertEqual((first["as_of"], second["as_of"]), ("2026-10-15", "2026-10-16"))
            self.assertNotEqual(
                (root / "s2026-10-15/readings-0000.csv").read_bytes(),
                (root / "s2026-10-16/readings-0000.csv").read_bytes(),
            )

    def test_custom_fault_rates_truth_manifest_records_revision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "f"
            sensor_backfill.write(
                out,
                homes=2,
                seed=11,
                days=1,
                cadence=720,
                as_of=da.AS_OF,
                fault_rates={"outlier": 0.05},
            )
            analysis = json.loads((out / "analysis/manifest.json").read_text())
            truth = json.loads((out / "truth/manifest.json").read_text())
            self.assertEqual(truth["seed"], 11)
            self.assertRegex(truth["generator_revision"], CORE_REVISION)
            self.assertEqual(truth["generator_revision"], analysis["generator_revision"])

    def test_manifests_record_seed_version_and_revision_for_every_seed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for seed in (1, 2):
                scale_fixture.write(
                    root / f"scale{seed}", n=4, per_home=2, seed=seed, as_of=da.AS_OF
                )
                manifest = json.loads((root / f"scale{seed}/manifest.json").read_text())
                self.assertEqual(manifest["seed"], seed)
                self.assertEqual(manifest["version"], scale_fixture.VERSION)
                self.assertRegex(manifest["generator_revision"], CORE_REVISION)


if __name__ == "__main__":
    unittest.main()
