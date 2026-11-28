"""Focused unit tests for immutable Blob ledger digests and scheduled verification."""

from __future__ import annotations

import json
import tempfile
import traceback
import unittest
import urllib.parse
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from zava_forward.core import ledger
from zava_forward.core.ledger_digest_blob import (
    ACCOUNT_URL_VAR,
    ALERT_MARKER,
    CONTAINER_VAR,
    DEFAULT_CONTAINER,
    MIN_RETENTION_DAYS_VAR,
    MISMATCH_RUNBOOK,
    MISSING_RUNBOOK,
    OK_MARKER,
    PROPOSED_OWNER,
    RECONCILE_ALERT_MARKER,
    RECONCILE_OK_MARKER,
    REQUIRE_LOCK_VAR,
    SAS_VAR,
    BlobLedgerDigestStore,
    InvalidDigestAnchorError,
    LedgerDigestBlobError,
    LedgerDigestBlobUncertain,
    main,
    open_ledger_digest_store,
    publish_ledger_digests,
    publish_ledger_digests_with_posture,
    reconcile_ledger_digests,
    run_scheduled_verification,
    verify_blob_retention_headers,
    verify_container_retention_lock,
    verify_ledger_digests,
)
from zava_forward.core.store import Store

ACCOUNT_URL = "https://stzavasecretacct.blob.core.windows.net"
SECRET_SAS = "sv=2024-11-04&ss=b&srt=co&sp=rwl&sig=SUPERSECRET_SAS_SIGNATURE_123"
LOCKED_UNTIL_RFC1123 = "Wed, 15 Nov 2028 02:00:00 GMT"
AS_OF_UTC = datetime(2026, 11, 15, 2, 0, 0, tzinfo=UTC)


def _sample_chain() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    specs = [
        ("2024-06-10T09:00:00+00:00", "u-1", "case.opened", "CASE-1", {"step": 1}),
        ("2025-03-12T14:30:00+00:00", "u-2", "survey.logged", "CASE-1", {"step": 2}),
        ("2026-08-01T11:15:00+00:00", "u-1", "pack.reviewed", "CASE-1", {"step": 3}),
        ("2026-11-14T16:45:00+00:00", "u-3", "signoff.recorded", "CASE-1", {"step": 4}),
    ]
    prev = ledger.GENESIS
    for at_val, who, action, case_id, detail in specs:
        entry: dict[str, Any] = ledger.make_entry(who, action, case_id, detail, prev, at=at_val)
        entries.append(entry)
        prev = str(entry["hash"])
    return entries


class _FakeImmutableBlobTransport:
    """In-memory Azure Blob REST fake supporting WORM headers, pagination, and fault injection."""

    def __init__(
        self,
        *,
        immutability_mode: str | None = "locked",
        immutability_until: str | None = LOCKED_UNTIL_RFC1123,
        creation_time: str | None = "Sun, 15 Nov 2026 02:00:00 GMT",
        page_size: int = 2,
        conflict_status: int = 409,
        conflict_code: str = "BlobAlreadyExists",
    ) -> None:
        self.blobs: dict[str, bytes] = {}
        self.immutability_mode = immutability_mode
        self.immutability_until = immutability_until
        self.creation_time = creation_time
        self.per_blob_headers: dict[str, dict[str, str]] = {}
        self.page_size = page_size
        self.conflict_status = conflict_status
        self.conflict_code = conflict_code
        self.calls: list[tuple[str, str, dict[str, str]]] = []
        self.next_put_status: int | None = None
        self.raise_on_method: str | None = None

    def _worm_headers(self, blob_name: str = "") -> dict[str, str]:
        if blob_name and blob_name in self.per_blob_headers:
            return dict(self.per_blob_headers[blob_name])
        headers: dict[str, str] = {}
        if self.immutability_mode is not None:
            headers["x-ms-immutability-policy-mode"] = self.immutability_mode
        if self.immutability_until is not None:
            headers["x-ms-immutability-policy-until-date"] = self.immutability_until
        if self.creation_time is not None:
            headers["x-ms-creation-time"] = self.creation_time
        return headers

    def __call__(
        self,
        method: str,
        url: str,
        headers: Mapping[str, str],
        body: bytes | None = None,
    ) -> tuple[int, Mapping[str, str], bytes]:
        copied_headers = {str(k): str(v) for k, v in headers.items()}
        self.calls.append((method, url, copied_headers))
        if self.raise_on_method == method:
            raise OSError(f"network fault talking to {ACCOUNT_URL}?{SECRET_SAS}")

        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed.query)
        if method == "GET" and query.get("comp") == ["list"]:
            all_names = sorted(self.blobs)
            marker_vals = query.get("marker", [""])
            start = int(marker_vals[0]) if marker_vals[0] else 0
            chunk = all_names[start : start + self.page_size]
            next_idx = start + self.page_size
            next_marker = str(next_idx) if next_idx < len(all_names) else ""
            items = "".join(f"<Blob><Name>{name}</Name></Blob>" for name in chunk)
            xml = (
                '<?xml version="1.0" encoding="utf-8"?>'
                "<EnumerationResults>"
                f"<Blobs>{items}</Blobs>"
                f"<NextMarker>{next_marker}</NextMarker>"
                "</EnumerationResults>"
            ).encode()
            return 200, {"Content-Type": "application/xml"}, xml

        parts = parsed.path.lstrip("/").split("/", 1)
        blob_name = urllib.parse.unquote(parts[1]) if len(parts) == 2 else ""

        if method == "PUT":
            if self.next_put_status is not None:
                forced = self.next_put_status
                self.next_put_status = None
                return forced, {}, b""
            if copied_headers.get("If-None-Match") != "*":
                return 400, {"x-ms-error-code": "MissingRequiredHeader"}, b""
            if blob_name in self.blobs:
                return (
                    self.conflict_status,
                    {"x-ms-error-code": self.conflict_code},
                    b"",
                )
            self.blobs[blob_name] = body or b""
            return 201, self._worm_headers(blob_name), b""

        if method == "GET":
            if blob_name not in self.blobs:
                return 404, {"x-ms-error-code": "BlobNotFound"}, b""
            return 200, self._worm_headers(blob_name), self.blobs[blob_name]

        return 405, {}, b""


class LedgerDigestBlobTests(unittest.TestCase):
    def test_retention_lock_accepts_locked_worm_policy_and_disjoint_lifecycle(self) -> None:
        policy = {
            "properties": {
                "state": "Locked",
                "immutabilityPeriodSinceCreationInDays": 365,
                "allowProtectedAppendWrites": False,
            }
        }
        rep = verify_container_retention_lock(
            policy,
            container_properties={"properties": {"publicAccess": "None"}},
            lifecycle_prefixes=["staff-results/", "temp-exports/"],
            require_locked=True,
            min_retention_days=365,
        )
        self.assertTrue(rep["intact"])
        self.assertTrue(rep["locked"])
        self.assertEqual(rep["retention_days"], 365)
        self.assertEqual(rep["problems"], [])

    def test_retention_lock_prelock_bicep_posture_vs_runtime_locked_requirement(self) -> None:
        arm_put_policy: dict[str, Any] = {
            "immutabilityPeriodSinceCreationInDays": 365,
            "allowProtectedAppendWrites": False,
        }
        prelock = verify_container_retention_lock(arm_put_policy, require_locked=False)
        self.assertTrue(prelock["intact"])
        self.assertFalse(prelock["locked"])

        for bad_state in (None, "Unlocked", "Disabled"):
            candidate = dict(arm_put_policy)
            if bad_state is not None:
                candidate["state"] = bad_state
            runtime = verify_container_retention_lock(candidate, require_locked=True)
            self.assertFalse(runtime["intact"])
            self.assertFalse(runtime["locked"])
            self.assertIn("retention_policy_not_locked", runtime["problems"])

    def test_retention_lock_rejects_short_or_boolean_days_and_missing_policy(self) -> None:
        self.assertIn(
            "missing_immutability_policy",
            verify_container_retention_lock(None)["problems"],
        )
        self.assertIn(
            "missing_immutability_policy",
            verify_container_retention_lock({})["problems"],
        )
        for bad_days in (0, 364, True, "365", None):
            rep = verify_container_retention_lock(
                {
                    "state": "Locked",
                    "immutabilityPeriodSinceCreationInDays": bad_days,
                    "allowProtectedAppendWrites": False,
                },
                min_retention_days=365,
            )
            self.assertFalse(rep["intact"])
            self.assertIn("insufficient_retention_days", rep["problems"])

        with self.assertRaises(ValueError):
            verify_container_retention_lock(
                {
                    "state": "Locked",
                    "immutabilityPeriodSinceCreationInDays": 365,
                    "allowProtectedAppendWrites": False,
                },
                min_retention_days=0,
            )
        with self.assertRaises(ValueError):
            verify_container_retention_lock(
                {
                    "state": "Locked",
                    "immutabilityPeriodSinceCreationInDays": 365,
                    "allowProtectedAppendWrites": False,
                },
                min_retention_days=True,
            )

    def test_retention_lock_rejects_append_writes_and_mutually_exclusive_arm_flags(self) -> None:
        both_set = verify_container_retention_lock(
            {
                "state": "Locked",
                "immutabilityPeriodSinceCreationInDays": 365,
                "allowProtectedAppendWrites": False,
                "allowProtectedAppendWritesAll": False,
            }
        )
        self.assertFalse(both_set["intact"])
        self.assertIn("mutually_exclusive_append_write_flags", both_set["problems"])

        append_true = verify_container_retention_lock(
            {
                "state": "Locked",
                "immutabilityPeriodSinceCreationInDays": 365,
                "allowProtectedAppendWrites": True,
            }
        )
        self.assertFalse(append_true["intact"])
        self.assertIn("protected_append_writes_not_disabled", append_true["problems"])

        append_all_true = verify_container_retention_lock(
            {
                "state": "Locked",
                "immutabilityPeriodSinceCreationInDays": 365,
                "allowProtectedAppendWritesAll": True,
            }
        )
        self.assertFalse(append_all_true["intact"])
        self.assertIn("protected_append_writes_not_disabled", append_all_true["problems"])
        self.assertIn("protected_append_writes_all_enabled", append_all_true["problems"])

    def test_retention_lock_rejects_public_access_and_overlapping_lifecycle_prefixes(self) -> None:
        base_policy = {
            "state": "Locked",
            "immutabilityPeriodSinceCreationInDays": 365,
            "allowProtectedAppendWrites": False,
        }
        pub = verify_container_retention_lock(
            base_policy,
            container_properties={"publicAccess": "Blob", "hasImmutabilityPolicy": False},
        )
        self.assertFalse(pub["intact"])
        self.assertIn("container_public_access_enabled", pub["problems"])
        self.assertIn("container_missing_immutability_policy", pub["problems"])

        for bad_prefix in (
            "",
            "/",
            "ledger",
            "ledger-digests",
            "ledger-digests/",
            "ledger-digests/digest-",
            "digest-",
            "year-",
        ):
            rep = verify_container_retention_lock(
                base_policy,
                lifecycle_prefixes=["staff-results/", bad_prefix],
            )
            self.assertFalse(rep["intact"], msg=f"expected overlap for {bad_prefix!r}")
            self.assertIn("lifecycle_rule_overlaps_digest_container", rep["problems"])

    def test_blob_retention_headers_accept_locked_rfc1123_and_iso8601_future_dates(self) -> None:
        rfc_rep = verify_blob_retention_headers(
            {
                "X-MS-Immutability-Policy-Mode": "Locked",
                "X-MS-Immutability-Policy-Until-Date": LOCKED_UNTIL_RFC1123,
            },
            as_of=AS_OF_UTC,
            created_at=datetime(2026, 11, 15, 0, 0, 0, tzinfo=UTC),
            min_retention_days=365,
        )
        self.assertTrue(rfc_rep["intact"])
        self.assertTrue(rfc_rep["locked"])

        iso_rep = verify_blob_retention_headers(
            {
                "x-ms-immutability-policy-mode": "locked",
                "x-ms-immutability-policy-until-date": "2028-11-15T02:00:00Z",
            },
            as_of=AS_OF_UTC,
        )
        self.assertTrue(iso_rep["intact"])
        self.assertTrue(iso_rep["locked"])

    def test_blob_retention_headers_reject_unlocked_missing_naive_expired_or_short_until(
        self,
    ) -> None:
        unlocked = verify_blob_retention_headers(
            {
                "x-ms-immutability-policy-mode": "unlocked",
                "x-ms-immutability-policy-until-date": LOCKED_UNTIL_RFC1123,
            },
            as_of=AS_OF_UTC,
        )
        self.assertFalse(unlocked["intact"])
        self.assertIn("blob_immutability_mode_not_locked", unlocked["problems"])

        naive = verify_blob_retention_headers(
            {
                "x-ms-immutability-policy-mode": "locked",
                "x-ms-immutability-policy-until-date": "2028-11-15T02:00:00",
            },
            as_of=AS_OF_UTC,
        )
        self.assertFalse(naive["intact"])
        self.assertIn("invalid_blob_immutability_until_date", naive["problems"])

        expired = verify_blob_retention_headers(
            {
                "x-ms-immutability-policy-mode": "locked",
                "x-ms-immutability-policy-until-date": "2026-11-15T02:00:00Z",
            },
            as_of=AS_OF_UTC,
        )
        self.assertFalse(expired["intact"])
        self.assertIn("blob_immutability_expired", expired["problems"])

        short = verify_blob_retention_headers(
            {
                "x-ms-immutability-policy-mode": "locked",
                "x-ms-immutability-policy-until-date": "2027-06-01T00:00:00Z",
            },
            as_of=AS_OF_UTC,
            created_at=AS_OF_UTC,
            min_retention_days=365,
        )
        self.assertFalse(short["intact"])
        self.assertIn("blob_immutability_shorter_than_minimum", short["problems"])

    def test_store_rejects_insecure_url_invalid_container_and_path_traversal_without_secret_leak(
        self,
    ) -> None:
        transport = _FakeImmutableBlobTransport()
        with self.assertRaises(LedgerDigestBlobError) as insecure_ctx:
            BlobLedgerDigestStore(
                "http://stzavasecretacct.blob.core.windows.net",
                DEFAULT_CONTAINER,
                sas=SECRET_SAS,
                transport=transport,
            )
        self.assertNotIn("stzavasecretacct", str(insecure_ctx.exception))
        self.assertNotIn("SUPERSECRET", str(insecure_ctx.exception))

        for bad_container in ("UPPERCASE", "bad--container", "-leading", "ab"):
            with self.assertRaises(LedgerDigestBlobError):
                BlobLedgerDigestStore(
                    ACCOUNT_URL, bad_container, sas=SECRET_SAS, transport=transport
                )

        store = BlobLedgerDigestStore(
            ACCOUNT_URL,
            DEFAULT_CONTAINER,
            sas=SECRET_SAS,
            transport=transport,
        )
        for bad_name in (
            "../digest-0000000001.json",
            "nested/digest-0000000001.json",
            "digest-1.json",
            "year-0000.json",
        ):
            with self.assertRaises(InvalidDigestAnchorError):
                store.read_anchor(bad_name)

    def test_store_create_anchor_enforces_if_none_match_and_idempotent_readback(self) -> None:
        for conflict_status, conflict_code in (
            (409, "BlobAlreadyExists"),
            (409, "BlobImmutableDueToPolicy"),
            (412, "ConditionNotMet"),
        ):
            transport = _FakeImmutableBlobTransport(
                conflict_status=conflict_status,
                conflict_code=conflict_code,
            )
            blob = BlobLedgerDigestStore(
                ACCOUNT_URL,
                DEFAULT_CONTAINER,
                sas=SECRET_SAS,
                transport=transport,
            )
            self.assertFalse(hasattr(blob, "delete"))
            self.assertFalse(hasattr(blob, "overwrite"))

            first = {
                "chain": "main",
                "algorithm": "sha256",
                "count": 1,
                "head": "a" * 64,
                "at": "2026-11-15T01:00:00+00:00",
            }
            retry = dict(first, at="2026-11-15T02:00:00+00:00")
            self.assertTrue(blob.create_anchor("digest-0000000001.json", first))
            self.assertEqual(transport.calls[0][2].get("If-None-Match"), "*")
            self.assertEqual(transport.calls[0][2].get("x-ms-blob-type"), "BlockBlob")
            self.assertFalse(blob.create_anchor("digest-0000000001.json", retry))

    def test_store_create_anchor_refuses_divergent_existing_remote_anchor_and_uncertain_5xx(
        self,
    ) -> None:
        transport = _FakeImmutableBlobTransport()
        blob = BlobLedgerDigestStore(
            ACCOUNT_URL,
            DEFAULT_CONTAINER,
            sas=SECRET_SAS,
            transport=transport,
        )
        original = {
            "chain": "main",
            "algorithm": "sha256",
            "count": 1,
            "head": "a" * 64,
            "at": "2026-11-15T01:00:00+00:00",
        }
        divergent = dict(original, head="b" * 64)
        self.assertTrue(blob.create_anchor("digest-0000000001.json", original))
        with self.assertRaises(LedgerDigestBlobError):
            blob.create_anchor("digest-0000000001.json", divergent)

        transport.next_put_status = 503
        with self.assertRaises(LedgerDigestBlobUncertain):
            blob.create_anchor(
                "digest-0000000002.json",
                dict(original, count=2),
            )

        transport.raise_on_method = "PUT"
        with self.assertRaises(LedgerDigestBlobUncertain) as err_ctx:
            blob.create_anchor(
                "digest-0000000003.json",
                dict(original, count=3),
            )
        self.assertNotIn("SUPERSECRET", str(err_ctx.exception))
        self.assertNotIn("stzavasecretacct", str(err_ctx.exception))

    def test_store_list_names_paginates_and_rejects_malformed_xml(self) -> None:
        transport = _FakeImmutableBlobTransport(page_size=1)
        blob = BlobLedgerDigestStore(
            ACCOUNT_URL,
            DEFAULT_CONTAINER,
            sas=SECRET_SAS,
            transport=transport,
        )
        for idx in (3, 1, 2):
            blob.create_anchor(
                f"digest-{idx:010d}.json",
                {
                    "chain": "main",
                    "algorithm": "sha256",
                    "count": idx,
                    "head": f"{idx:064x}",
                    "at": "2026-11-15T01:00:00+00:00",
                },
            )
        self.assertEqual(
            blob.list_names(),
            [
                "digest-0000000001.json",
                "digest-0000000002.json",
                "digest-0000000003.json",
            ],
        )

        def bad_xml_transport(
            method: str,
            url: str,
            headers: Mapping[str, str],
            body: bytes | None = None,
        ) -> tuple[int, Mapping[str, str], bytes]:
            return 200, {}, b"<UnexpectedRoot/>"

        bad_blob = BlobLedgerDigestStore(
            ACCOUNT_URL,
            DEFAULT_CONTAINER,
            sas=SECRET_SAS,
            transport=bad_xml_transport,
        )
        with self.assertRaises(LedgerDigestBlobError):
            bad_blob.list_names()

    def test_publish_and_verify_intact_multi_year_chain_with_retention_lock(self) -> None:
        entries = _sample_chain()
        transport = _FakeImmutableBlobTransport()
        blob = BlobLedgerDigestStore(
            ACCOUNT_URL,
            DEFAULT_CONTAINER,
            sas=SECRET_SAS,
            transport=transport,
        )
        uploaded = publish_ledger_digests(
            entries,
            blob,
            before_year=2026,
            published_at="2026-11-15T02:00:00+00:00",
        )
        self.assertEqual(
            uploaded,
            ["digest-0000000004.json", "year-2024.json", "year-2025.json"],
        )
        self.assertEqual(
            publish_ledger_digests(entries, blob, before_year=2026),
            [],
        )

        rep = verify_ledger_digests(
            entries,
            blob,
            require_retention_lock=True,
            require_current_head=True,
            retention_policy={
                "state": "Locked",
                "immutabilityPeriodSinceCreationInDays": 365,
                "allowProtectedAppendWrites": False,
            },
            container_properties={"publicAccess": "None"},
            lifecycle_prefixes=["staff-results/"],
            as_of=AS_OF_UTC,
        )
        self.assertTrue(rep["intact"])
        self.assertTrue(rep["retention_lock_verified"])
        self.assertEqual(rep["digests"], 1)
        self.assertEqual(rep["year_digests"], 2)
        self.assertEqual(rep["entries"], 4)

    def test_publish_refuses_to_anchor_broken_local_chain(self) -> None:
        entries = _sample_chain()
        entries[1] = dict(entries[1], detail={"step": 999})
        transport = _FakeImmutableBlobTransport()
        blob = BlobLedgerDigestStore(
            ACCOUNT_URL,
            DEFAULT_CONTAINER,
            sas=SECRET_SAS,
            transport=transport,
        )
        self.assertEqual(publish_ledger_digests(entries, blob, before_year=2026), [])
        self.assertEqual(transport.blobs, {})

    def test_verify_detects_mutated_entry_truncation_year_mismatch_and_missing_anchors(
        self,
    ) -> None:
        entries = _sample_chain()
        empty_transport = _FakeImmutableBlobTransport()
        empty_blob = BlobLedgerDigestStore(
            ACCOUNT_URL,
            DEFAULT_CONTAINER,
            sas=SECRET_SAS,
            transport=empty_transport,
        )
        empty_rep = verify_ledger_digests(entries, empty_blob)
        self.assertFalse(empty_rep["intact"])

        transport = _FakeImmutableBlobTransport()
        blob = BlobLedgerDigestStore(
            ACCOUNT_URL,
            DEFAULT_CONTAINER,
            sas=SECRET_SAS,
            transport=transport,
        )
        publish_ledger_digests(entries, blob, before_year=2026)

        mutated = [dict(e) for e in entries]
        mutated[2]["detail"] = {"tampered": True}
        self.assertFalse(verify_ledger_digests(mutated, blob)["intact"])

        truncated = entries[:3]
        trunc_rep = verify_ledger_digests(truncated, blob)
        self.assertFalse(trunc_rep["intact"])
        self.assertTrue(any(p["check"] == "chain" for p in trunc_rep["problems"]))

        missing_year_entries = entries[1:]
        year_rep = verify_ledger_digests(missing_year_entries, blob)
        self.assertFalse(year_rep["intact"])
        self.assertTrue(any(p["check"] == "years" for p in year_rep["problems"]))

    def test_verify_detects_corrupt_remote_anchor_stale_current_head_and_unlocked_blob_headers(
        self,
    ) -> None:
        entries = _sample_chain()
        transport = _FakeImmutableBlobTransport()
        blob = BlobLedgerDigestStore(
            ACCOUNT_URL,
            DEFAULT_CONTAINER,
            sas=SECRET_SAS,
            transport=transport,
        )
        publish_ledger_digests(entries[:3], blob, before_year=2026)

        stale = verify_ledger_digests(entries, blob, require_current_head=True)
        self.assertFalse(stale["intact"])
        self.assertTrue(any(p["check"] == "current_head" for p in stale["problems"]))

        transport.immutability_mode = "unlocked"
        unlocked_rep = verify_ledger_digests(
            entries[:3],
            blob,
            require_retention_lock=True,
            as_of=AS_OF_UTC,
        )
        self.assertFalse(unlocked_rep["intact"])
        self.assertFalse(unlocked_rep["retention_lock_verified"])
        self.assertTrue(any(p["check"] == "retention_headers" for p in unlocked_rep["problems"]))

        transport.immutability_mode = "locked"
        transport.blobs["digest-malformed.json"] = b"{}"
        transport.blobs["digest-0000000099.json"] = b"not-json"
        corrupt_rep = verify_ledger_digests(entries[:3], blob)
        self.assertFalse(corrupt_rep["intact"])
        self.assertGreaterEqual(
            sum(1 for p in corrupt_rep["problems"] if p["check"] == "digests"),
            2,
        )

    def test_reconcile_ledger_digests_validates_independent_record_and_retention_headers(
        self,
    ) -> None:
        entries = _sample_chain()
        transport = _FakeImmutableBlobTransport()
        blob = BlobLedgerDigestStore(
            ACCOUNT_URL,
            DEFAULT_CONTAINER,
            sas=SECRET_SAS,
            transport=transport,
        )
        publish_ledger_digests(entries, blob, before_year=2026)
        record = {
            name: json.loads(raw.decode("utf-8"))["head"] for name, raw in transport.blobs.items()
        }

        ok_rep = reconcile_ledger_digests(
            blob,
            record,
            require_retention_lock=True,
            as_of=AS_OF_UTC,
        )
        self.assertTrue(ok_rep["intact"])
        self.assertEqual(ok_rep["compared"], 3)

        mismatched = dict(record)
        mismatched["digest-0000000004.json"] = "f" * 64
        mismatched["digest-0000000099.json"] = "e" * 64
        bad_rep = reconcile_ledger_digests(blob, mismatched)
        self.assertFalse(bad_rep["intact"])

        transport.immutability_mode = "unlocked"
        unlocked_rec = reconcile_ledger_digests(
            blob,
            record,
            require_retention_lock=True,
            as_of=AS_OF_UTC,
        )
        self.assertFalse(unlocked_rec["intact"])

        with self.assertRaises(InvalidDigestAnchorError):
            reconcile_ledger_digests(blob, {"bad-name.json": "a" * 64})

    def test_scheduled_verification_emits_ok_only_when_intact_and_sanitized_alert_on_mismatch(
        self,
    ) -> None:
        entries = _sample_chain()
        transport = _FakeImmutableBlobTransport()
        blob = BlobLedgerDigestStore(
            ACCOUNT_URL,
            DEFAULT_CONTAINER,
            sas=SECRET_SAS,
            transport=transport,
        )

        ok_lines: list[str] = []
        ok_outcome = run_scheduled_verification(
            entries,
            blob,
            publish=True,
            before_year=2026,
            require_retention_lock=True,
            as_of=AS_OF_UTC,
            out=ok_lines.append,
        )
        self.assertEqual(ok_outcome["exit_code"], 0)
        self.assertEqual(ok_outcome["marker"], OK_MARKER)
        self.assertEqual(ok_outcome["runbook"], MISSING_RUNBOOK)
        self.assertEqual(ok_outcome["proposed_owner"], PROPOSED_OWNER)
        self.assertEqual(len(ok_lines), 1)
        self.assertIn(OK_MARKER, ok_lines[0])
        self.assertNotIn(ALERT_MARKER, ok_lines[0])

        tampered = [dict(e) for e in entries]
        tampered[-1]["detail"] = {"rewritten": 1}
        alert_lines: list[str] = []
        bad_outcome = run_scheduled_verification(
            tampered,
            blob,
            publish=False,
            require_retention_lock=True,
            as_of=AS_OF_UTC,
            out=alert_lines.append,
        )
        self.assertEqual(bad_outcome["exit_code"], 1)
        self.assertEqual(bad_outcome["marker"], ALERT_MARKER)
        self.assertEqual(bad_outcome["runbook"], MISMATCH_RUNBOOK)
        self.assertEqual(bad_outcome["proposed_owner"], PROPOSED_OWNER)
        self.assertEqual(bad_outcome["diagnostic"]["status"], "breach")
        self.assertEqual(len(alert_lines), 1)
        self.assertIn(ALERT_MARKER, alert_lines[0])
        self.assertNotIn(OK_MARKER, alert_lines[0])

        transport.raise_on_method = "GET"
        fault_lines: list[str] = []
        fault_outcome = run_scheduled_verification(
            entries,
            blob,
            out=fault_lines.append,
        )
        self.assertEqual(fault_outcome["exit_code"], 1)
        self.assertIn(ALERT_MARKER, fault_lines[0])
        self.assertNotIn(OK_MARKER, fault_lines[0])
        self.assertNotIn("SUPERSECRET", fault_lines[0])
        self.assertNotIn("stzavasecretacct", fault_lines[0])

    def test_scheduled_verification_alerts_sanitized_on_unexpected_exception(self) -> None:
        class _ExplodingStore(BlobLedgerDigestStore):
            def list_names(self) -> list[str]:
                raise ValueError(f"unexpected failure for {ACCOUNT_URL}?{SECRET_SAS}")

        blob = _ExplodingStore(
            ACCOUNT_URL,
            DEFAULT_CONTAINER,
            sas=SECRET_SAS,
            transport=_FakeImmutableBlobTransport(),
        )
        lines: list[str] = []
        outcome = run_scheduled_verification(_sample_chain(), blob, out=lines.append)

        self.assertEqual(outcome["exit_code"], 1)
        self.assertIs(outcome["intact"], False)
        self.assertEqual(outcome["marker"], ALERT_MARKER)
        self.assertEqual(outcome["diagnostic"]["status"], "blocked")
        self.assertIsNone(outcome["report"])
        self.assertEqual(len(lines), 1)
        self.assertIn(ALERT_MARKER, lines[0])
        self.assertIn("unexpected_verification_error", lines[0])
        self.assertNotIn(OK_MARKER, lines[0])
        self.assertNotIn("SUPERSECRET", lines[0])
        self.assertNotIn("stzavasecretacct", lines[0])

    def test_cli_main_alerts_on_missing_or_invalid_env_and_supports_publish_and_reconcile(
        self,
    ) -> None:
        unconfigured_lines: list[str] = []
        self.assertEqual(main(argv=[], env={}, out=unconfigured_lines.append), 1)
        self.assertTrue(any(ALERT_MARKER in line for line in unconfigured_lines))
        self.assertFalse(any(OK_MARKER in line for line in unconfigured_lines))

        bad_env_lines: list[str] = []
        self.assertEqual(
            main(
                argv=[],
                env={
                    ACCOUNT_URL_VAR: ACCOUNT_URL,
                    REQUIRE_LOCK_VAR: "not-a-bool",
                    MIN_RETENTION_DAYS_VAR: "0",
                },
                out=bad_env_lines.append,
            ),
            1,
        )
        self.assertTrue(any(ALERT_MARKER in line for line in bad_env_lines))

        with tempfile.TemporaryDirectory() as tmp:
            data_path = Path(tmp) / "zf.json"
            data_path.write_text(json.dumps({"cases": [], "staff": []}), encoding="utf-8")
            store = Store(str(data_path))
            store.audit("u-1", "case.created", "CASE-100", {"note": "synthetic"})
            transport = _FakeImmutableBlobTransport()
            env = {
                ACCOUNT_URL_VAR: ACCOUNT_URL,
                CONTAINER_VAR: DEFAULT_CONTAINER,
                SAS_VAR: SECRET_SAS,
                REQUIRE_LOCK_VAR: "true",
            }
            blob = open_ledger_digest_store(env, transport=transport)
            self.assertIsNotNone(blob)

            pub_lines: list[str] = []
            rc = main(
                argv=["--publish"],
                env=env,
                store=store,
                blob=blob,
                out=pub_lines.append,
            )
            self.assertEqual(rc, 0)
            self.assertTrue(any(OK_MARKER in line for line in pub_lines))

            rec_file = Path(tmp) / "record.json"
            record = {
                name: json.loads(raw.decode("utf-8"))["head"]
                for name, raw in transport.blobs.items()
            }
            rec_file.write_text(json.dumps(record), encoding="utf-8")
            rec_ok_lines: list[str] = []
            self.assertEqual(
                main(
                    argv=["--reconcile", str(rec_file)],
                    env=env,
                    blob=blob,
                    out=rec_ok_lines.append,
                ),
                0,
            )
            self.assertTrue(any(RECONCILE_OK_MARKER in line for line in rec_ok_lines))

            rec_file.write_text(
                json.dumps({"digest-0000000001.json": "0" * 64}),
                encoding="utf-8",
            )
            rec_bad_lines: list[str] = []
            self.assertEqual(
                main(
                    argv=["--reconcile", str(rec_file)],
                    env=env,
                    blob=blob,
                    out=rec_bad_lines.append,
                ),
                1,
            )
            self.assertTrue(any(RECONCILE_ALERT_MARKER in line for line in rec_bad_lines))
            self.assertEqual(main(argv=["--reconcile"], env=env, out=lambda _: None), 2)

    def test_container_retention_lock_immutable_versioning_and_human_gates(self) -> None:
        policy = {
            "state": "Locked",
            "immutabilityPeriodSinceCreationInDays": 365,
            "allowProtectedAppendWrites": False,
        }
        for bad_container in (
            None,
            {"publicAccess": "None"},
            {"publicAccess": "None", "immutableStorageWithVersioning": {"enabled": False}},
        ):
            rep = verify_container_retention_lock(
                policy,
                container_properties=bad_container,
                require_immutable_versioning=True,
            )
            self.assertFalse(rep["intact"])
            self.assertIn("immutable_storage_with_versioning_disabled", rep["problems"])

        ok_rep = verify_container_retention_lock(
            policy,
            container_properties={
                "publicAccess": "None",
                "immutableStorageWithVersioning": {"enabled": True},
            },
            require_immutable_versioning=True,
        )
        self.assertTrue(ok_rep["intact"])
        self.assertEqual(ok_rep["immutability_policy_state"], "Locked")
        self.assertIs(ok_rep["live_worm_lock_human_gated"], True)
        self.assertIs(ok_rep["retention_schedule_human_gated"], True)
        absent_rep = verify_container_retention_lock(None)
        self.assertEqual(absent_rep["immutability_policy_state"], "Absent")

    def test_blob_retention_headers_creation_time_and_minimum_retention_days(self) -> None:
        headers = {
            "x-ms-immutability-policy-mode": "locked",
            "x-ms-immutability-policy-until-date": LOCKED_UNTIL_RFC1123,
            "x-ms-creation-time": "Sun, 15 Nov 2026 02:00:00 GMT",
        }
        ok = verify_blob_retention_headers(headers, as_of=AS_OF_UTC, min_retention_days=365)
        self.assertTrue(ok["intact"])
        self.assertTrue(ok["locked"])
        self.assertEqual(ok["immutability_policy_state"], "Locked")
        self.assertEqual(ok["retention_days"], 731)

        short = verify_blob_retention_headers(headers, as_of=AS_OF_UTC, min_retention_days=800)
        self.assertFalse(short["intact"])
        self.assertFalse(short["locked"])
        self.assertIn("blob_immutability_shorter_than_minimum", short["problems"])

        bad_created = verify_blob_retention_headers(
            {**headers, "x-ms-creation-time": "not-a-date"},
            as_of=AS_OF_UTC,
        )
        self.assertFalse(bad_created["intact"])
        self.assertIn("invalid_blob_creation_time", bad_created["problems"])

    def test_publish_enforces_fail_closed_retention_lock_and_records_posture(self) -> None:
        entries = _sample_chain()
        for mode, expected_state in (("unlocked", "Unlocked"), (None, "Absent")):
            transport = _FakeImmutableBlobTransport(
                immutability_mode=mode,
                immutability_until=LOCKED_UNTIL_RFC1123 if mode else None,
            )
            blob = BlobLedgerDigestStore(
                ACCOUNT_URL,
                DEFAULT_CONTAINER,
                sas=SECRET_SAS,
                transport=transport,
            )
            with self.assertRaises(LedgerDigestBlobError):
                publish_ledger_digests(
                    entries,
                    blob,
                    before_year=2026,
                    require_retention_lock=True,
                    as_of=AS_OF_UTC,
                )
            put_calls = [c for c in transport.calls if c[0] == "PUT"]
            self.assertEqual(len(put_calls), 1)
            self.assertIsNotNone(blob.last_immutability_posture)
            assert blob.last_immutability_posture is not None
            self.assertEqual(
                blob.last_immutability_posture["immutability_policy_state"],
                expected_state,
            )
            self.assertFalse(blob.last_immutability_posture["locked"])

        locked_transport = _FakeImmutableBlobTransport()
        locked_blob = BlobLedgerDigestStore(
            ACCOUNT_URL,
            DEFAULT_CONTAINER,
            sas=SECRET_SAS,
            transport=locked_transport,
        )
        pub_result = publish_ledger_digests_with_posture(
            entries,
            locked_blob,
            before_year=2026,
            require_retention_lock=True,
            min_retention_days=365,
            as_of=AS_OF_UTC,
        )
        self.assertEqual(
            pub_result["uploaded"],
            ["digest-0000000004.json", "year-2024.json", "year-2025.json"],
        )
        self.assertEqual(pub_result["immutability_policy_state"], "Locked")
        self.assertTrue(pub_result["locked"])
        self.assertEqual(pub_result["retention_days"], 731)
        posture = pub_result["immutability_posture"]
        self.assertTrue(posture["live_worm_lock_human_gated"])
        self.assertTrue(posture["retention_schedule_human_gated"])

    def test_weakest_link_posture_decoupled_locked_and_sanitized_traceback(self) -> None:
        entries = _sample_chain()
        transport = _FakeImmutableBlobTransport()
        blob = BlobLedgerDigestStore(
            ACCOUNT_URL,
            DEFAULT_CONTAINER,
            sas=SECRET_SAS,
            transport=transport,
        )
        publish_ledger_digests(
            entries,
            blob,
            before_year=2026,
            require_retention_lock=True,
            as_of=AS_OF_UTC,
        )
        transport.per_blob_headers["year-2024.json"] = {
            "x-ms-immutability-policy-mode": "unlocked",
            "x-ms-immutability-policy-until-date": LOCKED_UNTIL_RFC1123,
            "x-ms-creation-time": "Sun, 15 Nov 2026 02:00:00 GMT",
        }
        advisory = verify_ledger_digests(
            entries,
            blob,
            require_retention_lock=False,
            as_of=AS_OF_UTC,
        )
        self.assertTrue(advisory["intact"])
        self.assertFalse(advisory["locked"])
        self.assertEqual(advisory["immutability_policy_state"], "Unlocked")

        enforced = verify_ledger_digests(
            entries,
            blob,
            require_retention_lock=True,
            as_of=AS_OF_UTC,
        )
        self.assertFalse(enforced["intact"])
        self.assertFalse(enforced["locked"])
        self.assertFalse(enforced["retention_lock_verified"])
        self.assertEqual(enforced["immutability_policy_state"], "Unlocked")

        transport.per_blob_headers.clear()
        tampered = [dict(e) for e in entries]
        tampered[-1]["detail"] = {"rewritten": 1}
        mismatch_rep = verify_ledger_digests(
            tampered,
            blob,
            require_retention_lock=True,
            as_of=AS_OF_UTC,
        )
        self.assertFalse(mismatch_rep["intact"])
        self.assertTrue(mismatch_rep["locked"])
        self.assertEqual(mismatch_rep["immutability_policy_state"], "Locked")

        lines: list[str] = []
        outcome = run_scheduled_verification(
            tampered,
            blob,
            publish=False,
            require_retention_lock=True,
            as_of=AS_OF_UTC,
            out=lines.append,
        )
        self.assertEqual(outcome["exit_code"], 1)
        self.assertEqual(outcome["immutability_policy_state"], "Locked")
        self.assertIs(outcome["locked"], True)
        self.assertEqual(outcome["retention_days"], 731)
        self.assertIs(outcome["immutability_posture"]["live_worm_lock_human_gated"], True)
        self.assertIs(outcome["immutability_posture"]["retention_schedule_human_gated"], True)
        payload = json.loads(lines[0].split(" ", 2)[2])
        self.assertEqual(payload["status"], "breach")

        transport.raise_on_method = "GET"
        with self.assertRaises(LedgerDigestBlobError) as ctx:
            blob.list_names()
        self.assertIsNone(ctx.exception.__cause__)
        self.assertTrue(ctx.exception.__suppress_context__)
        rendered_tb = "".join(traceback.format_exception(ctx.exception))
        self.assertNotIn("SUPERSECRET", rendered_tb)
        self.assertNotIn("stzavasecretacct", rendered_tb)

        transport.raise_on_method = "PUT"
        with self.assertRaises(LedgerDigestBlobUncertain) as put_ctx:
            blob.create_anchor(
                "digest-0000000099.json",
                ledger.make_digest(99, "a" * 64),
            )
        self.assertIsNone(put_ctx.exception.__cause__)
        self.assertTrue(put_ctx.exception.__suppress_context__)
        put_tb = "".join(traceback.format_exception(put_ctx.exception))
        self.assertNotIn("SUPERSECRET", put_tb)
        self.assertNotIn("stzavasecretacct", put_tb)


if __name__ == "__main__":
    unittest.main()
