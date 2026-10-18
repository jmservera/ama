"""Synthetic, reproducible before/after probes; never opens configured ZF_DATA."""

import copy
import json
import unittest

from test_resident_decisions import MEASURES, JsonResidentDecisions, SqlResidentDecisions


def probe(cls: type[JsonResidentDecisions], stable: str, reassign: bool) -> dict[str, object]:
    fixture = cls()
    fixture.setUp()
    try:
        fixture.scope()
        fixture.answer()
        store = fixture.store
        answer = store.cases["ZF-1"]["measure_decisions"][MEASURES[0]][0]
        snapshot = bool(answer.get("recorder_identity"))
        body = dict(
            action="service_open",
            route="Independent review",
            review_measure=MEASURES[0],
            review_decision_version=1,
            review_reference="SYN",
            summary="SYN",
            desired_outcome="SYN",
            next_update="2099-01-01",
            service_owner=fixture.pam["email"],
            redress_owner=fixture.rae["email"],
        )
        if reassign:
            store.resident_action(fixture.pam, "ZF-1", body)
        changed = dict(fixture.sam, email="changed@example.test")
        if stable == "oid":
            # Supplied before recording in the oid-only test below, not backfilled.
            changed["code"] = "CHANGED-CODE"
        if fixture.sql:
            store.db.execute(
                "UPDATE staff SET email=?, body=? WHERE email=?",
                (changed["email"], json.dumps(changed), fixture.sam["email"]),
            )
        else:
            store.staff.pop(fixture.sam["email"])
            store.staff[changed["email"]] = changed
        if reassign:
            body = dict(
                action="service_reassign",
                id="SR-1",
                expected_version=1,
                responsibility="redress",
                owner=changed["email"],
                note="SYN",
            )
        else:
            body["redress_owner"] = changed["email"]
        before = copy.deepcopy(store.cases["ZF-1"])
        audit = list(store.audit_entries())
        denied = False
        try:
            store.resident_action(fixture.pam, "ZF-1", body)
        except (ValueError, PermissionError):
            denied = True
        return dict(
            backend=cls.__name__,
            stable=stable,
            operation="reassign" if reassign else "open",
            snapshot=snapshot,
            denied=denied,
            case_unchanged=store.cases["ZF-1"] == before,
            audit_unchanged=list(store.audit_entries()) == audit,
        )
    finally:
        fixture.doCleanups()


class OidJson(JsonResidentDecisions):
    def setUp(self) -> None:
        super().setUp()
        self.sam["oid"] = "SYN-ORIGINAL-OID"
        self.register_followup_actor(self.sam)


class OidSql(SqlResidentDecisions):
    def setUp(self) -> None:
        super().setUp()
        self.sam["oid"] = "SYN-ORIGINAL-OID"
        self.register_followup_actor(self.sam)


if __name__ == "__main__":
    results = [
        probe(cls, stable, reassign)
        for cls, stable in (
            (JsonResidentDecisions, "code"),
            (SqlResidentDecisions, "code"),
            (OidJson, "oid"),
            (OidSql, "oid"),
        )
        for reassign in (False, True)
    ]
    print(json.dumps(results, indent=2))
    unittest.TestCase().assertTrue(all(row["denied"] for row in results))
