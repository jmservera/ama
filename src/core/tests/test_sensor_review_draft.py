"""Default-off sensor review drafts over an existing candidate (Refs #111).

Every approval in this file is SYNTHETIC TEST ONLY. It is not a company, professional or
approved-method signoff, and no rule is activated. Drafts are never tasks.
"""

import copy
import json
import os
import tempfile
import threading
import unittest
from collections.abc import Callable, Mapping
from contextlib import AbstractContextManager
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any
from unittest import mock

import dataset
from sensor_consumer_fixture import CONTROL, POLICY, SENSOR_STATE_TABLES
from zava_forward.core import projection
from zava_forward.core import sensor_analysis as sa
from zava_forward.core import sensor_review_draft as srd
from zava_forward.core.assistants import REGISTRY
from zava_forward.core.sensor_consumer import SensorConsumer, preflight
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import ConflictError, Store
from zava_forward.core.synthetic import sensor_scenarios as ss

CID = "ZF-1"
SYNTHETIC_APPROVAL = sa.RuleApproval(
    sa.RULE_ID, sa.ANALYSIS_VERSION, "SYNTHETIC TEST ONLY", "SYNTHETIC-TEST-SENTINEL"
)
APPROVED = sa.AnalysisPolicy(approval=SYNTHETIC_APPROVAL)
WINDOW = ss.Window(ss.START, ss.START + timedelta(days=ss.DAYS))
SCENARIOS = {c.truth.label: c for c in ss.generate() if c.truth.family == "damp"}
PEOPLE = {
    role: dict(code=f"R{i}", name=f"Person {i}", email=f"p{i}@example.test", role=role)
    for i, role in enumerate(
        projection.STAFF_ROLES + ("Contractor", "Application Administrator", "Resident")
    )
}
QI = PEOPLE["Quality Inspector"]
PM = PEOPLE["Retrofit Programme Manager"]
ON = {srd.FLAG: "1"}
Json = srd.Json

# The mixins below are not TestCase subclasses, so discovery skips them; type them as TestCase.
if TYPE_CHECKING:
    _Base = unittest.TestCase
else:
    _Base = object


def signal(
    label: str = "sustained_high_humidity",
    *,
    consent: str = "granted",
    as_of: datetime | None = None,
    **changes: Any,
) -> sa.Signal:
    rows = [dict(r, home_id=CID, sensor_id="SENS-SYN-1") for r in SCENARIOS[label].rows]
    value = sa.derive_signal(CID, rows, WINDOW, as_of or WINDOW.end, consent, APPROVED)
    return replace(value, **changes) if changes else value


def seed(directory: str) -> str:
    data = copy.deepcopy(dataset.DATA)
    data["staff"] = list(PEOPLE.values())
    path = os.path.join(directory, "seed.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return path


class DraftCases(_Base):
    """Backend-neutral cases. Subclasses set `sql` and implement open()."""

    sql = False
    env = ON
    store: srd.DraftStore

    def open(self, reset: bool = False) -> srd.DraftStore:
        raise NotImplementedError

    def version(self) -> int:
        raise NotImplementedError

    def read(self) -> Json:
        raise NotImplementedError

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        patch = mock.patch.dict(os.environ, self.env)
        patch.start()
        self.addCleanup(patch.stop)
        self.store = self.open(reset=True)
        self.addCleanup(self.close, self.store)
        self.base_audits = len(list(self.store.audit_entries()))

    def close(self, store: srd.DraftStore) -> None:
        if isinstance(store, SqlStore):
            store.db.close()

    def case(self, store: srd.DraftStore | None = None) -> Json:
        cases: Json = (store or self.store).cases[CID]
        return cases

    def audits(self, store: srd.DraftStore | None = None) -> int:
        return len(list((store or self.store).audit_entries())) - self.base_audits

    def set_staff(self, person: Json, **changes: object) -> None:
        updated = dict(person, **changes)
        if isinstance(self.store, SqlStore):
            self.store.db.execute(
                "UPDATE staff SET body=? WHERE email=?", (json.dumps(updated), person["email"])
            )
        else:
            self.store.staff[person["email"]] = updated

    def tamper(self, change: Callable[[Json], object]) -> None:
        with self.store.lock:
            change(self.store._case(CID)[srd.CASE_KEY][0])
            self.store.save()

    def propose(
        self,
        sig: sa.Signal | None = None,
        policy: sa.AnalysisPolicy = APPROVED,
        user: Mapping[str, object] = QI,
        *,
        at: str | None = None,
    ) -> Json:
        return srd._record_draft_synthetic(self.store, user, CID, sig or signal(), policy, at=at)

    def test_default_off_changes_nothing(self) -> None:
        before, audits = json.dumps(self.case(), sort_keys=True), self.audits()
        with mock.patch.dict(os.environ, {srd.FLAG: ""}):
            self.assertEqual(srd.read_drafts(self.store, QI, CID), {"state": "disabled"})
            with self.assertRaises(PermissionError):
                self.propose()
            with self.assertRaises(PermissionError):
                srd.draft_from_retained(self.store, QI, CID, WINDOW, WINDOW.end)
        self.assertEqual((json.dumps(self.case(), sort_keys=True), self.audits()), (before, audits))

    def test_role_gate_precedes_flag_and_matches_the_sensor_screen_roles(self) -> None:
        self.assertEqual(srd.DRAFT_ROLES, tuple(REGISTRY["quality-evidence"]["roles"]))
        for flag in ("1", ""):
            for role, person in PEOPLE.items():
                if role in srd.DRAFT_ROLES:
                    continue
                with (
                    self.subTest(role=role, flag=flag),
                    mock.patch.dict(os.environ, {srd.FLAG: flag}),
                ):
                    with self.assertRaises(PermissionError):
                        srd.read_drafts(self.store, person, CID)
                    with self.assertRaises(PermissionError):
                        self.propose(user=person)
        self.assertEqual(self.audits(), 0)

    def test_current_staff_and_scope_are_rechecked(self) -> None:
        cases = (
            ("disabled", QI, dict(disabled=True)),
            ("inactive", QI, dict(active=False)),
            ("role changed", QI, dict(role="Resident Liaison Officer")),
            ("case scope", QI, dict(case_ids=["ZF-2"])),
            ("area scope", QI, dict(areas=["Nowhere"])),
            ("malformed scope", QI, dict(case_ids="ZF-1")),
        )
        for name, person, change in cases:
            with self.subTest(name):
                self.set_staff(person, **change)
                with self.assertRaises(PermissionError):
                    srd.read_drafts(self.store, person, CID)
                with self.assertRaises(PermissionError):
                    self.propose()
                self.set_staff(person)
        self.assertEqual(self.audits(), 0)
        with self.assertRaises(KeyError):
            srd.read_drafts(self.store, QI, "ZF-MISSING")

    def test_default_denial_without_an_approved_rule(self) -> None:
        wrong = replace(SYNTHETIC_APPROVAL, rule_id="OTHER")
        for policy in (sa.AnalysisPolicy(), replace(APPROVED, approval=wrong)):
            result = self.propose(signal(), policy)
            self.assertEqual(result["refusal"], "NO_APPROVED_RULE")
        self.assertNotIn(srd.CASE_KEY, self.case())
        self.assertEqual(self.audits(), 0)

    def test_refusals_write_nothing(self) -> None:
        future = signal(as_of=WINDOW.end - timedelta(days=1))
        cases = (
            (signal(consent="unknown"), "SIGNAL_INSUFFICIENT"),
            (signal(consent="declined"), "SIGNAL_DECLINED"),
            (signal(as_of=WINDOW.end + timedelta(days=30)), "SIGNAL_STALE"),
            (signal("normal"), "NO_REVIEW_SIGNAL"),
            (signal(home_id="ZF-2"), "SIGNAL_HOME_MISMATCH"),
            (replace(future, sufficiency=sa.SUFFICIENT, outcome=sa.REVIEW), "FUTURE_READINGS"),
        )
        for sig, code in cases:
            with self.subTest(code):
                result = self.propose(sig)
                self.assertEqual((result["created"], result["refusal"]), (False, code))
        self.assertNotIn(srd.CASE_KEY, self.case())
        self.assertEqual(self.audits(), 0)

    def test_exact_candidate_lineage_and_no_side_effects(self) -> None:
        sig = signal()
        expected = sa.review_task_candidate(sig, APPROVED)
        assert expected is not None
        before = copy.deepcopy(self.case())
        recs = json.dumps(self.store.data["recommendations"], sort_keys=True)
        result = self.propose(sig, at="2026-11-10T05:00:00Z")
        self.assertTrue(result["created"])
        record = self.case()[srd.CASE_KEY][0]
        self.assertEqual(record["candidate"], sa.as_dict(expected))
        self.assertEqual(record["task_key"], expected.task_key)
        self.assertEqual(
            (
                record["state"],
                record["manual_review_only"],
                record["approval_verified"],
                record["activation"],
            ),
            ("PROPOSED_UNAPPROVED", True, False, None),
        )
        view = result["draft"]
        self.assertEqual(view["candidate"]["task_key"], expected.task_key)
        self.assertFalse(
            any(
                view["candidate"][k]
                for k in ("changes_ranking", "starts_clock", "releases_hold", "diagnoses_hazard")
            )
        )
        after = copy.deepcopy(self.case())
        after.pop(srd.CASE_KEY)
        self.assertEqual(after, before)
        self.assertEqual(json.dumps(self.store.data["recommendations"], sort_keys=True), recs)
        self.assertEqual(self.audits(), 1)

    def test_idempotent_reopen_and_immutable_provenance(self) -> None:
        first = self.propose(at="2026-11-10T05:00:00Z")
        stored = json.dumps(self.case()[srd.CASE_KEY][0], sort_keys=True)
        audits, version = self.audits(), self.version()
        again = self.propose(
            signal(as_of=WINDOW.end + timedelta(hours=1)), at="2027-01-01T00:00:00Z"
        )
        self.assertEqual((again["created"], again["existing"]), (False, True))
        self.assertEqual(again["draft"], first["draft"])
        self.assertEqual((self.audits(), self.version()), (audits, version))
        self.assertEqual(len(self.case()[srd.CASE_KEY]), 1)
        other = self.propose(signal("repeated_overnight_peaks"))
        self.assertTrue(other["created"])
        self.assertEqual(len(self.case()[srd.CASE_KEY]), 2)
        self.assertEqual(json.dumps(self.case()[srd.CASE_KEY][0], sort_keys=True), stored)

    def test_bound_without_eviction(self) -> None:
        for i in range(srd.MAX_DRAFTS):
            self.assertTrue(self.propose(signal(input_digest=f"{i:064d}"))["created"])
        over = self.propose(signal(input_digest="f" * 64))
        self.assertEqual(over["refusal"], "DRAFT_LIMIT_REACHED")
        replay = self.propose(signal(input_digest=f"{0:064d}"))
        self.assertTrue(replay["existing"])
        self.assertEqual(len(self.case()[srd.CASE_KEY]), srd.MAX_DRAFTS)

    def test_restart_durability(self) -> None:
        self.propose()
        stored = json.dumps(self.case()[srd.CASE_KEY], sort_keys=True)
        self.close(self.store)
        self.store = self.open()
        self.addCleanup(self.close, self.store)
        self.assertEqual(json.dumps(self.case()[srd.CASE_KEY], sort_keys=True), stored)
        self.assertTrue(self.propose()["existing"])
        self.assertEqual(len(self.case()[srd.CASE_KEY]), 1)

    def test_tampered_draft_is_withheld_and_never_overwritten(self) -> None:
        self.propose()
        self.tamper(lambda r: r["candidate"].__setitem__("summary", "tampered"))
        key = self.case()[srd.CASE_KEY][0]["task_key"]
        again = self.propose()
        self.assertEqual(again["draft"], {"state": "INTEGRITY_MISMATCH", "task_key": key})
        self.assertEqual(self.case()[srd.CASE_KEY][0]["candidate"]["summary"], "tampered")

    def test_generic_staff_and_contractor_detail_never_carry_drafts(self) -> None:
        self.propose()
        for role, person in PEOPLE.items():
            with self.subTest(role=role):
                detail = json.dumps(self.store.detail(CID, person) or {})
                self.assertNotIn(srd.CASE_KEY, detail)
                self.assertNotIn("SYNTHETIC-TEST-SENTINEL", detail)
        self.assertIn(srd.CASE_KEY, self.store.detail(CID))

    def test_read_is_allowlisted_and_never_shows_the_digest_or_unknown_keys(self) -> None:
        self.propose()
        self.tamper(lambda r: r.__setitem__("resident_phone", "07000"))
        if isinstance(self, SqlDraftCases):
            self.grant()
        read = self.read()
        if self.sql:
            self.assertEqual(read["state"], "ok")
            text = json.dumps(read)
            self.assertNotIn("07000", text)
            self.assertNotIn(self.case()[srd.CASE_KEY][0]["draft_digest"], text)
            self.assertEqual(read["drafts"][0]["state"], "INTEGRITY_MISMATCH")

    def test_write_failure_restores_the_list_and_retry_creates_one(self) -> None:
        audits = self.audits()
        with mock.patch.object(self.store, "save", side_effect=RuntimeError("disk")):
            with self.assertRaises(RuntimeError):
                self.propose()
        self.assertNotIn(srd.CASE_KEY, self.case())
        self.assertEqual(self.audits(), audits)
        self.assertTrue(self.propose()["created"])
        self.assertEqual((len(self.case()[srd.CASE_KEY]), self.audits()), (1, audits + 1))

    def test_concurrent_same_key_creates_exactly_one(self) -> None:
        results: list[bool] = []
        threads = [
            threading.Thread(target=lambda: results.append(self.propose()["created"]))
            for _ in range(4)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(
            (sorted(results), len(self.case()[srd.CASE_KEY]), self.audits()),
            ([False] * 3 + [True], 1, 1),
        )

    def test_synthetic_label_is_not_an_approval(self) -> None:
        view = self.propose()["draft"]
        self.assertFalse(view["approval_verified"])
        self.assertIn("Not an approved task", view["label"])
        self.assertEqual(view["candidate"]["approval_reference"], "SYNTHETIC-TEST-SENTINEL")


class JsonDraftCases(DraftCases, unittest.TestCase):
    store: Store

    def open(self, reset: bool = False) -> Store:
        return Store(seed(self.tmp.name))

    def version(self) -> int:
        version: int = self.store.version
        return version

    def read(self) -> Json:
        return srd.read_drafts(self.store, QI, CID)

    def test_read_fails_closed_without_a_consent_source(self) -> None:
        self.propose()
        read = self.read()
        self.assertEqual((read["state"], read["drafts"]), ("consent-withheld", []))
        self.assertNotIn("summary", json.dumps(read))

    def test_served_write_is_unavailable_without_retained_sql(self) -> None:
        result = srd.draft_from_retained(self.store, QI, CID, WINDOW, WINDOW.end)
        self.assertEqual(result["refusal"], "RETAINED_READINGS_UNAVAILABLE")
        self.assertNotIn(srd.CASE_KEY, self.case())

    def disk_drafts(self) -> list[dict[str, object]]:
        with open(self.store.live_path, encoding="utf-8") as f:
            cases = {c["id"]: c for c in json.load(f)["cases"]}
        drafts: list[dict[str, object]] = cases[CID].get(srd.CASE_KEY, [])
        return drafts

    def memory_drafts(self) -> list[dict[str, object]]:
        drafts: list[dict[str, object]] = self.case().get(srd.CASE_KEY, [])
        return drafts

    def fail_audit(self, error: Exception) -> AbstractContextManager[mock.MagicMock]:
        return mock.patch.object(self.store, "audit", side_effect=error)

    def test_audit_failure_after_committed_save_keeps_memory_and_disk(self) -> None:
        audits = self.audits()
        with self.fail_audit(OSError("audit disk full")):
            with self.assertRaises((OSError, RuntimeError)) as raised:
                self.propose(at="2026-11-10T05:00:00Z")
        self.assertEqual(len(self.memory_drafts()), 1)
        self.assertEqual(self.disk_drafts(), self.memory_drafts())
        self.assertEqual(self.audits(), audits)
        error = raised.exception
        assert isinstance(error, srd.DraftAuditError)
        self.assertEqual(error.draft["state"], "PROPOSED_UNAPPROVED")
        self.assertIn("saved", str(error))
        self.assertIn("audit", str(error))

    def test_unrelated_save_and_reload_keep_the_draft_after_audit_failure(self) -> None:
        with self.fail_audit(OSError("audit disk full")):
            with self.assertRaises((OSError, RuntimeError)):
                self.propose(at="2026-11-10T05:00:00Z")
        stored = json.dumps(self.memory_drafts(), sort_keys=True)
        self.store.save()
        self.assertEqual(json.dumps(self.disk_drafts(), sort_keys=True), stored)
        reopened = self.open().cases[CID].get(srd.CASE_KEY, [])
        self.assertEqual(json.dumps(reopened, sort_keys=True), stored)
        self.assertEqual(len(reopened), 1)

    def test_retry_after_audit_failure_is_idempotent_and_keeps_provenance(self) -> None:
        with self.fail_audit(OSError("audit disk full")):
            with self.assertRaises((OSError, RuntimeError)):
                self.propose(at="2026-11-10T05:00:00Z")
        first = json.dumps(self.memory_drafts(), sort_keys=True)
        audits = self.audits()
        again = self.propose(at="2027-01-01T00:00:00Z", user=PM)
        self.assertEqual((again["created"], again["existing"]), (False, True))
        self.assertEqual(again["draft"]["created_at"], "2026-11-10T05:00:00Z")
        self.assertEqual(again["draft"]["created_by"]["role"], "Quality Inspector")
        self.assertEqual(json.dumps(self.memory_drafts(), sort_keys=True), first)
        self.assertEqual(json.dumps(self.disk_drafts(), sort_keys=True), first)
        self.assertEqual(self.audits(), audits)

    def test_non_io_audit_failure_still_keeps_the_committed_draft(self) -> None:
        with self.fail_audit(ValueError("ledger")):
            with self.assertRaises(ValueError):
                self.propose(at="2026-11-10T05:00:00Z")
        self.assertEqual(len(self.memory_drafts()), 1)
        self.assertEqual(self.disk_drafts(), self.memory_drafts())


class SqlDraftCases(DraftCases):
    sql = True
    store: SqlStore

    def version(self) -> int:
        version: int = self.store._rv[CID]
        return version

    def read(self, user: Mapping[str, object] = QI) -> Json:
        return srd.read_drafts(self.store, user, CID)

    def grant(self, store: SqlStore | None = None, consent: str = "granted") -> SensorConsumer:
        consumer = SensorConsumer(store or self.store)
        policy = replace(
            POLICY,
            window_start="2024-01-01T00:00:00Z",
            window_end="2024-01-29T00:00:00Z",
            max_past_seconds=30 * 86400,
        )
        control = replace(
            CONTROL,
            consent=consent,
            mapping_start=policy.window_start,
            mapping_end=policy.window_end,
            calibration_start=policy.window_start,
            calibration_end=policy.window_end,
        )
        consumer.configure(policy, [control])
        return consumer

    def load(self, consumer: SensorConsumer, label: str = "sustained_high_humidity") -> None:
        rows = [dict(r, home_id=CID, sensor_id="SENS-SYN-1") for r in SCENARIOS[label].rows]
        for i in range(0, len(rows), 100):
            for row in preflight(rows[i : i + 100]):
                self.assertEqual(consumer.process(row, "2024-01-29T00:00:00Z").status, "accepted")

    def test_read_follows_current_consent_and_withholds_derived_content(self) -> None:
        self.propose()
        for consent in ("unknown", "declined"):
            self.grant(consent=consent)
            read = self.read()
            self.assertEqual((read["state"], read["drafts"]), ("consent-withheld", []))
            self.assertNotIn("summary", json.dumps(read))
        self.grant()
        read = self.read()
        self.assertEqual((read["state"], len(read["drafts"])), ("ok", 1))
        text = json.dumps(read)
        self.assertNotIn(self.case()[srd.CASE_KEY][0]["draft_digest"], text)
        self.assertNotIn("home", read["drafts"][0])

    def test_read_allowlist_drops_unknown_keys(self) -> None:
        self.propose()
        self.grant()
        stored = self.case()[srd.CASE_KEY][0]
        stored["candidate"]["resident_phone"] = "07000"
        stored["draft_digest"] = srd._digest(stored)
        text = json.dumps(self.read())
        self.assertNotIn("07000", text)
        self.assertIn(stored["task_key"], text)

    def test_retained_readings_refusals_and_approved_synthetic_draft(self) -> None:
        consumer = self.grant()
        self.load(consumer)
        served = srd.draft_from_retained(self.store, QI, CID, WINDOW, WINDOW.end)
        self.assertEqual(served["refusal"], "NO_APPROVED_RULE")
        stale = srd.draft_from_retained(
            self.store, QI, CID, WINDOW, WINDOW.end + timedelta(days=30)
        )
        self.assertEqual(stale["refusal"], "SIGNAL_STALE")
        early = srd.draft_from_retained(self.store, QI, CID, WINDOW, WINDOW.end - timedelta(days=1))
        self.assertIn(early["refusal"], ("FUTURE_READINGS", "SIGNAL_STALE", "SIGNAL_INSUFFICIENT"))
        self.assertNotIn(srd.CASE_KEY, self.case())
        with mock.patch.object(srd, "server_policy", return_value=APPROVED):
            made = srd.draft_from_retained(
                self.store, QI, CID, WINDOW, WINDOW.end, at="2026-11-10T05:00:00Z"
            )
            self.assertTrue(made["created"])
            again = srd.draft_from_retained(
                self.store, QI, CID, WINDOW, WINDOW.end + timedelta(hours=1)
            )
            self.assertTrue(again["existing"])
            expected = sa.review_task_candidate(signal(), APPROVED)
            assert expected is not None
            self.assertEqual(made["draft"]["task_key"], expected.task_key)
            self.grant(consent="declined")
            declined = srd.draft_from_retained(self.store, QI, CID, WINDOW, WINDOW.end)
            self.assertEqual(declined["refusal"], "SIGNAL_DECLINED")
        self.assertEqual(len(self.case()[srd.CASE_KEY]), 1)

    def test_weather_only_window_is_refused(self) -> None:
        from test_sensor_consumer_live import live

        consumer = self.grant()
        consumer.process(live(datetime(2024, 1, 2, 1, 5, tzinfo=UTC)), "2024-01-29T00:00:00Z")
        with mock.patch.object(srd, "server_policy", return_value=APPROVED):
            result = srd.draft_from_retained(self.store, QI, CID, WINDOW, WINDOW.end)
        self.assertFalse(result["created"])
        self.assertNotIn(srd.CASE_KEY, self.case())

    def test_request_window_validation_follows_authorization(self) -> None:
        bad: tuple[object, ...] = (
            None,
            {},
            {"window_start": "2024-01-01T00:00:00Z"},
            {"window_start": "2024-01-01T00:00:00Z", "window_end": "2024-01-02T00:00:00Z", "x": 1},
            {"window_start": "2024-01-01T05:00:00Z", "window_end": "2024-01-02T00:00:00Z"},
            {"window_start": "2024-01-01T00:00:00+01:00", "window_end": "2024-01-02T00:00:00Z"},
            {"window_start": "2024-01-02T00:00:00Z", "window_end": "2024-01-01T00:00:00Z"},
            {"window_start": "2024-01-01T00:00:00Z", "window_end": "2024-03-01T00:00:00Z"},
            {"window_start": 1, "window_end": 2},
        )
        for body in bad:
            with self.subTest(body=body), self.assertRaises(ValueError):
                srd.draft_from_request(self.store, QI, CID, body)
        with self.assertRaises(PermissionError):
            srd.draft_from_request(self.store, PEOPLE["Contractor"], CID, None)
        good = {"window_start": "2024-01-01T00:00:00Z", "window_end": "2024-01-29T00:00:00Z"}
        self.grant()
        self.assertEqual(srd.draft_from_request(self.store, PM, CID, good)["created"], False)

    def test_sql_failure_after_audit_leaves_no_orphan_audit(self) -> None:
        audits = self.audits()

        def failing() -> None:
            raise RuntimeError("before commit")

        with mock.patch.object(self.store, "save", side_effect=failing):
            with self.assertRaises(RuntimeError):
                self.propose()
        self.assertNotIn(srd.CASE_KEY, self.case())
        self.assertEqual(self.audits(), audits)
        self.assertTrue(self.propose()["created"])
        self.assertEqual(self.audits(), audits + 1)

    def test_conflict_rolls_back_and_retry_creates_exactly_one(self) -> None:
        other = self.open()
        self.addCleanup(self.close, other)
        srd._record_draft_synthetic(other, QI, CID, signal("repeated_overnight_peaks"), APPROVED)
        audits = self.audits()
        mine = signal()
        try:
            result = self.propose(mine)
        except ConflictError:
            result = None
        keys = [r["task_key"] for r in self.case()[srd.CASE_KEY]]
        self.assertEqual(len(keys), len(set(keys)))
        if result is None:
            self.assertEqual(self.audits(), audits)
            self.assertEqual(len(keys), 1)
            self.assertTrue(self.propose(mine)["created"])
        self.assertEqual(len(self.case()[srd.CASE_KEY]), 2)
        self.assertEqual(self.audits(), audits + 1)
        self.assertEqual(len(self.open().cases[CID][srd.CASE_KEY]), 2)


class SqliteDraftCases(SqlDraftCases, unittest.TestCase):
    def open(self, reset: bool = False) -> SqlStore:
        base = self.tmp.name
        path = (
            seed(base)
            if reset or not os.path.exists(os.path.join(base, "seed.json"))
            else os.path.join(base, "seed.json")
        )
        return SqlStore(path, os.path.join(base, "state.sqlite"))


@unittest.skipUnless(
    os.environ.get("ZF_SENSOR_DRAFT_MSSQL") == "1", "requires ZF_SENSOR_DRAFT_MSSQL=1"
)
class MssqlDraftCases(SqlDraftCases, unittest.TestCase):
    env = dict(ON, ZF_SENSOR_MSSQL="1")

    def open(self, reset: bool = False) -> SqlStore:
        from zava_forward.core.mssqlstore import MssqlStore, _Conn, connection_string

        base = self.tmp.name
        path = (
            seed(base)
            if reset or not os.path.exists(os.path.join(base, "seed.json"))
            else os.path.join(base, "seed.json")
        )
        if reset:
            db = _Conn(connection_string())
            try:
                for table in ("cases", "staff", *SENSOR_STATE_TABLES, "sensor_register"):
                    db.execute(f"IF OBJECT_ID(N'{table}', N'U') IS NOT NULL DELETE FROM {table}")
            finally:
                db.close()
        store = MssqlStore(path, state_dir=base)
        self.assertEqual(type(store).__name__, "MssqlStore")
        return store


if __name__ == "__main__":
    unittest.main()
