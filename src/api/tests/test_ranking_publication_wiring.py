"""Ranking publication wired to the store and API (issue 79, PR-006, ADR 0002 decision 4).

Publishing is a manager action, idempotent, audited and read back by a verifying
status endpoint. Nothing here changes a ranking, the unsigned policy or any case.
"""

import copy
import os
import threading
import unittest
from unittest.mock import patch

from zava_forward.core import controls, ranking, ranking_publication

from test_role_matrix import QualityMatrix

PM_EMAIL = "pam"


class PublicationWiring(QualityMatrix):
    def archive(self):
        return self.store._ranking_archive()

    def test_status_and_publish_are_manager_only(self):
        for actor in ("sam", "quin", "kim"):
            self.assertEqual(self.call(actor, "/api/ranking/publication")[0], 403, actor)
            self.assertEqual(self.call(actor, "/api/ranking/publish", {})[0], 403, actor)
        self.assertFalse(os.path.exists(self.archive()))
        self.assertEqual(list(self.store.audit_entries()), [])

    def test_publish_archives_verifies_and_is_idempotent(self):
        code, status = self.call(PM_EMAIL, "/api/ranking/publication")
        self.assertEqual(code, 200)
        self.assertEqual((status["count"], status["latest"], status["overdue"]), (0, None, True))
        self.assertFalse(status["policy_signed"])
        self.assertEqual(status["signoff_problems"], ["No named policy owner."])
        self.assertEqual(status["schedule"]["owner"], "to be named")

        before = copy.deepcopy(self.store.cases)
        code, first = self.call(PM_EMAIL, "/api/ranking/publish", {})
        self.assertEqual((code, first["written"]), (200, True))
        self.assertEqual(first["published_on"], controls.today())
        code, again = self.call(PM_EMAIL, "/api/ranking/publish", {})
        self.assertEqual((code, again["written"]), (200, False))
        self.assertEqual(again["snapshot_hash"], first["snapshot_hash"])
        self.assertEqual(self.store.cases, before)

        status = self.call(PM_EMAIL, "/api/ranking/publication")[1]
        self.assertEqual((status["count"], status["problems"], status["overdue"]), (1, [], False))
        self.assertEqual(ranking_publication.verify(self.archive())["problems"], [])
        actions = [e["action"] for e in self.store.audit_entries()]
        self.assertEqual(
            actions, ["ranking_snapshot_published", "ranking_snapshot_already_published"]
        )
        self.assertEqual(ranking.CURRENT["owner"], "to be named")

    def test_concurrent_publish_is_serialised_and_audit_chain_intact(self):
        manager = {"email": PM_EMAIL, "role": "Retrofit Programme Manager"}
        barrier = threading.Barrier(2)
        results, errors = [], []

        def run():
            try:
                barrier.wait()
                results.append(self.store.publish_ranking_snapshot(manager)["written"])
            except Exception as e:  # noqa: BLE001 - surfaced by the assertion below
                errors.append(e)

        threads = [threading.Thread(target=run) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=30)
        self.assertEqual(errors, [])
        self.assertEqual(sorted(results), [False, True])
        actions = sorted(e["action"] for e in self.store.audit_entries())
        self.assertEqual(
            actions, ["ranking_snapshot_already_published", "ranking_snapshot_published"]
        )
        self.assertTrue(self.store.verify_audit())
        self.assertEqual(ranking_publication.verify(self.archive())["problems"], [])

    def test_edited_archive_is_reported_not_hidden(self):
        self.call(PM_EMAIL, "/api/ranking/publish", {})
        name = os.listdir(self.archive())[0]
        path = os.path.join(self.archive(), name)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        with open(path, "w", encoding="utf-8") as f:
            f.write(text.replace('"rank":1', '"rank":9', 1))
        status = self.call(PM_EMAIL, "/api/ranking/publication")[1]
        self.assertEqual(len(status["problems"]), 1)

    def test_corrupt_final_file_is_refused_and_not_audited_as_already_published(self):
        self.call(PM_EMAIL, "/api/ranking/publish", {})
        path = os.path.join(self.archive(), os.listdir(self.archive())[0])
        damaged = '{"published_on":"2026-01-01","snapshot":{}}'
        with open(path, "w", encoding="utf-8") as f:
            f.write(damaged)
        code, body = self.call(PM_EMAIL, "/api/ranking/publish", {})
        self.assertGreaterEqual(code, 400, body)
        with open(path, encoding="utf-8") as f:
            self.assertEqual(f.read(), damaged)
        actions = [e["action"] for e in self.store.audit_entries()]
        self.assertEqual(actions, ["ranking_snapshot_published"])

    def test_unsigned_policy_publication_is_recorded_in_audit_and_response(self):
        code, body = self.call(PM_EMAIL, "/api/ranking/publish", {})
        self.assertEqual((code, body["policy_signed"]), (200, False))
        entry = list(self.store.audit_entries())[0]
        self.assertIn("(unsigned)", entry["detail"])

    def test_status_listing_error_is_a_structured_problem(self):
        self.call(PM_EMAIL, "/api/ranking/publish", {})
        with patch.object(os, "listdir", side_effect=PermissionError("denied")):
            code, status = self.call(PM_EMAIL, "/api/ranking/publication")
        self.assertEqual(code, 200)
        self.assertEqual((status["count"], status["latest"], status["overdue"]), (0, None, True))
        self.assertEqual(len(status["problems"]), 1)
        self.assertIn("PermissionError", status["problems"][0])

    def test_publication_becomes_overdue_the_next_day(self):
        self.call(PM_EMAIL, "/api/ranking/publish", {})
        with patch.object(controls, "today", return_value="2999-01-01"):
            self.assertTrue(self.call(PM_EMAIL, "/api/ranking/publication")[1]["overdue"])

    def test_get_does_not_publish(self):
        self.assertEqual(self.call(PM_EMAIL, "/api/ranking/publish")[0], 403)
        self.assertFalse(os.path.exists(self.archive()))


if __name__ == "__main__":
    unittest.main()
