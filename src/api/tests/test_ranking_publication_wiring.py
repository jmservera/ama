"""Ranking publication wired to the store and API (issue 79, PR-006, ADR 0002 decision 4).

Publishing is a manager action, idempotent, audited and read back by a verifying
status endpoint. Nothing here changes a ranking, the unsigned policy or any case.
"""

import copy
import errno
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

    def test_unsupported_hard_links_are_a_storage_failure_not_an_authorization_one(self):
        for number in (errno.EPERM, errno.ENOTSUP):
            with self.subTest(errno=errno.errorcode[number]):
                unsupported = OSError(number, "hard links unsupported")
                with patch.object(os, "link", side_effect=unsupported):
                    code, body = self.call(PM_EMAIL, "/api/ranking/publish", {})
                self.assertEqual(code, 503)
                self.assertIn("hard links", body["error"])
                self.assertIn("could not be confirmed", body["error"])
                self.assertNotIn(self.archive(), body["error"])
                self.assertEqual(os.listdir(self.archive()), [])
                self.assertEqual(list(self.store.audit_entries()), [])
        self.assertEqual(self.call("sam", "/api/ranking/publish", {})[0], 403)
        self.assertEqual(self.call(PM_EMAIL, "/api/ranking/publish", {})[0], 200)

    def test_stage_cleanup_failure_after_commit_is_audited_and_reported(self):
        real = os.unlink

        def unlink(path, *args, **kwargs):
            if os.path.basename(path).startswith(".ranking-"):
                raise OSError(errno.EROFS, "read-only")
            real(path, *args, **kwargs)

        with patch.object(os, "unlink", side_effect=unlink):
            code, body = self.call(PM_EMAIL, "/api/ranking/publish", {})
        self.assertEqual((code, body["written"]), (200, True))
        self.assertIn("temporary file", body["warning"])
        self.assertNotIn(self.archive(), body["warning"])
        actions = [e["action"] for e in self.store.audit_entries()]
        self.assertEqual(actions, ["ranking_snapshot_published"])
        self.assertEqual(ranking_publication.verify(self.archive())["problems"], [])

    def test_link_and_cleanup_failure_is_logged_and_path_free(self):
        real = os.unlink

        def unlink(path, *args, **kwargs):
            if os.path.basename(path).startswith(".ranking-"):
                raise OSError(errno.EROFS, "read-only")
            real(path, *args, **kwargs)

        os.makedirs(self.archive(), exist_ok=True)
        foreign = os.path.join(self.archive(), "operator-note.txt")
        with open(foreign, "w", encoding="utf-8") as f:
            f.write("keep")
        with (
            patch.object(os, "link", side_effect=OSError(errno.EPERM, "no links")),
            patch.object(os, "unlink", side_effect=unlink),
            self.assertLogs("zava_forward.core.store", "WARNING") as logs,
        ):
            code, body = self.call(PM_EMAIL, "/api/ranking/publish", {})
        stage = next(n for n in os.listdir(self.archive()) if n.endswith(".tmp"))
        self.assertEqual(code, 503)
        self.assertIn("temporary file could not be removed", body["error"])
        self.assertNotIn(stage, body["error"])
        self.assertNotIn(self.archive(), body["error"])
        self.assertTrue(any(stage in line for line in logs.output))
        self.assertTrue(os.path.exists(foreign))
        self.assertEqual(list(self.store.audit_entries()), [])

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

    def test_directory_sync_failure_after_link_is_audited_as_unconfirmed(self):
        import stat

        real = os.fsync

        def failing(fd):
            if stat.S_ISDIR(os.fstat(fd).st_mode):
                raise OSError(5, "sync failed in /private/archive")
            return real(fd)

        with patch.object(os, "fsync", failing):
            code, body = self.call(PM_EMAIL, "/api/ranking/publish", {})
        self.assertEqual((code, body.get("outcome")), (409, "committed_unconfirmed"))
        self.assertNotIn("/", body["error"])
        self.assertNotIn("sync failed", body["error"])
        self.assertEqual(len(os.listdir(self.archive())), 1)
        self.assertEqual(ranking_publication.verify(self.archive())["problems"], [])
        entries = list(self.store.audit_entries())
        self.assertEqual(
            [e["action"] for e in entries], ["ranking_snapshot_publication_unconfirmed"]
        )
        self.assertEqual(entries[0]["who"], "pam@example.test")
        self.assertIn("unconfirmed", entries[0]["detail"])
        self.assertIn("unsigned", entries[0]["detail"])
        self.assertNotIn("/private", entries[0]["detail"])
        self.assertTrue(self.store.verify_audit())

    def test_parent_folder_sync_failure_is_audited_as_unconfirmed_and_retry_is_sound(self):
        import stat

        parent = os.path.dirname(os.path.abspath(self.archive()))
        real = os.fsync
        faulted = {"on": True}

        def failing(fd):
            if (
                faulted["on"]
                and stat.S_ISDIR(os.fstat(fd).st_mode)
                and os.path.samestat(os.fstat(fd), os.stat(parent))
            ):
                raise OSError(5, "sync failed in /private/parent")
            return real(fd)

        with patch.object(os, "fsync", failing):
            code, body = self.call(PM_EMAIL, "/api/ranking/publish", {})
            self.assertEqual((code, body.get("outcome")), (409, "committed_unconfirmed"))
            self.assertNotIn("/", body["error"])
            self.assertNotIn("sync failed", body["error"])
            names = os.listdir(self.archive())
            self.assertEqual(len(names), 1)
            with open(os.path.join(self.archive(), names[0]), encoding="utf-8") as f:
                original = f.read()
            self.assertEqual(ranking_publication.verify(self.archive())["problems"], [])
            self.assertEqual(
                [e["action"] for e in self.store.audit_entries()],
                ["ranking_snapshot_publication_unconfirmed"],
            )
            self.assertNotIn("/private", list(self.store.audit_entries())[0]["detail"])
            code, again = self.call(PM_EMAIL, "/api/ranking/publish", {})
            self.assertEqual((code, again.get("outcome")), (409, "committed_unconfirmed"))
            faulted["on"] = False
            code, done = self.call(PM_EMAIL, "/api/ranking/publish", {})
        self.assertEqual((code, done["written"]), (200, False))
        with open(os.path.join(self.archive(), names[0]), encoding="utf-8") as f:
            self.assertEqual(f.read(), original)
        self.assertTrue(self.store.verify_audit())

    def test_unreadable_mount_id_is_audited_as_unconfirmed_and_retry_is_sound(self):
        def unreadable(fd):
            raise OSError(5, "no mount id at /private/proc")

        with patch.object(ranking_publication, "_mount_id", unreadable, create=True):
            code, body = self.call(PM_EMAIL, "/api/ranking/publish", {})
            self.assertEqual((code, body.get("outcome")), (409, "committed_unconfirmed"))
            self.assertNotIn("/", body["error"])
            self.assertEqual(len(os.listdir(self.archive())), 1)
            self.assertEqual(ranking_publication.verify(self.archive())["problems"], [])
            self.assertEqual(
                [e["action"] for e in self.store.audit_entries()],
                ["ranking_snapshot_publication_unconfirmed"],
            )
        code, done = self.call(PM_EMAIL, "/api/ranking/publish", {})
        self.assertEqual((code, done["written"]), (200, False))
        self.assertTrue(self.store.verify_audit())

    def test_audit_failure_after_unconfirmed_directory_sync_is_logged_and_surfaced(self):
        import stat

        real = os.fsync

        def failing(fd):
            if stat.S_ISDIR(os.fstat(fd).st_mode):
                raise OSError(5, "sync failed")
            return real(fd)

        manager = {"email": PM_EMAIL, "role": "Retrofit Programme Manager"}
        with (
            patch.object(os, "fsync", failing),
            patch.object(self.store, "audit", side_effect=OSError(28, "no space")),
            self.assertLogs("zava_forward.core.store", level="ERROR") as logs,
            self.assertRaises(OSError),
        ):
            self.store.publish_ranking_snapshot(manager)
        self.assertIn("audit", logs.output[0])
        self.assertEqual(len(os.listdir(self.archive())), 1)

    def test_unconfirmed_sync_with_retained_stage_is_409_audited_logged_and_retry_confirms(self):
        import stat

        real_sync, real_unlink = os.fsync, os.unlink

        def failing(fd):
            if stat.S_ISDIR(os.fstat(fd).st_mode):
                raise OSError(errno.EIO, "sync failed in /private/archive")
            return real_sync(fd)

        def unlink(path, *args, **kwargs):
            if os.path.basename(path).startswith(".ranking-"):
                raise OSError(errno.EROFS, "read-only")
            real_unlink(path, *args, **kwargs)

        with (
            patch.object(os, "fsync", failing),
            patch.object(os, "unlink", side_effect=unlink),
            self.assertLogs("zava_forward.core.store", "WARNING") as logs,
        ):
            code, body = self.call(PM_EMAIL, "/api/ranking/publish", {})
        stage = next(n for n in os.listdir(self.archive()) if n.endswith(".tmp"))
        self.assertEqual((code, body.get("outcome")), (409, "committed_unconfirmed"))
        self.assertNotIn(stage, body["error"])
        self.assertNotIn("/private", body["error"])
        self.assertTrue(any(stage in line for line in logs.output))
        self.assertEqual(
            [e["action"] for e in self.store.audit_entries()],
            ["ranking_snapshot_publication_unconfirmed"],
        )
        code, body = self.call(PM_EMAIL, "/api/ranking/publish", {})
        self.assertEqual((code, body["written"]), (200, False))
        self.assertEqual(
            [e["action"] for e in self.store.audit_entries()][-1],
            "ranking_snapshot_already_published",
        )

    def test_stage_cleanup_failure_still_audits_and_returns_unconfirmed_not_403(self):
        import stat

        real_fsync, real_unlink = os.fsync, os.unlink

        def failing_fsync(fd):
            if stat.S_ISDIR(os.fstat(fd).st_mode):
                raise OSError(5, "sync failed")
            return real_fsync(fd)

        def failing_unlink(path, *a, **k):
            if os.path.basename(path).startswith(".ranking-"):
                raise PermissionError(13, "read-only /private/archive")
            return real_unlink(path, *a, **k)

        with patch.object(os, "fsync", failing_fsync), patch.object(os, "unlink", failing_unlink):
            code, body = self.call(PM_EMAIL, "/api/ranking/publish", {})
        self.assertEqual((code, body.get("outcome")), (409, "committed_unconfirmed"))
        self.assertNotIn("/", body["error"])
        self.assertNotIn("read-only", body["error"])
        actions = [e["action"] for e in self.store.audit_entries()]
        self.assertEqual(actions, ["ranking_snapshot_publication_unconfirmed"])
        names = os.listdir(self.archive())
        self.assertEqual(sum(n.startswith("ranking-") for n in names), 1)

    def test_publication_becomes_overdue_the_next_day(self):
        self.call(PM_EMAIL, "/api/ranking/publish", {})
        with patch.object(controls, "today", return_value="2999-01-01"):
            self.assertTrue(self.call(PM_EMAIL, "/api/ranking/publication")[1]["overdue"])

    def test_get_does_not_publish(self):
        self.assertEqual(self.call(PM_EMAIL, "/api/ranking/publish")[0], 403)
        self.assertFalse(os.path.exists(self.archive()))


class BlobPublicationWiring(QualityMatrix):
    """The same routes with the owner-selected Blob archive on a mock REST transport (Refs #1258)."""

    def setUp(self):
        super().setUp()
        from ranking_blob_fixture import SAS, FakeBlobContainer, URL
        from zava_forward.core import ranking_archive_blob as rab

        self.fake = FakeBlobContainer(page_size=1)
        self.blob = rab.BlobRankingArchive(URL, "ranking-archive", sas=SAS, transport=self.fake, env={})
        self.archive_patch = patch.object(self.store, "_ranking_archive", return_value=self.blob)
        self.archive_patch.start()
        self.addCleanup(self.archive_patch.stop)

    def clean(self, text):
        for secret in ("SENTINEL", "acct.blob.core.windows.net", "ranking-archive", "hard links", "folder"):
            self.assertNotIn(secret, text)

    def test_publish_is_manager_only_idempotent_audited_and_verified(self):
        for actor in ("sam", "quin", "kim"):
            self.assertEqual(self.call(actor, "/api/ranking/publish", {})[0], 403)
        self.assertEqual(self.fake.calls, [])
        code, first = self.call(PM_EMAIL, "/api/ranking/publish", {})
        self.assertEqual((code, first["written"], first["published_on"]), (200, True, controls.today()))
        code, again = self.call(PM_EMAIL, "/api/ranking/publish", {})
        self.assertEqual((code, again["written"]), (200, False))
        status = self.call(PM_EMAIL, "/api/ranking/publication")[1]
        self.assertEqual((status["count"], status["problems"], status["overdue"]), (1, [], False))
        self.assertEqual(
            [e["action"] for e in self.store.audit_entries()],
            ["ranking_snapshot_published", "ranking_snapshot_already_published"],
        )
        self.assertTrue(self.store.verify_audit())
        self.assertEqual({c[0] for c in self.fake.calls}, {"PUT", "GET"})

    def test_concurrent_publish_keeps_one_record_and_an_intact_audit_chain(self):
        manager = {"email": PM_EMAIL, "role": "Retrofit Programme Manager"}
        results = []
        threads = [threading.Thread(target=lambda: results.append(self.store.publish_ranking_snapshot(manager)["written"])) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(30)
        self.assertEqual(sorted(results), [False, True])
        self.assertEqual(len(self.fake.blobs), 1)
        self.assertTrue(self.store.verify_audit())

    def test_uncertain_write_is_409_audited_without_claiming_the_write_and_retry_is_sound(self):
        for fault in ("lost", "unreachable", 503):
            with self.subTest(fault=fault):
                self.fake.blobs.clear()
                self.fake.meta.clear()
                before = len(list(self.store.audit_entries()))
                self.fake.put_faults = [fault]
                code, body = self.call(PM_EMAIL, "/api/ranking/publish", {})
                self.assertEqual((code, body.get("outcome")), (409, "committed_unconfirmed"))
                self.clean(body["error"])
                self.assertIn("may or may not", body["error"])
                entries = list(self.store.audit_entries())[before:]
                self.assertEqual([e["action"] for e in entries], ["ranking_snapshot_publication_unconfirmed"])
                self.assertNotIn("record written", entries[0]["detail"])
                self.assertIn("unconfirmed", entries[0]["detail"])
                self.clean(entries[0]["detail"])
                code, retry = self.call(PM_EMAIL, "/api/ranking/publish", {})
                self.assertEqual((code, retry["written"]), (200, fault != "lost"))
        self.assertTrue(self.store.verify_audit())

    def test_definite_refusal_is_503_path_free_and_not_audited_as_published(self):
        self.fake.put_faults = [403]
        code, body = self.call(PM_EMAIL, "/api/ranking/publish", {})
        self.assertEqual(code, 503)
        self.clean(body["error"])
        self.assertIn("could not be confirmed", body["error"])
        self.assertEqual(self.fake.blobs, {})
        self.assertEqual(list(self.store.audit_entries()), [])

    def test_unavailable_configuration_is_503_path_free_with_no_fallback_to_a_folder(self):
        self.archive_patch.stop()
        env = {"ZF_RANKING_ARCHIVE": "azure-blob", "ZF_BLOB_ACCOUNT_URL": "https://acct.blob.core.windows.net"}
        with patch.dict(os.environ, env):
            code, body = self.call(PM_EMAIL, "/api/ranking/publish", {})
            status_code, status = self.call(PM_EMAIL, "/api/ranking/publication")
        self.assertEqual(code, 503)
        self.clean(body["error"])
        self.assertEqual(status_code, 200)
        self.assertEqual(status["count"], 0)
        self.assertEqual(len(status["problems"]), 1)
        self.clean(status["problems"][0])
        self.assertFalse(os.path.exists(os.path.join(os.path.dirname(self.store.db_path), "ranking-archive")))
        self.assertEqual(list(self.store.audit_entries()), [])

    def test_store_selects_the_adapter_from_the_environment(self):
        self.archive_patch.stop()
        env = {"ZF_RANKING_ARCHIVE": "azure-blob", "ZF_BLOB_ACCOUNT_URL": "https://acct.blob.core.windows.net",
               "ZF_RANKING_BLOB_CONTAINER": "ranking-archive", "ZF_BLOB_SAS": "sig=SENTINEL"}
        with patch.dict(os.environ, env):
            self.assertEqual(type(self.store._ranking_archive()).__name__, "BlobRankingArchive")
        with patch.dict(os.environ, {"ZF_RANKING_ARCHIVE": "local"}):
            self.assertEqual(os.path.basename(self.store._ranking_archive()), "ranking-archive")

    def test_status_reports_a_tampered_blob_and_an_unreadable_listing(self):
        self.call(PM_EMAIL, "/api/ranking/publish", {})
        name = next(iter(self.fake.blobs))
        self.fake.blobs[name] = self.fake.blobs[name].replace(b'"rank":1', b'"rank":9', 1)
        status = self.call(PM_EMAIL, "/api/ranking/publication")[1]
        self.assertEqual(len(status["problems"]), 1)
        self.fake.list_status = 500
        code, status = self.call(PM_EMAIL, "/api/ranking/publication")
        self.assertEqual((code, status["count"], status["latest"], status["overdue"]), (200, 0, None, True))
        self.assertIn("ranking archive", status["problems"][0])
        self.clean(status["problems"][0])

    def test_publish_route_is_a_conditional_create_and_does_not_list(self):
        self.fake.list_status = 500
        code, first = self.call(PM_EMAIL, "/api/ranking/publish", {})
        self.assertEqual((code, first["written"]), (200, True))
        self.assertEqual([c for c in self.fake.calls if "comp=list" in c[1]], [])
        self.assertEqual(len(self.fake.blobs), 1)
        code, status = self.call(PM_EMAIL, "/api/ranking/publication")
        self.assertEqual((code, status["count"], status["latest"]), (200, 0, None))
        self.assertEqual(len(status["problems"]), 1)
        self.clean(status["problems"][0])

    def test_structurally_invalid_200_listing_is_unreadable_status_not_healthy_empty(self):
        bodies = (
            b"<Error><Code>InternalError</Code></Error>",
            b"<EnumerationResults/>",
            b"<EnumerationResults><Blobs><Blob/></Blobs></EnumerationResults>",
        )
        for body in bodies:
            with self.subTest(body=body):
                self.fake.list_body = body
                code, status = self.call(PM_EMAIL, "/api/ranking/publication")
                self.assertEqual((code, status["count"], status["latest"], status["overdue"]), (200, 0, None, True))
                self.assertEqual(len(status["problems"]), 1)
                self.assertIn("ranking archive", status["problems"][0])
                self.clean(status["problems"][0])
        self.fake.list_body = b"<EnumerationResults><Blobs/></EnumerationResults>"
        code, status = self.call(PM_EMAIL, "/api/ranking/publication")
        self.assertEqual((code, status["count"], status["problems"]), (200, 0, []))
        self.assertEqual(self.fake.requests("PUT"), [])


if __name__ == "__main__":
    unittest.main()
