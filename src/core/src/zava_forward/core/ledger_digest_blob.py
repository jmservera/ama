"""Immutable Azure Blob ledger digest verification, create-only anchoring, and scheduled alerting.

Provides pure, deterministic checks for Azure Storage container time-based retention locks
(ARM immutabilityPolicies and Blob response headers), create-only publication and read-back
verification of hash-chained ledger head and sealed-year digests, and sanitized console alert
emission compatible with Azure Container Apps scheduled log alerts.

Errors never embed storage account URLs, SAS credentials, bearer tokens, or driver strings.
"""

from __future__ import annotations

import email.utils
import json
import os
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, datetime, timedelta
from typing import Any

from zava_forward.core import ledger
from zava_forward.core.documents import AzureBlobDocumentStore
from zava_forward.core.monitoring_coverage import (
    BLOCKED,
    BREACH,
    DIGITAL,
    WITHIN,
    sanitize_diagnostic,
)

ACCOUNT_URL_VAR = "ZF_DIGEST_ACCOUNT_URL"
CONTAINER_VAR = "ZF_DIGEST_CONTAINER"
CLIENT_ID_VAR = "ZF_DIGEST_CLIENT_ID"
SAS_VAR = "ZF_DIGEST_SAS"
DIGEST_DIR_VAR = "ZF_DIGEST_DIR"
REQUIRE_LOCK_VAR = "ZF_DIGEST_REQUIRE_RETENTION_LOCK"
MIN_RETENTION_DAYS_VAR = "ZF_DIGEST_MIN_RETENTION_DAYS"

DEFAULT_CONTAINER = "ledger-digests"
DEFAULT_MIN_RETENTION_DAYS = 365

ALERT_MARKER = "LEDGER_DIGEST_ALERT"
OK_MARKER = "LEDGER_DIGEST_OK"
RECONCILE_OK_MARKER = "LEDGER_DIGEST_RECONCILE_OK"
RECONCILE_ALERT_MARKER = "LEDGER_DIGEST_RECONCILE_ALERT"

MISMATCH_RUNBOOK = "ledger-digest-mismatch"
MISSING_RUNBOOK = "ledger-verify-missing"
PROPOSED_OWNER = DIGITAL
VERIFICATION_TASK = "ledger-verify"

_CONTAINER_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{1,61}[a-z0-9])?$")
_ANCHOR_NAME_RE = re.compile(
    r"^(?:digest-(?:[0-9]{10}|[1-9][0-9]{10,})|year-(?!0000)[0-9]{4})\.json$"
)
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_YEAR_RE = re.compile(r"^[0-9]{4}$")
_MAX_PAGES = 1000

Transport = Callable[..., tuple[int, Mapping[str, str], bytes]]
OutputSink = Callable[[str], object]


class LedgerDigestBlobError(RuntimeError):
    """Deterministic configuration, policy, transport, listing, or digest anchor failure."""


class LedgerDigestBlobUncertain(LedgerDigestBlobError):
    """A conditional create request was dispatched and its remote outcome is unknown."""


class InvalidDigestAnchorError(LedgerDigestBlobError):
    """Remote or supplied digest bytes cannot serve as valid anchor evidence."""


def valid_container_name(container: str) -> bool:
    """Return True when container satisfies Azure Blob DNS-safe naming rules."""
    return bool(
        isinstance(container, str)
        and "--" not in container
        and _CONTAINER_RE.fullmatch(container) is not None
    )


def valid_anchor_name(name: str) -> bool:
    """Return True when name is a canonical root head or sealed-year digest blob name."""
    return isinstance(name, str) and _ANCHOR_NAME_RE.fullmatch(name) is not None


def valid_anchor(name: str, digest: Mapping[str, Any] | Any) -> bool:
    """Return True when digest matches the canonical schema for anchor blob name."""
    if not valid_anchor_name(name) or not isinstance(digest, Mapping):
        return False
    count = digest.get("count")
    head = digest.get("head")
    if (
        digest.get("chain") != "main"
        or digest.get("algorithm") != "sha256"
        or type(count) is not int
        or count < 0
        or not isinstance(head, str)
        or _SHA256_RE.fullmatch(head) is None
    ):
        return False
    if name.startswith("digest-"):
        return name == f"digest-{count:010d}.json" and (count != 0 or head == ledger.GENESIS)
    year = digest.get("year")
    first_prev = digest.get("first_prev")
    return (
        isinstance(year, str)
        and _YEAR_RE.fullmatch(year) is not None
        and year != "0000"
        and name == f"year-{year}.json"
        and count > 0
        and isinstance(first_prev, str)
        and _SHA256_RE.fullmatch(first_prev) is not None
    )


def logical_anchor_equal(
    name: str,
    expected: Mapping[str, Any],
    actual: Mapping[str, Any],
) -> bool:
    """Compare immutable logical anchor fields while ignoring volatile publication timestamps."""
    if not valid_anchor(name, expected) or not valid_anchor(name, actual):
        return False
    keys: tuple[str, ...] = ("chain", "algorithm", "count", "head")
    if name.startswith("year-"):
        keys = (*keys, "year", "first_prev")
    return all(expected.get(k) == actual.get(k) for k in keys)


def _header(headers: Mapping[str, str], target: str) -> str | None:
    lowered = target.lower()
    for key, value in headers.items():
        if key.lower() == lowered:
            return value
    return None


def _ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")
    return value.astimezone(UTC)


def _parse_utc_timestamp(raw: str) -> datetime | None:
    text = raw.strip()
    if not text:
        return None
    try:
        iso_candidate = text[:-1] + "+00:00" if text.endswith("Z") else text
        parsed_iso = datetime.fromisoformat(iso_candidate)
        if parsed_iso.tzinfo is not None and parsed_iso.utcoffset() is not None:
            return parsed_iso.astimezone(UTC)
    except ValueError:
        pass
    try:
        parsed_http = email.utils.parsedate_to_datetime(text)
    except (TypeError, ValueError):
        return None
    if parsed_http.tzinfo is None or parsed_http.utcoffset() is None:
        return None
    return parsed_http.astimezone(UTC)


def _unwrap_arm_properties(resource_or_props: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = resource_or_props.get("properties")
    if isinstance(nested, Mapping):
        return nested
    return resource_or_props


def verify_container_retention_lock(
    policy: Mapping[str, Any] | None,
    *,
    container_properties: Mapping[str, Any] | None = None,
    lifecycle_prefixes: Sequence[str] = (),
    container_name: str = DEFAULT_CONTAINER,
    require_locked: bool = True,
    require_immutable_versioning: bool = False,
    min_retention_days: int = DEFAULT_MIN_RETENTION_DAYS,
) -> dict[str, Any]:
    """Validate container immutability policy, public access, and lifecycle deletion rules.

    Accepts either an ARM resource dictionary containing ``properties`` or a direct properties
    mapping. When ``require_locked`` is True (runtime verification posture), ``state`` must equal
    ``"Locked"``. When ``require_locked`` is False (pre-lock ARM template inspection posture, since
    ARM PUT creates time-based WORM policies in ``Unlocked`` state before ``lockImmutabilityPolicy``
    is run), an omitted or ``"Unlocked"`` state is accepted while ``locked`` accurately reports
    False.
    """
    if type(min_retention_days) is not int or min_retention_days < 1:
        raise ValueError("min_retention_days must be a positive integer")
    if not valid_container_name(container_name):
        raise ValueError("container_name is not a valid Blob container name")

    problems: list[str] = []

    if container_properties is not None:
        cprops = _unwrap_arm_properties(container_properties)
        public_access = cprops.get("publicAccess")
        if public_access not in (None, "None"):
            problems.append("container_public_access_enabled")
        if cprops.get("hasImmutabilityPolicy") is False:
            problems.append("container_missing_immutability_policy")
        versioning_cfg = cprops.get("immutableStorageWithVersioning")
        if require_immutable_versioning:
            if not isinstance(versioning_cfg, Mapping) or versioning_cfg.get("enabled") is not True:
                problems.append("immutable_storage_with_versioning_disabled")
        elif versioning_cfg is not None and (
            not isinstance(versioning_cfg, Mapping) or versioning_cfg.get("enabled") is False
        ):
            problems.append("immutable_storage_with_versioning_disabled")
    elif require_immutable_versioning:
        problems.append("immutable_storage_with_versioning_disabled")

    props: Mapping[str, Any] | None = None
    if isinstance(policy, Mapping):
        props = _unwrap_arm_properties(policy)

    state: Any = None
    days: Any = None
    locked = False
    immutability_policy_state = "Absent"

    if props is None or len(props) == 0:
        problems.append("missing_immutability_policy")
    else:
        state = props.get("state")
        locked = state == "Locked"
        if state is None or state == "Unlocked":
            immutability_policy_state = "Unlocked"
        elif state == "Locked":
            immutability_policy_state = "Locked"
        elif isinstance(state, str) and state.strip():
            immutability_policy_state = state.strip()
        else:
            immutability_policy_state = "Invalid"

        if require_locked:
            if state != "Locked":
                problems.append("retention_policy_not_locked")
        elif state is not None and state not in ("Unlocked", "Locked"):
            problems.append("invalid_retention_policy_state")

        days = props.get("immutabilityPeriodSinceCreationInDays")
        if type(days) is not int or days < min_retention_days:
            problems.append("insufficient_retention_days")

        has_append = (
            "allowProtectedAppendWrites" in props
            and props["allowProtectedAppendWrites"] is not None
        )
        has_append_all = (
            "allowProtectedAppendWritesAll" in props
            and props["allowProtectedAppendWritesAll"] is not None
        )
        if has_append and has_append_all:
            problems.append("mutually_exclusive_append_write_flags")
        if props.get("allowProtectedAppendWrites") is not False:
            problems.append("protected_append_writes_not_disabled")
        if props.get("allowProtectedAppendWritesAll") not in (None, False):
            problems.append("protected_append_writes_all_enabled")

    target_root = f"{container_name}/"
    overlapping_prefixes: list[str] = []
    for raw_prefix in lifecycle_prefixes:
        if not isinstance(raw_prefix, str):
            overlapping_prefixes.append("<non-string>")
            continue
        norm = raw_prefix.strip().lstrip("/")
        if (
            target_root.startswith(norm)
            or norm.startswith(target_root)
            or norm.startswith(("digest-", "year-"))
        ):
            overlapping_prefixes.append(raw_prefix)
    if overlapping_prefixes:
        problems.append("lifecycle_rule_overlaps_digest_container")

    effective_locked = bool(locked and not problems)
    return {
        "intact": not problems,
        "locked": effective_locked,
        "state": state if isinstance(state, str) else None,
        "immutability_policy_state": immutability_policy_state,
        "retention_days": days if type(days) is int else None,
        "min_retention_days": min_retention_days,
        "overlapping_lifecycle_prefixes": overlapping_prefixes,
        "live_worm_lock_human_gated": True,
        "retention_schedule_human_gated": True,
        "problems": problems,
    }


def verify_blob_retention_headers(
    headers: Mapping[str, str],
    *,
    as_of: datetime | None = None,
    created_at: datetime | None = None,
    min_retention_days: int | None = None,
) -> dict[str, Any]:
    """Validate Blob response immutability headers for locked WORM enforcement."""
    if min_retention_days is not None and (
        type(min_retention_days) is not int or min_retention_days < 1
    ):
        raise ValueError("min_retention_days must be a positive integer")

    ref_time = _ensure_utc(as_of) if as_of is not None else datetime.now(UTC)
    problems: list[str] = []
    created_utc = _ensure_utc(created_at) if created_at is not None else None
    if created_utc is None:
        raw_created = _header(headers, "x-ms-creation-time")
        if isinstance(raw_created, str) and raw_created.strip():
            created_utc = _parse_utc_timestamp(raw_created)
            if created_utc is None:
                problems.append("invalid_blob_creation_time")

    raw_mode = _header(headers, "x-ms-immutability-policy-mode")
    stripped_mode = raw_mode.strip() if isinstance(raw_mode, str) else ""
    mode = stripped_mode.lower() if stripped_mode else None
    if mode != "locked":
        problems.append("blob_immutability_mode_not_locked")

    raw_until = _header(headers, "x-ms-immutability-policy-until-date")
    until_dt = _parse_utc_timestamp(raw_until) if isinstance(raw_until, str) else None
    retention_days: int | None = None
    retention_days_exact = False
    if until_dt is None:
        problems.append("invalid_blob_immutability_until_date")
    else:
        if created_utc is not None:
            retention_days = max(0, (until_dt - created_utc) // timedelta(days=1))
            retention_days_exact = True
        else:
            retention_days = max(0, (until_dt - ref_time) // timedelta(days=1))
        if until_dt <= ref_time:
            problems.append("blob_immutability_expired")
        if (
            created_utc is not None
            and min_retention_days is not None
            and until_dt < created_utc + timedelta(days=min_retention_days)
        ):
            problems.append("blob_immutability_shorter_than_minimum")

    if mode is None:
        immutability_policy_state = "Absent"
    elif mode == "unlocked":
        immutability_policy_state = "Unlocked"
    elif mode == "locked":
        if "blob_immutability_expired" in problems:
            immutability_policy_state = "Expired"
        elif "invalid_blob_immutability_until_date" in problems:
            immutability_policy_state = "Invalid"
        else:
            immutability_policy_state = "Locked"
    else:
        immutability_policy_state = stripped_mode

    effective_locked = bool(mode == "locked" and not problems)
    return {
        "intact": not problems,
        "locked": effective_locked,
        "mode": mode,
        "immutability_policy_state": immutability_policy_state,
        "retention_days": retention_days,
        "retention_days_exact": retention_days_exact,
        "until": until_dt.isoformat() if until_dt is not None else None,
        "live_worm_lock_human_gated": True,
        "retention_schedule_human_gated": True,
        "problems": problems,
    }


def synthesize_immutability_posture(
    *,
    policy_report: Mapping[str, Any] | None = None,
    header_reports: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Synthesize weakest-link container immutability and retention-lock posture metadata.

    ``locked`` is True only when at least one source was inspected and every inspected policy and
    anchor header report is intact and in ``"Locked"`` state. Live Azure WORM policy locking and
    Legal retention-schedule approval remain explicitly marked human-gated.
    """
    has_policy = policy_report is not None
    header_list = list(header_reports)
    if not has_policy and not header_list:
        return {
            "immutability_policy_state": "Absent",
            "retention_days": None,
            "locked": False,
            "policy_checked": False,
            "anchors_checked": 0,
            "live_worm_lock_human_gated": True,
            "retention_schedule_human_gated": True,
        }

    states: list[str] = []
    locked_flags: list[bool] = []
    exact_days: list[int] = []
    estimated_days: list[int] = []

    if policy_report is not None:
        p_state = str(policy_report.get("immutability_policy_state") or "Absent")
        p_locked = bool(
            policy_report.get("locked") is True
            and policy_report.get("intact") is True
            and p_state == "Locked"
        )
        states.append(p_state)
        locked_flags.append(p_locked)
        p_days = policy_report.get("retention_days")
        if type(p_days) is int:
            exact_days.append(p_days)

    for h_rep in header_list:
        h_state = str(h_rep.get("immutability_policy_state") or "Absent")
        h_locked = bool(
            h_rep.get("locked") is True and h_rep.get("intact") is True and h_state == "Locked"
        )
        states.append(h_state)
        locked_flags.append(h_locked)
        h_days = h_rep.get("retention_days")
        if type(h_days) is int:
            if h_rep.get("retention_days_exact") is True:
                exact_days.append(h_days)
            else:
                estimated_days.append(h_days)

    all_locked = bool(locked_flags) and all(locked_flags)
    if all_locked:
        effective_state = "Locked"
    elif "Absent" in states:
        effective_state = "Absent"
    elif "Unlocked" in states:
        effective_state = "Unlocked"
    else:
        non_locked = [s for s in states if s != "Locked"]
        effective_state = non_locked[0] if non_locked else "Locked"

    retention_days: int | None = None
    if exact_days:
        retention_days = min(exact_days)
    elif estimated_days:
        retention_days = min(estimated_days)

    return {
        "immutability_policy_state": effective_state,
        "retention_days": retention_days,
        "locked": all_locked,
        "policy_checked": has_policy,
        "anchors_checked": len(header_list),
        "live_worm_lock_human_gated": True,
        "retention_schedule_human_gated": True,
    }


def _parse_listing_page(body: bytes) -> tuple[list[str], str]:
    """Parse one Azure Blob List Blobs XML response page strictly."""
    unreadable = "digest container listing was unreadable"
    try:
        root = ET.fromstring(body)
    except (ET.ParseError, LookupError, ValueError):
        raise LedgerDigestBlobError(unreadable) from None
    if root.tag != "EnumerationResults":
        raise LedgerDigestBlobError(unreadable)
    blobs = root.findall("Blobs")
    if len(blobs) != 1:
        raise LedgerDigestBlobError(unreadable)
    names: list[str] = []
    for blob_elem in blobs[0]:
        if blob_elem.tag == "BlobPrefix":
            continue
        if blob_elem.tag != "Blob":
            raise LedgerDigestBlobError(unreadable)
        name_elems = blob_elem.findall("Name")
        if len(name_elems) != 1 or len(name_elems[0]) or not (name_elems[0].text or "").strip():
            raise LedgerDigestBlobError(unreadable)
        names.append(name_elems[0].text or "")
    next_marker = (root.findtext("NextMarker") or "").strip()
    return names, next_marker


class BlobLedgerDigestStore:
    """Create-only Azure Blob adapter for root ledger head and sealed-year digest anchors."""

    def __init__(
        self,
        account_url: str,
        container: str = DEFAULT_CONTAINER,
        *,
        sas: str | None = None,
        client_id: str | None = None,
        transport: Transport | None = None,
        env: Mapping[str, str] | None = None,
    ) -> None:
        if not valid_container_name(container):
            raise LedgerDigestBlobError("ledger digest container name is invalid")
        try:
            self._store = AzureBlobDocumentStore(
                account_url,
                container,
                sas=sas,
                client_id=client_id,
                transport=transport,
                env=env,
            )
        except ValueError:
            raise LedgerDigestBlobError("ledger digest store configuration is invalid") from None
        self.container = container
        self.last_immutability_posture: dict[str, Any] | None = None

    def _blob_url(self, name: str) -> str:
        url = f"{self._store.base}/{urllib.parse.quote(name, safe='')}"
        return f"{url}?{self._store.sas}" if self._store.sas else url

    def _send(
        self,
        method: str,
        url: str,
        extra: dict[str, str],
        body: bytes | None,
        operation: str,
    ) -> tuple[int, Mapping[str, str], bytes]:
        try:
            headers: dict[str, str] = self._store._headers(extra)
        except Exception:
            raise LedgerDigestBlobError(
                f"digest container {operation} refused: authorization unavailable"
            ) from None
        try:
            result: tuple[int, Mapping[str, str], bytes] = self._store.transport(
                method, url, headers, body
            )
        except Exception:
            if method == "PUT":
                raise LedgerDigestBlobUncertain(
                    f"digest container {operation} outcome is unknown"
                ) from None
            raise LedgerDigestBlobError(
                f"digest container {operation} failed: storage unreachable"
            ) from None
        return result

    def create_anchor_with_headers(
        self,
        name: str,
        digest: Mapping[str, Any],
    ) -> tuple[bool, dict[str, str]]:
        """Upload one canonical digest anchor create-only and return `(created, headers)`."""
        if not valid_anchor(name, digest):
            raise InvalidDigestAnchorError("invalid local digest anchor")
        data = json.dumps(dict(digest), sort_keys=True).encode("utf-8")
        extra = {
            "x-ms-blob-type": "BlockBlob",
            "Content-Type": "application/json",
            "Content-Length": str(len(data)),
            "If-None-Match": "*",
        }
        status, headers, _ = self._send("PUT", self._blob_url(name), extra, data, "upload")
        if status in (200, 201):
            return True, dict(headers)
        error_code = _header(headers, "x-ms-error-code")
        if status == 412 or (
            status == 409 and error_code in (None, "BlobAlreadyExists", "BlobImmutableDueToPolicy")
        ):
            existing, get_headers = self.read_anchor_with_headers(name)
            if not logical_anchor_equal(name, digest, existing):
                raise LedgerDigestBlobError(
                    "existing remote digest anchor differs from local digest"
                )
            return False, get_headers
        if status == 408 or status >= 500:
            raise LedgerDigestBlobUncertain(
                f"digest container upload outcome is unknown (HTTP {status})"
            )
        raise LedgerDigestBlobError(f"digest container upload refused (HTTP {status})")

    def create_anchor(self, name: str, digest: Mapping[str, Any]) -> bool:
        """Upload one canonical digest anchor create-only (`If-None-Match: *`).

        Returns True when newly written (`200`/`201`). On `409`/`412` existing-blob responses,
        reads back the remote anchor and returns False only when its immutable logical digest
        fields match ``digest``; raises ``LedgerDigestBlobError`` on any divergence or read failure.
        """
        created, _ = self.create_anchor_with_headers(name, digest)
        return created

    def read_anchor_with_headers(self, name: str) -> tuple[dict[str, Any], dict[str, str]]:
        """Download and parse one canonical digest anchor alongside its response headers."""
        if not valid_anchor_name(name):
            raise InvalidDigestAnchorError("invalid digest anchor name")
        status, headers, body = self._send("GET", self._blob_url(name), {}, None, "download")
        if status != 200:
            raise LedgerDigestBlobError(f"digest container download refused (HTTP {status})")
        try:
            decoded = body.decode("utf-8")
            parsed = json.loads(decoded)
        except (UnicodeDecodeError, ValueError):
            raise InvalidDigestAnchorError("invalid remote digest anchor") from None
        if not isinstance(parsed, dict) or not valid_anchor(name, parsed):
            raise InvalidDigestAnchorError("invalid remote digest anchor")
        return parsed, dict(headers)

    def read_anchor(self, name: str) -> dict[str, Any]:
        """Download and validate one canonical digest anchor."""
        parsed, _ = self.read_anchor_with_headers(name)
        return parsed

    def list_names(self) -> list[str]:
        """List all blob names in the digest container across paginated XML responses."""
        found: list[str] = []
        marker = ""
        for _ in range(_MAX_PAGES):
            query: dict[str, str] = {"restype": "container", "comp": "list"}
            if marker:
                query["marker"] = marker
            url = f"{self._store.base}?{urllib.parse.urlencode(query)}"
            if self._store.sas:
                url = f"{url}&{self._store.sas}"
            status, _, body = self._send("GET", url, {}, None, "listing")
            if status != 200:
                raise LedgerDigestBlobError(f"digest container listing refused (HTTP {status})")
            page, marker = _parse_listing_page(body)
            found.extend(page)
            if not marker:
                return sorted(found)
        raise LedgerDigestBlobError("digest container listing exceeded page limit")


def open_ledger_digest_store(
    env: Mapping[str, str] | None = None,
    transport: Transport | None = None,
) -> BlobLedgerDigestStore | None:
    """Open the configured BlobLedgerDigestStore, or return None when account URL is unset."""
    cfg = os.environ if env is None else env
    raw_url = (cfg.get(ACCOUNT_URL_VAR) or "").strip()
    if not raw_url:
        return None
    container = (cfg.get(CONTAINER_VAR) or DEFAULT_CONTAINER).strip()
    return BlobLedgerDigestStore(
        raw_url,
        container,
        sas=cfg.get(SAS_VAR),
        client_id=cfg.get(CLIENT_ID_VAR),
        transport=transport,
        env=cfg,
    )


def make_head_digest(
    count: int,
    head: str,
    *,
    published_at: str | None = None,
    chain: str = "main",
) -> dict[str, Any]:
    """Build a canonical head digest dictionary."""
    stamp = published_at or datetime.now(UTC).isoformat(timespec="seconds")
    return {
        "chain": chain,
        "algorithm": "sha256",
        "count": count,
        "head": head,
        "at": stamp,
    }


def publish_ledger_digests(
    entries: Sequence[Mapping[str, Any]],
    blob: BlobLedgerDigestStore,
    *,
    head_digests: Sequence[Mapping[str, Any]] | None = None,
    sealed_year_digests: Sequence[Mapping[str, Any]] | None = None,
    before_year: int | str | None = None,
    published_at: str | None = None,
    require_retention_lock: bool = False,
    retention_policy: Mapping[str, Any] | None = None,
    container_properties: Mapping[str, Any] | None = None,
    lifecycle_prefixes: Sequence[str] = (),
    min_retention_days: int = DEFAULT_MIN_RETENTION_DAYS,
    as_of: datetime | None = None,
    posture_out: dict[str, Any] | None = None,
) -> list[str]:
    """Verify the local hash chain, check container/blob WORM posture, and upload missing anchors.

    Never anchors a broken chain or local digest that disagrees with ``entries``. Records
    weakest-link immutability posture metadata on ``blob.last_immutability_posture`` (and optional
    ``posture_out``), failing closed with ``LedgerDigestBlobError`` when ``require_retention_lock``
    is True and container/blob retention lock evidence is absent, unlocked, expired, or shorter
    than ``min_retention_days``.
    """
    if type(min_retention_days) is not int or min_retention_days < 1:
        raise ValueError("min_retention_days must be a positive integer")
    ref_time = _ensure_utc(as_of) if as_of is not None else datetime.now(UTC)

    def _record_posture(posture: dict[str, Any]) -> dict[str, Any]:
        blob.last_immutability_posture = dict(posture)
        if posture_out is not None:
            posture_out.clear()
            posture_out.update(posture)
        return posture

    policy_checked = (
        retention_policy is not None or container_properties is not None or bool(lifecycle_prefixes)
    )
    policy_rep: dict[str, Any] | None = None
    if policy_checked:
        policy_rep = verify_container_retention_lock(
            retention_policy,
            container_properties=container_properties,
            lifecycle_prefixes=lifecycle_prefixes,
            container_name=blob.container,
            require_locked=require_retention_lock,
            min_retention_days=min_retention_days,
        )
        if not policy_rep["intact"]:
            _record_posture(synthesize_immutability_posture(policy_report=policy_rep))
            raise LedgerDigestBlobError(
                "digest container retention policy check failed: "
                + ", ".join(policy_rep["problems"])
            )

    entry_list = [dict(e) for e in entries]
    chain_rep: dict[str, Any] = ledger.verify_entries(entry_list)
    if not chain_rep["intact"] or (entry_list and not ledger.verify_years(entry_list)["intact"]):
        _record_posture(synthesize_immutability_posture(policy_report=policy_rep))
        return []

    cutoff = datetime.now(UTC).year if before_year is None else before_year
    heads_to_publish = (
        [dict(d) for d in head_digests]
        if head_digests is not None
        else [
            make_head_digest(
                int(chain_rep["entries"]),
                str(chain_rep["head"]),
                published_at=published_at,
            )
        ]
    )
    years_to_publish = (
        [dict(d) for d in sealed_year_digests]
        if sealed_year_digests is not None
        else [dict(d) for d in ledger.year_digests(entry_list, before=cutoff)]
    )

    valid_heads: list[tuple[str, dict[str, Any]]] = []
    for digest in heads_to_publish:
        count = digest.get("count")
        if type(count) is not int or count < 0:
            raise InvalidDigestAnchorError("invalid local head digest")
        name = f"digest-{count:010d}.json"
        if not valid_anchor(name, digest):
            raise InvalidDigestAnchorError("invalid local head digest")
        valid_heads.append((name, digest))

    valid_years: list[tuple[str, dict[str, Any]]] = []
    for digest in years_to_publish:
        year = digest.get("year")
        if not isinstance(year, str):
            raise InvalidDigestAnchorError("invalid local year digest")
        name = f"year-{year}.json"
        if not valid_anchor(name, digest):
            raise InvalidDigestAnchorError("invalid local year digest")
        valid_years.append((name, digest))

    if valid_heads and not ledger.verify_entries(entry_list, [d for _, d in valid_heads])["intact"]:
        raise InvalidDigestAnchorError("local head digest does not match ledger chain")
    if valid_years:
        if (
            not entry_list
            or not ledger.verify_years(entry_list, [d for _, d in valid_years])["intact"]
        ):
            raise InvalidDigestAnchorError("local year digest does not match ledger chain")

    uploaded: list[str] = []
    header_reps: list[dict[str, Any]] = []
    for name, digest in [*valid_heads, *valid_years]:
        created, resp_headers = blob.create_anchor_with_headers(name, digest)
        if created:
            uploaded.append(name)
            if (
                require_retention_lock
                and _header(resp_headers, "x-ms-immutability-policy-mode") is None
            ):
                _, get_headers = blob.read_anchor_with_headers(name)
                if _header(get_headers, "x-ms-immutability-policy-mode") is not None:
                    resp_headers = get_headers
        header_rep = verify_blob_retention_headers(
            resp_headers,
            as_of=ref_time,
            created_at=ref_time if created else None,
            min_retention_days=min_retention_days,
        )
        header_reps.append(header_rep)
        if require_retention_lock and not header_rep["intact"]:
            _record_posture(
                synthesize_immutability_posture(
                    policy_report=policy_rep,
                    header_reports=header_reps,
                )
            )
            raise LedgerDigestBlobError(
                "digest anchor lacks required immutable retention lock: "
                + ", ".join(header_rep["problems"])
            )

    posture = _record_posture(
        synthesize_immutability_posture(
            policy_report=policy_rep,
            header_reports=header_reps,
        )
    )
    if require_retention_lock and not posture["locked"]:
        raise LedgerDigestBlobError("digest container retention lock could not be verified")
    return uploaded


def publish_ledger_digests_with_posture(
    entries: Sequence[Mapping[str, Any]],
    blob: BlobLedgerDigestStore,
    *,
    head_digests: Sequence[Mapping[str, Any]] | None = None,
    sealed_year_digests: Sequence[Mapping[str, Any]] | None = None,
    before_year: int | str | None = None,
    published_at: str | None = None,
    require_retention_lock: bool = False,
    retention_policy: Mapping[str, Any] | None = None,
    container_properties: Mapping[str, Any] | None = None,
    lifecycle_prefixes: Sequence[str] = (),
    min_retention_days: int = DEFAULT_MIN_RETENTION_DAYS,
    as_of: datetime | None = None,
) -> dict[str, Any]:
    """Publish ledger digests and return uploaded names with recorded immutability posture."""
    posture: dict[str, Any] = {}
    uploaded = publish_ledger_digests(
        entries,
        blob,
        head_digests=head_digests,
        sealed_year_digests=sealed_year_digests,
        before_year=before_year,
        published_at=published_at,
        require_retention_lock=require_retention_lock,
        retention_policy=retention_policy,
        container_properties=container_properties,
        lifecycle_prefixes=lifecycle_prefixes,
        min_retention_days=min_retention_days,
        as_of=as_of,
        posture_out=posture,
    )
    return {
        "uploaded": uploaded,
        "immutability_policy_state": posture["immutability_policy_state"],
        "retention_days": posture["retention_days"],
        "locked": posture["locked"],
        "immutability_posture": posture,
    }


def publish_store_digests(
    store: Any,
    blob: BlobLedgerDigestStore,
    *,
    require_retention_lock: bool = False,
    retention_policy: Mapping[str, Any] | None = None,
    container_properties: Mapping[str, Any] | None = None,
    lifecycle_prefixes: Sequence[str] = (),
    min_retention_days: int = DEFAULT_MIN_RETENTION_DAYS,
    as_of: datetime | None = None,
    posture_out: dict[str, Any] | None = None,
) -> list[str]:
    """Write local head and sealed-year digests via store, then upload missing anchors."""
    entries = [dict(e) for e in store.audit_entries()]
    if not ledger.verify_entries(entries)["intact"]:
        return publish_ledger_digests(
            entries,
            blob,
            require_retention_lock=require_retention_lock,
            retention_policy=retention_policy,
            container_properties=container_properties,
            lifecycle_prefixes=lifecycle_prefixes,
            min_retention_days=min_retention_days,
            as_of=as_of,
            posture_out=posture_out,
        )
    store.write_digest()
    store.write_year_digests()
    raw_heads = ledger.read_digests(store.digest_dir)
    raw_years = [
        d for d in ledger.read_year_digests(store.digest_dir) if isinstance(d, dict) and "year" in d
    ]
    return publish_ledger_digests(
        entries,
        blob,
        head_digests=raw_heads,
        sealed_year_digests=raw_years,
        require_retention_lock=require_retention_lock,
        retention_policy=retention_policy,
        container_properties=container_properties,
        lifecycle_prefixes=lifecycle_prefixes,
        min_retention_days=min_retention_days,
        as_of=as_of,
        posture_out=posture_out,
    )


def verify_ledger_digests(
    entries: Sequence[Mapping[str, Any]],
    blob: BlobLedgerDigestStore,
    *,
    require_retention_lock: bool = False,
    require_current_head: bool = False,
    retention_policy: Mapping[str, Any] | None = None,
    container_properties: Mapping[str, Any] | None = None,
    lifecycle_prefixes: Sequence[str] = (),
    min_retention_days: int = DEFAULT_MIN_RETENTION_DAYS,
    as_of: datetime | None = None,
) -> dict[str, Any]:
    """Verify ledger entries solely against anchors in the immutable Blob container."""
    if type(min_retention_days) is not int or min_retention_days < 1:
        raise ValueError("min_retention_days must be a positive integer")
    problems: list[dict[str, Any]] = []
    policy_checked = (
        retention_policy is not None or container_properties is not None or bool(lifecycle_prefixes)
    )
    policy_rep: dict[str, Any] | None = None
    if policy_checked:
        policy_rep = verify_container_retention_lock(
            retention_policy,
            container_properties=container_properties,
            lifecycle_prefixes=lifecycle_prefixes,
            container_name=blob.container,
            require_locked=require_retention_lock,
            min_retention_days=min_retention_days,
        )
        if not policy_rep["intact"]:
            problems.append(
                {
                    "check": "retention_policy",
                    "problems": policy_rep["problems"],
                }
            )

    names = blob.list_names()
    heads: list[dict[str, Any]] = []
    years: list[dict[str, Any]] = []
    header_reps: list[dict[str, Any]] = []

    for name in names:
        if not name.startswith(("digest-", "year-")):
            continue
        if not valid_anchor_name(name):
            problems.append(
                {
                    "check": "digests",
                    "name": name,
                    "problem": "invalid remote digest anchor",
                }
            )
            continue
        try:
            digest, headers = blob.read_anchor_with_headers(name)
        except InvalidDigestAnchorError:
            problems.append(
                {
                    "check": "digests",
                    "name": name,
                    "problem": "invalid remote digest anchor",
                }
            )
            continue
        header_rep = verify_blob_retention_headers(
            headers,
            as_of=as_of,
            min_retention_days=min_retention_days,
        )
        header_reps.append(header_rep)
        if require_retention_lock and not header_rep["intact"]:
            problems.append(
                {
                    "check": "retention_headers",
                    "name": name,
                    "problems": header_rep["problems"],
                }
            )
        if name.startswith("digest-"):
            heads.append(digest)
        else:
            years.append(digest)

    entry_list = [dict(e) for e in entries]
    chain_rep: dict[str, Any] = ledger.verify_entries(entry_list, heads)
    year_rep: dict[str, Any] = (
        ledger.verify_years(entry_list, years)
        if entry_list
        else {
            "intact": not years,
            "years": {},
            "missing_years": [str(d["year"]) for d in years],
        }
    )

    if not chain_rep["intact"]:
        problems.append(
            {
                "check": "chain",
                "problem": chain_rep["problem"],
                "digest_mismatches": chain_rep["digest_mismatches"],
            }
        )
    if not year_rep["intact"]:
        problems.append(
            {
                "check": "years",
                "missing_years": year_rep["missing_years"],
                "broken": {
                    year_key: info["problems"]
                    for year_key, info in year_rep["years"].items()
                    if not info["intact"]
                },
            }
        )
    if not heads and not years:
        problems.append(
            {
                "check": "digests",
                "problem": (
                    "the container holds no recognized head or year digest anchors "
                    "to verify against"
                ),
            }
        )
    elif (
        require_current_head
        and chain_rep["problem"] is None
        and not any(
            d.get("count") == len(entry_list) and d.get("head") == chain_rep["head"] for d in heads
        )
    ):
        problems.append(
            {
                "check": "current_head",
                "problem": "the container does not hold an anchor for the current ledger head",
                "expected_count": len(entry_list),
            }
        )

    posture = synthesize_immutability_posture(
        policy_report=policy_rep,
        header_reports=header_reps,
    )
    blob.last_immutability_posture = dict(posture)
    if require_retention_lock and not posture["locked"]:
        if not any(p["check"] in ("retention_policy", "retention_headers") for p in problems):
            problems.append(
                {
                    "check": "retention_lock",
                    "problem": "immutable container retention lock was not verified",
                }
            )

    lock_verified = bool(require_retention_lock and posture["locked"])
    return {
        "intact": not problems,
        "digests": len(heads),
        "year_digests": len(years),
        "entries": int(chain_rep["entries"]),
        "retention_lock_verified": lock_verified,
        "immutability_policy_state": posture["immutability_policy_state"],
        "retention_days": posture["retention_days"],
        "locked": posture["locked"],
        "immutability_posture": posture,
        "problems": problems,
    }


def reconcile_ledger_digests(
    blob: BlobLedgerDigestStore,
    record: Mapping[str, str],
    *,
    require_retention_lock: bool = False,
    retention_policy: Mapping[str, Any] | None = None,
    container_properties: Mapping[str, Any] | None = None,
    lifecycle_prefixes: Sequence[str] = (),
    min_retention_days: int = DEFAULT_MIN_RETENTION_DAYS,
    as_of: datetime | None = None,
) -> dict[str, Any]:
    """Compare remote container anchors against an independent second-person SHA-256 record."""
    if type(min_retention_days) is not int or min_retention_days < 1:
        raise ValueError("min_retention_days must be a positive integer")
    if (
        not isinstance(record, Mapping)
        or not record
        or any(
            not valid_anchor_name(k) or not isinstance(v, str) or _SHA256_RE.fullmatch(v) is None
            for k, v in record.items()
        )
    ):
        raise InvalidDigestAnchorError(
            "the independent record must map canonical anchor names to SHA-256 heads"
        )

    problems: list[dict[str, Any]] = []
    policy_checked = (
        retention_policy is not None or container_properties is not None or bool(lifecycle_prefixes)
    )
    policy_rep: dict[str, Any] | None = None
    if policy_checked:
        policy_rep = verify_container_retention_lock(
            retention_policy,
            container_properties=container_properties,
            lifecycle_prefixes=lifecycle_prefixes,
            container_name=blob.container,
            require_locked=require_retention_lock,
            min_retention_days=min_retention_days,
        )
        if not policy_rep["intact"]:
            problems.append(
                {
                    "check": "retention_policy",
                    "problems": policy_rep["problems"],
                }
            )

    remote: dict[str, str] = {}
    header_reps: list[dict[str, Any]] = []
    for name in blob.list_names():
        if not name.startswith(("digest-", "year-")):
            continue
        if not valid_anchor_name(name):
            problems.append(
                {"check": "remote", "name": name, "problem": "invalid remote digest anchor"}
            )
            continue
        try:
            digest, headers = blob.read_anchor_with_headers(name)
        except InvalidDigestAnchorError:
            problems.append(
                {"check": "remote", "name": name, "problem": "invalid remote digest anchor"}
            )
            continue
        header_rep = verify_blob_retention_headers(
            headers,
            as_of=as_of,
            min_retention_days=min_retention_days,
        )
        header_reps.append(header_rep)
        if require_retention_lock and not header_rep["intact"]:
            problems.append(
                {
                    "check": "retention_headers",
                    "name": name,
                    "problems": header_rep["problems"],
                }
            )
        remote[name] = str(digest["head"])

    for name in sorted(set(record) - set(remote)):
        problems.append(
            {
                "check": "record",
                "name": name,
                "problem": "recorded anchor is absent from the container",
            }
        )
    for name in sorted(set(remote) - set(record)):
        problems.append(
            {
                "check": "remote",
                "name": name,
                "problem": "remote anchor is not in the independent record",
            }
        )
    for name in sorted(set(record) & set(remote)):
        if record[name] != remote[name]:
            problems.append(
                {
                    "check": "head",
                    "name": name,
                    "problem": "remote head differs from the independent record",
                }
            )

    posture = synthesize_immutability_posture(
        policy_report=policy_rep,
        header_reports=header_reps,
    )
    blob.last_immutability_posture = dict(posture)
    if require_retention_lock and not posture["locked"]:
        if not any(p["check"] in ("retention_policy", "retention_headers") for p in problems):
            problems.append(
                {
                    "check": "retention_lock",
                    "problem": "immutable container retention lock was not verified",
                }
            )

    return {
        "intact": not problems,
        "compared": len(set(record) & set(remote)),
        "retention_lock_verified": bool(require_retention_lock and posture["locked"]),
        "immutability_policy_state": posture["immutability_policy_state"],
        "retention_days": posture["retention_days"],
        "locked": posture["locked"],
        "immutability_posture": posture,
        "problems": problems,
    }


def _parse_bool_env(env: Mapping[str, str], key: str, *, default: bool = False) -> bool:
    raw = env.get(key)
    if raw is None or raw.strip() == "":
        return default
    lowered = raw.strip().lower()
    if lowered in ("1", "true", "yes", "on"):
        return True
    if lowered in ("0", "false", "no", "off"):
        return False
    raise LedgerDigestBlobError(f"{key} must be a boolean value")


def _parse_min_days_env(env: Mapping[str, str]) -> int:
    raw = env.get(MIN_RETENTION_DAYS_VAR)
    if raw is None or raw.strip() == "":
        return DEFAULT_MIN_RETENTION_DAYS
    text = raw.strip()
    if not text.isdigit():
        raise LedgerDigestBlobError(f"{MIN_RETENTION_DAYS_VAR} must be a positive integer")
    days = int(text)
    if days < 1:
        raise LedgerDigestBlobError(f"{MIN_RETENTION_DAYS_VAR} must be at least 1")
    return days


def _emit_alert(
    out: OutputSink,
    *,
    status: str,
    problem_count: int,
    entry_count: int,
    reason_code: str,
) -> dict[str, Any]:
    diagnostic = sanitize_diagnostic(
        {
            "alert": MISMATCH_RUNBOOK,
            "severity": "1",
            "task": VERIFICATION_TASK,
            "count": max(1, problem_count),
            "denominator": max(0, entry_count),
            "status": status,
            "owner_role": PROPOSED_OWNER,
            "offline_only": False,
        }
    )
    out(f"{ALERT_MARKER} {reason_code} {json.dumps(diagnostic, sort_keys=True)}")
    return diagnostic


def _emit_ok(
    out: OutputSink,
    *,
    anchor_count: int,
    entry_count: int,
) -> dict[str, Any]:
    diagnostic = sanitize_diagnostic(
        {
            "alert": MISSING_RUNBOOK,
            "severity": "info",
            "task": VERIFICATION_TASK,
            "count": max(0, anchor_count),
            "denominator": max(0, entry_count),
            "status": WITHIN,
            "owner_role": PROPOSED_OWNER,
            "offline_only": False,
        }
    )
    out(
        f"{OK_MARKER} ledger matches the immutable digests {json.dumps(diagnostic, sort_keys=True)}"
    )
    return diagnostic


def run_scheduled_verification(
    entries: Sequence[Mapping[str, Any]],
    blob: BlobLedgerDigestStore,
    *,
    publish: bool = False,
    head_digests: Sequence[Mapping[str, Any]] | None = None,
    sealed_year_digests: Sequence[Mapping[str, Any]] | None = None,
    before_year: int | str | None = None,
    published_at: str | None = None,
    require_retention_lock: bool = False,
    require_current_head: bool | None = None,
    retention_policy: Mapping[str, Any] | None = None,
    container_properties: Mapping[str, Any] | None = None,
    lifecycle_prefixes: Sequence[str] = (),
    min_retention_days: int = DEFAULT_MIN_RETENTION_DAYS,
    as_of: datetime | None = None,
    out: OutputSink = print,
) -> dict[str, Any]:
    """Run scheduled ledger digest publication/verification and emit sanitized console markers."""
    published: list[str] = []
    check_current_head = publish if require_current_head is None else require_current_head
    entry_list = [dict(e) for e in entries]

    try:
        if publish:
            published = publish_ledger_digests(
                entry_list,
                blob,
                head_digests=head_digests,
                sealed_year_digests=sealed_year_digests,
                before_year=before_year,
                published_at=published_at,
                require_retention_lock=require_retention_lock,
                retention_policy=retention_policy,
                container_properties=container_properties,
                lifecycle_prefixes=lifecycle_prefixes,
                min_retention_days=min_retention_days,
                as_of=as_of,
            )
        report = verify_ledger_digests(
            entry_list,
            blob,
            require_retention_lock=require_retention_lock,
            require_current_head=check_current_head,
            retention_policy=retention_policy,
            container_properties=container_properties,
            lifecycle_prefixes=lifecycle_prefixes,
            min_retention_days=min_retention_days,
            as_of=as_of,
        )
    except LedgerDigestBlobError:
        err_posture = (
            dict(blob.last_immutability_posture)
            if blob.last_immutability_posture is not None
            else synthesize_immutability_posture()
        )
        diag = _emit_alert(
            out,
            status=BLOCKED,
            problem_count=1,
            entry_count=len(entry_list),
            reason_code="digest_store_verification_failed",
        )
        return {
            "exit_code": 1,
            "intact": False,
            "marker": ALERT_MARKER,
            "runbook": MISMATCH_RUNBOOK,
            "proposed_owner": PROPOSED_OWNER,
            "diagnostic": diag,
            "published": published,
            "immutability_policy_state": err_posture["immutability_policy_state"],
            "retention_days": err_posture["retention_days"],
            "locked": err_posture["locked"],
            "immutability_posture": err_posture,
            "report": None,
        }
    except Exception:
        err_posture = (
            dict(blob.last_immutability_posture)
            if blob.last_immutability_posture is not None
            else synthesize_immutability_posture()
        )
        diag = _emit_alert(
            out,
            status=BLOCKED,
            problem_count=1,
            entry_count=len(entry_list),
            reason_code="unexpected_verification_error",
        )
        return {
            "exit_code": 1,
            "intact": False,
            "marker": ALERT_MARKER,
            "runbook": MISMATCH_RUNBOOK,
            "proposed_owner": PROPOSED_OWNER,
            "diagnostic": diag,
            "published": published,
            "immutability_policy_state": err_posture["immutability_policy_state"],
            "retention_days": err_posture["retention_days"],
            "locked": err_posture["locked"],
            "immutability_posture": err_posture,
            "report": None,
        }

    if not report["intact"]:
        diag = _emit_alert(
            out,
            status=BREACH,
            problem_count=len(report["problems"]),
            entry_count=int(report["entries"]),
            reason_code="ledger_digest_mismatch",
        )
        return {
            "exit_code": 1,
            "intact": False,
            "marker": ALERT_MARKER,
            "runbook": MISMATCH_RUNBOOK,
            "proposed_owner": PROPOSED_OWNER,
            "diagnostic": diag,
            "published": published,
            "immutability_policy_state": report["immutability_policy_state"],
            "retention_days": report["retention_days"],
            "locked": report["locked"],
            "immutability_posture": report["immutability_posture"],
            "report": report,
        }

    diag = _emit_ok(
        out,
        anchor_count=int(report["digests"]) + int(report["year_digests"]),
        entry_count=int(report["entries"]),
    )
    return {
        "exit_code": 0,
        "intact": True,
        "marker": OK_MARKER,
        "runbook": MISSING_RUNBOOK,
        "proposed_owner": PROPOSED_OWNER,
        "diagnostic": diag,
        "published": published,
        "immutability_policy_state": report["immutability_policy_state"],
        "retention_days": report["retention_days"],
        "locked": report["locked"],
        "immutability_posture": report["immutability_posture"],
        "report": report,
    }


def _run_reconcile_cli(
    path: str,
    cfg: Mapping[str, str],
    blob: BlobLedgerDigestStore | None,
    out: OutputSink,
) -> int:
    try:
        require_lock = _parse_bool_env(cfg, REQUIRE_LOCK_VAR, default=False)
        min_days = _parse_min_days_env(cfg)
        resolved_blob = blob or open_ledger_digest_store(cfg)
    except LedgerDigestBlobError:
        out(f"{RECONCILE_ALERT_MARKER} cannot reconcile: invalid digest configuration")
        return 1
    if resolved_blob is None:
        out(f"{RECONCILE_ALERT_MARKER} cannot reconcile: {ACCOUNT_URL_VAR} is not set")
        return 1
    try:
        with open(path, encoding="utf-8") as handle:
            record = json.load(handle)
        rep = reconcile_ledger_digests(
            resolved_blob,
            record,
            require_retention_lock=require_lock,
            min_retention_days=min_days,
        )
    except (OSError, ValueError, LedgerDigestBlobError) as exc:
        out(f"{RECONCILE_ALERT_MARKER} cannot reconcile: {type(exc).__name__}")
        return 1
    if not rep["intact"]:
        out(f"{RECONCILE_ALERT_MARKER} remote anchors do not match the independent record")
        return 1
    out(f"{RECONCILE_OK_MARKER} remote anchors match the independent record")
    return 0


def main(
    argv: Sequence[str] | None = None,
    env: Mapping[str, str] | None = None,
    store: Any = None,
    blob: BlobLedgerDigestStore | None = None,
    out: OutputSink = print,
) -> int:
    """CLI entrypoint for scheduled ledger digest verification or independent reconciliation."""
    args = list(sys.argv[1:] if argv is None else argv)
    cfg: Mapping[str, str] = os.environ if env is None else env

    if "--reconcile" in args:
        idx = args.index("--reconcile")
        if idx + 1 >= len(args):
            out("--reconcile needs the path of the independent record")
            return 2
        return _run_reconcile_cli(args[idx + 1], cfg, blob, out)

    try:
        require_lock = _parse_bool_env(cfg, REQUIRE_LOCK_VAR, default=False)
        min_days = _parse_min_days_env(cfg)
        resolved_blob = blob or open_ledger_digest_store(cfg)
        if resolved_blob is None:
            _emit_alert(
                out,
                status=BLOCKED,
                problem_count=1,
                entry_count=0,
                reason_code="digest_store_unconfigured",
            )
            return 1
        resolved_store = store
        if resolved_store is None:
            from zava_forward.core.factory import open_store

            resolved_store = open_store(cfg)
        publish_flag = "--publish" in args
        entries = [dict(e) for e in resolved_store.audit_entries()]
        head_digests: Sequence[Mapping[str, Any]] | None = None
        year_digests: Sequence[Mapping[str, Any]] | None = None
        if publish_flag and hasattr(resolved_store, "write_digest"):
            if ledger.verify_entries(entries)["intact"]:
                resolved_store.write_digest()
                if hasattr(resolved_store, "write_year_digests"):
                    resolved_store.write_year_digests()
                digest_dir = getattr(resolved_store, "digest_dir", None)
                if digest_dir:
                    head_digests = ledger.read_digests(digest_dir)
                    year_digests = [
                        d
                        for d in ledger.read_year_digests(digest_dir)
                        if isinstance(d, dict) and "year" in d
                    ]
    except LedgerDigestBlobError:
        _emit_alert(
            out,
            status=BLOCKED,
            problem_count=1,
            entry_count=0,
            reason_code="digest_configuration_invalid",
        )
        return 1
    except Exception:
        _emit_alert(
            out,
            status=BLOCKED,
            problem_count=1,
            entry_count=0,
            reason_code="store_unavailable",
        )
        return 1

    outcome = run_scheduled_verification(
        entries,
        resolved_blob,
        publish=publish_flag,
        head_digests=head_digests,
        sealed_year_digests=year_digests,
        require_retention_lock=require_lock,
        min_retention_days=min_days,
        out=out,
    )
    return int(outcome["exit_code"])


if __name__ == "__main__":
    sys.exit(main())
