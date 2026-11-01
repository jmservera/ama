"""Material change revokes release records and records the trigger; constructed evidence."""

import json
import sqlite3
import unittest
from typing import Any

from tests.release_support import fixture

from zava_forward.core import ai_registry, assistants, rai_release
from zava_forward.core import assistant_release as rel


class Ai:
    provider = "azure-openai"
    endpoint = "https://example.invalid"
    fast = "dep"
    strong = "dep"
    model_version = "model-1"


class Invalidation(unittest.TestCase):
    def setUp(self) -> None:
        self.task = "stock-prioritisation"
        self.db = sqlite3.connect(":memory:", isolation_level=None)
        for ddl in rel.SQLITE_DDL:
            self.db.execute(ddl)
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS assistant_events "
            "(id TEXT PRIMARY KEY, task_id TEXT NOT NULL, at REAL NOT NULL, body TEXT NOT NULL)"
        )
        self.binding = assistants.runtime_binding(self.task, Ai())
        self.spec = ai_registry.get(self.task)
        rec = fixture(self.task, self.binding, "model-1")
        self.db.execute(
            "INSERT INTO assistant_releases (id,capability,status,body,revision) "
            "VALUES ('r1',?,'active',?,1)",
            (self.task, rel.canonical(rec)),
        )

    def status(self) -> str:
        return self.db.execute("SELECT status FROM assistant_releases WHERE id='r1'").fetchone()[0]

    def test_matching_exercise_record_is_admitted_and_kept_active(self) -> None:
        self.assertIsNone(rel.admission(self.db, self.task, self.binding, 1.0))
        self.assertEqual(self.status(), "active")

    def test_each_material_change_revokes_and_records_trigger(self) -> None:
        cases: dict[str, dict[str, Any]] = {
            "model": {"deployment": "other"},
            "prompt": {"prompt_version": "changed"},
            "policy": {"policy_version": "changed"},
            "data": {"data_version": "changed"},
            "permissions": {"permission_version": "changed"},
            "evidence": {"evaluation_version": "changed"},
        }
        for trigger, change in cases.items():
            with self.subTest(trigger=trigger):
                self.db.execute("UPDATE assistant_releases SET status='active' WHERE id='r1'")
                denied = rel.admission(self.db, self.task, dict(self.binding, **change), 1.0)
                self.assertIsNotNone(denied)
                self.assertEqual(self.status(), "revoked")
                bodies = [
                    json.loads(b)
                    for (b,) in self.db.execute(
                        "SELECT body FROM assistant_events WHERE task_id='r1'"
                    )
                ]
                self.assertTrue(any(trigger in b.get("reason", "") for b in bodies))

    def test_denial_keeps_mismatched_fields_after_revocation(self) -> None:
        changed = dict(self.binding, policy_version="changed")
        for _ in range(2):
            denied = rel.admission(self.db, self.task, changed, 1.0)
            assert denied is not None
            self.assertEqual(denied["missing"], ["policy_version"])
        self.assertEqual(self.status(), "revoked")
        again = rel.admission(self.db, self.task, self.binding, 1.0)
        assert again is not None
        self.assertEqual(again["missing"], ["policy_version"])

    def test_failed_audit_write_rolls_back_revocation_and_denies(self) -> None:
        self.db.execute("DROP TABLE assistant_events")
        changed = dict(self.binding, policy_version="changed")
        denied = rel.admission(self.db, self.task, changed, 1.0)
        self.assertIn("could not be recorded", denied["reason"])
        self.assertEqual(self.status(), "active")

    def test_intended_use_change_invalidates(self) -> None:
        self.assertEqual(
            rai_release.changed_triggers(
                fixture(self.task, self.binding),
                dict(self.spec, intended_use="Changed"),
                self.binding,
            ),
            ["intended_use"],
        )

    def test_unchanged_binding_has_no_triggers(self) -> None:
        self.assertEqual(
            rai_release.changed_triggers(fixture(self.task, self.binding), self.spec, self.binding),
            [],
        )


if __name__ == "__main__":
    unittest.main()
