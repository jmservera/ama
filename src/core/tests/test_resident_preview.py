"""Resident preview boundary: default-deny grants, positive-allowlist view, safe start-up."""

import copy
import json
import tempfile
import unittest
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

from zava_forward.core import resident_preview as rp
from zava_forward.core.synthetic.resident_preview_fixture import build

CANARY = "SYN-CANARY"
OTHER_PEOPLE = ("Blake Synthetic", "Casey Unrelated", "Otherville", "3 Synthetic Row")


class Base(unittest.TestCase):
    root: Path
    dataset: Path
    grants: Path
    store: Any
    work: tempfile.TemporaryDirectory[str]
    tmp: tempfile.TemporaryDirectory[str]

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory(prefix="ama444-test-")
        cls.root = Path(cls.tmp.name) / "fixture"
        build(cls.root)
        cls.dataset = cls.root / "dataset.json"
        cls.grants = cls.root / "grants.json"
        cls.store, cls.work = rp.open_store(cls.dataset)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.work.cleanup()
        cls.tmp.cleanup()

    def view(self, subject: str) -> dict[str, Any]:
        view: dict[str, Any] = rp.resident_view(self.store, rp.resolve_grant(self.grants, subject))
        return view

    def denied(self, subject: str, code: str, path: Path | None = None) -> None:
        with self.assertRaises(rp.GrantDenied) as raised:
            rp.resolve_grant(path or self.grants, subject)
        self.assertEqual(raised.exception.code, code)
        self.assertEqual(str(raised.exception), "You cannot see this page.")

    def variant(self, edit: Any) -> Path:
        data = json.loads(self.grants.read_text())
        edit(data)
        path = (
            Path(self.tmp.name) / f"variant-{len(list(Path(self.tmp.name).glob('variant-*')))}.json"
        )
        path.write_text(json.dumps(data))
        return path


class ResidentView(Base):
    def test_resident_a_sees_confirmed_only(self) -> None:
        view = self.view("SYN-RES-A")
        self.assertEqual(view["banner"], rp.BANNER)
        self.assertTrue(view["read_only"])
        appointments = view["appointments"]
        self.assertEqual(
            appointments["confirmed"]["items"], [{"date": "2098-01-01", "period": "Morning"}]
        )
        self.assertEqual(appointments["offers"]["items"], [])
        self.assertEqual(appointments["offers"]["heading"], "Offered times (not confirmed)")
        self.assertEqual(view["home"]["address"], "1 Synthetic Row")

    def test_resident_b_offer_is_not_a_confirmed_arrangement(self) -> None:
        appointments = self.view("SYN-RES-B")["appointments"]
        self.assertEqual(appointments["confirmed"]["items"], [])
        self.assertEqual(len(appointments["offers"]["items"]), 1)
        self.assertEqual(appointments["unknown"]["count"], 0)

    def test_progress_text_is_mapped_and_unknown_stays_unknown(self) -> None:
        self.assertEqual(
            self.view("SYN-RES-B")["progress"], rp.STAGE_TEXT["Survey being booked"][0]
        )
        case = self.store.cases["SYN-C2"]
        original = case["stage"]
        try:
            case["stage"] = "Invented staff-only stage"
            view = self.view("SYN-RES-B")
            self.assertEqual(view["progress"], rp.UNKNOWN_PROGRESS)
            self.assertEqual(view["next_step"], rp.UNKNOWN_NEXT)
        finally:
            case["stage"] = original

    def test_every_view_is_canary_free_and_isolated(self) -> None:
        for subject in ("SYN-RES-A", "SYN-RES-B", "SYN-REP-B", "SYN-REP-WRONG"):
            text = json.dumps(self.view(subject))
            self.assertNotIn(CANARY, text, subject)
            for fragment in (
                "sam@example",
                "pam@example",
                "Alex Synthetic" if "B" in subject else "Blake",
            ):
                self.assertNotIn(fragment, text, subject)
        self.assertNotIn("Blake", json.dumps(self.view("SYN-RES-A")))
        self.assertNotIn("Alex", json.dumps(self.view("SYN-RES-B")))
        for subject in ("SYN-RES-A", "SYN-RES-B"):
            for other in OTHER_PEOPLE:
                self.assertNotIn(other, json.dumps(self.view(subject)))

    def test_new_staff_field_stays_hidden_until_mapped(self) -> None:
        case = self.store.cases["SYN-C1"]
        case["new_staff_field"] = "SYN-NEW-FIELD-CANARY"
        try:
            self.assertNotIn("SYN-NEW-FIELD-CANARY", json.dumps(self.view("SYN-RES-A")))
        finally:
            del case["new_staff_field"]

    def test_booked_stages_do_not_claim_a_booking(self) -> None:
        for stage in ("Survey booked", "Install booked"):
            text = " ".join(rp.STAGE_TEXT[stage]).lower()
            self.assertNotIn("is booked", text, stage)
            self.assertNotIn("recorded as booked", text, stage)

    def test_view_does_not_mutate_the_store(self) -> None:
        before = json.dumps(self.store.data, sort_keys=True)
        for subject in ("SYN-RES-A", "SYN-RES-B", "SYN-REP-B", "SYN-REP-WRONG"):
            self.view(subject)
        self.assertEqual(before, json.dumps(self.store.data, sort_keys=True))

    def test_unavailable_features_are_listed(self) -> None:
        names = [item["feature"] for item in self.view("SYN-RES-A")["unavailable"]]
        for expected in ("Messages", "Uploads", "Downloads", "Consent and decisions"):
            self.assertIn(expected, names)
        self.assertIn("housing officer", " ".join(self.view("SYN-RES-A")["help"]["routes"]))

    def test_legacy_appointments_text_never_shown(self) -> None:
        self.assertNotIn("LEGACY", json.dumps(self.view("SYN-RES-A")))

    def test_unknown_appointment_state_is_counted_not_confirmed(self) -> None:
        orders = self.store.data["procurement"]["work_orders"]
        order = next(w for w in orders if w["case_id"] == "SYN-C1")
        offer = order["appointment_offer"]
        order["appointment_offer"] = None
        try:
            appointments = self.view("SYN-RES-A")["appointments"]
            self.assertEqual(appointments["confirmed"]["items"], [])
            self.assertEqual(appointments["unknown"]["count"], 1)
        finally:
            order["appointment_offer"] = offer

    def test_ended_or_paused_offer_is_not_shown_as_a_live_offer(self) -> None:
        orders = self.store.data["procurement"]["work_orders"]
        order = next(w for w in orders if w["case_id"] == "SYN-C2")
        offer = order["appointment_offer"]
        for key in ("ended", "paused"):
            original = offer.get(key)
            offer[key] = True
            try:
                appointments = self.view("SYN-RES-B")["appointments"]
                self.assertEqual(appointments["offers"]["items"], [], key)
                self.assertEqual(appointments["unknown"]["count"], 1, key)
            finally:
                offer[key] = original


class Representative(Base):
    def test_valid_representative_sees_only_covered_tasks(self) -> None:
        view = self.view("SYN-REP-B")
        self.assertEqual(view["viewer"]["kind"], "representative")
        self.assertNotIn("home", view)
        self.assertIn("appointments", view)
        self.assertTrue(any("Works decision" in t for t in view["tasks_not_shown"]))

    def test_grant_task_not_in_domain_record_is_not_shown(self) -> None:
        view = self.view("SYN-REP-WRONG")
        self.assertNotIn("appointments", view)
        self.assertIn("progress", view)

    def test_no_current_authority_denies(self) -> None:
        case = self.store.cases["SYN-C2"]
        saved = copy.deepcopy(case["representative_authorities"])
        case["representative_authorities"] = {}
        try:
            with self.assertRaises(rp.GrantDenied):
                self.view("SYN-REP-B")
        finally:
            case["representative_authorities"] = saved

    def test_malformed_authority_record_denies_not_crashes(self) -> None:
        case = self.store.cases["SYN-C2"]
        saved = copy.deepcopy(case["representative_authorities"])
        case["representative_authorities"] = {"SYN-REP-B": ["not-a-dict"]}
        try:
            with self.assertRaises(rp.GrantDenied):
                self.view("SYN-REP-B")
        finally:
            case["representative_authorities"] = saved

    def test_expired_authority_denies(self) -> None:
        case = self.store.cases["SYN-C2"]
        saved = copy.deepcopy(case["representative_authorities"])
        case["representative_authorities"]["SYN-REP-B"][-1]["review_date"] = "2026-01-02"
        try:
            with self.assertRaises(rp.GrantDenied):
                self.view("SYN-REP-B")
        finally:
            case["representative_authorities"] = saved


class RepresentativeAuthorityBoundary(Base):
    """R1 in residents.md: authority ends on its review date and only Confirmed counts."""

    def edit_authority(self, **changes: Any) -> Any:
        case = self.store.cases["SYN-C2"]
        saved = copy.deepcopy(case["representative_authorities"])
        case["representative_authorities"]["SYN-REP-B"][-1].update(changes)
        self.addCleanup(case.__setitem__, "representative_authorities", saved)

    def test_authority_is_unavailable_on_the_review_date(self) -> None:
        self.edit_authority(review_date=date.today().isoformat())
        with self.assertRaises(rp.GrantDenied) as raised:
            self.view("SYN-REP-B")
        self.assertEqual(raised.exception.code, "no_current_authority")

    def test_authority_is_available_until_the_day_before_review(self) -> None:
        self.edit_authority(review_date=(date.today() + timedelta(days=1)).isoformat())
        self.assertIn("appointments", self.view("SYN-REP-B"))

    def test_unconfirmed_authority_denies_without_case_detail(self) -> None:
        self.edit_authority(status="Pending")
        with self.assertRaises(rp.GrantDenied) as raised:
            self.view("SYN-REP-B")
        self.assertEqual(str(raised.exception), "You cannot see this page.")
        for text in (CANARY, *OTHER_PEOPLE):
            self.assertNotIn(text, str(raised.exception))

    def test_representative_view_is_not_the_household_record(self) -> None:
        view = self.view("SYN-REP-B")
        self.assertNotIn("home", view)
        self.assertNotIn("1 Synthetic Row", json.dumps(view))


class DefaultDeny(Base):
    def test_denials(self) -> None:
        self.denied("SYN-RES-EXPIRED", "expired")
        self.denied("SYN-RES-REVOKED", "revoked")
        self.denied("SYN-RES-AMBIG", "ambiguous")
        self.denied("SYN-RES-NOGRANT", "no_grant")
        self.denied("SYN-NOT-A-SUBJECT", "unknown_subject")
        self.denied("", "unknown_subject")
        self.denied("*", "unknown_subject")

    def test_expiry_applies_at_the_next_request(self) -> None:
        grant = rp.resolve_grant(self.grants, "SYN-RES-A", datetime(2030, 1, 1, tzinfo=UTC))
        self.assertEqual(grant.case_id, "SYN-C1")
        shortened = self.variant(
            lambda d: d["grants"][0].update(valid_to="2026-06-01T00:00:00+00:00")
        )
        self.denied("SYN-RES-A", "expired", shortened)

    def test_revocation_applies_at_the_next_request(self) -> None:
        self.assertEqual(rp.resolve_grant(self.grants, "SYN-RES-A").case_id, "SYN-C1")
        revoked = self.variant(lambda d: d["grants"][0].update(revoked=True))
        self.denied("SYN-RES-A", "revoked", revoked)

    def test_not_yet_valid_is_denied(self) -> None:
        future = self.variant(
            lambda d: d["grants"][0].update(
                valid_from="2098-01-01T00:00:00+00:00", valid_to="2099-01-01T00:00:00+00:00"
            )
        )
        self.denied("SYN-RES-A", "expired", future)

    def test_malformed_grants_deny(self) -> None:
        edits = {
            "extra key": lambda g: g.update(extra=1),
            "missing key": lambda g: g.pop("case_id"),
            "wildcard case": lambda g: g.update(case_id="*"),
            "empty case": lambda g: g.update(case_id=" "),
            "action granted": lambda g: g.update(actions=["write"]),
            "unknown field": lambda g: g.update(fields=["staff_notes"]),
            "empty fields": lambda g: g.update(fields=[]),
            "duplicate fields": lambda g: g.update(fields=["home", "home"]),
            "naive time": lambda g: g.update(valid_from="2026-01-01T00:00:00"),
            "bad time": lambda g: g.update(valid_to="soon"),
            "inverted window": lambda g: g.update(valid_to="2025-01-01T00:00:00+00:00"),
            "string revoked": lambda g: g.update(revoked="false"),
            "bad kind": lambda g: g.update(kind="staff"),
            "representative keys on resident": lambda g: g.update(tasks=["Attend"]),
        }
        for name, edit in edits.items():
            path = self.variant(lambda d, e=edit: e(d["grants"][0]))
            with self.subTest(name):
                self.denied("SYN-RES-A", "malformed", path)

    def test_malformed_representative_denies(self) -> None:
        path = self.variant(lambda d: d["grants"][2].update(tasks=["Anything"]))
        self.denied("SYN-REP-B", "malformed", path)
        path = self.variant(lambda d: d["grants"][2].pop("measure"))
        self.denied("SYN-REP-B", "malformed", path)

    def test_fixture_not_synthetic_or_missing_denies(self) -> None:
        path = self.variant(lambda d: d["fixture"].update(synthetic=False))
        self.denied("SYN-RES-A", "fixture_unavailable", path)
        self.denied("SYN-RES-A", "fixture_unavailable", Path(self.tmp.name) / "missing.json")

    def test_grant_for_missing_case_denies(self) -> None:
        path = self.variant(lambda d: d["grants"][0].update(case_id="SYN-NO-SUCH"))
        with self.assertRaises(rp.GrantDenied):
            rp.resident_view(self.store, rp.resolve_grant(path, "SYN-RES-A"))


class SafeStart(Base):
    def start(self, env: dict[str, str] | None = None, host: str = "127.0.0.1", **kw: Any) -> Any:
        return rp.safe_start(
            env or {}, kw.get("dataset", self.dataset), kw.get("fixture", self.grants), host
        )

    def test_accepts_loopback_with_clean_environment(self) -> None:
        data, fixture = self.start()
        self.assertEqual((data, fixture), (self.dataset.resolve(), self.grants.resolve()))
        self.start(host="::1")

    def test_refuses_non_loopback_hosts(self) -> None:
        for host in ("0.0.0.0", "", "localhost", "192.168.1.5", "::", "example.com"):
            with self.subTest(host), self.assertRaises(rp.PreviewConfigError):
                self.start(host=host)

    def test_refuses_cloud_store_ai_and_normal_data_environment(self) -> None:
        for key in (
            "ZF_DATA",
            "ZF_SQL_SERVER",
            "AI_ENDPOINT",
            "AZURE_CLIENT_ID",
            "IDENTITY_ENDPOINT",
            "MSSQL_CONN",
            "APPLICATIONINSIGHTS_CONNECTION_STRING",
            "OPENAI_API_KEY",
            "SQL_URL",
            "zf_data",
        ):
            with self.subTest(key), self.assertRaises(rp.PreviewConfigError):
                self.start({key: "x"})

    def test_refuses_missing_symlink_and_normal_location(self) -> None:
        with self.assertRaises(rp.PreviewConfigError):
            self.start(dataset=self.root / "nope.json")
        link = Path(self.tmp.name) / "link.json"
        link.symlink_to(self.dataset)
        with self.assertRaises(rp.PreviewConfigError):
            self.start(dataset=link)
        with self.assertRaises(rp.PreviewConfigError):
            self.start(dataset=self.root)

    def test_refuses_unmarked_or_mismatched_files(self) -> None:
        plain = Path(self.tmp.name) / "plain.json"
        plain.write_text(json.dumps(dict(cases=[], staff=[])))
        with self.assertRaises(rp.PreviewConfigError):
            self.start(dataset=plain)
        mismatched = Path(self.tmp.name) / "mismatch.json"
        data = json.loads(self.dataset.read_text())
        data["synthetic_preview"]["fixture_id"] = "SOMETHING-ELSE"
        mismatched.write_text(json.dumps(data))
        with self.assertRaises(rp.PreviewConfigError):
            self.start(dataset=mismatched)
        not_json = Path(self.tmp.name) / "bad.json"
        not_json.write_text("{")
        with self.assertRaises(rp.PreviewConfigError):
            self.start(fixture=not_json)

    def test_refuses_files_under_the_normal_data_location(self) -> None:
        home = Path.home() / ".zava-forward"
        self.assertFalse(home.exists() and (home / "data" / "dataset.json").exists())
        with self.assertRaises(rp.PreviewConfigError):
            rp.safe_start({}, home / "data" / "dataset.json", self.grants, "127.0.0.1")

    def test_builder_refuses_an_existing_directory(self) -> None:
        with self.assertRaises(FileExistsError):
            build(self.root)

    def test_open_store_works_on_a_private_copy(self) -> None:
        before = self.dataset.read_bytes()
        store, work = rp.open_store(self.dataset)
        try:
            store.save()
            self.assertEqual(before, self.dataset.read_bytes())
            self.assertFalse(Path(work.name).samefile(self.root))
        finally:
            work.cleanup()


if __name__ == "__main__":
    unittest.main()
