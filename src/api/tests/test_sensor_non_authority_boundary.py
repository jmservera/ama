"""No sensor signal diagnoses a hazard, starts a clock, releases a hold or changes ranking.

End-to-end boundary for issue 109 criterion 3 (Refs #109, #111): retained fictional readings,
analysis, review candidates and a synthetic-approval review draft leave hazard state, the
service-owned hazard clocks, holds and portfolio ranking untouched. Constructed approvals are
SYNTHETIC TEST ONLY, never an actual signoff.
"""

import copy
import json
import random
import tempfile
import unittest
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, ClassVar

import dataset
from sensor_consumer_fixture import CONTROL, POLICY
from zava_forward.core import ranking
from zava_forward.core import sensor_analysis as sa
from zava_forward.core import sensor_analysis_store as sas
from zava_forward.core import sensor_review_draft as srd
from zava_forward.core.sensor_consumer import SensorConsumer, preflight
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.synthetic import sensor_scenarios as ss

DAYS = 7
WINDOW = ss.Window(ss.START, ss.START + timedelta(days=DAYS))
START = "2024-01-01T00:00:00Z"
END = "2024-01-08T00:00:00Z"
RECEIVED = END
POLICY_7D = replace(POLICY, window_start=START, window_end=END, max_past_seconds=86400 * 8)
APPROVED = sa.AnalysisPolicy(
    approval=sa.RuleApproval(
        sa.RULE_ID, sa.ANALYSIS_VERSION, "SYNTHETIC TEST ONLY", "SYNTHETIC-TEST-SENTINEL"
    )
)
ENV = {srd.FLAG: "1"}
AWARE = "2026-01-01T10:00:00Z"
TIMES = dict(
    response_due_at="2026-01-02T10:00:00Z",
    resident_update_due_at="2026-01-03T10:00:00Z",
)
# Home, temperature, humidity and consent. ZF-1 and ZF-2 carry live safety state.
HOMES = (
    ("ZF-1", "SENS-SYN-1", ("5.00", "6.00"), ("100.00", "98.00"), "granted"),
    ("ZF-2", "SENS-SYN-2", ("45.00", "44.00"), ("99.00", "97.00"), "granted"),
    ("ZF-3", "SENS-SYN-3", ("-10.00", "-9.00"), ("98.00", "96.00"), "granted"),
    ("ZF-4", "SENS-SYN-4", ("19.00", "20.00"), ("55.00", "57.00"), "granted"),
    ("ZF-5", "SENS-SYN-5", ("20.00", "21.00"), ("100.00", "98.00"), "declined"),
)
Spec = tuple[str, str, tuple[str, str], tuple[str, str], str]
SENSOR_PREFIX = "sensor_"


def readings(
    home: str, sensor: str, temperature: tuple[str, str], humidity: tuple[str, str]
) -> list[dict[str, object]]:
    template = next(
        c for c in ss.generate() if c.truth.family == "damp" and c.truth.label == "normal"
    ).rows[: DAYS * 24]
    rows = []
    for n, row in enumerate(template):
        at = datetime.strptime(str(row["observed_at"]), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
        rows.append(
            dict(
                row,
                home_id=home,
                sensor_id=sensor,
                reading_id=f"{sensor}-{int(at.timestamp())}",
                temperature_c=temperature[n % 2],
                humidity_pct=humidity[n % 2],
            )
        )
    return rows


def staff(code: str, role: str) -> dict[str, str]:
    return dict(code=code, name=f"Person {code}", email=f"{code.lower()}@example.test", role=role)


def stable(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Drop the data version and meta row, which any permitted draft write advances."""
    tables = {k: v for k, v in snapshot["tables"].items() if k != "meta"}
    return {k: v for k, v in snapshot.items() if k != "version"} | {"tables": tables}


class SensorNonAuthorityBoundary(unittest.TestCase):
    store: ClassVar[SqlStore]
    consumer: ClassVar[SensorConsumer]
    tmp: ClassVar[tempfile.TemporaryDirectory[str]]
    before: ClassVar[dict[str, Any]]
    table_names: ClassVar[list[str]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        data = copy.deepcopy(dataset.DATA)
        data["staff"].extend(
            [
                staff("BS-1", "Building Safety Liaison"),
                staff("BS-2", "Building Safety Liaison"),
                staff("QI-1", "Quality Inspector"),
            ]
        )
        seed = Path(cls.tmp.name) / "constructed.json"
        seed.write_text(json.dumps(data))
        cls.store = SqlStore(str(seed), str(seed.with_suffix(".sqlite")))
        cls.addClassCleanup(cls.store.db.close)
        cls.consumer = SensorConsumer(cls.store)
        if cls.consumer.mssql:
            raise unittest.SkipTest("SQLite-only focused test")
        cls.seed_safety_state()
        cls.before = cls.snapshot()
        cls.ingest(list(HOMES))

    @classmethod
    def seed_safety_state(cls) -> None:
        store = cls.store
        sam, pam = store.staff["sam@example.test"], store.staff["pam@example.test"]
        bea = store.staff["bs-1@example.test"]
        meta = dict(source="SYN fixture report", aware_at=AWARE)
        store.raise_hazard(sam, "ZF-1", "Damp and mould", "Emergency", "", meta)
        store.refer_hazard(sam, "ZF-1", 0, bea["email"], "SYN-JOB-1", dict(evidence="SYN-SENT"))
        store.receive_hazard(bea, "ZF-1", 0, "SYN-RECEIVED")
        store.accept_hazard(bea, "ZF-1", 0, "SYN-ACCEPTED")
        store.observe_hazard_times(bea, "ZF-1", 0, dict(evidence="SYN-TIMES", **TIMES))
        store.raise_hazard(sam, "ZF-2", "Damp and mould", "Emergency", "", meta)
        store.place_legal_hold(pam, "ZF-3", "SYN-HOLD-1")

    @classmethod
    def ingest(cls, sensors: list[Spec]) -> None:
        controls = [
            replace(
                CONTROL,
                sensor_id=sensor,
                home_id=home,
                consent=consent,
                mapping_start=START,
                mapping_end=END,
                calibration_start=START,
                calibration_end=END,
            )
            for home, sensor, _, _, consent in sensors
        ]
        cls.consumer.configure(POLICY_7D, controls)
        rows: list[dict[str, object]] = []
        for home, sensor, temperature, humidity, _ in sensors:
            rows += readings(home, sensor, temperature, humidity)
        random.Random(109).shuffle(rows)
        # The consumer rejects out-of-order rows per sensor, so deliver each sensor in time order.
        rows.sort(key=lambda r: (str(r["sensor_id"]), str(r["observed_at"])))
        for start in range(0, len(rows), 100):
            for item in preflight(rows[start : start + 100]):
                cls.consumer.process(item, RECEIVED)

    @classmethod
    def snapshot(cls) -> dict[str, Any]:
        store = cls.store
        with store.lock:
            cases = json.loads(json.dumps(store.cases, sort_keys=True, default=str))
        for case in cases.values():
            case.pop(srd.CASE_KEY, None)
        tables: dict[str, Any] = {}
        baseline_names: list[str] = []
        names = [
            row[0] for row in store.db.execute("SELECT name FROM sqlite_master WHERE type='table'")
        ]
        baseline = getattr(cls, "table_names", None)
        for name in sorted(names):
            if (
                name.startswith(SENSOR_PREFIX)
                or "audit" in name
                or name == "sqlite_sequence"
                or name == "cases"
            ):
                continue
            if baseline is not None and name not in baseline:
                continue
            baseline_names.append(name)
            tables[name] = [list(r) for r in store.db.execute(f"SELECT * FROM {name}").fetchall()]
        cls.table_names = baseline_names
        open_cases = [c for c in cases.values() if not c["closed"]]
        return dict(
            cases=cases,
            hazards={cid: store.hazard_states(cid) for cid in sorted(cases)},
            ranking=ranking.canonical(ranking.rank(open_cases, ranking.CURRENT)),
            served_ranking=json.dumps(store._ranking(), sort_keys=True),
            version=store.version,
            tables=tables,
        )

    def test_extreme_and_normal_readings_change_no_authority_state(self) -> None:
        before = self.before
        self.assertEqual(
            [h["state"] for h in before["hazards"]["ZF-1"]], ["Accepted"], "baseline hazard"
        )
        self.assertTrue(before["cases"]["ZF-3"]["legal_hold"]["active"])
        retained = self.store.db.execute("SELECT COUNT(*) FROM sensor_reading").fetchone()[0]
        self.assertEqual(retained, 4 * DAYS * 24, "declined home retains nothing")

        outcomes = {}
        for home, *_ in HOMES:
            for policy in (None, APPROVED):
                signal = sas.analyse_retained(self.consumer, home, WINDOW, WINDOW.end, policy)
                candidate = sa.review_task_candidate(signal, policy)
                outcomes[(home, policy is not None)] = (signal, candidate)
                self.assertFalse(signal.diagnoses_hazard)
                self.assertEqual(signal.priority_effect, "NONE")
                if candidate is not None:
                    for flag in ("changes_ranking", "starts_clock", "releases_hold"):
                        self.assertFalse(getattr(candidate, flag), flag)
                    self.assertFalse(candidate.diagnoses_hazard)
                    self.assertEqual(candidate.status, "PROPOSED")
                    self.assertTrue(candidate.resident_report_unaffected)
        self.assertEqual(outcomes[("ZF-1", True)][0].outcome, sa.REVIEW)
        self.assertIsNotNone(outcomes[("ZF-1", True)][1], "adverse readings must be non-vacuous")
        self.assertIsNone(outcomes[("ZF-1", False)][1])
        self.assertEqual(outcomes[("ZF-4", True)][0].outcome, sa.NO_SIGNAL)
        self.assertEqual(outcomes[("ZF-5", True)][0].sufficiency, sa.DECLINED)
        self.assertIsNone(outcomes[("ZF-5", True)][1])
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.store.version, before["version"])

    def test_review_draft_adds_only_the_draft_record(self) -> None:
        qi = self.store.staff["qi-1@example.test"]
        signal = sas.analyse_retained(self.consumer, "ZF-1", WINDOW, WINDOW.end, APPROVED)
        audits = self.store.db.execute("SELECT COUNT(*) FROM audit").fetchone()[0]
        made = srd._record_draft_synthetic(
            self.store, qi, "ZF-1", signal, APPROVED, env=ENV, at="2024-01-08T00:00:00Z"
        )
        self.assertTrue(made["created"], made)
        count = self.store.db.execute("SELECT COUNT(*) FROM audit").fetchone()[0]
        self.assertEqual(count, audits + 1)
        draft = self.store.cases["ZF-1"][srd.CASE_KEY][0]
        self.assertEqual(draft["state"], srd.STATE)
        self.assertTrue(draft["manual_review_only"])
        self.assertIsNone(draft["activation"])
        for flag in ("changes_ranking", "starts_clock", "releases_hold", "diagnoses_hazard"):
            self.assertFalse(draft["candidate"][flag], flag)
        after = stable(self.snapshot())
        for key in after["tables"]:
            self.assertEqual(after["tables"][key], stable(self.before)["tables"][key], key)
        self.assertEqual(after, stable(self.before))

    def test_drafts_stay_refused_for_the_served_policy_and_leave_state_unchanged(self) -> None:
        qi = self.store.staff["qi-1@example.test"]
        refused = srd.draft_from_retained(
            self.store, qi, "ZF-1", WINDOW, WINDOW.end + timedelta(days=1), env=ENV
        )
        self.assertFalse(refused["created"])
        after = stable(self.snapshot())
        for key in after["tables"]:
            self.assertEqual(after["tables"][key], stable(self.before)["tables"][key], key)
        self.assertEqual(after, stable(self.before))

    def test_hazard_hold_and_clock_stay_service_owned_after_sensor_activity(self) -> None:
        hazards = {h["index"]: h for h in self.store.hazard_states("ZF-1")}
        accepted = hazards[0]
        self.assertEqual(accepted["state"], "Accepted")
        self.assertEqual(accepted["hold"]["status"], "Active")
        recorded = self.before["hazards"]["ZF-1"][0]
        for field in ("aware_at", "response_due_at", "resident_update_due_at", "responded_at"):
            self.assertEqual(accepted[field], recorded[field], field)
        for field in ("aware_at", "response_due_at", "resident_update_due_at"):
            self.assertIsNotNone(accepted[field], field)
        self.assertEqual([h["state"] for h in self.store.hazard_states("ZF-2")], ["Raised"])
        self.assertEqual(self.store.hazard_states("ZF-2")[0]["hold"]["status"], "Active")
        for case_id in ("ZF-3", "ZF-5"):
            self.assertEqual(self.store.hazard_states(case_id), [])
        self.assertTrue(self.store.cases["ZF-3"]["legal_hold"]["active"])
        self.assertNotIn(srd.CASE_KEY, self.store.cases["ZF-2"])


if __name__ == "__main__":
    unittest.main()
