"""Ranking archive in Azure Blob JSON persistence (Refs #1258).

The transport is an in-memory mock (ranking_blob_fixture), not an emulator or a real account.
"""

import contextlib
import hashlib
import io
import json
import logging
import threading
import unittest

from ranking_blob_fixture import SAS, URL, FakeBlobContainer
from test_ranking_publication import AS_OF, snap
from zava_forward.core import ranking
from zava_forward.core import ranking_archive_blob as rab
from zava_forward.core import ranking_publication as rp

CONTAINER = "ranking-archive"
SECRETS = ("SENTINEL-SAS-SECRET", "SENTINEL-TOKEN", "acct.blob.core.windows.net", CONTAINER)


def opened(fake):
    return rab.BlobRankingArchive(URL, CONTAINER, sas=SAS, transport=fake, env={})


def assert_clean(test, text):
    for secret in SECRETS:
        test.assertNotIn(secret, text)


class ConditionalCreateTests(unittest.TestCase):
    def setUp(self):
        self.fake = FakeBlobContainer()
        self.archive = opened(self.fake)
        self.snap = snap()
        self.name = rp._name(self.snap)

    def test_first_publication_is_one_conditional_create_with_verifiable_metadata(self):
        out = rp.publish(self.snap, self.archive, "2026-10-10")
        self.assertEqual(
            (out["written"], out["published_on"], out["path"]), (True, "2026-10-10", self.name)
        )
        puts = self.fake.requests("PUT")
        self.assertEqual(len(puts), 1)
        self.assertEqual(puts[0][2]["If-None-Match"], "*")
        raw = self.fake.blobs[self.name]
        self.assertEqual(json.loads(raw), {"published_on": "2026-10-10", "snapshot": self.snap})
        meta = self.fake.meta[self.name]
        self.assertEqual(meta["record_sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(
            {k: meta[k] for k in ("policy_version", "as_of", "published_on", "snapshot_hash")},
            {
                "policy_version": self.snap["policy_version"],
                "as_of": AS_OF,
                "published_on": "2026-10-10",
                "snapshot_hash": self.snap["snapshot_hash"],
            },
        )
        self.assertEqual({c[0] for c in self.fake.calls}, {"PUT"})

    def test_conditional_create_never_lists_so_an_unreadable_listing_does_not_block_it(self):
        self.fake.list_status = 500
        out = rp.publish(self.snap, self.archive, "2026-10-10")
        self.assertEqual((out["written"], out["path"]), (True, self.name))
        self.assertEqual([c for c in self.fake.calls if "comp=list" in c[1]], [])
        self.assertEqual(len(self.fake.requests("PUT")), 1)

    def test_repeat_is_idempotent_and_keeps_the_original_date_and_bytes(self):
        rp.publish(self.snap, self.archive, "2026-10-10")
        before = dict(self.fake.blobs)
        again = rp.publish(self.snap, self.archive, "2026-10-20")
        self.assertEqual((again["written"], again["published_on"]), (False, "2026-10-10"))
        self.assertEqual(self.fake.blobs, before)
        self.assertEqual({m for m, *_ in self.fake.calls}, {"PUT", "GET"})

    def test_changed_input_is_a_new_record_never_an_overwrite(self):
        rp.publish(self.snap, self.archive, "2026-10-10")
        first = dict(self.fake.blobs)
        other = ranking.snapshot([], ranking.POLICY_V1, AS_OF)
        self.assertTrue(rp.publish(other, self.archive, "2026-10-10")["written"])
        self.assertEqual(len(self.fake.blobs), 2)
        self.assertEqual({k: self.fake.blobs[k] for k in first}, first)

    def test_concurrent_writers_keep_one_record_and_one_reports_it(self):
        barrier = threading.Barrier(2)
        self.fake.put_gate = lambda: barrier.wait(10)
        results, errors = [], []

        def run(day):
            try:
                results.append(rp.publish(self.snap, self.archive, day))
            except Exception as e:  # noqa: BLE001 - asserted below
                errors.append(e)

        threads = [threading.Thread(target=run, args=(d,)) for d in ("2026-10-10", "2026-10-11")]
        for t in threads:
            t.start()
        for t in threads:
            t.join(20)
        self.assertEqual(errors, [])
        self.assertEqual(sorted(r["written"] for r in results), [False, True])
        self.assertEqual(len(self.fake.blobs), 1)
        self.assertEqual(
            {r["published_on"] for r in results},
            {json.loads(self.fake.blobs[self.name])["published_on"]},
        )

    def test_existing_record_that_is_damaged_different_or_unverifiable_is_refused_untouched(self):
        rp.publish(self.snap, self.archive, "2026-10-10")
        good = self.fake.blobs[self.name]
        meta = dict(self.fake.meta[self.name])
        broken = {
            "not json": (b"{", meta),
            "different snapshot": (
                json.dumps(
                    {"published_on": "2026-10-10", "snapshot": {**self.snap, "total": 99}}
                ).encode(),
                meta,
            ),
            "bad date": (
                json.dumps({"published_on": "2026-13-40", "snapshot": self.snap}).encode(),
                meta,
            ),
            "metadata missing": (good, {}),
            "metadata altered": (good, {**meta, "snapshot_hash": "0" * 64}),
            "bytes altered after metadata": (good + b" ", meta),
        }
        for label, (raw, m) in broken.items():
            with self.subTest(label):
                self.fake.blobs[self.name], self.fake.meta[self.name] = raw, m
                with self.assertRaises(rp.PublicationError) as ctx:
                    rp.publish(self.snap, self.archive, "2026-10-11")
                assert_clean(self, str(ctx.exception))
                self.assertEqual(self.fake.blobs[self.name], raw)

    def test_conflict_classification(self):
        for fault, expect in [
            ((409, "BlobAlreadyExists"), "exists"),
            (409, "exists"),
            (412, "exists"),
            ((409, "BlobImmutableDueToPolicy"), "refused"),
            (403, "refused"),
            (404, "refused"),
            (400, "refused"),
        ]:
            with self.subTest(fault=fault):
                self.fake.blobs.clear()
                self.fake.put_faults = [fault]
                if expect == "exists":
                    self.fake.blobs[self.name] = json.dumps(
                        {"published_on": "2026-10-01", "snapshot": self.snap},
                        sort_keys=True,
                        separators=(",", ":"),
                    ).encode()
                    self.fake.meta[self.name] = rab.metadata_for(
                        self.snap, "2026-10-01", self.fake.blobs[self.name]
                    )
                    self.assertEqual(
                        rp.publish(self.snap, self.archive, "2026-10-10")["published_on"],
                        "2026-10-01",
                    )
                else:
                    with self.assertRaises(rab.BlobArchiveError) as ctx:
                        rp.publish(self.snap, self.archive, "2026-10-10")
                    assert_clean(self, str(ctx.exception))
                    self.assertNotIsInstance(ctx.exception, rp.DurabilityUnconfirmedError)

    def test_exists_without_a_readable_record_is_refused_not_confirmed(self):
        self.fake.put_faults = [(409, "BlobAlreadyExists")]
        with self.assertRaises(rab.BlobArchiveError):
            rp.publish(self.snap, self.archive, "2026-10-10")
        self.fake.put_faults = [412]
        self.fake.blobs[self.name] = b"x"
        self.fake.get_faults[self.name] = 500
        with self.assertRaises(rab.BlobArchiveError):
            rp.publish(self.snap, self.archive, "2026-10-10")

    def test_mixed_case_metadata_headers_verify(self):
        self.fake.mixed_case = True
        rp.publish(self.snap, self.archive, "2026-10-10")
        self.assertFalse(rp.publish(self.snap, self.archive, "2026-10-12")["written"])
        self.assertEqual(rp.verify(self.archive)["problems"], [])

    def test_adapter_can_only_create_read_and_list(self):
        for forbidden in ("put", "delete", "list_ids", "get"):
            self.assertFalse(hasattr(self.archive, forbidden), forbidden)
        with self.assertRaises(ValueError):
            self.archive.create("../escape.json", b"{}", {})
        with self.assertRaises(ValueError):
            self.archive.read("other-container/ranking-x.json")
        self.assertEqual(self.fake.calls, [])


class UncertainWriteTests(unittest.TestCase):
    def setUp(self):
        self.fake = FakeBlobContainer()
        self.archive = opened(self.fake)
        self.snap = snap()
        self.name = rp._name(self.snap)

    def uncertain(self, fault):
        self.fake.put_faults = [fault]
        with self.assertRaises(rp.DurabilityUnconfirmedError) as ctx:
            rp.publish(self.snap, self.archive, "2026-10-10")
        err = ctx.exception
        self.assertIsInstance(err, rp.ArchiveWriteUncertainError)
        self.assertIsNone(err.written)
        self.assertEqual((err.published_on, err.path), ("2026-10-10", self.name))
        text = str(err)
        assert_clean(self, text + repr(err.__cause__) + repr(err.__context__))
        self.assertIn("may or may not", text)
        self.assertNotIn("was written", text)
        self.assertEqual({m for m, *_ in self.fake.calls}, {"PUT"})
        return err

    def test_lost_response_after_commit_is_unconfirmed_then_retry_reports_the_record(self):
        self.uncertain("lost")
        self.assertIn(self.name, self.fake.blobs)
        retry = rp.publish(self.snap, self.archive, "2026-10-12")
        self.assertEqual((retry["written"], retry["published_on"]), (False, "2026-10-10"))

    def test_failure_before_commit_leaves_nothing_and_the_retry_writes(self):
        self.uncertain("unreachable")
        self.assertEqual(self.fake.blobs, {})
        self.assertTrue(rp.publish(self.snap, self.archive, "2026-10-12")["written"])

    def test_server_error_timeout_and_busy_are_unconfirmed_not_failed(self):
        for status in (500, 503, 504, 408):
            with self.subTest(status):
                self.fake.blobs.clear()
                self.uncertain(status)

    def test_a_changed_input_retry_is_a_new_record_and_the_first_attempt_stays_visible_by_hash(
        self,
    ):
        self.uncertain("lost")
        other = ranking.snapshot([], ranking.POLICY_V1, AS_OF)
        self.assertTrue(rp.publish(other, self.archive, "2026-10-12")["written"])
        self.assertEqual(len(self.fake.blobs), 2)

    def test_authorization_failure_before_dispatch_is_a_refusal_with_nothing_sent(self):
        def no_token(method, url, headers, body, timeout=20):
            self.fake.calls.append((method, url, headers, body))
            return 500, {}, b""

        archive = rab.BlobRankingArchive(
            URL,
            CONTAINER,
            transport=no_token,
            env={"IDENTITY_ENDPOINT": "http://identity.local/msi", "IDENTITY_HEADER": "H"},
        )
        with self.assertRaises(rab.BlobArchiveError) as ctx:
            rp.publish(self.snap, archive, "2026-10-10")
        self.assertNotIsInstance(ctx.exception, rp.DurabilityUnconfirmedError)
        assert_clean(self, str(ctx.exception))
        self.assertEqual([c for c in self.fake.calls if c[0] == "PUT"], [])

    def test_managed_identity_token_is_used_and_never_logged(self):
        archive = rab.BlobRankingArchive(
            URL,
            CONTAINER,
            transport=self.fake,
            env={"IDENTITY_ENDPOINT": "http://identity.local/msi", "IDENTITY_HEADER": "H"},
        )
        with self.assertLogs(level="DEBUG") as logs:
            logging.getLogger("probe").debug("probe")
            rp.publish(self.snap, archive, "2026-10-10")
        put = self.fake.requests("PUT")[0]
        self.assertEqual(put[2]["Authorization"], "Bearer SENTINEL-TOKEN")
        self.assertNotIn("sig=", put[1])
        assert_clean(self, "\n".join(logs.output))


class ConfigurationTests(unittest.TestCase):
    def test_unset_selector_keeps_the_local_folder_adapter(self):
        self.assertIsNone(rab.open_ranking_archive({}))
        self.assertIsNone(rab.open_ranking_archive({"ZF_RANKING_ARCHIVE": "local"}))

    def test_invalid_or_missing_configuration_refuses_without_echoing_or_sending(self):
        fake = FakeBlobContainer()
        base = {
            "ZF_RANKING_ARCHIVE": "azure-blob",
            "ZF_BLOB_ACCOUNT_URL": URL,
            "ZF_RANKING_BLOB_CONTAINER": CONTAINER,
            "ZF_BLOB_SAS": SAS,
        }
        cases = {
            "unknown selector": {**base, "ZF_RANKING_ARCHIVE": "blobby"},
            "no url": {k: v for k, v in base.items() if k != "ZF_BLOB_ACCOUNT_URL"},
            "http url": {**base, "ZF_BLOB_ACCOUNT_URL": "http://acct.blob.core.windows.net"},
            "no container": {k: v for k, v in base.items() if k != "ZF_RANKING_BLOB_CONTAINER"},
            "bad container": {**base, "ZF_RANKING_BLOB_CONTAINER": "../Bad Name"},
        }
        for label, env in cases.items():
            with self.subTest(label):
                with self.assertRaises(rab.BlobArchiveError) as ctx:
                    rab.open_ranking_archive(env, fake)
                assert_clean(self, str(ctx.exception))
                self.assertNotIn("Bad Name", str(ctx.exception))
        self.assertEqual(fake.calls, [])
        self.assertIsInstance(rab.open_ranking_archive(base, fake), rab.BlobRankingArchive)


class VerifyTests(unittest.TestCase):
    def setUp(self):
        self.fake = FakeBlobContainer(page_size=2)
        self.archive = opened(self.fake)
        self.snaps = [
            ranking.snapshot([], ranking.POLICY_V1, d)
            for d in ("2026-10-01", "2026-10-02", "2026-10-03")
        ]
        for i, s in enumerate(self.snaps):
            rp.publish(s, self.archive, f"2026-10-0{i + 1}")

    def test_verify_pages_through_the_listing_and_reports_latest_and_overdue(self):
        out = rp.verify(self.archive)
        self.assertEqual((out["count"], out["problems"], out["latest"]), (3, [], "2026-10-03"))
        self.assertGreater(len(self.fake.requests("GET")), 3)
        self.assertTrue(rp.overdue(self.archive, "2026-10-04"))
        self.assertFalse(rp.overdue(self.archive, "2026-10-03"))

    def test_tampered_bytes_metadata_name_policy_and_date_are_reported(self):
        names = sorted(self.fake.blobs)
        raw = json.loads(self.fake.blobs[names[0]])
        self.fake.blobs[names[0]] = json.dumps({**raw, "published_on": "2026-02-31"}).encode()
        self.fake.meta[names[1]]["snapshot_hash"] = "f" * 64
        del self.fake.meta[names[2]]["record_sha256"]
        problems = rp.verify(self.archive)["problems"]
        self.assertEqual(len(problems), 3, problems)
        for p in problems:
            assert_clean(self, p)

    def test_unlisted_or_foreign_names_are_ignored_and_a_misnamed_record_is_a_problem(self):
        self.fake.blobs["notes.txt"] = b"x"
        self.fake.blobs["ranking-9.9-2026-01-01-aaaaaaaaaaaa.json"] = self.fake.blobs[
            sorted(self.fake.blobs)[0]
        ]
        self.fake.meta["ranking-9.9-2026-01-01-aaaaaaaaaaaa.json"] = {}
        out = rp.verify(self.archive)
        self.assertEqual(out["count"], 4)
        self.assertEqual(len(out["problems"]), 1)

    def test_unreadable_listing_is_an_error_never_an_empty_archive(self):
        self.fake.list_status = 500
        with self.assertRaises(OSError) as ctx:
            rp.verify(self.archive)
        assert_clean(self, str(ctx.exception))
        self.fake.list_status = 403
        with self.assertRaises(OSError):
            rp.overdue(self.archive, "2026-10-04")

    def test_structurally_invalid_200_listing_is_an_error_never_an_empty_archive(self):
        ok = "ranking-1.0.0-2026-10-01-aaaaaaaaaaaa.json"

        def page(inner):
            return f"<EnumerationResults>{inner}</EnumerationResults>".encode()

        def blob(inner):
            return page(f"<Blobs><Blob>{inner}</Blob></Blobs>")

        bodies = {
            "error root": b"<Error><Code>InternalError</Code></Error>",
            "bare root": b"<EnumerationResults/>",
            "wrong root": b"<Other><Blobs/></Other>",
            "nested blobs": page("<X><Blobs/></X>"),
            "two blobs": page("<Blobs/><Blobs/>"),
            "stray name only": page(f"<Name>{ok}</Name>"),
            "blob without name": blob(""),
            "blank name": blob("<Name> </Name>"),
            "empty name": blob("<Name/>"),
            "deep name": blob(f"<P><Name>{ok}</Name></P>"),
            "two names": blob(f"<Name>{ok}</Name><Name>{ok}</Name>"),
            "name with child": blob(f"<Name>{ok}<Other/></Name>"),
            "foreign child of blobs": page(f"<Blobs><Item><Name>{ok}</Name></Item></Blobs>"),
            "unsupported encoding": b'<?xml version="1.0" encoding="x-unknown"?><A><Blobs/></A>',
            "not xml": b"",
        }
        for label, body in bodies.items():
            with self.subTest(label):
                self.fake.list_body = body
                for call in (
                    self.archive.names,
                    lambda: rp.verify(self.archive),
                    lambda: rp.overdue(self.archive, "2026-10-04"),
                ):
                    with self.assertRaises(rab.BlobArchiveError) as ctx:
                        call()
                    self.assertEqual(str(ctx.exception), "ranking archive listing was unreadable")
                    assert_clean(self, repr(ctx.exception))

    def test_valid_empty_and_ordinary_listings_are_still_accepted(self):
        ok = "ranking-1.0.0-2026-10-01-aaaaaaaaaaaa.json"
        attrs = 'ServiceEndpoint="https://x/" ContainerName="c"'
        for body in (
            f"<EnumerationResults {attrs}><Blobs/><NextMarker/></EnumerationResults>",
            f"<EnumerationResults {attrs}><Blobs></Blobs></EnumerationResults>",
            f"<EnumerationResults {attrs}><Blobs><Blob><Name>notes.txt</Name></Blob></Blobs>"
            "<NextMarker> </NextMarker></EnumerationResults>",
        ):
            self.fake.list_body = body.encode()
            self.assertEqual(self.archive.names(), [])
        self.fake.list_body = (
            f"<EnumerationResults {attrs}><Blobs><Blob><Name>{ok}</Name><Properties><Name>x</Name>"
            f"</Properties></Blob></Blobs><Name>stray</Name></EnumerationResults>"
        ).encode()
        self.assertEqual(self.archive.names(), [ok])
        self.fake.list_body = None
        self.assertEqual(rp.verify(self.archive)["count"], 3)

    def test_unreadable_record_is_a_problem_not_a_pass(self):
        name = sorted(self.fake.blobs)[0]
        self.fake.get_faults[name] = 503
        out = rp.verify(self.archive)
        self.assertEqual(out["count"], 3)
        self.assertEqual(len(out["problems"]), 1)

    def test_no_request_leaks_the_secret_into_the_url_of_a_listing_error(self):
        self.fake.list_status = 500
        with contextlib.redirect_stderr(io.StringIO()) as err, self.assertRaises(OSError):
            rp.verify(self.archive)
        assert_clean(self, err.getvalue())


if __name__ == "__main__":
    unittest.main()
