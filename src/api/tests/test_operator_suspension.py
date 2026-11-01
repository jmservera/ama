"""Bounded incident drills. Every actor, result and permission is constructed."""

import copy
import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from typing import Any
from unittest.mock import patch

import release_support
from zava_forward.core import assistant_release, assistants, continuity, rai_release
from zava_forward.core.ai import Ai
from zava_forward.core.store import ConflictError

import test_continuity_epoch_export as epoch_fixtures
from test_assistants import Base

CAP = "stock-prioritisation"
AUTHORITY = "Constructed fixture authority, not OD-35 appointment"


def incident(scope: str = CAP) -> dict[str, Any]:
    return dict(
        scope=scope,
        reason="Seeded critical unsupported claim",
        incident_owner="Fixture owner",
        containment="Stop affected proposals",
        comms_owner="Fixture owner",
        comms_audience="Synthetic staff",
        evidence="synthetic:incident-221",
        resident_impact="Constructed resident could receive an unsupported claim",
        remediation="Correct prompt and rerun negative controls",
        restart_authority=AUTHORITY,
        synthetic=True,
        trigger="guardrail breach",
    )


def provision(test: Any, store: Any = None) -> dict[str, Any]:
    store = store or test.store
    person = test.people["Programme Support Officer"]
    person["oid"] = "constructed-independent-restart-oid"
    with store.dblock:
        row = store.db.execute(
            "SELECT body FROM staff WHERE email=?", (person["email"],)
        ).fetchone()
        current = json.loads(row[0])
        current["oid"] = person["oid"]
        store.db.execute(
            "UPDATE staff SET body=? WHERE email=?", (json.dumps(current), person["email"])
        )
    return dict(person, auth_provider="trusted-proxy", rule_roles=["ai_restart"])


def propose(test: Any, s: dict[str, Any], store: Any = None) -> Any:
    return (store or test.store).restart_propose(
        test.pm,
        dict(
            id=s["id"],
            corrective_evidence="synthetic:corrective-tests-221",
            test_id="constructed-negative-and-fallback-drill",
            result="Pass",
            evidence_class="constructed-fixture",
        ),
    )


def decision(s: dict[str, Any]) -> dict[str, Any]:
    return dict(
        id=s["id"],
        epoch=s["proposal"]["epoch"],
        proposal_digest=s["proposal"]["digest"],
        decision="Restart",
        authority_ref=s["restart_authority"],
    )


def restart(test: Any, s: dict[str, Any], store: Any = None) -> Any:
    store = store or test.store
    actor = provision(test, store)
    return store.restart_decide(actor, decision(propose(test, s, store)))


def transaction_failures(test: Any, s: dict[str, Any], actor: dict[str, Any]) -> None:
    before = copy.deepcopy(test.store.continuity_view(test.pm))
    with patch.object(
        test.store, "_proc_write", side_effect=RuntimeError("constructed write fault")
    ):
        with test.assertRaises(RuntimeError):
            test.store.restart_decide(actor, decision(s))
    test.assertEqual(test.other().store.continuity_view(test.pm), before)
    denials = sum(row["action"] == "ai_restart_decide_denied" for row in test.store.audit_entries())
    with patch.object(
        test.store, "_proc_write", side_effect=PermissionError("constructed writer refusal")
    ):
        with test.assertRaises(PermissionError):
            test.store.restart_decide(actor, decision(s))
    reopened = test.other().store
    test.assertEqual(
        sum(row["action"] == "ai_restart_decide_denied" for row in reopened.audit_entries()),
        denials + 1,
    )
    test.assertEqual(reopened.continuity_view(test.pm), before)
    original = test.store.save
    other = test.other()

    def concurrent_save() -> None:
        other.store.suspend(test.people["Quality Inspector"], incident("quality-evidence"))
        original()

    with patch.object(test.store, "save", side_effect=concurrent_save):
        with test.assertRaises(ConflictError):
            test.store.restart_decide(actor, decision(s))
    test.assertEqual(test.store.continuity_view(test.pm)["suspensions"][0]["status"], "Suspended")


def retained_snapshot(test: Any, kind: str, variant: str, scope: str | None = None) -> None:
    """Exercise persisted current/retained evidence through the real incident writer."""
    legacy = kind == "legacy"
    scope = scope or ("summary" if legacy else CAP)
    current_only = variant.startswith("current-")
    if legacy:
        epoch_fixtures.LegacyTests.prepare_ai(test, test.store)
    source = None
    if not current_only:
        if legacy:
            output = test.store.ai_run(test.pm, "ZF-1", scope)
            test.store.review_ai(test.pm, output["record_id"], "accept")
            source = copy.deepcopy(
                next(
                    r for r in test.store.data["recommendations"] if r["id"] == output["record_id"]
                )
            )
        else:
            queued = test.service.invoke(test.pm, scope, "ZF-1")
            ready = test.service.detail(test.pm, queued["id"])
            if ready["state"] == "pending":
                test.assertTrue(test.service.execute(ready["id"]))
                ready = test.service.detail(test.pm, ready["id"])
            ready = test.verify(ready)
            source = test.service.review(
                test.pm, ready["id"], "accept", ready["revision"], "Constructed review"
            )
    key = f"legacy:{scope}" if legacy else scope
    malformed = {
        "json": "{broken",
        "null": "null",
        "array": "[]",
        "pairs": '[["registry_version","unsafe"]]',
        "number": "17",
        "string": '"not an object"',
        "object": "{}",
    }
    with test.service.transaction() as db:
        if source:
            rid = source["release"]["id"]
            raw = db.execute("SELECT body FROM assistant_releases WHERE id=?", (rid,)).fetchone()[0]
        else:
            rid, raw = db.execute(
                "SELECT id,body FROM assistant_releases WHERE capability=? ORDER BY id",
                (key,),
            ).fetchall()[-1]
        original = json.loads(raw)
        if not current_only:
            assert source is not None
            release_key = continuity.sha(source["id"])[:32]
            current_id = "fx-zz-current-" + release_key
            rid = "fx-retained-" + release_key
            test.assertLessEqual(len(current_id), 64)
            test.assertLessEqual(len(rid), 64)
            db.execute(
                "INSERT INTO assistant_releases (id,capability,status,body,revision) "
                "VALUES (?,?,'active',?,1)",
                (
                    current_id,
                    key,
                    json.dumps(dict(original, release_version="new")),
                ),
            )
            db.execute(
                "INSERT INTO assistant_releases (id,capability,status,body,revision) "
                "VALUES (?,?,'revoked',?,1)",
                (rid, key, raw),
            )
            source["release"] = rai_release.reference(dict(original, id=rid, status="active"))
            if legacy:
                source["envelope"]["release"] = source["release"]
        stored = raw
        if variant.startswith(("current-", "historical-")):
            stored = malformed[variant.split("-", 1)[1]]
        elif variant in ("prior", "mismatch"):
            assert source is not None
            retained = dict(original, registry_version="retained-prior-registry")
            stored = json.dumps(retained)
            source["release"] = rai_release.reference(dict(retained, id=rid, status="active"))
            version = "wrong-version" if variant == "mismatch" else retained["registry_version"]
            if legacy:
                source["envelope"]["task_version"] = version
                source["envelope"]["release"] = source["release"]
            else:
                source["version"] = version
        elif variant == "missing":
            assert source is not None
            source["release"] = None
        elif variant.startswith("version-"):
            assert source is not None
            invalid_versions: dict[str, Any] = {
                "version-null": None,
                "version-number": 17,
                "version-object": {"version": original["registry_version"]},
                "version-array": [original["registry_version"]],
                "version-bool": True,
            }
            if legacy:
                source["envelope"]["task_version"] = invalid_versions[variant]
            else:
                source["version"] = invalid_versions[variant]
        db.execute("UPDATE assistant_releases SET body=? WHERE id=?", (stored, rid))
        if source:
            table = "recommendations" if legacy else "assistant_tasks"
            db.execute(f"UPDATE {table} SET body=? WHERE id=?", (json.dumps(source), source["id"]))
    if legacy and source:
        with test.store.lock:
            retained = next(
                r for r in test.store.data["recommendations"] if r["id"] == source["id"]
            )
            retained.update(source)
            test.store.save()
    test.store.suspend(test.people["Quality Inspector"], incident(scope))
    reopened = test.other().store
    reopened.ai = test.store.ai
    s = reopened.continuity_view(test.pm)["suspensions"][-1]
    complete = variant in ("valid", "prior")
    test.assertEqual(s["snapshot_complete"], complete)
    test.assertTrue(reopened.continuity_block(scope))
    with test.service.transaction() as db:
        test.assertEqual(
            db.execute("SELECT body FROM assistant_releases WHERE id=?", (rid,)).fetchone()[0],
            stored,
        )
    if source:
        affected = s["affected"] if legacy else s["affected_assistant_tasks"]
        impact = next(r for r in affected if r["id"] == source["id"])
        test.assertEqual(impact["state"], "Accepted" if legacy else "accepted")
        test.assertEqual(impact["release"], source["release"])
        test.assertEqual(impact["complete"], complete)
        if variant in ("prior", "mismatch"):
            test.assertEqual(impact["binding"]["registry_version"], "retained-prior-registry")
            test.assertEqual(impact["release_snapshot"]["id"], rid)
            test.assertNotEqual(
                impact["binding"]["registry_version"],
                s["incident_versions"]["versions"][0]["binding"]["registry_version"],
            )
        if not complete:
            test.assertTrue(impact["incomplete"])
        if variant.startswith("historical-") and variant != "historical-object":
            test.assertEqual(impact["release_snapshot"]["raw_body"], stored)
    if current_only:
        test.assertFalse(s["incident_versions"]["complete"])
        test.assertTrue(s["incident_versions"]["versions"][0]["missing"])
    if complete:
        propose(test, s, reopened)
    else:
        with test.assertRaises(PermissionError):
            propose(test, s, reopened)
        test.assertEqual(
            reopened.continuity_view(test.pm)["suspensions"][-1]["status"], "Suspended"
        )


def duplicate_scope(test: Any, scope: str = CAP) -> None:
    test.store.suspend(test.people["Quality Inspector"], incident("all"))
    test.store.suspend(test.people["Quality Inspector"], incident(scope))
    before = copy.deepcopy(test.store.continuity_view(test.pm))
    audit = list(test.store.audit_entries())
    with test.assertRaisesRegex(ValueError, "already suspended"):
        test.store.suspend(test.people["Quality Inspector"], incident(scope))
    reopened = test.other().store
    test.assertEqual(reopened.continuity_view(test.pm), before)
    test.assertTrue(continuity.history_valid(reopened._cont()))
    after = list(reopened.audit_entries())
    test.assertEqual(len(after), len(audit) + 1)
    test.assertEqual(after[-1]["action"], "ai_suspend_denied")


def drill(test: Any) -> None:
    ready = test.run_ready(CAP)
    pending = test.service.invoke(test.pm, CAP, "ZF-2")
    other = test.verify(test.run_ready("assessment-preparation"))
    other = test.service.review(
        test.pm, other["id"], "accept", other["revision"], "Constructed independent review"
    )
    queued = test.service.invoke(test.pm, "funding-evidence", "ZF-1")
    claimed = test.service.claim(queued["id"], "independent-task")
    test.store.suspend(test.people["Quality Inspector"], incident())
    s = test.store.continuity_view(test.pm)["suspensions"][-1]
    test.assertEqual(s["affected_assistant_total"], 2)
    affected = {row["id"]: row for row in s["affected_assistant_tasks"]}
    test.assertEqual(set(affected), {ready["id"], pending["id"]})
    test.assertEqual(affected[ready["id"]]["release"], ready["release"])
    test.assertEqual(
        s["incident_versions"]["versions"][0]["binding"],
        assistants.runtime_binding(CAP, test.provider),
    )
    test.assertFalse(test.service.detail(test.pm, ready["id"])["actionable"])
    with test.assertRaises(PermissionError):
        test.verify(ready)
    calls = test.provider.calls
    test.assertFalse(test.service.execute(pending["id"]))
    denied = test.service.invoke(test.pm, CAP, "ZF-2")
    test.assertFalse(test.service.execute(denied["id"]))
    test.assertEqual(test.provider.calls, calls)
    test.assertTrue(test.service.detail(test.pm, other["id"])["actionable"])
    from test_assistants import proposal

    test.assertTrue(
        test.service.complete(
            claimed,
            dict(outcome="returned", source="ai", model="test-model", usage=None),
            proposal(claimed["snapshot"]),
        )
    )
    test.assertEqual(test.service.detail(test.pm, queued["id"])["state"], "ready")
    test.store.log_call(test.pm, "ZF-1", "Spoke", "Synthetic manual fallback")
    test.store.raise_hazard(
        test.pm,
        "ZF-1",
        "Damp and mould",
        "Emergency",
        "Synthetic hazard",
        dict(source="Synthetic officer", aware_at="2026-10-01T00:00:00Z"),
    )
    test.assertTrue(test.other().store.cases["ZF-1"]["hazards"])
    actor = provision(test)
    p = propose(test, s)
    with test.assertRaises(PermissionError):
        test.store.restart_decide(dict(actor, oid="forged"), decision(p))
    with test.assertRaises(PermissionError):
        test.store.restart_decide(dict(actor, rule_roles=[]), decision(p))
    test.assertTrue(
        any(row["action"] == "ai_restart_decide_denied" for row in test.store.audit_entries())
    )
    transaction_failures(test, p, actor)
    p = propose(test, s)
    test.store.restart_decide(actor, decision(p))
    test.assertFalse(test.service.detail(test.pm, ready["id"])["actionable"])
    fresh = test.service.invoke(test.pm, CAP, "ZF-1")
    test.assertTrue(test.service.execute(fresh["id"]))
    bundle = test.store.continuity_export(test.pm, test.service.export())
    exported = next(p for p in bundle["assistant_proposals"] if p["id"] == fresh["id"])
    test.assertTrue(exported["epoch_current"])
    test.assertTrue(exported["actionable"])
    reopened = test.other()
    test.assertEqual(
        reopened.store.continuity_view(test.pm)["suspensions"][0]["status"], "Restarted"
    )
    reopened.store.ai = Ai()
    with reopened.transaction() as db:
        test.assertIsNotNone(reopened.suspended(db, CAP))
    test.assertFalse(reopened.detail(test.pm, fresh["id"])["actionable"])
    retained_snapshot(test, "assistant", "prior")
    restart(test, test.store.continuity_view(test.pm)["suspensions"][-1])
    retained_snapshot(test, "assistant", "historical-null")
    retained_snapshot(test, "legacy", "mismatch")
    retained_snapshot(test, "assistant", "current-json", "funding-evidence")
    duplicate_scope(test, "assessment-preparation")
    release_support.install(test.store)
    with test.service.transaction() as db:
        test.assertTrue(continuity.candidate(test.store, db, "all")["complete"])


class OperatorIncident(Base):
    def test_retained_release_shape_and_version_matrix(self) -> None:
        variants = (
            "valid",
            "prior",
            "mismatch",
            "missing",
            "version-null",
            "version-number",
            "version-object",
            "version-array",
            "version-bool",
        ) + tuple(
            f"{path}-{shape}"
            for path in ("current", "historical")
            for shape in ("json", "null", "array", "pairs", "number", "string", "object")
        )
        for kind in ("assistant", "legacy"):
            for variant in variants:
                with self.subTest(kind=kind, variant=variant):
                    fixture = Base()
                    fixture.setUp()
                    try:
                        retained_snapshot(fixture, kind, variant)
                    finally:
                        fixture.tearDown()
                        fixture.doCleanups()

    def test_all_scope_does_not_hide_duplicate_task_scope(self) -> None:
        duplicate_scope(self)
        with self.service.transaction() as db:
            malformed = copy.deepcopy(self.store._cont())
            malformed["epoch"] += 1
            db.execute("UPDATE meta SET value=? WHERE key='continuity'", (json.dumps(malformed),))
        reopened = self.other().store
        before = copy.deepcopy(reopened._cont())
        with self.assertRaisesRegex(PermissionError, "history"):
            reopened.suspend(self.people["Quality Inspector"], incident("funding-evidence"))
        self.assertEqual(self.other().store._cont(), before)

    def test_legacy_prior_release_snapshot_and_reopen(self) -> None:
        epoch_fixtures.LegacyTests.prepare_ai(self, self.store)
        output = self.store.ai_run(self.pm, "ZF-1", "summary")
        self.store.review_ai(self.pm, output["record_id"], "accept")
        retained = next(
            r for r in self.store.data["recommendations"] if r["id"] == output["record_id"]
        )
        original = copy.deepcopy(retained)
        rid = retained["release"]["id"]
        with self.service.transaction() as db:
            raw = db.execute(
                "SELECT capability,body FROM assistant_releases WHERE id=?", (rid,)
            ).fetchone()
            updated = dict(json.loads(raw[1]), release_version="later-v2")
            db.execute(
                "INSERT INTO assistant_releases (id,capability,status,body,revision) "
                "VALUES (?,?,'active',?,1)",
                ("later-summary", raw[0], json.dumps(updated)),
            )
        self.store.suspend(self.people["Quality Inspector"], incident("summary"))
        s = self.other().store.continuity_view(self.pm)["suspensions"][-1]
        self.assertTrue(s["snapshot_complete"])
        self.assertEqual(len(s["affected"]), 1)
        affected = s["affected"][0]
        self.assertEqual(affected["state"], "Accepted")
        self.assertEqual(affected["release"], original["release"])
        self.assertEqual(affected["release_snapshot"]["release_version"], "fixture-v1")
        self.assertEqual(
            affected["binding"], {key: json.loads(raw[1])[key] for key in assistant_release.BOUND}
        )
        self.assertNotEqual(affected["release"], s["incident_versions"]["versions"][0]["release"])
        propose(self, s)

    def test_incomplete_legacy_snapshot_contains_but_denies_restart(self) -> None:
        epoch_fixtures.LegacyTests.prepare_ai(self, self.store)
        output = self.store.ai_run(self.pm, "ZF-1", "summary")
        with self.store.lock:
            original = next(
                r for r in self.store.data["recommendations"] if r["id"] == output["record_id"]
            )
            for field, value in (
                ("release", None),
                ("release", dict(original["release"], id="missing-reference")),
                ("release", dict(original["release"], digest="altered")),
                ("envelope", None),
                ("prompt_version", None),
            ):
                rec = copy.deepcopy(original)
                rec.update(id=f"unknown-{len(self.store.data['recommendations'])}")
                rec[field] = value
                self.store.data["recommendations"].append(rec)
            self.store.save()
        self.store.suspend(self.people["Quality Inspector"], incident("summary"))
        reopened = self.other().store
        s = reopened.continuity_view(self.pm)["suspensions"][-1]
        self.assertEqual(len(s["affected"]), 6)
        self.assertFalse(s["snapshot_complete"])
        self.assertTrue(reopened.continuity_block("summary"))
        with self.assertRaises(PermissionError):
            propose(self, s, reopened)
        self.assertEqual(
            reopened.continuity_view(self.pm)["suspensions"][-1]["status"], "Suspended"
        )

    def test_malformed_history_runtime_and_generic_export(self) -> None:
        ready = self.run_ready(CAP)
        pending = self.service.invoke(self.pm, CAP, "ZF-2")
        s = self.store.suspend(self.people["Quality Inspector"], incident("quality-evidence"))
        restart(self, s)
        valid = copy.deepcopy(self.store._cont())
        self.assertTrue(self.service.detail(self.pm, ready["id"])["actionable"])
        malformed = []
        bad = copy.deepcopy(valid)
        bad["suspensions"][0]["scope"] = "not-registered"
        malformed.append(bad)
        bad = copy.deepcopy(valid)
        bad["suspensions"][0]["restart"] = {}
        malformed.append(bad)
        bad = copy.deepcopy(valid)
        bad["epoch"] = 4
        bad["suspensions"][0]["restart"]["new_epoch"] = 4
        malformed.append(bad)
        bad = copy.deepcopy(valid)
        bad["suspensions"][0]["status"] = "unknown"
        malformed.append(bad)
        malformed_entries: tuple[Any, ...] = (None, [], {}, "unknown")
        for value in malformed_entries:
            bad = copy.deepcopy(valid)
            bad["suspensions"][0] = value
            malformed.append(bad)
        bad = copy.deepcopy(valid)
        bad["suspensions"][0].pop("id")
        malformed.append(bad)
        for index, bad in enumerate(malformed):
            with self.subTest(history=index), self.store.lock:
                self.store.data["continuity"] = bad
                self.store.save()
                self.assertFalse(self.store.continuity_view(self.pm)["history_valid"])
                with self.assertRaises(PermissionError):
                    propose(self, s)
                self.assertFalse(self.service.detail(self.pm, ready["id"])["actionable"])
                self.assertIsNone(self.service.claim(pending["id"], "invalid-history"))
                self.assertFalse(self.service.export()["proposals"][0]["relied_on"])
                source = self.service.export()
                source["proposals"] = [dict(id="generic", continuity_epoch=bad["epoch"])]
                bundle = self.store.continuity_export(self.pm, source)
                generic = bundle["assistant_proposals"][0]
                self.assertFalse(generic["epoch_current"])
                self.assertFalse(generic["actionable"])
        with self.store.lock:
            self.store.data["continuity"] = valid
            self.store.save()
        for record in (
            dict(id="generic", continuity_epoch=2),
            dict(task="unknown", continuity_epoch=2),
            dict(capability=None, continuity_epoch=2),
            dict(capability=CAP, task="quality-evidence", continuity_epoch=2),
            None,
        ):
            self.assertFalse(self.store.ai_epoch_current(record))
        self.assertFalse(continuity.epoch_current(dict(task=CAP, continuity_epoch=0), 0))
        source = self.service.export()
        source["proposals"] = [dict(id="generic", continuity_epoch=2)]
        generic = self.store.continuity_export(self.pm, source)["assistant_proposals"][0]
        self.assertFalse(generic["epoch_current"])
        self.assertFalse(generic["relied_on"])
        from zava_forward.api.auth import PasswordProvider
        from zava_forward.api.server import App, make_handler

        password = PasswordProvider(self.store, "synthetic-export-password")
        cookie = password.login(self.pm["email"], "synthetic-export-password")
        app = App(self.store, provider=password)
        server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        original_source = self.service.export()
        original_row = next(p for p in original_source["proposals"] if p["id"] == ready["id"])
        calls = self.provider.calls
        try:
            capabilities: tuple[Any, ...] = (None, [], {})
            for capability in capabilities:
                with self.service.transaction() as db:
                    body = self.service._row(db, ready["id"])
                    if capability is None:
                        body.pop("capability", None)
                    else:
                        body["capability"] = capability
                    db.execute(
                        "UPDATE assistant_tasks SET body=? WHERE id=?",
                        (json.dumps(body), ready["id"]),
                    )
                for path in ("source", "http"):
                    with self.subTest(capability=capability, export=path):
                        if path == "source":
                            source = self.service.export()
                            rows = source["proposals"]
                            self.assertEqual(source["total"], original_source["total"])
                        else:
                            request = urllib.request.Request(
                                f"http://127.0.0.1:{server.server_port}/api/continuity/export",
                                headers={"Cookie": f"zf_session={cookie}"},
                            )
                            with urllib.request.urlopen(request, timeout=10) as response:
                                self.assertEqual(response.status, 200)
                                rows = json.load(response)["assistant_proposals"]
                        self.assertEqual(len(rows), len(original_source["proposals"]))
                        exported_generic = next(p for p in rows if p["id"] == ready["id"])
                        self.assertEqual(exported_generic["provenance"], original_row["provenance"])
                        self.assertEqual(exported_generic.get("capability"), body.get("capability"))
                        if capability is None:
                            self.assertNotIn("capability", exported_generic)
                        self.assertFalse(exported_generic["epoch_current"])
                        self.assertTrue(exported_generic["stale"])
                        self.assertFalse(exported_generic["actionable"])
                        self.assertFalse(exported_generic["relied_on"])
                        self.assertEqual(exported_generic["suspension"], "unavailable")
                        with self.service.transaction() as db:
                            self.assertEqual(self.service._row(db, ready["id"]), body)
                        self.assertEqual(self.provider.calls, calls)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(10)
            app.assistants.stop()
        legacy = dict(
            id="old-priority",
            source="ai",
            status="Proposed",
            items=[],
            deterministic=[],
            policy_version="unknown",
            continuity_epoch=0,
        )
        self.assertTrue(self.store.ai_epoch_current(legacy))
        exported = self.store._export_record(legacy)
        self.assertEqual(exported["task"], "priority")
        self.assertFalse(exported["actionable"])
        self.assertIn("release", exported["historical_unknowns"])

    def test_early_denials_are_durable_once_without_verified_attribution(self) -> None:
        s = self.store.suspend(self.people["Quality Inspector"], incident())
        actor = provision(self)
        s = propose(self, s)
        before = copy.deepcopy(self.store.continuity_view(self.pm))
        for bad in (
            dict(actor, oid="forged"),
            dict(actor, email="missing@example.test"),
            dict(actor, role="Quality Inspector"),
        ):
            count = sum(
                r["action"] == "ai_restart_decide_denied" for r in self.store.audit_entries()
            )
            with self.assertRaises(PermissionError):
                self.store.restart_decide(bad, decision(s))
            reopened = self.other().store
            denials = [
                r for r in reopened.audit_entries() if r["action"] == "ai_restart_decide_denied"
            ]
            self.assertEqual(len(denials), count + 1)
            self.assertEqual(denials[-1]["who"], "unverified")
            self.assertFalse(json.loads(denials[-1]["detail"])["identity_verified"])
            self.assertEqual(reopened.continuity_view(self.pm), before)
        with self.store.dblock:
            current = dict(self.people["Programme Support Officer"], disabled=True)
            self.store.db.execute(
                "UPDATE staff SET body=? WHERE email=?", (json.dumps(current), actor["email"])
            )
        with self.assertRaises(PermissionError):
            self.store.restart_decide(actor, decision(s))
        last = list(self.other().store.audit_entries())[-1]
        self.assertEqual(last["action"], "ai_restart_decide_denied")
        self.assertEqual(last["who"], "unverified")
        with self.store.dblock:
            current.pop("disabled")
            self.store.db.execute(
                "UPDATE staff SET body=? WHERE email=?", (json.dumps(current), actor["email"])
            )
        count = sum(r["action"] == "ai_restart_decide_denied" for r in self.store.audit_entries())
        with patch.object(
            self.store, "_proc_write", side_effect=PermissionError("constructed writer refusal")
        ):
            with self.assertRaises(PermissionError):
                self.store.restart_decide(actor, decision(s))
        reopened = self.other().store
        denials = [r for r in reopened.audit_entries() if r["action"] == "ai_restart_decide_denied"]
        self.assertEqual(len(denials), count + 1)
        self.assertTrue(json.loads(denials[-1]["detail"])["identity_verified"])
        self.assertFalse(json.loads(denials[-1]["detail"])["authority_verified"])
        self.assertEqual(reopened.continuity_view(self.pm), before)
        from zava_forward.core.store import Store

        live, audit = str(self.root / "denial.json"), str(self.root / "denial-audit.jsonl")
        store = Store(str(self.seed), live, audit)
        store.suspend(self.people["Quality Inspector"], incident())
        with self.assertRaises(PermissionError):
            store.restart_decide(dict(actor, oid="forged"), decision(s))
        reopened_json = Store(str(self.seed), live, audit)
        denials = [
            r for r in reopened_json.audit_entries() if r["action"] == "ai_restart_decide_denied"
        ]
        self.assertEqual(len(denials), 1)
        self.assertEqual(denials[0]["who"], "unverified")
        self.assertEqual(
            reopened_json.continuity_view(self.pm)["suspensions"][0]["status"], "Suspended"
        )

    def test_incident_snapshot_and_reopen(self) -> None:
        drill(self)
        from zava_forward.core.store import Store

        live, audit = str(self.root / "incident.json"), str(self.root / "incident-audit.jsonl")
        store = Store(str(self.seed), live, audit)
        store.suspend(self.people["Quality Inspector"], incident())
        reopened = Store(str(self.seed), live, audit)
        self.assertTrue(reopened.continuity_block(CAP))
        retained = reopened.continuity_view(self.pm)["suspensions"][0]
        self.assertEqual(retained["evidence"], "synthetic:incident-221")
        self.assertFalse(retained["snapshot_complete"])
        with self.assertRaises(PermissionError):
            propose(self, retained, reopened)

    def test_restart_negative_matrix(self) -> None:
        s = self.store.suspend(self.people["Quality Inspector"], incident())
        actor = provision(self)
        for key, bad in (
            ("result", "Fail"),
            ("evidence_class", "actual"),
            ("test_id", ""),
            ("corrective_evidence", ""),
        ):
            body = dict(
                id=s["id"],
                corrective_evidence="synthetic:tests",
                test_id="tests",
                result="Pass",
                evidence_class="constructed-fixture",
            )
            body[key] = bad
            with self.subTest(key=key), self.assertRaises((ValueError, PermissionError)):
                self.store.restart_propose(self.pm, body)
        s = propose(self, s)
        for actor_bad in (
            self.pm,
            self.people["Quality Inspector"],
            dict(actor, auth_provider="password"),
            dict(actor, oid="forged"),
            dict(actor, rule_roles=[]),
        ):
            with self.assertRaises(PermissionError):
                self.store.restart_decide(actor_bad, decision(s))
        for field, value in (
            ("epoch", 99),
            ("proposal_digest", "wrong"),
            ("authority_ref", "invented"),
        ):
            with self.assertRaises(PermissionError):
                self.store.restart_decide(actor, dict(decision(s), **{field: value}))
        with self.store.lock:
            self.store._cont()["suspensions"][0]["proposal"]["corrective_evidence"] = "altered"
            self.store.save()
        with self.assertRaises(PermissionError):
            self.store.restart_decide(actor, decision(s))
        s = propose(self, s)
        self.store.restart_decide(actor, decision(s))
        with self.assertRaises(ValueError):
            self.store.restart_decide(actor, decision(s))

    def test_candidate_drift_and_reproposal(self) -> None:
        s = self.store.suspend(self.people["Quality Inspector"], incident())
        actor = provision(self)
        s = propose(self, s)
        original = copy.deepcopy(s["incident_versions"])
        for key in assistant_release.BOUND:
            with self.subTest(binding=key):
                old = assistants.runtime_binding
                with patch.object(
                    assistants,
                    "runtime_binding",
                    side_effect=lambda *a, old=old, key=key: dict(old(*a), **{key: "changed"}),
                ):
                    with self.assertRaises(PermissionError):
                        self.store.restart_decide(actor, decision(s))
        self.service.approvers = {self.pm["email"]}
        from test_assistant_release import body

        self.service.record_release(self.pm, body(self.service, release_version="corrected-v2"))
        with self.assertRaises(PermissionError):
            self.store.restart_decide(actor, decision(s))
        s = propose(self, s)
        self.assertEqual(s["incident_versions"], original)
        self.assertEqual(len(s["proposals"]), 2)
        self.store.restart_decide(actor, decision(s))

    def test_constructed_restart_actual_hold(self) -> None:
        s = self.store.suspend(self.people["Quality Inspector"], incident())
        restart(self, s)
        ready = self.verify(self.run_ready(CAP))
        for accepted in (False, True):
            if accepted:
                ready = self.service.review(
                    self.pm, ready["id"], "accept", ready["revision"], "Fixture review"
                )
            source = self.service.export()
            bundle = self.store.continuity_export(self.pm, source)
            projections = (
                self.service.detail(self.pm, ready["id"]),
                next(
                    p for p in self.service.listing(self.pm)["proposals"] if p["id"] == ready["id"]
                ),
                next(p for p in source["proposals"] if p["id"] == ready["id"]),
                next(p for p in bundle["assistant_proposals"] if p["id"] == ready["id"]),
            )
            for p in projections:
                self.assertTrue(p["epoch_current"])
                self.assertTrue(p["actionable"])
                self.assertEqual(p["relied_on"], accepted)
        collected = self.service.export()
        ai = Ai()
        ai.endpoint, ai.fast, ai.model_version = "https://synthetic.invalid", "test", "test-model"
        calls = []
        ai.evidence = lambda *a, **kw: calls.append(1)
        self.store.ai = ai
        import release_support

        release_support.install(self.store, ai, cls="actual")
        p = self.service.invoke(self.pm, CAP, "ZF-1")
        self.assertEqual(p["state"], "disabled")
        self.assertFalse(self.service.execute(p["id"]))
        self.assertEqual(calls, [])
        for service in (self.service, self.other()):
            service.store.ai = ai
            collected["constructed"] = True
            bundle = service.store.continuity_export(self.pm, collected)
            p = next(p for p in bundle["assistant_proposals"] if p["id"] == ready["id"])
            self.assertTrue(p["epoch_current"])
            self.assertFalse(p["actionable"])
            self.assertFalse(p["relied_on"])
            self.assertFalse(service.detail(self.pm, ready["id"])["actionable"])
        self.assertIn(
            "OD-35", self.store.continuity_view(self.pm)["suspensions"][0]["actual_authority"]
        )

    def test_rollback_and_conflict(self) -> None:
        s = self.store.suspend(self.people["Quality Inspector"], incident())
        actor = provision(self)
        s = propose(self, s)
        transaction_failures(self, s, actor)
        self.assertTrue(self.service.suspended(self.store.db, CAP))

    def test_snapshot_boundary(self) -> None:
        original = self.store.save
        created = []

        def concurrent_enqueue() -> None:
            created.append(self.service.invoke(self.pm, CAP, "ZF-1")["id"])
            original()

        with patch.object(self.store, "save", side_effect=concurrent_enqueue):
            self.store.suspend(self.people["Quality Inspector"], incident())
        s = self.store.continuity_view(self.pm)["suspensions"][-1]
        self.assertEqual([row["id"] for row in s["affected_assistant_tasks"]], created)
        self.assertFalse(self.service.execute(created[0]))

    def test_relevant_history_failclosed(self) -> None:
        s = self.store.suspend(self.people["Quality Inspector"], incident())
        restart(self, s)
        doc = self.store.continuity_view(self.pm)
        for epoch in (None, -1, 3, True):
            self.assertFalse(continuity.epoch_current(dict(task=CAP, continuity_epoch=epoch), doc))
        self.assertTrue(
            continuity.epoch_current(dict(task="assessment-preparation", continuity_epoch=0), doc)
        )
        self.assertFalse(continuity.epoch_current(dict(task=CAP, continuity_epoch=0), doc))

    def test_manual_hazard_drill(self) -> None:
        self.store.suspend(self.people["Quality Inspector"], incident("all"))
        self.store.log_call(self.pm, "ZF-1", "Spoke", "Synthetic manual fallback")
        self.store.raise_hazard(
            self.pm,
            "ZF-1",
            "Damp and mould",
            "Emergency",
            "Synthetic hazard",
            dict(source="Synthetic officer observation", aware_at="2026-10-01T00:00:00Z"),
        )
        reopened = self.other().store
        self.assertTrue(reopened.cases["ZF-1"]["hazards"])
        self.assertIn("Synthetic manual fallback", json.dumps(reopened.cases["ZF-1"]))

    def test_breach_record_names_authority_and_drill_sequence(self) -> None:
        body = incident("all")
        self.store.suspend(self.people["Quality Inspector"], body)
        s = self.store.continuity_view(self.pm)["suspensions"][0]
        self.assertEqual(s["restart_authority"], AUTHORITY)
        self.assertIn("OD-35", s["actual_authority"])
        self.assertEqual(s["trigger"], "guardrail breach")
        self.store.log_call(self.pm, "ZF-1", "Spoke", "Synthetic drill call")
        with self.assertRaises(PermissionError):
            self.store.restart_decide(provision(self), dict(id=s["id"], decision="Restart"))
        self.assertEqual(
            self.store.continuity_view(self.pm)["suspensions"][0]["status"], "Suspended"
        )
        unnamed = dict(incident("quality-evidence"))
        unnamed.pop("restart_authority")
        self.store.suspend(self.people["Quality Inspector"], unnamed)
        held = self.store.continuity_view(self.pm)["suspensions"]
        self.assertTrue(any(x["restart_authority"].startswith("Unavailable") for x in held))
        self.assertIn("Synthetic drill call", json.dumps(self.store.cases["ZF-1"]))

    def test_trusted_capability(self) -> None:
        from test_auth import ENV, principal
        from zava_forward.api.auth import PasswordProvider, TrustedProxyProvider
        from zava_forward.api.server import App, make_handler

        actor = provision(self)
        self.store.staff[actor["email"]]["oid"] = actor["oid"]
        provider = TrustedProxyProvider(self.store, dict(ENV, ZF_AUTH_EMAIL_FALLBACK="1"))
        roles = ("ZavaForward.SupportOfficer", "ZavaForward.AIRestart")
        entra_oid = "dddddddd-0000-0000-0000-000000000007"
        bound = provider.authenticate(
            {"X-MS-CLIENT-PRINCIPAL": principal(roles=roles, oid=entra_oid, email=actor["email"])}
        )
        self.assertIsNotNone(bound)
        self.assertEqual(bound["rule_roles"], ["ai_restart"])
        self.assertNotEqual(bound["email"], actor["email"])
        fallback = bound
        s = self.store.suspend(self.people["Quality Inspector"], incident())
        s = propose(self, s)
        self.assertEqual(fallback["oid"], entra_oid)
        self.store.staff[actor["email"]].update(
            auth_provider="trusted-proxy", rule_roles=["ai_restart"]
        )
        password = PasswordProvider(self.store, "synthetic-only-password")
        cookie = password.login(actor["email"], "synthetic-only-password")
        seeded = password.authenticate({"Cookie": f"zf_session={cookie}"})
        self.assertEqual(seeded["rule_roles"], [])
        with self.assertRaises(PermissionError):
            self.store.restart_decide(seeded, decision(s))
        for route in (password, provider):
            app = App(self.store, provider=route)
            server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
            thread = threading.Thread(target=server.serve_forever)
            thread.start()
            before = copy.deepcopy(self.store.continuity_view(self.pm))
            count = sum(
                r["action"] == "ai_restart_decide_denied" for r in self.store.audit_entries()
            )
            try:
                request = urllib.request.Request(
                    f"http://127.0.0.1:{server.server_port}/api/continuity/restart-decide",
                    data=json.dumps(decision(s)).encode(),
                    headers={
                        "Content-Type": "application/json",
                        "X-ZF-CSRF": "1",
                        "Cookie": f"zf_session={cookie}",
                        "X-MS-CLIENT-PRINCIPAL": principal(roles=roles, oid=entra_oid),
                    },
                )
                if route is password:
                    with self.assertRaises(urllib.error.HTTPError) as refused:
                        urllib.request.urlopen(request, timeout=10)
                    self.assertEqual(refused.exception.code, 403)
                    refused.exception.close()
                    reopened = self.other().store
                    denials = [
                        r
                        for r in reopened.audit_entries()
                        if r["action"] == "ai_restart_decide_denied"
                    ]
                    self.assertEqual(len(denials), count + 1)
                    detail = json.loads(denials[-1]["detail"])
                    self.assertTrue(detail["identity_verified"])
                    self.assertFalse(detail["authority_verified"])
                    self.assertEqual(reopened.continuity_view(self.pm), before)
                else:
                    with urllib.request.urlopen(request, timeout=10) as response:
                        self.assertEqual(response.status, 200)
                        self.assertTrue(json.load(response)["actual_hold"])
            finally:
                server.shutdown()
                server.server_close()
                thread.join(10)
                app.assistants.stop()

    def test_authority_revalidation(self) -> None:
        s = self.store.suspend(self.people["Quality Inspector"], incident())
        actor = provision(self)
        s = propose(self, s)
        original = self.store.save

        def revoke_before_save() -> None:
            with self.store.dblock:
                current = dict(self.people["Programme Support Officer"], disabled=True)
                self.store.db.execute(
                    "UPDATE staff SET body=? WHERE email=?", (json.dumps(current), actor["email"])
                )
            original()

        with patch.object(self.store, "save", side_effect=revoke_before_save):
            with self.assertRaises(PermissionError):
                self.store.restart_decide(actor, decision(s))
        self.assertEqual(
            self.other().store.continuity_view(self.pm)["suspensions"][0]["status"], "Suspended"
        )


if __name__ == "__main__":
    unittest.main()
