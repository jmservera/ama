"""Sensor analysis outputs are reproducible from retained readings alone (Refs #111 criterion 1).

Fictional exercise data and a constructed approval: SYNTHETIC TEST ONLY, never a signoff.
"""

import json
import os
import random
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from datetime import timedelta
from pathlib import Path
from typing import ClassVar

from sensor_consumer_fixture import CONTROL, POLICY, store_at
from zava_forward.core import sensor_analysis as sa
from zava_forward.core import sensor_analysis_store as sas
from zava_forward.core.sensor_consumer import SensorConsumer, preflight
from zava_forward.core.synthetic import sensor_scenarios as ss

HOME = CONTROL.home_id
WINDOW = ss.Window(ss.START, ss.START + timedelta(days=ss.DAYS))
AS_OF = WINDOW.end
STAMP_START = "2024-01-01T00:00:00Z"
STAMP_END = "2024-01-29T00:00:00Z"
RECEIVED = STAMP_END
SC_POLICY = replace(
    POLICY, window_start=STAMP_START, window_end=STAMP_END, max_past_seconds=86400 * 30
)
SC_CONTROL = replace(
    CONTROL,
    mapping_start=STAMP_START,
    mapping_end=STAMP_END,
    calibration_start=STAMP_START,
    calibration_end=STAMP_END,
)
APPROVED = sa.AnalysisPolicy(
    approval=sa.RuleApproval(
        sa.RULE_ID, sa.ANALYSIS_VERSION, "SYNTHETIC TEST ONLY", "SYNTHETIC-TEST-SENTINEL"
    )
)
FRESH = """
import json, sys
from datetime import timedelta
from zava_forward.core import sensor_analysis as sa
from zava_forward.core import sensor_analysis_store as sas
from zava_forward.core.sensor_consumer import SensorConsumer
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.synthetic import sensor_scenarios as ss
seed, db, home = sys.argv[1:4]
policy = sa.AnalysisPolicy(approval=sa.RuleApproval(
    sa.RULE_ID, sa.ANALYSIS_VERSION, "SYNTHETIC TEST ONLY", "SYNTHETIC-TEST-SENTINEL"))
window = ss.Window(ss.START, ss.START + timedelta(days=ss.DAYS))
consumer = SensorConsumer(SqlStore(seed, db))
signal = sas.analyse_retained(consumer, home, window, window.end, policy)
cand = sa.review_task_candidate(signal, policy)
body = dict(signal=sa.as_dict(signal), candidate=cand and sa.as_dict(cand))
print(json.dumps(body, sort_keys=True))
"""


def scenario_rows(label: str) -> list[dict[str, object]]:
    case = next(c for c in ss.generate() if c.truth.family == "damp" and c.truth.label == label)
    return [dict(r, home_id=HOME, sensor_id=SC_CONTROL.sensor_id) for r in case.rows]


def render(consumer: SensorConsumer, policy: sa.AnalysisPolicy | None = None) -> bytes:
    signal = sas.analyse_retained(consumer, HOME, WINDOW, AS_OF, policy)
    candidate = sa.review_task_candidate(signal, policy)
    payload = dict(signal=sa.as_dict(signal), candidate=candidate and sa.as_dict(candidate))
    return json.dumps(payload, sort_keys=True).encode()


PLAN = (
    ("sustained_high_humidity", "ordered", 100),
    ("sustained_high_humidity", "ordered", 37),
    ("sustained_high_humidity", "shuffled", 100),
    ("repeated_overnight_peaks", "ordered", 100),
    ("normal", "ordered", 100),
    ("missing_data", "ordered", 100),
)


def arrival(label: str, order: str) -> list[dict[str, object]]:
    rows = scenario_rows(label)
    if order == "shuffled":
        random.Random(20241114).shuffle(rows)
    return rows


class Reproducibility(unittest.TestCase):
    tmp: tempfile.TemporaryDirectory[str]
    consumers: ClassVar[dict[tuple[str, str, int], SensorConsumer]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.consumers = {}
        for label, order, size in PLAN:
            folder = Path(cls.tmp.name) / f"{label}-{order}-{size}"
            folder.mkdir()
            store = store_at(str(folder), reset=True)
            cls.addClassCleanup(store.db.close)
            consumer = SensorConsumer(store)
            if consumer.mssql:
                raise unittest.SkipTest("SQLite-only focused test")
            consumer.configure(SC_POLICY, [SC_CONTROL])
            rows = arrival(label, order)
            for start in range(0, len(rows), size):
                for item in preflight(rows[start : start + size]):
                    consumer.process(item, RECEIVED)
            cls.consumers[(label, order, size)] = consumer

    def consumer(self, label: str, order: str = "ordered", size: int = 100) -> SensorConsumer:
        return self.consumers[(label, order, size)]

    def test_outputs_identical_across_row_orders_batch_sizes_and_replays(self) -> None:
        for label in ("sustained_high_humidity", "repeated_overnight_peaks", "normal"):
            with self.subTest(label=label):
                consumer = self.consumer(label)
                first = render(consumer, APPROVED)
                self.assertEqual(first, render(consumer, APPROVED))
                retained = consumer.observed_series([HOME])
                self.assertEqual(len(retained), 672)
                rng = random.Random(7)
                for permuted in (retained[::-1], rng.sample(retained, len(retained))):
                    signal = sa.derive_signal(HOME, permuted, WINDOW, AS_OF, "granted", APPROVED)
                    candidate = sa.review_task_candidate(signal, APPROVED)
                    payload = dict(
                        signal=sa.as_dict(signal), candidate=candidate and sa.as_dict(candidate)
                    )
                    self.assertEqual(json.dumps(payload, sort_keys=True).encode(), first)
        small = self.consumer("sustained_high_humidity", size=37)
        self.assertEqual(
            render(small, APPROVED), render(self.consumer("sustained_high_humidity"), APPROVED)
        )
        body = json.loads(render(self.consumer("sustained_high_humidity"), APPROVED))
        self.assertEqual(body["signal"]["analysis_version"], sa.ANALYSIS_VERSION)
        self.assertEqual(body["signal"]["policy_version"], sa.ANALYSIS_VERSION)
        self.assertTrue(body["signal"]["threshold_label"].startswith("EXERCISE VALUE"))

    def test_redelivery_does_not_change_the_retained_set_or_output(self) -> None:
        consumer = self.consumer("repeated_overnight_peaks")
        before = render(consumer, APPROVED)
        rows = scenario_rows("repeated_overnight_peaks")[:100]
        for item in preflight(rows):
            consumer.process(item, RECEIVED)
        self.assertEqual(len(consumer.observed_series([HOME])), 672)
        self.assertEqual(render(consumer, APPROVED), before)

    def test_out_of_order_arrival_is_rejected_so_only_retained_rows_drive_a_deterministic_result(
        self,
    ) -> None:
        shuffled = self.consumer("sustained_high_humidity", "shuffled")
        retained = shuffled.observed_series([HOME])
        self.assertLess(len(retained), 672)
        signal = sas.analyse_retained(shuffled, HOME, WINDOW, AS_OF, APPROVED)
        self.assertEqual(
            signal, sa.derive_signal(HOME, retained, WINDOW, AS_OF, "granted", APPROVED)
        )
        self.assertEqual((signal.sufficiency, signal.priority_effect), (sa.INSUFFICIENT, "NONE"))
        self.assertIsNone(sa.review_task_candidate(signal, APPROVED))
        self.assertEqual(render(shuffled, APPROVED), render(shuffled, APPROVED))

    def test_review_task_trigger_is_stable_and_follows_only_retained_readings(self) -> None:
        reference = self.consumer("sustained_high_humidity")
        signal = sas.analyse_retained(reference, HOME, WINDOW, AS_OF, APPROVED)
        candidate = sa.review_task_candidate(signal, APPROVED)
        assert candidate is not None
        again = sa.review_task_candidate(
            sas.analyse_retained(
                self.consumer("sustained_high_humidity", size=37), HOME, WINDOW, AS_OF, APPROVED
            ),
            APPROVED,
        )
        self.assertEqual(candidate, again)
        self.assertEqual(candidate.status, "PROPOSED")
        self.assertIsNone(sa.review_task_candidate(signal))
        for label in ("normal", "missing_data"):
            quiet = sas.analyse_retained(self.consumer(label), HOME, WINDOW, AS_OF, APPROVED)
            self.assertIsNone(sa.review_task_candidate(quiet, APPROVED))

    def test_a_changed_retained_reading_changes_the_digest_not_the_versions(self) -> None:
        rows = [dict(r) for r in self.consumer("sustained_high_humidity").observed_series([HOME])]
        first = sa.derive_signal(HOME, rows, WINDOW, AS_OF, "granted", APPROVED)
        rows[10]["humidity_pct"] = "12.00"
        second = sa.derive_signal(HOME, rows, WINDOW, AS_OF, "granted", APPROVED)
        self.assertNotEqual(first.input_digest, second.input_digest)
        for key in ("analysis_version", "policy_version", "threshold_label"):
            self.assertEqual(getattr(first, key), getattr(second, key))

    def test_fresh_process_reconstructs_identical_output_from_retained_readings_only(self) -> None:
        expected = render(self.consumer("sustained_high_humidity"), APPROVED)
        folder = Path(self.tmp.name) / "sustained_high_humidity-ordered-100"
        seed, db = folder / "constructed.json", folder / "constructed.sqlite"
        for env_hash in ("0", "1", "random"):
            env = dict(os.environ, PYTHONHASHSEED=env_hash, PYTHONDONTWRITEBYTECODE="1")
            done = subprocess.run(
                [sys.executable, "-B", "-c", FRESH, str(seed), str(db), HOME],
                capture_output=True,
                check=True,
                env=env,
                text=True,
            )
            self.assertEqual(done.stdout.strip().encode(), expected)


if __name__ == "__main__":
    unittest.main()
