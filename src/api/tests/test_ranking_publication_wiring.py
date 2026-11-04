"""Ranking publication wired to the store and API (issue 79, PR-006, ADR 0002 decision 4).

Publishing is a manager action, idempotent, audited and read back by a verifying
status endpoint. Nothing here changes a ranking, the unsigned policy or any case.
"""
import copy
import os
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
        self.assertEqual(actions, ["ranking_snapshot_published",
                                   "ranking_snapshot_already_published"])
        self.assertEqual(ranking.CURRENT["owner"], "to be named")

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

    def test_publication_becomes_overdue_the_next_day(self):
        self.call(PM_EMAIL, "/api/ranking/publish", {})
        with patch.object(controls, "today", return_value="2999-01-01"):
            self.assertTrue(self.call(PM_EMAIL, "/api/ranking/publication")[1]["overdue"])

    def test_get_does_not_publish(self):
        self.assertEqual(self.call(PM_EMAIL, "/api/ranking/publish")[0], 403)
        self.assertFalse(os.path.exists(self.archive()))


if __name__ == "__main__":
    unittest.main()
