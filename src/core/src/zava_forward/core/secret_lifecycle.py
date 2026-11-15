"""Key Vault secret lifecycle verification and signed scheduled access-review ledger."""

from __future__ import annotations

import datetime as dt
import hashlib
import hmac
import json
import math
import re
from collections.abc import Mapping, Sequence
from typing import Any
from urllib.parse import urlparse

GENESIS_HASH = "0" * 64

DATA_ROLES: dict[str, str] = {
    "Key Vault Secrets User": "read",
    "Key Vault Secrets Officer": "write",
    "Key Vault Administrator": "admin",
    "Key Vault Reader": "metadata",
    "Owner": "no data-plane access",
}
REQUIRED: tuple[str, ...] = ("name", "owner", "rotationIntervalDays", "expiryAlertDays")
SAFE_ORDER: tuple[str, ...] = ("append", "store", "refresh", "verify", "delete_old")

VALID_ROTATION_STAGES = frozenset(
    {"dual_secret_overlap", "post_switchover", "post_retire", "rollback"}
)
VALID_ASSIGNMENT_DECISIONS = frozenset({"keep", "remove"})
VALID_ANOMALY_DISPOSITIONS = frozenset({"remediated", "revoked", "accepted_exception"})

PLATFORM_NOTIFICATION_OPS = frozenset(
    {
        "SecretNearExpiryEventGridNotification",
        "SecretExpiredEventGridNotification",
        "CertificateNearExpiryEventGridNotification",
        "CertificateExpiredEventGridNotification",
        "KeyNearExpiryEventGridNotification",
        "KeyExpiredEventGridNotification",
    }
)

_FORBIDDEN_SECRET_KEYS = frozenset(
    {
        "value",
        "secrettext",
        "secretvalue",
        "password",
        "clientsecret",
        "cookie",
        "setcookie",
        "token",
        "accesstoken",
        "refreshtoken",
        "idtoken",
        "sas",
        "sastoken",
        "connectionstring",
        "privatekey",
        "signingkey",
    }
)

_SENSITIVE_VALUE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"[?&](?:sig|sv|se|sp|spr|srt|ss)=[^&\s]+", re.IGNORECASE),
    re.compile(r"\b(?:Bearer|Basic)\s+[A-Za-z0-9._~+/=-]{8,}", re.IGNORECASE),
    re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    re.compile(
        r"\b(?:SharedAccessSignature|AccountKey|SharedAccessKey|Pwd|Password)\s*=",
        re.IGNORECASE,
    ),
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
)

_ARM_ENVELOPE_KEYS = frozenset({"value", "nextLink", "@odata.context", "@odata.nextLink"})
_VAULT_NAME_RE = re.compile(r"^[A-Za-z0-9-]{3,24}$")
_ARM_VAULT_ID_RE = re.compile(
    r"/providers/microsoft\.keyvault/vaults/([A-Za-z0-9-]+)(?:/|$)",
    re.IGNORECASE,
)
_FULL_VAULT_RESOURCE_ID_RE = re.compile(
    r"^(/subscriptions/([^/\s]+)/resourcegroups/([^/\s]+))"
    r"/providers/microsoft\.keyvault/vaults/([A-Za-z0-9-]{3,24})/?$",
    re.IGNORECASE,
)
_KEY_ID_TOKEN_RE = re.compile(r"^[A-Za-z0-9._:-]{3,128}$")
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")

_PLACEHOLDER_REVIEWERS = frozenset(
    {
        "pending",
        "tbd",
        "todo",
        "unknown",
        "none",
        "n/a",
        "na",
        "unassigned",
        "operator",
        "same operator",
        "reviewer pending",
        "open item",
    }
)
_AUTOMATED_REVIEWER_TOKENS = frozenset(
    {
        "system",
        "agent",
        "bot",
        "copilot",
        "automation",
        "pipeline",
        "github-actions",
        "service-principal",
        "serviceprincipal",
        "managed-identity",
        "managedidentity",
        "cron",
    }
)


class SecretLifecycleError(ValueError):
    """Domain validation error for Key Vault secret lifecycle operations."""


class SecretExposureError(SecretLifecycleError):
    """Raised when raw secret or credential material is supplied to a metadata-only boundary."""


def _normalize_key_name(key: str) -> str:
    return key.replace("-", "").replace("_", "").strip().lower()


def _canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _sha256_canonical(payload: Any) -> str:
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _safe_token(val: Any, fallback: str) -> str:
    if isinstance(val, str):
        cleaned = val.strip()
        if _KEY_ID_TOKEN_RE.match(cleaned):
            return cleaned
    return fallback


def _safe_vault(val: Any) -> str:
    if isinstance(val, str):
        cleaned = val.strip()
        if _VAULT_NAME_RE.match(cleaned):
            return cleaned
    return "<invalid-vault>"


def _fmt_http_status(val: Any) -> str:
    if not isinstance(val, bool) and isinstance(val, int) and 100 <= val <= 599:
        return str(val)
    return "<invalid-status>"


def assert_no_secret_material(payload: Any, *, path: str = "$") -> None:
    """Reject raw secret keys, credential strings, or non-finite floats without echoing values."""
    if not isinstance(payload, bool) and isinstance(payload, float) and not math.isfinite(payload):
        raise SecretLifecycleError(f"non-finite numeric value refused at {path}")
    if isinstance(payload, Mapping):
        for raw_key, item in payload.items():
            key_str = str(raw_key)
            child_path = f"{path}.{key_str}"
            if _normalize_key_name(key_str) in _FORBIDDEN_SECRET_KEYS:
                raise SecretExposureError(f"secret material refused at {child_path}")
            if isinstance(raw_key, str):
                for pattern in _SENSITIVE_VALUE_PATTERNS:
                    if pattern.search(raw_key):
                        raise SecretExposureError(f"credential pattern refused in key at {path}")
            assert_no_secret_material(item, path=child_path)
        return
    if isinstance(payload, Sequence) and not isinstance(payload, (str, bytes, bytearray)):
        for idx, item in enumerate(payload):
            assert_no_secret_material(item, path=f"{path}[{idx}]")
        return
    if isinstance(payload, str):
        for pattern in _SENSITIVE_VALUE_PATTERNS:
            if pattern.search(payload):
                raise SecretExposureError(f"credential pattern refused at {path}")


def unwrap_arm_list_envelope(payload: Any, *, label: str = "$") -> list[dict[str, Any]]:
    """Unwrap an optional top-level ARM/Graph `{\"value\": [...]}` metadata list envelope."""
    if isinstance(payload, Mapping):
        keys = {str(k) for k in payload}
        raw_value = payload.get("value")
        if (
            "value" in keys
            and keys <= _ARM_ENVELOPE_KEYS
            and isinstance(raw_value, list)
            and all(isinstance(row, Mapping) for row in raw_value)
        ):
            for extra_key in keys - {"value"}:
                assert_no_secret_material(payload[extra_key], path=f"{label}.{extra_key}")
            assert_no_secret_material(raw_value, path=f"{label}.value")
            for link_key in ("nextLink", "@odata.nextLink"):
                if link_key in payload and payload[link_key] not in (None, ""):
                    raise SecretLifecycleError(
                        f"{label} is paginated ({link_key} present); "
                        "export all pages before auditing"
                    )
            return [dict(row) for row in raw_value]
        assert_no_secret_material(payload, path=label)
        raise SecretLifecycleError(f"{label} must be a JSON array or ARM list envelope")
    if isinstance(payload, list) and all(isinstance(row, Mapping) for row in payload):
        assert_no_secret_material(payload, path=label)
        return [dict(row) for row in payload]
    assert_no_secret_material(payload, path=label)
    raise SecretLifecycleError(f"{label} must be a JSON array of metadata objects")


def parse_time(value: str) -> dt.datetime:
    """Parse an ISO-8601 timestamp into a timezone-aware UTC datetime."""
    if not isinstance(value, str) or not value.strip():
        raise SecretLifecycleError("timestamp must be a non-empty ISO-8601 string")
    parsed = dt.datetime.fromisoformat(value.strip())
    if parsed.tzinfo is None:
        raise SecretLifecycleError("timestamp must include an explicit timezone offset")
    return parsed.astimezone(dt.UTC)


def validate_human_reviewer(reviewer: str) -> str:
    """Validate that a reviewer string names a human rather than a placeholder or bot."""
    if not isinstance(reviewer, str):
        raise SecretLifecycleError("reviewer must be a non-empty human name")
    assert_no_secret_material(reviewer, path="$.reviewer")
    cleaned = " ".join(reviewer.split())
    if len(cleaned) < 3:
        raise SecretLifecycleError("reviewer must name an accountable human")
    lowered = cleaned.lower()
    if lowered in _PLACEHOLDER_REVIEWERS or "pending" in lowered:
        raise SecretLifecycleError("reviewer cannot be a placeholder or pending marker")
    tokens = {tok for tok in re.split(r"[^a-z0-9-]+", lowered) if tok}
    if tokens & _AUTOMATED_REVIEWER_TOKENS:
        raise SecretLifecycleError("reviewer must be a human, not an automated principal")
    return cleaned


def validate_inventory(inventory: Mapping[str, Any]) -> list[str]:
    """Return structural problems in `infra/secret-inventory.json`."""
    assert_no_secret_material(inventory, path="$.inventory")
    problems: list[str] = []
    secrets = inventory.get("secrets", [])
    if not isinstance(secrets, Sequence) or isinstance(secrets, (str, bytes)):
        return ["inventory secrets must be a list"]
    for entry in secrets:
        if not isinstance(entry, Mapping):
            problems.append("?: invalid secret entry")
            continue
        for key in REQUIRED:
            if not entry.get(key):
                problems.append(f"{entry.get('name', '?')}: missing {key}")
    if not secrets:
        problems.append("inventory has no secrets")
    return problems


def check_secrets(
    inventory: Mapping[str, Any],
    listed: Sequence[Mapping[str, Any]],
    now: dt.datetime,
) -> list[tuple[str, str, str]]:
    """Findings for each inventoried secret, using only metadata (never values)."""
    assert_no_secret_material(inventory, path="$.inventory")
    assert_no_secret_material(listed, path="$.secrets")
    findings: list[tuple[str, str, str]] = []
    by_name = {str(item["name"]): item for item in listed if "name" in item}
    for entry in inventory["secrets"]:
        name = str(entry["name"])
        item = by_name.get(name)
        if item is None:
            findings.append((name, "missing", "secret not present in the vault"))
            continue
        attrs = item.get("attributes", {})
        if not isinstance(attrs, Mapping):
            attrs = {}
        if not attrs.get("enabled", True):
            findings.append((name, "disabled", "secret is disabled"))
        expires = attrs.get("expires")
        if not expires:
            findings.append((name, "no-expiry", "no expiry date is set"))
        else:
            left = (parse_time(str(expires)) - now).days
            alert_days = int(entry["expiryAlertDays"])
            if left < 0:
                findings.append((name, "expired", f"expired {-left} days ago"))
            elif left <= alert_days:
                findings.append(
                    (
                        name,
                        "expiring",
                        f"{left} days left, inside the {alert_days} day alert window",
                    )
                )
        updated = attrs.get("updated") or attrs.get("created")
        if updated:
            age = (now - parse_time(str(updated))).days
            interval = int(entry["rotationIntervalDays"])
            if age > interval:
                findings.append(
                    (
                        name,
                        "rotation-overdue",
                        f"{age} days since last change, interval {interval}",
                    )
                )
    return findings


def access_review(
    inventory: Mapping[str, Any],
    assignments: Sequence[Mapping[str, Any]],
    reviewer: str,
    now: dt.datetime,
) -> dict[str, Any]:
    """Generate a pending RBAC access review worksheet compatible with legacy CLI usage."""
    assert_no_secret_material(inventory, path="$.inventory")
    assert_no_secret_material(assignments, path="$.assignments")
    assert_no_secret_material(reviewer, path="$.reviewer")
    rows: list[dict[str, Any]] = []
    for item in assignments:
        role = str(item.get("roleDefinitionName", ""))
        rows.append(
            {
                "principalId": item.get("principalId"),
                "principalType": item.get("principalType"),
                "role": role,
                "access": DATA_ROLES.get(role, "unclassified, needs justification"),
                "scope": item.get("scope"),
                "decision": "pending",
            }
        )
    interval_days = int(inventory["reviewIntervalDays"])
    return {
        "reviewedAt": now.isoformat(),
        "reviewer": reviewer,
        "nextReviewDue": (now + dt.timedelta(days=interval_days)).date().isoformat(),
        "assignments": rows,
        "note": "Each decision stays pending until a named human marks keep or remove.",
    }


def rotation_plan(vault: str, app_id: str) -> list[str]:
    """Return the ordered zero-downtime Entra client-secret rotation steps."""
    assert_no_secret_material(vault, path="$.vault")
    assert_no_secret_material(app_id, path="$.appId")
    return [
        (
            f"1. az ad app credential reset --id {app_id} --append "
            "--display-name container-apps-auth-NEW --years 1 --query password -o tsv "
            "| tr -d '\\r\\n' | az keyvault secret set "
            f"--vault-name {vault} --name entra-client-secret --expires <iso> "
            "--file /dev/stdin --output none (old credential stays valid; never prints secret)"
        ),
        (
            f"2. Confirm the new version of entra-client-secret in {vault} "
            "is enabled with an explicit expiry date and record keyId via az ad app credential list"
        ),
        (
            "3. Wait for the versionless reference to refresh (up to 30 minutes; "
            ">= 60-minute dual-secret overlap) or restart the active revision"
        ),
        (
            "4. Sign in through /sign-in and confirm /app and a data API return 200 "
            "with fresh OAuth token exchange for an authorised user"
        ),
        f"5. Only then az ad app credential delete --id {app_id} --key-id <old key id>",
        "6. Record the rotation date, signed receipt, and operator in the rotation log",
    ]


def rotation_timeline(order: Sequence[str]) -> list[dict[str, Any]]:
    """Model the Entra credential, vault, and Container App states for a rotation order."""
    valid = {"old"}
    vault = "old"
    presented = "old"
    timeline: list[dict[str, Any]] = []
    for step in order:
        if step == "append":
            valid.add("new")
        elif step == "store":
            vault = "new"
        elif step == "refresh":
            presented = vault
        elif step == "delete_old":
            valid.discard("old")
        timeline.append(
            {
                "step": step,
                "presented": presented,
                "valid": sorted(valid),
                "signInOk": presented in valid,
            }
        )
    return timeline


def review_status(record: Mapping[str, Any], now: dt.datetime) -> list[str]:
    """Problems that stop an access review record counting as completed and current."""
    assert_no_secret_material(record, path="$.record")
    problems: list[str] = []
    if not str(record.get("reviewer") or "").strip():
        problems.append("no reviewer recorded")
    rows = record.get("assignments", [])
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)) or not rows:
        problems.append("no assignments recorded")
        rows = []
    for row in rows:
        if not isinstance(row, Mapping):
            problems.append("invalid assignment row")
            continue
        if row.get("decision") not in VALID_ASSIGNMENT_DECISIONS:
            pid_tok = _safe_token(row.get("principalId"), "<invalid-principal>")
            problems.append(f"{pid_tok}: decision is not finalized, needs keep or remove")
    due = record.get("nextReviewDue")
    if not due:
        problems.append("no nextReviewDue date")
    else:
        due_str = str(due).strip() if isinstance(due, str) else ""
        try:
            if len(due_str) != 10:
                raise ValueError("expected YYYY-MM-DD")
            due_date = dt.date.fromisoformat(due_str)
            if now.astimezone(dt.UTC).date() > due_date:
                problems.append(f"review overdue since {due_str}")
        except ValueError:
            problems.append("invalid nextReviewDue date")
    return problems


def _extract_secret_uri_parts(
    uri: str,
) -> tuple[str | None, str | None, str | None]:
    parsed = urlparse(uri.strip())
    if parsed.scheme.lower() != "https" or not parsed.netloc.lower().endswith(".vault.azure.net"):
        return None, None, None
    vault_host = parsed.netloc.lower().removesuffix(".vault.azure.net")
    parts = [seg for seg in parsed.path.split("/") if seg]
    if len(parts) == 2 and parts[0] == "secrets":
        return vault_host, parts[1], None
    if len(parts) == 3 and parts[0] == "secrets":
        return vault_host, parts[1], parts[2]
    return None, None, None


def _compute_overlap_minutes(
    start_a: dt.datetime,
    end_a: dt.datetime,
    start_b: dt.datetime,
    end_b: dt.datetime,
) -> float:
    overlap_start = max(start_a, start_b)
    overlap_end = min(end_a, end_b)
    if overlap_end <= overlap_start:
        return 0.0
    return round((overlap_end - overlap_start).total_seconds() / 60.0, 2)


def _validate_probe_batch(
    batch: Mapping[str, Any],
    *,
    now_utc: dt.datetime,
    browser_mode: bool,
    require_authenticated_probe: bool,
    require_fresh_token_exchange: bool = False,
    min_probe_samples: int = 3,
    min_probe_span_seconds: int = 60,
    max_probe_gap_seconds: int = 60,
) -> tuple[list[str], dt.datetime | None, dt.datetime | None]:
    issues: list[str] = []
    raw_stage = batch.get("stage")
    if isinstance(raw_stage, str) and raw_stage in VALID_ROTATION_STAGES:
        stage_label = raw_stage
    else:
        stage_label = "<invalid-stage>"
        issues.append("probe[<invalid-stage>]: invalid healthProbes stage")
    raw_total = batch.get("totalSamples")
    total_samples: int | None = None
    if isinstance(raw_total, bool) or not isinstance(raw_total, int):
        issues.append(
            f"probe[{stage_label}]: totalSamples must be an integer >= {min_probe_samples}"
        )
    else:
        total_samples = raw_total
        if total_samples < min_probe_samples:
            issues.append(f"probe[{stage_label}]: totalSamples must be >= {min_probe_samples}")

    raw_errors = batch.get("errorCount")
    if isinstance(raw_errors, bool) or not isinstance(raw_errors, int) or raw_errors < 0:
        issues.append(f"probe[{stage_label}]: errorCount must be a non-negative integer")
    elif raw_errors != 0:
        issues.append(f"probe[{stage_label}]: observed {raw_errors} error/auth-drop samples")

    first_dt: dt.datetime | None = None
    last_dt: dt.datetime | None = None
    raw_first = batch.get("firstSampleAt")
    raw_last = batch.get("lastSampleAt")
    if not isinstance(raw_first, str) or not raw_first.strip():
        issues.append(
            f"probe[{stage_label}]: firstSampleAt timezone-aware ISO-8601 timestamp is required"
        )
    else:
        try:
            first_dt = parse_time(raw_first)
        except (ValueError, TypeError):
            issues.append(
                f"probe[{stage_label}]: firstSampleAt is not a valid "
                "timezone-aware ISO-8601 timestamp"
            )
    if not isinstance(raw_last, str) or not raw_last.strip():
        issues.append(
            f"probe[{stage_label}]: lastSampleAt timezone-aware ISO-8601 timestamp is required"
        )
    else:
        try:
            last_dt = parse_time(raw_last)
        except (ValueError, TypeError):
            issues.append(
                f"probe[{stage_label}]: lastSampleAt is not a valid "
                "timezone-aware ISO-8601 timestamp"
            )

    raw_gap = batch.get("maxGapSeconds")
    max_gap: float | None = None
    if (
        isinstance(raw_gap, bool)
        or not isinstance(raw_gap, (int, float))
        or not math.isfinite(float(raw_gap))
    ):
        issues.append(f"probe[{stage_label}]: maxGapSeconds finite numeric bound is required")
    elif float(raw_gap) <= 0.0 or float(raw_gap) > float(max_probe_gap_seconds):
        issues.append(
            f"probe[{stage_label}]: maxGapSeconds must be > 0 and <= {max_probe_gap_seconds}"
        )
    else:
        max_gap = float(raw_gap)

    valid_window: tuple[dt.datetime, dt.datetime] | None = None
    if first_dt is not None and last_dt is not None:
        if last_dt <= first_dt:
            issues.append(f"probe[{stage_label}]: lastSampleAt must be after firstSampleAt")
        else:
            valid_window = (first_dt, last_dt)
            if last_dt > now_utc:
                issues.append(
                    f"probe[{stage_label}]: lastSampleAt cannot be in the future relative to now"
                )
            span_s = (last_dt - first_dt).total_seconds()
            if span_s < float(min_probe_span_seconds):
                issues.append(
                    f"probe[{stage_label}]: sample window {span_s:.1f}s is shorter than "
                    f"required {min_probe_span_seconds}s"
                )
            if total_samples is not None and total_samples >= 2 and max_gap is not None:
                if (total_samples - 1) * max_gap + 1e-6 < span_s:
                    issues.append(
                        f"probe[{stage_label}]: totalSamples={total_samples} with "
                        f"maxGapSeconds={max_gap} cannot cover {span_s:.1f}s window"
                    )

    hz_status = batch.get("healthzStatus")
    if isinstance(hz_status, bool) or hz_status != 200:
        issues.append(
            f"probe[{stage_label}]: /healthz returned {_fmt_http_status(hz_status)}, expected 200"
        )
    anon_status = batch.get("anonymousApiStatus")
    if isinstance(anon_status, bool) or anon_status != 401:
        issues.append(
            f"probe[{stage_label}]: anonymous /api/me returned "
            f"{_fmt_http_status(anon_status)}, expected exact 401"
        )
    redir_status = batch.get("signInRedirectStatus")
    if browser_mode and (isinstance(redir_status, bool) or redir_status != 302):
        issues.append(
            f"probe[{stage_label}]: /sign-in returned "
            f"{_fmt_http_status(redir_status)}, expected 302"
        )
    auth_status = batch.get("authenticatedApiStatus")
    if require_authenticated_probe:
        if isinstance(auth_status, bool) or auth_status != 200:
            issues.append(
                f"probe[{stage_label}]: authenticated session probe returned "
                f"{_fmt_http_status(auth_status)}, expected 200 to prove "
                "Entra client-secret token exchange"
            )
        if require_fresh_token_exchange and batch.get("freshTokenExchangeVerified") is not True:
            issues.append(
                f"probe[{stage_label}]: freshTokenExchangeVerified must be true to prove "
                "live Entra OAuth token exchange rather than cached session reuse"
            )
    elif auth_status is not None and (isinstance(auth_status, bool) or auth_status != 200):
        issues.append(
            f"probe[{stage_label}]: authenticated session probe returned "
            f"{_fmt_http_status(auth_status)}, expected 200"
        )
    if valid_window is not None:
        return issues, valid_window[0], valid_window[1]
    return issues, None, None


def _validate_stage_probe_batches(
    batches: Sequence[Mapping[str, Any]],
    *,
    stage_label: str,
    now_utc: dt.datetime,
    browser_mode: bool,
    require_authenticated_probe: bool,
    require_fresh_token_exchange: bool,
    min_probe_samples: int,
    min_probe_span_seconds: int,
    max_probe_gap_seconds: int,
) -> tuple[list[str], tuple[dt.datetime, dt.datetime] | None]:
    issues: list[str] = []
    windows: list[tuple[dt.datetime, dt.datetime]] = []
    for batch in batches:
        b_issues, b_start, b_end = _validate_probe_batch(
            batch,
            now_utc=now_utc,
            browser_mode=browser_mode,
            require_authenticated_probe=require_authenticated_probe,
            require_fresh_token_exchange=require_fresh_token_exchange,
            min_probe_samples=min_probe_samples,
            min_probe_span_seconds=min_probe_span_seconds,
            max_probe_gap_seconds=max_probe_gap_seconds,
        )
        issues.extend(b_issues)
        if b_start is not None and b_end is not None:
            windows.append((b_start, b_end))
    if len(windows) != len(batches) or not windows:
        return issues, None
    windows.sort(key=lambda pair: (pair[0], pair[1]))
    for idx in range(1, len(windows)):
        prev_end = windows[idx - 1][1]
        next_start = windows[idx][0]
        gap_s = (next_start - prev_end).total_seconds()
        if gap_s < 0.0:
            issues.append(f"probe[{stage_label}]: overlapping probe batches within stage")
        elif gap_s > float(max_probe_gap_seconds):
            issues.append(
                f"probe[{stage_label}]: inter-batch gap {gap_s:.1f}s exceeds "
                f"max_probe_gap_seconds={max_probe_gap_seconds}"
            )
    return issues, (windows[0][0], windows[-1][1])


def _parse_non_negative_float(raw: Any) -> float | None:
    if isinstance(raw, bool) or not isinstance(raw, (int, float)):
        return None
    val = float(raw)
    return val if math.isfinite(val) and val >= 0.0 else None


def _parse_required_utc(
    mapping: Mapping[str, Any], key: str, *, label: str, problems: list[str]
) -> dt.datetime | None:
    raw = mapping.get(key)
    if not isinstance(raw, str) or not raw.strip():
        problems.append(f"{label}.{key} timezone-aware ISO-8601 timestamp is required")
        return None
    try:
        return parse_time(raw)
    except (ValueError, TypeError):
        problems.append(f"{label}.{key} is not a valid timezone-aware ISO-8601 timestamp")
        return None


def _parse_single_created_value(val: Any) -> dt.datetime | None:
    if isinstance(val, bool):
        return None
    if isinstance(val, str):
        if not val.strip():
            return None
        try:
            return parse_time(val)
        except (ValueError, TypeError):
            return None
    if isinstance(val, (int, float)):
        fval = float(val)
        if not math.isfinite(fval) or fval <= 0.0:
            return None
        try:
            return dt.datetime.fromtimestamp(fval, tz=dt.UTC)
        except (OverflowError, OSError, ValueError):
            return None
    return None


def _parse_kv_version_created(
    row: Mapping[str, Any], *, label: str, now_utc: dt.datetime
) -> tuple[dt.datetime | None, str | None]:
    parsed_candidates: list[dt.datetime] = []
    for field_name in ("created", "createdAt"):
        if field_name in row and row.get(field_name) is not None:
            cand = _parse_single_created_value(row.get(field_name))
            if cand is None:
                return None, f"{label}.{field_name} is not a valid UTC timestamp"
            parsed_candidates.append(cand)
    if "attributes" in row and row.get("attributes") is not None:
        attrs = row.get("attributes")
        if not isinstance(attrs, Mapping):
            return None, f"{label} attributes must be a mapping"
        if "created" in attrs and attrs.get("created") is not None:
            attr_cand = _parse_single_created_value(attrs.get("created"))
            if attr_cand is None:
                return None, f"{label}.attributes.created is not a valid UTC timestamp"
            parsed_candidates.append(attr_cand)
    if not parsed_candidates:
        return None, f"{label} created timestamp is required"
    first = parsed_candidates[0]
    for other in parsed_candidates[1:]:
        if other != first:
            return None, f"{label} created timestamp conflicts across metadata fields"
    if first > now_utc:
        return None, f"{label} created timestamp cannot be in the future"
    return first, None


def _parse_strict_enabled(row: Mapping[str, Any], *, label: str) -> tuple[bool | None, str | None]:
    has_top = "enabled" in row
    top_val = row.get("enabled")
    if has_top and not isinstance(top_val, bool):
        return None, f"{label} enabled must be a boolean"

    has_attr = False
    attr_val: Any = None
    if "attributes" in row and row.get("attributes") is not None:
        attrs = row.get("attributes")
        if not isinstance(attrs, Mapping):
            return None, f"{label} attributes must be a mapping"
        if "enabled" in attrs:
            has_attr = True
            attr_val = attrs.get("enabled")
            if not isinstance(attr_val, bool):
                return None, f"{label} attributes.enabled must be a boolean"

    if has_top and has_attr and top_val != attr_val:
        return None, f"{label} enabled conflicts with attributes.enabled"
    if has_top:
        assert isinstance(top_val, bool)
        return top_val, None
    if has_attr:
        assert isinstance(attr_val, bool)
        return attr_val, None
    return True, None


def _normalize_rotation_signing_key(signing_key: str | bytes | bytearray) -> bytes:
    if isinstance(signing_key, bool) or not isinstance(signing_key, (str, bytes, bytearray)):
        raise SecretLifecycleError("rotation signing_key must be bytes or str of at least 32 bytes")
    raw = (
        signing_key.strip().encode("utf-8")
        if isinstance(signing_key, str)
        else bytes(signing_key).strip()
    )
    if len(raw) < 32:
        raise SecretLifecycleError("rotation signing_key must be at least 32 bytes")
    return raw


def _compute_rotation_receipt_signature(
    receipt_payload: Mapping[str, Any], key_bytes: bytes
) -> str:
    unsigned = {
        k: v for k, v in receipt_payload.items() if k not in {"signature", "signatureAlgorithm"}
    }
    digest = _sha256_canonical(unsigned)
    return hmac.new(key_bytes, digest.encode("ascii"), hashlib.sha256).hexdigest()


def verify_staged_entra_rotation(
    evidence: Mapping[str, Any],
    *,
    now: dt.datetime,
    min_overlap_minutes: int = 60,
    max_validity_days: int = 366,
    require_browser_mode: bool = True,
    signing_key: str | bytes | bytearray | None = None,
    min_probe_samples: int = 3,
    min_probe_span_seconds: int = 60,
    max_probe_gap_seconds: int = 60,
) -> dict[str, Any]:
    """Verify dual-secret overlap, version switchover, probes, and rollback without secrets."""
    assert_no_secret_material(evidence, path="$.evidence")
    if not isinstance(require_browser_mode, bool):
        raise SecretLifecycleError("require_browser_mode must be a boolean")
    if (
        isinstance(min_probe_samples, bool)
        or not isinstance(min_probe_samples, int)
        or min_probe_samples < 2
    ):
        raise SecretLifecycleError("min_probe_samples must be an integer >= 2")
    if (
        isinstance(min_probe_span_seconds, bool)
        or not isinstance(min_probe_span_seconds, int)
        or min_probe_span_seconds < 1
    ):
        raise SecretLifecycleError("min_probe_span_seconds must be an integer >= 1")
    if (
        isinstance(max_probe_gap_seconds, bool)
        or not isinstance(max_probe_gap_seconds, int)
        or max_probe_gap_seconds < 1
    ):
        raise SecretLifecycleError("max_probe_gap_seconds must be an integer >= 1")
    norm_key = _normalize_rotation_signing_key(signing_key) if signing_key is not None else None
    if min_overlap_minutes < 1:
        raise SecretLifecycleError("min_overlap_minutes must be >= 1")
    if now.tzinfo is None:
        raise SecretLifecycleError("now must include an explicit timezone offset")
    now_utc = now.astimezone(dt.UTC)

    problems: list[str] = []
    raw_top_stage = evidence.get("stage")
    stage = raw_top_stage.strip() if isinstance(raw_top_stage, str) else ""
    if stage not in VALID_ROTATION_STAGES:
        problems.append("invalid rotation stage")

    vault_name = str(evidence.get("vaultName") or "").strip()
    if not _VAULT_NAME_RE.match(vault_name):
        problems.append("vaultName must be 3-24 alphanumeric or hyphen characters")
    secret_name = str(evidence.get("secretName") or "").strip()
    if not secret_name:
        problems.append("secretName is required")
    prior_secret_name = str(evidence.get("priorSecretName") or secret_name).strip()
    app_id = str(evidence.get("appId") or "").strip()
    if not app_id:
        problems.append("appId is required")
    expected_identity = str(evidence.get("expectedIdentityId") or "").strip()
    if not expected_identity:
        problems.append("expectedIdentityId is required")
    raw_browser_mode = evidence.get("browserMode", True)
    if not isinstance(raw_browser_mode, bool):
        problems.append("browserMode must be a boolean")
        browser_mode = True
    else:
        browser_mode = raw_browser_mode
        if require_browser_mode and not browser_mode:
            problems.append(
                "browserMode=false is not permitted when require_browser_mode is enabled"
            )
    effective_browser_mode = True if require_browser_mode else browser_mode

    overlap_minutes = 0.0
    elapsed_overlap_minutes = 0.0
    overlap_ok = False
    needs_receipt_overlap_check = False
    overlap_start_dt: dt.datetime | None = None
    p_start_dt: dt.datetime | None = None
    rp_end_dt: dt.datetime | None = None
    effective_retired_at: dt.datetime | None = None
    creds = evidence.get("credentials")
    prior_key_id = ""
    next_key_id = ""
    prior_cred_active = False

    if not isinstance(creds, Mapping):
        problems.append("credentials metadata mapping is required")
    else:
        prior_key_id = str(creds.get("priorKeyId") or "").strip()
        next_key_id = str(creds.get("nextKeyId") or "").strip()
        safe_prior_kid = _safe_token(prior_key_id, "<invalid-key-id>")
        safe_next_kid = _safe_token(next_key_id, "<invalid-key-id>")
        if not prior_key_id or not next_key_id:
            problems.append("credentials.priorKeyId and credentials.nextKeyId are required")
        elif prior_key_id == next_key_id:
            problems.append("credentials.priorKeyId and credentials.nextKeyId must differ")

        raw_entries = creds.get("entries", [])
        cred_by_id: dict[str, Mapping[str, Any]] = {}
        cred_enabled_by_id: dict[str, bool] = {}
        if isinstance(raw_entries, Sequence) and not isinstance(raw_entries, (str, bytes)):
            for idx, row in enumerate(raw_entries):
                if not isinstance(row, Mapping):
                    problems.append(f"credentials.entries[{idx}] must be a metadata mapping")
                    continue
                en_flag, en_err = _parse_strict_enabled(row, label=f"credentials.entries[{idx}]")
                if en_err is not None:
                    problems.append(en_err)
                    continue
                assert en_flag is not None
                if row.get("keyId"):
                    kid = str(row["keyId"])
                    cred_by_id[kid] = row
                    cred_enabled_by_id[kid] = en_flag
        else:
            problems.append("credentials.entries must be a list")

        prior_row = cred_by_id.get(prior_key_id)
        next_row = cred_by_id.get(next_key_id)

        if stage in {"dual_secret_overlap", "post_switchover"}:
            if prior_row is None:
                problems.append(f"prior Entra credential {safe_prior_kid} missing during {stage}")
            if next_row is None:
                problems.append(f"next Entra credential {safe_next_kid} missing during {stage}")
            if prior_row is not None and next_row is not None:
                p_start = _parse_required_utc(
                    prior_row, "startDateTime", label="priorCredential", problems=problems
                )
                p_end = _parse_required_utc(
                    prior_row, "endDateTime", label="priorCredential", problems=problems
                )
                n_start = _parse_required_utc(
                    next_row, "startDateTime", label="nextCredential", problems=problems
                )
                n_end = _parse_required_utc(
                    next_row, "endDateTime", label="nextCredential", problems=problems
                )
                if (
                    p_start is not None
                    and p_end is not None
                    and n_start is not None
                    and n_end is not None
                ):
                    p_start_dt = p_start
                    overlap_start_dt = max(p_start, n_start)
                    p_enabled = cred_enabled_by_id.get(prior_key_id, True)
                    n_enabled = cred_enabled_by_id.get(next_key_id, True)
                    prior_cred_active = p_enabled and (p_start <= now_utc < p_end)
                    next_cred_active = n_enabled and (n_start <= now_utc < n_end)
                    if not prior_cred_active:
                        problems.append(
                            f"prior Entra credential {safe_prior_kid} is not active at now"
                        )
                    if not next_cred_active:
                        problems.append(
                            f"next Entra credential {safe_next_kid} is not active at now"
                        )
                    if (n_end - n_start) > dt.timedelta(days=max_validity_days):
                        problems.append(
                            f"next Entra credential {safe_next_kid} exceeds "
                            f"{max_validity_days}d lifetime"
                        )
                    overlap_minutes = _compute_overlap_minutes(p_start, p_end, n_start, n_end)
                    elapsed_overlap_minutes = _compute_overlap_minutes(
                        p_start, min(p_end, now_utc), n_start, min(n_end, now_utc)
                    )
                    if overlap_minutes < float(min_overlap_minutes):
                        problems.append(
                            f"dual-secret overlap {overlap_minutes}m is below "
                            f"required {min_overlap_minutes}m"
                        )
                    elif stage == "post_switchover" and elapsed_overlap_minutes < float(
                        min_overlap_minutes
                    ):
                        problems.append(
                            f"elapsed dual-secret overlap {elapsed_overlap_minutes}m at now "
                            f"is below required {min_overlap_minutes}m"
                        )
                    elif prior_cred_active and next_cred_active:
                        overlap_ok = True
        elif stage == "rollback":
            if prior_row is None:
                problems.append(
                    f"prior Entra credential {safe_prior_kid} missing; rollback cannot authenticate"
                )
            else:
                p_start = _parse_required_utc(
                    prior_row, "startDateTime", label="priorCredential", problems=problems
                )
                p_end = _parse_required_utc(
                    prior_row, "endDateTime", label="priorCredential", problems=problems
                )
                if p_start is not None and p_end is not None:
                    p_start_dt = p_start
                    p_enabled = cred_enabled_by_id.get(prior_key_id, True)
                    prior_cred_active = p_enabled and (p_start <= now_utc < p_end)
                    if not prior_cred_active:
                        problems.append(
                            f"prior Entra credential {safe_prior_kid} expired/inactive "
                            "during rollback"
                        )
                    if next_row is not None:
                        n_start = _parse_required_utc(
                            next_row, "startDateTime", label="nextCredential", problems=problems
                        )
                        n_end = _parse_required_utc(
                            next_row, "endDateTime", label="nextCredential", problems=problems
                        )
                        if n_start is not None and n_end is not None:
                            overlap_minutes = _compute_overlap_minutes(
                                p_start, p_end, n_start, n_end
                            )
                            elapsed_overlap_minutes = _compute_overlap_minutes(
                                p_start, min(p_end, now_utc), n_start, min(n_end, now_utc)
                            )
        elif stage == "post_retire":
            if prior_row is not None:
                problems.append(
                    f"prior Entra credential {safe_prior_kid} is still present in post_retire"
                )
            if next_row is None:
                problems.append(f"next Entra credential {safe_next_kid} missing in post_retire")
            else:
                n_start = _parse_required_utc(
                    next_row, "startDateTime", label="nextCredential", problems=problems
                )
                n_end = _parse_required_utc(
                    next_row, "endDateTime", label="nextCredential", problems=problems
                )
                if n_start is not None and n_end is not None:
                    n_enabled = cred_enabled_by_id.get(next_key_id, True)
                    if not (n_enabled and n_start <= now_utc < n_end):
                        problems.append(
                            f"next Entra credential {safe_next_kid} is not active at now"
                        )
                    if (n_end - n_start) > dt.timedelta(days=max_validity_days):
                        problems.append(
                            f"next Entra credential {safe_next_kid} exceeds "
                            f"{max_validity_days}d lifetime"
                        )

                retired_at_from_struct: dt.datetime | None = None
                retired_prior = creds.get("retiredPriorCredential")
                if retired_prior is not None:
                    if not isinstance(retired_prior, Mapping):
                        problems.append("credentials.retiredPriorCredential must be a mapping")
                    else:
                        r_key = str(retired_prior.get("keyId") or "")
                        if r_key != prior_key_id:
                            problems.append(
                                "retiredPriorCredential.keyId does not match priorKeyId"
                            )
                        else:
                            rp_start = _parse_required_utc(
                                retired_prior,
                                "startDateTime",
                                label="retiredPriorCredential",
                                problems=problems,
                            )
                            rp_end = _parse_required_utc(
                                retired_prior,
                                "endDateTime",
                                label="retiredPriorCredential",
                                problems=problems,
                            )
                            retired_at_from_struct = _parse_required_utc(
                                retired_prior,
                                "retiredAt",
                                label="retiredPriorCredential",
                                problems=problems,
                            )
                            if (
                                rp_start is not None
                                and rp_end is not None
                                and retired_at_from_struct is not None
                                and n_start is not None
                                and n_end is not None
                            ):
                                rp_end_dt = rp_end
                                overlap_start_dt = max(rp_start, n_start)
                                if retired_at_from_struct > now_utc:
                                    problems.append(
                                        "retiredPriorCredential.retiredAt cannot be in the future"
                                    )
                                overlap_minutes = _compute_overlap_minutes(
                                    rp_start,
                                    min(rp_end, retired_at_from_struct),
                                    n_start,
                                    min(n_end, retired_at_from_struct),
                                )
                                elapsed_overlap_minutes = _compute_overlap_minutes(
                                    rp_start,
                                    min(rp_end, retired_at_from_struct, now_utc),
                                    n_start,
                                    min(n_end, retired_at_from_struct, now_utc),
                                )
                                if retired_at_from_struct <= now_utc:
                                    if elapsed_overlap_minutes < float(min_overlap_minutes):
                                        problems.append(
                                            f"pre-retirement overlap {elapsed_overlap_minutes}m "
                                            f"is below required {min_overlap_minutes}m"
                                        )
                                    else:
                                        overlap_ok = True
                else:
                    needs_receipt_overlap_check = True

                prior_retired_prop_dt: dt.datetime | None = None
                if "priorRetiredAt" in creds and creds.get("priorRetiredAt") is not None:
                    prior_retired_prop_dt = _parse_required_utc(
                        creds,
                        "priorRetiredAt",
                        label="credentials",
                        problems=problems,
                    )
                if (
                    retired_at_from_struct is not None
                    and prior_retired_prop_dt is not None
                    and retired_at_from_struct != prior_retired_prop_dt
                ):
                    problems.append(
                        "credentials.priorRetiredAt conflicts with retiredPriorCredential.retiredAt"
                    )
                effective_retired_at = (
                    retired_at_from_struct
                    if retired_at_from_struct is not None
                    else prior_retired_prop_dt
                )
                if effective_retired_at is None:
                    problems.append(
                        "post_retire requires retiredPriorCredential.retiredAt or "
                        "credentials.priorRetiredAt"
                    )
                elif effective_retired_at > now_utc and retired_at_from_struct is None:
                    problems.append("credentials.priorRetiredAt cannot be in the future")

    versions = evidence.get("secretVersions")
    prior_version_id = ""
    next_version_id = ""
    prior_version_enabled = False
    kv_versions_ok = False
    before_kv_problems = len(problems)
    ver_enabled_by_id: dict[str, bool] = {}
    ver_secret_by_id: dict[str, str] = {}
    ver_created_by_id: dict[str, dt.datetime] = {}

    if not isinstance(versions, Mapping):
        problems.append("secretVersions metadata mapping is required")
    else:
        prior_version_id = str(versions.get("priorVersionId") or "").strip()
        next_version_id = str(versions.get("nextVersionId") or "").strip()
        if not prior_version_id or not next_version_id:
            problems.append(
                "secretVersions.priorVersionId and secretVersions.nextVersionId are required"
            )
        elif prior_version_id == next_version_id:
            problems.append("priorVersionId and nextVersionId must differ")

        raw_ver_entries = versions.get("entries", [])
        ver_by_id: dict[str, Mapping[str, Any]] = {}
        if isinstance(raw_ver_entries, Sequence) and not isinstance(raw_ver_entries, (str, bytes)):
            for idx, row in enumerate(raw_ver_entries):
                if not isinstance(row, Mapping):
                    problems.append("secretVersions.entries must contain metadata mappings")
                    continue
                en_flag, en_err = _parse_strict_enabled(row, label=f"secretVersions.entries[{idx}]")
                if en_err is not None:
                    problems.append(en_err)
                    continue
                assert en_flag is not None
                created_dt, created_err = _parse_kv_version_created(
                    row, label=f"secretVersions.entries[{idx}]", now_utc=now_utc
                )
                if created_err is not None:
                    problems.append(created_err)
                    continue
                assert created_dt is not None
                ver_id = str(row.get("version") or "").strip()
                uri = str(row.get("id") or "").strip()
                if not uri:
                    problems.append(
                        f"secretVersions.entries[{idx}] missing versioned Key Vault id URI"
                    )
                    continue
                v_host, v_sec, v_ver = _extract_secret_uri_parts(uri)
                if v_host is None or v_sec is None or v_ver is None or v_host != vault_name.lower():
                    problems.append(
                        f"secretVersions.entries[{idx}].id is not a valid versioned "
                        "Key Vault URI for expected vault"
                    )
                    continue
                if not ver_id:
                    ver_id = v_ver
                elif v_ver != ver_id:
                    problems.append(
                        f"secretVersions.entries[{idx}] version conflicts with versioned id URI"
                    )
                    continue
                explicit_sec = str(row.get("secretName") or "").strip()
                if explicit_sec and explicit_sec.lower() != v_sec.lower():
                    problems.append(
                        f"secretVersions.entries[{idx}] secretName conflicts with versioned id URI"
                    )
                    continue
                if ver_id == prior_version_id and v_sec.lower() != prior_secret_name.lower():
                    problems.append("priorVersionId URI does not target expected priorSecretName")
                if ver_id == next_version_id and v_sec.lower() != secret_name.lower():
                    problems.append("nextVersionId URI does not target expected secretName")
                if ver_id in ver_by_id:
                    problems.append(f"duplicate secretVersions.entries[{idx}] version identifier")
                    continue
                ver_by_id[ver_id] = row
                ver_enabled_by_id[ver_id] = en_flag
                ver_secret_by_id[ver_id] = v_sec.lower()
                ver_created_by_id[ver_id] = created_dt
        else:
            problems.append("secretVersions.entries must be a list")

        prior_ver = ver_by_id.get(prior_version_id)
        next_ver = ver_by_id.get(next_version_id)

        if prior_ver is None:
            problems.append("Key Vault priorVersionId missing or invalid in secretVersions.entries")
        else:
            prior_version_enabled = ver_enabled_by_id[prior_version_id]
            if stage in {"dual_secret_overlap", "post_switchover", "rollback"}:
                if not prior_version_enabled:
                    problems.append(f"Key Vault priorVersionId must stay enabled in {stage}")
                p_exp = _parse_required_utc(
                    prior_ver, "expires", label="priorVersion", problems=problems
                )
                if p_exp is not None and p_exp <= now_utc:
                    problems.append("Key Vault priorVersionId must have future expiry")
            elif stage == "post_retire" and prior_version_enabled:
                problems.append("Key Vault priorVersionId must be disabled in post_retire")

        if next_ver is None:
            if stage != "rollback":
                problems.append(
                    "Key Vault nextVersionId missing or invalid in secretVersions.entries"
                )
        elif stage != "rollback":
            if not ver_enabled_by_id[next_version_id]:
                problems.append("Key Vault nextVersionId is disabled")
            n_exp = _parse_required_utc(next_ver, "expires", label="nextVersion", problems=problems)
            if n_exp is not None:
                if n_exp <= now_utc:
                    problems.append("Key Vault nextVersionId is already expired")
                elif (n_exp - now_utc) > dt.timedelta(days=max_validity_days):
                    problems.append(f"Key Vault nextVersionId expiry exceeds {max_validity_days}d")

        if (
            stage != "rollback"
            and prior_secret_name.lower() == secret_name.lower()
            and prior_version_id in ver_created_by_id
            and next_version_id in ver_created_by_id
            and ver_created_by_id[next_version_id] <= ver_created_by_id[prior_version_id]
        ):
            problems.append(
                "Key Vault nextVersionId must have a newer created timestamp than priorVersionId"
            )

        kv_versions_ok = len(problems) == before_kv_problems

    prior_ver_created_dt = ver_created_by_id.get(prior_version_id)
    next_ver_created_dt = ver_created_by_id.get(next_version_id)

    version_switchover_verified = False
    rollback_revision_restored = False
    switchover_dt: dt.datetime | None = None
    rollback_dt: dt.datetime | None = None
    app = evidence.get("containerApp")
    if not isinstance(app, Mapping):
        problems.append("containerApp metadata mapping is required")
    else:
        before_app_binding_problems = len(problems)
        setting_name = str(app.get("clientSecretSettingName") or "").strip()
        if not setting_name:
            problems.append("containerApp.clientSecretSettingName is required")
        raw_secrets = app.get("secrets", [])
        matched_secret: Mapping[str, Any] | None = None
        if isinstance(raw_secrets, Sequence) and not isinstance(raw_secrets, (str, bytes)):
            for sec in raw_secrets:
                if isinstance(sec, Mapping) and str(sec.get("name") or "") == setting_name:
                    matched_secret = sec
                    break
        if matched_secret is None:
            problems.append("containerApp.secrets missing configured clientSecretSettingName")
        else:
            sec_identity = str(matched_secret.get("identity") or "").strip()
            if sec_identity.lower() != expected_identity.lower():
                problems.append("containerApp secret identity does not match expectedIdentityId")
            kv_url = str(matched_secret.get("keyVaultUrl") or "").strip()
            u_vault, u_sec, u_ver = _extract_secret_uri_parts(kv_url)
            if u_vault != vault_name.lower() or u_sec is None:
                problems.append("containerApp secret keyVaultUrl does not target expected vault")
            elif stage in {"post_switchover", "post_retire"}:
                if u_sec.lower() != secret_name.lower():
                    problems.append(
                        "containerApp secret keyVaultUrl does not target expected secretName"
                    )
                if u_ver is not None:
                    if u_ver != next_version_id:
                        problems.append(
                            "containerApp secret keyVaultUrl version pin does not match "
                            "nextVersionId"
                        )
                else:
                    newer_or_equal_on_secret = [
                        vid
                        for vid, c_dt in ver_created_by_id.items()
                        if vid != next_version_id
                        and ver_secret_by_id.get(vid) == secret_name.lower()
                        and (next_ver_created_dt is None or c_dt >= next_ver_created_dt)
                    ]
                    if next_ver_created_dt is None or newer_or_equal_on_secret:
                        problems.append(
                            "versionless keyVaultUrl requires nextVersionId to be the newest "
                            "secret version on secretName"
                        )
            elif stage == "rollback":
                if u_sec.lower() != prior_secret_name.lower():
                    problems.append(
                        "rollback containerApp secret keyVaultUrl does not target priorSecretName"
                    )
                elif u_ver is not None:
                    if u_ver != prior_version_id:
                        problems.append(
                            "rollback containerApp secret keyVaultUrl version pin does not match "
                            "priorVersionId"
                        )
                elif prior_secret_name.lower() == secret_name.lower():
                    problems.append(
                        "rollback for in-place secretName requires version-pinned priorVersionId "
                        "keyVaultUrl because Key Vault versionless resolution returns "
                        "SecretDisabled when the newest version is disabled"
                    )
                else:
                    other_enabled_on_prior = [
                        vid
                        for vid, is_en in ver_enabled_by_id.items()
                        if is_en
                        and vid != prior_version_id
                        and ver_secret_by_id.get(vid) == prior_secret_name.lower()
                    ]
                    newer_or_equal_on_prior = [
                        vid
                        for vid, c_dt in ver_created_by_id.items()
                        if vid != prior_version_id
                        and ver_secret_by_id.get(vid) == prior_secret_name.lower()
                        and (prior_ver_created_dt is None or c_dt >= prior_ver_created_dt)
                    ]
                    if (
                        other_enabled_on_prior
                        or prior_ver_created_dt is None
                        or newer_or_equal_on_prior
                    ):
                        problems.append(
                            "rollback with versionless priorSecretName keyVaultUrl requires "
                            "priorVersionId to be the newest and sole enabled version on "
                            "priorSecretName"
                        )
            elif stage == "dual_secret_overlap" and u_sec.lower() not in {
                secret_name.lower(),
                prior_secret_name.lower(),
            }:
                problems.append("containerApp secret keyVaultUrl targets unexpected secret path")

        if stage in {"post_switchover", "post_retire"}:
            switchover_dt = _parse_required_utc(
                app, "switchoverAt", label="containerApp", problems=problems
            )
            if switchover_dt is not None:
                if switchover_dt > now_utc:
                    problems.append("containerApp.switchoverAt cannot be in the future")
                if next_ver_created_dt is not None and switchover_dt < next_ver_created_dt:
                    problems.append(
                        "containerApp.switchoverAt cannot precede nextVersionId created timestamp"
                    )
                if overlap_start_dt is not None and switchover_dt < (
                    overlap_start_dt + dt.timedelta(minutes=min_overlap_minutes)
                ):
                    problems.append(
                        "containerApp.switchoverAt precedes completion of required "
                        f"{min_overlap_minutes}m dual-secret overlap window"
                    )
                if rp_end_dt is not None and switchover_dt > rp_end_dt:
                    problems.append(
                        "containerApp.switchoverAt exceeds prior Entra credential endDateTime"
                    )
                if effective_retired_at is not None and effective_retired_at < switchover_dt:
                    problems.append(
                        "post_retire retirement timestamp cannot precede containerApp.switchoverAt"
                    )
        elif stage == "rollback":
            rollback_dt = _parse_required_utc(
                app, "rollbackAt", label="containerApp", problems=problems
            )
            if rollback_dt is not None:
                if rollback_dt > now_utc:
                    problems.append("containerApp.rollbackAt cannot be in the future")
                if p_start_dt is not None and rollback_dt < p_start_dt:
                    problems.append(
                        "containerApp.rollbackAt cannot precede prior Entra credential "
                        "startDateTime"
                    )

        app_binding_ok = len(problems) == before_app_binding_problems

        raw_revisions = app.get("revisions", [])
        serving_revisions: list[Mapping[str, Any]] = []
        total_weight = 0
        rev_meta_ok = True
        if isinstance(raw_revisions, Sequence) and not isinstance(raw_revisions, (str, bytes)):
            for idx, rev in enumerate(raw_revisions):
                if not isinstance(rev, Mapping):
                    problems.append(f"containerApp.revisions[{idx}] must be a mapping")
                    rev_meta_ok = False
                    continue
                active_val = rev.get("active", True)
                if not isinstance(active_val, bool):
                    problems.append(f"containerApp.revisions[{idx}].active must be a boolean")
                    rev_meta_ok = False
                    continue
                if not active_val:
                    continue
                raw_weight = rev.get("trafficWeight", 0)
                if (
                    isinstance(raw_weight, bool)
                    or not isinstance(raw_weight, int)
                    or raw_weight < 0
                ):
                    problems.append(
                        f"containerApp.revisions[{idx}].trafficWeight "
                        "must be a non-negative integer"
                    )
                    rev_meta_ok = False
                    continue
                if raw_weight > 0:
                    serving_revisions.append(rev)
                    total_weight += raw_weight
        else:
            problems.append("containerApp.revisions must be a list")
            rev_meta_ok = False
        if not serving_revisions:
            problems.append("containerApp has no active traffic-bearing revisions")
        elif total_weight != 100:
            problems.append(f"active trafficWeight sum is {total_weight}, expected 100")
        else:
            all_healthy = rev_meta_ok
            for idx, rev in enumerate(serving_revisions):
                run_state = str(rev.get("runningState") or "")
                raw_replicas = rev.get("replicasReady", 0)
                if isinstance(raw_replicas, bool) or not isinstance(raw_replicas, int):
                    all_healthy = False
                    problems.append(f"serving revision[{idx}] replicasReady must be an integer")
                    continue
                replicas = raw_replicas
                if run_state not in {"Running", "RunningAtMaxScale"} or replicas < 1:
                    all_healthy = False
                    problems.append(
                        f"serving revision[{idx}] unhealthy: "
                        f"runningState={run_state in {'Running', 'RunningAtMaxScale'}} "
                        f"replicas={replicas}"
                    )
            if stage in {"post_switchover", "post_retire"}:
                switched = all(
                    str(r.get("secretVersionId") or "") == next_version_id
                    and str(r.get("secretName") or secret_name).lower() == secret_name.lower()
                    for r in serving_revisions
                )
                if not switched:
                    problems.append(
                        "serving revisions have not switched over to expected nextVersionId"
                    )
                elif all_healthy and kv_versions_ok and app_binding_ok:
                    version_switchover_verified = True
            elif stage == "dual_secret_overlap":
                valid_vers = {prior_version_id, next_version_id}
                unexpected_vers = [
                    r
                    for r in serving_revisions
                    if str(r.get("secretVersionId") or "") not in valid_vers
                ]
                if unexpected_vers:
                    problems.append("serving revision holds an unexpected secretVersionId")
                version_switchover_verified = (
                    all_healthy
                    and kv_versions_ok
                    and app_binding_ok
                    and all(
                        str(r.get("secretVersionId") or "") == next_version_id
                        for r in serving_revisions
                    )
                )
            elif stage == "rollback":
                restored = all(
                    str(r.get("secretVersionId") or "") == prior_version_id
                    and str(r.get("secretName") or prior_secret_name).lower()
                    == prior_secret_name.lower()
                    for r in serving_revisions
                )
                if not restored:
                    problems.append(
                        "rollback serving revisions do not point to expected priorVersionId"
                    )
                elif all_healthy and kv_versions_ok and app_binding_ok:
                    rollback_revision_restored = True

    if needs_receipt_overlap_check:
        prior_receipt = evidence.get("priorSwitchoverReceipt")
        if isinstance(prior_receipt, Mapping):
            if norm_key is None:
                problems.append(
                    "priorSwitchoverReceipt requires signing_key for HMAC-SHA256 verification"
                )
            else:
                rec_sig = prior_receipt.get("signature")
                sig_valid = (
                    prior_receipt.get("signatureAlgorithm") == "HMAC-SHA256"
                    and isinstance(rec_sig, str)
                    and bool(_HEX64_RE.match(rec_sig))
                    and hmac.compare_digest(
                        rec_sig,
                        _compute_rotation_receipt_signature(prior_receipt, norm_key),
                    )
                )
                rec_overlap = _parse_non_negative_float(prior_receipt.get("overlapMinutes"))
                rec_elapsed = _parse_non_negative_float(prior_receipt.get("elapsedOverlapMinutes"))
                rec_sw_dt: dt.datetime | None = None
                raw_rec_sw = prior_receipt.get("switchoverAt")
                if isinstance(raw_rec_sw, str) and raw_rec_sw.strip():
                    try:
                        rec_sw_dt = parse_time(raw_rec_sw)
                    except (ValueError, TypeError):
                        rec_sw_dt = None
                identity_bound = (
                    prior_receipt.get("vaultName") == vault_name
                    and prior_receipt.get("appId") == app_id
                    and prior_receipt.get("secretName") == secret_name
                    and prior_receipt.get("priorSecretName") == prior_secret_name
                    and bool(prior_key_id)
                    and prior_receipt.get("priorKeyId") == prior_key_id
                    and bool(next_key_id)
                    and prior_receipt.get("nextKeyId") == next_key_id
                    and bool(prior_version_id)
                    and prior_receipt.get("priorVersionId") == prior_version_id
                    and bool(next_version_id)
                    and prior_receipt.get("nextVersionId") == next_version_id
                    and rec_sw_dt is not None
                    and switchover_dt is not None
                    and rec_sw_dt == switchover_dt
                )
                if (
                    sig_valid
                    and prior_receipt.get("stage") == "post_switchover"
                    and prior_receipt.get("ok") is True
                    and prior_receipt.get("safeToRetirePriorCredential") is True
                    and rec_overlap is not None
                    and rec_overlap >= float(min_overlap_minutes)
                    and rec_elapsed is not None
                    and rec_elapsed >= float(min_overlap_minutes)
                    and _HEX64_RE.match(str(prior_receipt.get("evidenceDigest") or ""))
                    and identity_bound
                ):
                    overlap_minutes = rec_overlap
                    elapsed_overlap_minutes = rec_elapsed
                    overlap_ok = True
                else:
                    problems.append(
                        "priorSwitchoverReceipt failed HMAC-SHA256 signature or bound "
                        "post_switchover gate verification"
                    )
        else:
            problems.append(
                "post_retire requires retiredPriorCredential timestamps or "
                "a signed priorSwitchoverReceipt"
            )

    raw_probes = evidence.get("healthProbes", [])
    probes_by_stage: dict[str, list[Mapping[str, Any]]] = {}
    if isinstance(raw_probes, Sequence) and not isinstance(raw_probes, (str, bytes)):
        for batch in raw_probes:
            if isinstance(batch, Mapping):
                raw_b_stage = batch.get("stage")
                p_stage = (
                    raw_b_stage
                    if isinstance(raw_b_stage, str) and raw_b_stage in VALID_ROTATION_STAGES
                    else "<invalid-stage>"
                )
                probes_by_stage.setdefault(p_stage, []).append(batch)
            else:
                problems.append("healthProbes entries must be probe batch mappings")
    else:
        problems.append("healthProbes must be a list of probe batches")

    zero_downtime_verified = False
    rollback_probes_ok = False
    pre_rollback_hold_problems = 0

    if not probes_by_stage:
        problems.append("at least one healthProbes batch is required")
    elif stage == "rollback":
        if "<invalid-stage>" in probes_by_stage:
            problems.append("probe[<invalid-stage>]: invalid healthProbes stage")
        rb_batches = probes_by_stage.get("rollback", [])
        if not rb_batches:
            problems.append("rollback stage requires a rollback healthProbes batch")
        else:
            rb_issues, rb_win = _validate_stage_probe_batches(
                rb_batches,
                stage_label="rollback",
                now_utc=now_utc,
                browser_mode=effective_browser_mode,
                require_authenticated_probe=effective_browser_mode,
                require_fresh_token_exchange=effective_browser_mode,
                min_probe_samples=min_probe_samples,
                min_probe_span_seconds=min_probe_span_seconds,
                max_probe_gap_seconds=max_probe_gap_seconds,
            )
            if rb_win is not None and rollback_dt is not None and rb_win[0] < rollback_dt:
                rb_issues.append(
                    "probe[rollback]: firstSampleAt must be at or after containerApp.rollbackAt"
                )
            if rb_issues or rollback_dt is None:
                problems.extend(rb_issues)
            else:
                rollback_probes_ok = True
        pre_rollback_hold_problems = len(problems)
        problems.append("forward rotation aborted; rollback hold active")
    else:
        required_probe_stages: dict[str, list[str]] = {
            "dual_secret_overlap": ["dual_secret_overlap"],
            "post_switchover": ["dual_secret_overlap", "post_switchover"],
            "post_retire": ["post_switchover", "post_retire"],
        }
        probe_issues: list[str] = []
        for req_stage in required_probe_stages.get(stage, []):
            if req_stage not in probes_by_stage:
                probe_issues.append(f"missing required healthProbes batch for stage {req_stage!r}")
        stage_windows: dict[str, tuple[dt.datetime, dt.datetime]] = {}
        for p_stage, batches in probes_by_stage.items():
            req_auth = effective_browser_mode and p_stage in {"post_switchover", "post_retire"}
            st_issues, st_win = _validate_stage_probe_batches(
                batches,
                stage_label=p_stage,
                now_utc=now_utc,
                browser_mode=effective_browser_mode,
                require_authenticated_probe=req_auth,
                require_fresh_token_exchange=req_auth,
                min_probe_samples=min_probe_samples,
                min_probe_span_seconds=min_probe_span_seconds,
                max_probe_gap_seconds=max_probe_gap_seconds,
            )
            probe_issues.extend(st_issues)
            if st_win is not None and p_stage in VALID_ROTATION_STAGES:
                stage_windows[p_stage] = st_win

        ordered_stages = [
            s
            for s in ("dual_secret_overlap", "post_switchover", "post_retire")
            if s in stage_windows
        ]
        for idx in range(1, len(ordered_stages)):
            prev_s = ordered_stages[idx - 1]
            next_s = ordered_stages[idx]
            if stage_windows[next_s][0] < stage_windows[prev_s][1]:
                probe_issues.append(f"probe stage {next_s!r} starts before {prev_s!r} completed")
        if "dual_secret_overlap" in stage_windows:
            dso_start = stage_windows["dual_secret_overlap"][0]
            if overlap_start_dt is not None and dso_start < overlap_start_dt:
                probe_issues.append(
                    "probe[dual_secret_overlap]: firstSampleAt precedes credential overlap start"
                )
            if next_ver_created_dt is not None and dso_start < next_ver_created_dt:
                probe_issues.append(
                    "probe[dual_secret_overlap]: firstSampleAt precedes nextVersionId creation"
                )
        if "post_switchover" in stage_windows:
            psw_start = stage_windows["post_switchover"][0]
            if switchover_dt is not None and psw_start < switchover_dt:
                probe_issues.append(
                    "probe[post_switchover]: firstSampleAt must be at or after "
                    "containerApp.switchoverAt"
                )
            if next_ver_created_dt is not None and psw_start < next_ver_created_dt:
                probe_issues.append(
                    "probe[post_switchover]: firstSampleAt precedes nextVersionId creation"
                )
        if stage == "post_retire":
            if (
                effective_retired_at is not None
                and "post_switchover" in stage_windows
                and effective_retired_at < stage_windows["post_switchover"][1]
            ):
                probe_issues.append(
                    "post_retire retirement timestamp precedes completion of post_switchover probes"
                )
            if "post_retire" in stage_windows:
                if effective_retired_at is None:
                    probe_issues.append(
                        "probe[post_retire]: prior credential retirement timestamp is required"
                    )
                elif stage_windows["post_retire"][0] < effective_retired_at:
                    probe_issues.append(
                        "probe[post_retire]: firstSampleAt must be at or after "
                        "retiredAt / priorRetiredAt"
                    )

        if probe_issues:
            problems.extend(probe_issues)
        else:
            zero_downtime_verified = True

    rollback_verified = (
        stage == "rollback"
        and pre_rollback_hold_problems == 0
        and prior_cred_active
        and prior_version_enabled
        and rollback_revision_restored
        and rollback_probes_ok
    )
    ok = len(problems) == 0 and stage != "rollback"
    post_retire_verified = stage == "post_retire" and ok and overlap_ok
    safe_to_retire = (
        stage == "post_switchover"
        and ok
        and overlap_ok
        and version_switchover_verified
        and zero_downtime_verified
    )

    receipt: dict[str, Any] = {
        "ok": ok,
        "stage": stage,
        "vaultName": vault_name,
        "secretName": secret_name,
        "priorSecretName": prior_secret_name,
        "appId": app_id,
        "priorKeyId": prior_key_id,
        "nextKeyId": next_key_id,
        "priorVersionId": prior_version_id,
        "nextVersionId": next_version_id,
        "overlapMinutes": overlap_minutes,
        "elapsedOverlapMinutes": elapsed_overlap_minutes,
        "zeroDowntimeVerified": zero_downtime_verified,
        "versionSwitchoverVerified": version_switchover_verified,
        "rollbackVerified": rollback_verified,
        "postRetireVerified": post_retire_verified,
        "safeToRetirePriorCredential": safe_to_retire,
        "problems": problems,
        "evidenceDigest": _sha256_canonical(evidence),
    }
    if stage in {"post_switchover", "post_retire"} and switchover_dt is not None:
        receipt["switchoverAt"] = switchover_dt.isoformat()
    if norm_key is not None:
        receipt["signatureAlgorithm"] = "HMAC-SHA256"
        receipt["signature"] = _compute_rotation_receipt_signature(receipt, norm_key)
    return receipt


def default_expected_caller_policy(
    role_matrix: Mapping[str, Any],
    principal_map: Mapping[str, str],
) -> dict[str, dict[str, Any]]:
    """Build fail-closed Key Vault data-plane caller expectations from `role-assignments.json`.

    Only explicitly supplied `principal_map` entries (`symbolic_identity -> principal_oid`)
    are mapped; live RBAC assignment OIDs are never auto-trusted.
    """
    assert_no_secret_material(role_matrix, path="$.roleMatrix")
    assert_no_secret_material(principal_map, path="$.principalMap")

    built_in_roles = {
        str(k): str(v) for k, v in dict(role_matrix.get("builtInRoles") or {}).items()
    }
    kv_grants: dict[str, list[tuple[str, str]]] = {}
    all_identities: set[str] = set()
    for row in role_matrix.get("assignments", []):
        if not isinstance(row, Mapping):
            continue
        ident = str(row.get("identity") or "").strip()
        if not ident:
            continue
        all_identities.add(ident)
        if str(row.get("resource") or "") == "keyvault":
            role_id = str(row.get("roleId") or "").strip()
            role_name = built_in_roles.get(role_id, "")
            if not role_name or role_name not in DATA_ROLES:
                raise SecretLifecycleError(
                    f"keyvault assignment for {ident!r} references unmapped or unsupported "
                    f"roleId {role_id!r}"
                )
            scope_desc = str(row.get("scope") or "").strip()
            kv_grants.setdefault(ident, []).append((role_name, scope_desc))

    seen_oids: dict[str, str] = {}
    policy_by_oid: dict[str, dict[str, Any]] = {}

    for ident, raw_oid in principal_map.items():
        sym = str(ident).strip()
        oid = str(raw_oid).strip()
        if not sym or not oid:
            raise SecretLifecycleError("principal_map keys and OIDs must be non-empty strings")
        if oid in seen_oids and seen_oids[oid] != sym:
            raise SecretLifecycleError(
                f"duplicate principal OID mapped to both {seen_oids[oid]!r} and {sym!r}"
            )
        seen_oids[oid] = sym

        grants = kv_grants.get(sym, [])
        if not grants:
            if sym in all_identities:
                policy_by_oid[oid] = {
                    "identity": sym,
                    "forbidden": True,
                    "allowedRoles": [],
                    "allowedRoleScopes": {},
                    "allowedOperations": [],
                    "allowedSecrets": [],
                    "allowStagedEntraPrefix": False,
                }
            else:
                raise SecretLifecycleError(
                    f"principal_map identity {sym!r} has no Key Vault grant "
                    "in role-assignments.json"
                )
            continue

        allowed_roles: set[str] = set()
        allowed_role_scopes: dict[str, set[str]] = {}
        allowed_ops: set[str] = set()
        allowed_secrets: set[str] = set()
        allow_staged_entra = False

        for role_name, scope_desc in grants:
            allowed_roles.add(role_name)
            access_level = DATA_ROLES.get(role_name, "")
            if access_level == "read":
                allowed_ops.add("SecretGet")
            elif access_level == "write":
                allowed_ops.update({"SecretGet", "SecretSet"})
            elif access_level == "admin":
                allowed_ops.update({"SecretGet", "SecretSet", "SecretDelete", "SecretList"})

            scoped_match = re.match(r"^Secret\s+([A-Za-z0-9-]+)\s+only$", scope_desc)
            if scoped_match:
                sec_lower = scoped_match.group(1).lower()
                allowed_secrets.add(sec_lower)
                allowed_role_scopes.setdefault(role_name, set()).add(f"secret:{sec_lower}")
            elif scope_desc == "Key Vault":
                allowed_role_scopes.setdefault(role_name, set()).add("vault")
                if sym == "api":
                    allowed_secrets.update({"entra-client-secret", "entra-token-store-sas"})
                    allow_staged_entra = True
            else:
                raise SecretLifecycleError(
                    f"unrecognized Key Vault scope descriptor {scope_desc!r} for identity {sym!r}"
                )

        policy_by_oid[oid] = {
            "identity": sym,
            "forbidden": False,
            "allowedRoles": sorted(allowed_roles),
            "allowedRoleScopes": {
                r_name: sorted(scopes) for r_name, scopes in sorted(allowed_role_scopes.items())
            },
            "allowedOperations": sorted(allowed_ops),
            "allowedSecrets": sorted(allowed_secrets),
            "allowStagedEntraPrefix": allow_staged_entra,
        }

    return policy_by_oid


def _classify_arm_kv_scope(scope_value: Any, expected_vault_lower: str) -> str:
    if not isinstance(scope_value, str) or not scope_value.strip():
        return "invalid_scope"
    cleaned = scope_value.strip()
    if cleaned != "/":
        cleaned = cleaned.rstrip("/")
    kv_match = re.fullmatch(
        r"(/subscriptions/[^/\s]+/resourcegroups/[^/\s]+)"
        r"/providers/microsoft\.keyvault/vaults/([^/\s]+)(/.*)?",
        cleaned,
        re.IGNORECASE,
    )
    if kv_match is not None:
        v_name = kv_match.group(2)
        rest = kv_match.group(3) or ""
        if not _VAULT_NAME_RE.match(v_name) or v_name.lower() != expected_vault_lower:
            return "wrong_vault"
        if rest == "":
            return "vault"
        sec_match = re.fullmatch(r"/secrets/([A-Za-z0-9-]+)", rest, re.IGNORECASE)
        if sec_match is not None:
            return f"secret:{sec_match.group(1).lower()}"
        return "invalid_scope"

    if (
        cleaned == "/"
        or re.fullmatch(
            r"/providers/microsoft\.management/managementgroups/[^/\s]+",
            cleaned,
            re.IGNORECASE,
        )
        or re.fullmatch(r"/subscriptions/[^/\s]+", cleaned, re.IGNORECASE)
        or re.fullmatch(
            r"/subscriptions/[^/\s]+/resourcegroups/[^/\s]+",
            cleaned,
            re.IGNORECASE,
        )
    ):
        return "broader_parent"

    if "/providers/" in cleaned.lower():
        return "wrong_vault"
    return "invalid_scope"


def merge_vault_role_assignments(
    inherited_assignments: Any,
    all_assignments: Any,
    *,
    vault_resource_id: str,
) -> list[dict[str, Any]]:
    """Combine `--scope <vault-id> --include-inherited` ancestors with child secret scopes.

    Preserves root `/`, management-group, subscription, resource-group, and vault
    assignments from `inherited_assignments` (verifying they target `vault_resource_id`'s
    chain) and attaches `<vault-id>` and `<vault-id>/secrets/*` assignments from
    `all_assignments`, deduplicated deterministically.
    """
    assert_no_secret_material(vault_resource_id, path="$.vaultResourceId")
    inh_unwrapped = unwrap_arm_list_envelope(inherited_assignments, label="$.inheritedAssignments")
    all_unwrapped = unwrap_arm_list_envelope(all_assignments, label="$.allAssignments")

    if not isinstance(vault_resource_id, str) or not vault_resource_id.strip():
        raise SecretLifecycleError("vault_resource_id must be a non-empty ARM vault resource ID")
    match = _FULL_VAULT_RESOURCE_ID_RE.match(vault_resource_id.strip())
    if match is None:
        raise SecretLifecycleError(
            "vault_resource_id must be a full ARM Microsoft.KeyVault/vaults resource ID"
        )
    rg_prefix_lower = match.group(1).lower()
    sub_prefix_lower = f"/subscriptions/{match.group(2).lower()}"
    vault_name_lower = match.group(4).lower()
    vault_prefix_lower = f"{rg_prefix_lower}/providers/microsoft.keyvault/vaults/{vault_name_lower}"
    if not isinstance(inh_unwrapped, Sequence) or isinstance(inh_unwrapped, (str, bytes)):
        raise SecretLifecycleError("inherited_assignments must be a list of role assignments")
    if not isinstance(all_unwrapped, Sequence) or isinstance(all_unwrapped, (str, bytes)):
        raise SecretLifecycleError("all_assignments must be a list of role assignments")

    merged_by_key: dict[str, dict[str, Any]] = {}

    for idx, row in enumerate(inh_unwrapped):
        if not isinstance(row, Mapping):
            raise SecretLifecycleError(f"inherited_assignments[{idx}] must be a mapping")
        raw_scope = row.get("scope")
        cls = _classify_arm_kv_scope(raw_scope, vault_name_lower)
        if cls not in {"vault", "broader_parent"}:
            raise SecretLifecycleError(
                f"inherited_assignments[{idx}] scope does not belong to "
                f"vault {_safe_vault(vault_name_lower)!r} or its ARM ancestors"
            )
        assert isinstance(raw_scope, str)
        stripped = raw_scope.strip()
        norm_lower = "/" if stripped == "/" else stripped.rstrip("/").lower()
        if norm_lower.startswith("/subscriptions/") and norm_lower not in {
            sub_prefix_lower,
            rg_prefix_lower,
            vault_prefix_lower,
        }:
            raise SecretLifecycleError(
                f"inherited_assignments[{idx}] scope belongs to a different "
                "subscription or resource group than vault_resource_id"
            )
        dedupe_key = str(row.get("id") or "").strip().lower() or f"digest:{_sha256_canonical(row)}"
        if dedupe_key not in merged_by_key:
            merged_by_key[dedupe_key] = dict(row)

    for idx, row in enumerate(all_unwrapped):
        if not isinstance(row, Mapping):
            raise SecretLifecycleError(f"all_assignments[{idx}] must be a mapping")
        raw_scope = row.get("scope")
        if not isinstance(raw_scope, str) or not raw_scope.strip():
            continue
        norm_lower = raw_scope.strip().rstrip("/").lower()
        if norm_lower != vault_prefix_lower and not norm_lower.startswith(vault_prefix_lower + "/"):
            continue
        cls = _classify_arm_kv_scope(raw_scope, vault_name_lower)
        if cls == "vault" or cls.startswith("secret:"):
            dedupe_key = (
                str(row.get("id") or "").strip().lower() or f"digest:{_sha256_canonical(row)}"
            )
            if dedupe_key not in merged_by_key:
                merged_by_key[dedupe_key] = dict(row)

    return list(merged_by_key.values())


def _extract_uri_vault_name(uri: str) -> str | None:
    parsed = urlparse(uri.strip())
    if parsed.scheme.lower() != "https" or not parsed.netloc.lower().endswith(".vault.azure.net"):
        return None
    vault_host = parsed.netloc.lower().removesuffix(".vault.azure.net")
    return vault_host if _VAULT_NAME_RE.match(vault_host) else None


def _extract_arm_vault_name(resource_id: str) -> str | None:
    match = _ARM_VAULT_ID_RE.search(resource_id.strip())
    if not match:
        return None
    vault_name = match.group(1).lower()
    return vault_name if _VAULT_NAME_RE.match(vault_name) else None


def _validate_diag_row_vault(row: Mapping[str, Any], expected_vault_lower: str) -> str | None:
    found_identifier = False
    for uri_field in ("id_s", "requestUri_s"):
        raw_uri = str(row.get(uri_field) or "").strip()
        if not raw_uri:
            continue
        found_identifier = True
        uri_vault = _extract_uri_vault_name(raw_uri)
        if uri_vault is None:
            return (
                f"diagnostic {uri_field} is not a valid Key Vault URI for {expected_vault_lower!r}"
            )
        if uri_vault != expected_vault_lower:
            return (
                f"diagnostic {uri_field} targets vault {uri_vault!r}, "
                f"expected {expected_vault_lower!r}"
            )
    for arm_field in ("ResourceId", "_ResourceId", "resourceId"):
        raw_arm = str(row.get(arm_field) or "").strip()
        if not raw_arm:
            continue
        found_identifier = True
        arm_vault = (
            _extract_uri_vault_name(raw_arm)
            if raw_arm.lower().startswith("https://")
            else _extract_arm_vault_name(raw_arm)
        )
        if arm_vault is None:
            return (
                f"diagnostic {arm_field} is not a valid Key Vault resource identifier "
                f"for {expected_vault_lower!r}"
            )
        if arm_vault != expected_vault_lower:
            return (
                f"diagnostic {arm_field} targets vault {arm_vault!r}, "
                f"expected {expected_vault_lower!r}"
            )
    if not found_identifier:
        return f"diagnostic event lacks vault identifier for {expected_vault_lower!r}"
    return None


def _compute_audit_digest(
    *,
    vault_name: str,
    window_start: str,
    window_end: str,
    rbac_assignments: Sequence[Mapping[str, Any]],
    caller_summaries: Sequence[Mapping[str, Any]],
    system_notification_count: int,
    anomalies: Sequence[Mapping[str, Any]],
) -> str:
    return _sha256_canonical(
        {
            "vaultName": vault_name,
            "windowStart": window_start,
            "windowEnd": window_end,
            "rbacAssignments": [dict(r) for r in rbac_assignments],
            "callerSummaries": [dict(c) for c in caller_summaries],
            "systemNotificationCount": system_notification_count,
            "anomalies": [dict(a) for a in anomalies],
        }
    )


def _extract_diag_secret_name(row: Mapping[str, Any]) -> str | None:
    explicit = str(row.get("secretName") or "").strip()
    if explicit:
        return explicit
    for uri_field in ("id_s", "requestUri_s", "resourceId"):
        raw_uri = str(row.get(uri_field) or "").strip()
        if not raw_uri:
            continue
        parsed = urlparse(raw_uri)
        parts = [seg for seg in parsed.path.split("/") if seg]
        for idx, seg in enumerate(parts):
            if seg.lower() == "secrets" and idx + 1 < len(parts):
                return parts[idx + 1]
    return None


def _secret_allowed(secret_name: str | None, caller_rule: Mapping[str, Any]) -> bool:
    if secret_name is None:
        return False
    sec_norm = secret_name.strip().lower()
    if not sec_norm:
        return False
    allowed = {str(s).lower() for s in caller_rule.get("allowedSecrets", [])}
    if sec_norm in allowed:
        return True
    return bool(caller_rule.get("allowStagedEntraPrefix", False)) and sec_norm.startswith("entra-")


def audit_keyvault_data_plane_access(
    *,
    vault_name: str,
    inventory: Mapping[str, Any],
    assignments: Sequence[Mapping[str, Any]],
    diagnostics: Sequence[Mapping[str, Any]],
    expected_callers: Mapping[str, Mapping[str, Any]],
    window_start: dt.datetime,
    window_end: dt.datetime,
    denied_401_threshold: int = 5,
    max_window_days: int = 95,
) -> dict[str, Any]:
    """Audit Key Vault RBAC assignments and `AzureDiagnostics` data-plane operations."""
    assert_no_secret_material(vault_name, path="$.vaultName")
    assert_no_secret_material(inventory, path="$.inventory")
    assert_no_secret_material(assignments, path="$.assignments")
    assert_no_secret_material(diagnostics, path="$.diagnostics")
    assert_no_secret_material(expected_callers, path="$.expectedCallers")

    cleaned_vault = vault_name.strip()
    if not _VAULT_NAME_RE.match(cleaned_vault):
        raise SecretLifecycleError("vault_name must be 3-24 alphanumeric or hyphen characters")
    if window_start.tzinfo is None or window_end.tzinfo is None:
        raise SecretLifecycleError(
            "window_start and window_end must include explicit timezone offsets"
        )
    w_start_utc = window_start.astimezone(dt.UTC)
    w_end_utc = window_end.astimezone(dt.UTC)
    if w_end_utc <= w_start_utc:
        raise SecretLifecycleError("window_end must be greater than window_start")
    if (w_end_utc - w_start_utc) > dt.timedelta(days=max_window_days):
        raise SecretLifecycleError(f"audit window exceeds {max_window_days} days")
    if denied_401_threshold < 1:
        raise SecretLifecycleError("denied_401_threshold must be >= 1")

    inv_problems = validate_inventory(inventory)
    if inv_problems:
        raise SecretLifecycleError("; ".join(inv_problems))

    rbac_rows: list[dict[str, Any]] = []
    anomalies: list[dict[str, Any]] = []
    seen_assignment_ids: set[str] = set()
    seen_anomaly_ids: set[str] = set()
    expected_vault_lower = cleaned_vault.lower()

    def _add_anomaly(kind: str, principal_id: str, identity: str, detail: str) -> None:
        anom_key = f"{cleaned_vault}|{kind}|{principal_id}|{detail}"
        anom_id = "anom-" + hashlib.sha256(anom_key.encode("utf-8")).hexdigest()[:16]
        if anom_id in seen_anomaly_ids:
            return
        seen_anomaly_ids.add(anom_id)
        anomalies.append(
            {
                "anomalyId": anom_id,
                "kind": kind,
                "principalId": principal_id,
                "identity": identity,
                "detail": detail,
            }
        )

    sorted_assignments = sorted(
        assignments,
        key=lambda item: (
            str(item.get("principalId") or ""),
            str(item.get("roleDefinitionName") or ""),
            str(item.get("scope") or ""),
        ),
    )
    for item in sorted_assignments:
        pid = str(item.get("principalId") or "").strip()
        ptype = str(item.get("principalType") or "").strip()
        role = str(item.get("roleDefinitionName") or "").strip()
        scope = str(item.get("scope") or "").strip()
        access = DATA_ROLES.get(role, "unclassified, needs justification")
        asgn_id = (
            "asgn-" + hashlib.sha256(f"{pid}|{ptype}|{role}|{scope}".encode()).hexdigest()[:16]
        )
        if asgn_id in seen_assignment_ids:
            continue
        seen_assignment_ids.add(asgn_id)
        caller_rule = expected_callers.get(pid)
        mapped_identity = str(caller_rule.get("identity")) if caller_rule else "unmapped"
        rbac_rows.append(
            {
                "assignmentId": asgn_id,
                "principalId": pid,
                "principalType": ptype,
                "identity": mapped_identity,
                "role": role,
                "access": access,
                "scope": scope,
            }
        )
        scope_class = _classify_arm_kv_scope(scope, expected_vault_lower)
        if scope_class in {"wrong_vault", "invalid_scope"}:
            _add_anomaly(
                "wrong_vault_rbac_scope",
                pid or "<missing>",
                mapped_identity,
                f"RBAC assignment for role {role!r} has {scope_class} scope",
            )

        if role not in DATA_ROLES:
            _add_anomaly(
                "unclassified_rbac_role",
                pid or "<missing>",
                mapped_identity,
                f"RBAC role {role!r} at {scope or '/'} is unclassified for Key Vault review",
            )
        elif access in {"read", "write", "admin"}:
            if caller_rule is None:
                _add_anomaly(
                    "unmapped_rbac_principal",
                    pid or "<missing>",
                    "unmapped",
                    f"data-plane RBAC role {role!r} assigned to unmapped principal {pid!r}",
                )
            elif bool(caller_rule.get("forbidden", False)):
                _add_anomaly(
                    "forbidden_workload_caller",
                    pid,
                    mapped_identity,
                    f"forbidden workload {mapped_identity!r} holds Key Vault RBAC role {role!r}",
                )
            else:
                role_allowed = True
                if caller_rule.get("allowedRoles") is not None:
                    allowed_roles = {str(r) for r in caller_rule["allowedRoles"]}
                    if role not in allowed_roles:
                        role_allowed = False
                        _add_anomaly(
                            "excess_rbac_privilege",
                            pid,
                            mapped_identity,
                            f"caller {mapped_identity!r} ({pid}) holds RBAC role {role!r} "
                            f"outside allowed roles {sorted(allowed_roles)}",
                        )
                allowed_scopes_map = caller_rule.get("allowedRoleScopes")
                if (
                    role_allowed
                    and scope_class not in {"wrong_vault", "invalid_scope"}
                    and isinstance(allowed_scopes_map, Mapping)
                ):
                    permitted_scopes = {str(s).lower() for s in allowed_scopes_map.get(role, [])}
                    if scope_class not in permitted_scopes:
                        _add_anomaly(
                            "excess_rbac_privilege",
                            pid,
                            mapped_identity,
                            f"caller {mapped_identity!r} ({pid}) holds RBAC role {role!r} "
                            f"at scope {scope_class!r} outside allowed scopes "
                            f"{sorted(permitted_scopes)}",
                        )

    system_notification_count = 0
    out_of_window_count = 0
    per_caller: dict[str, dict[str, Any]] = {}

    for row in diagnostics:
        ts_raw = row.get("TimeGenerated") or row.get("timeGenerated") or row.get("timestamp")
        if not ts_raw:
            raise SecretLifecycleError("diagnostic event missing TimeGenerated timestamp")
        ts = parse_time(str(ts_raw))
        if ts < w_start_utc or ts > w_end_utc:
            out_of_window_count += 1
            continue

        op = str(row.get("OperationName") or row.get("operationName") or "").strip()
        if not op:
            raise SecretLifecycleError("diagnostic event missing OperationName")

        raw_pid = (
            row.get("identity_claim_oid_g")
            or row.get("callerObjectId")
            or row.get("principalId")
            or ""
        )
        pid = str(raw_pid).strip()

        vault_mismatch = _validate_diag_row_vault(row, expected_vault_lower)
        if vault_mismatch is not None:
            anom_pid = pid or "<unattributed>"
            anom_rule = expected_callers.get(pid) if pid else None
            anom_ident = (
                str(anom_rule.get("identity"))
                if anom_rule
                else ("system" if not pid else "unexpected")
            )
            _add_anomaly("wrong_vault_diagnostic", anom_pid, anom_ident, vault_mismatch)
            continue

        if not pid and op in PLATFORM_NOTIFICATION_OPS:
            system_notification_count += 1
            continue
        if not pid:
            pid = "<anonymous>"

        status_raw = (
            row.get("httpStatusCode_d")
            if row.get("httpStatusCode_d") is not None
            else row.get("statusCode", row.get("httpStatusCode", 0))
        )
        if status_raw is None or (isinstance(status_raw, str) and not status_raw.strip()):
            status_code = 0
        elif isinstance(status_raw, bool):
            raise SecretLifecycleError("diagnostic event has invalid boolean HTTP status code")
        elif isinstance(status_raw, int):
            if status_raw < 0 or status_raw > 999:
                raise SecretLifecycleError("diagnostic event HTTP status code out of range")
            status_code = status_raw
        elif isinstance(status_raw, (float, str)):
            try:
                f_status = float(status_raw)
            except ValueError as exc:
                raise SecretLifecycleError(
                    "diagnostic event has non-numeric HTTP status code"
                ) from exc
            if (
                not math.isfinite(f_status)
                or not f_status.is_integer()
                or f_status < 0
                or f_status > 999
            ):
                raise SecretLifecycleError("diagnostic event HTTP status code out of range")
            status_code = int(f_status)
        else:
            raise SecretLifecycleError("diagnostic event has invalid HTTP status code type")
        secret_name = _extract_diag_secret_name(row)

        bucket = per_caller.get(pid)
        if bucket is None:
            rule = expected_callers.get(pid)
            bucket = {
                "principalId": pid,
                "identity": str(rule.get("identity")) if rule else "unexpected",
                "totalCalls": 0,
                "operations": {},
                "secrets": set(),
                "statusCodes": {},
                "firstSeen": ts,
                "lastSeen": ts,
                "disallowedOps": set(),
                "outOfScopeSecrets": set(),
            }
            per_caller[pid] = bucket

        bucket["totalCalls"] += 1
        ops_map: dict[str, int] = bucket["operations"]
        ops_map[op] = ops_map.get(op, 0) + 1
        if secret_name:
            bucket["secrets"].add(secret_name)
        status_key = str(status_code)
        sc_map: dict[str, int] = bucket["statusCodes"]
        sc_map[status_key] = sc_map.get(status_key, 0) + 1
        bucket["firstSeen"] = min(bucket["firstSeen"], ts)
        bucket["lastSeen"] = max(bucket["lastSeen"], ts)

        rule = expected_callers.get(pid)
        if rule is not None and not bool(rule.get("forbidden", False)):
            allowed_ops = {str(x) for x in rule.get("allowedOperations", [])}
            if op not in allowed_ops:
                bucket["disallowedOps"].add(op)
            if not _secret_allowed(secret_name, rule):
                bucket["outOfScopeSecrets"].add(secret_name or "<vault-scope>")

    caller_summaries: list[dict[str, Any]] = []
    for pid in sorted(per_caller):
        bucket = per_caller[pid]
        rule = expected_callers.get(pid)
        ident = str(bucket["identity"])
        ops_sorted = dict(sorted(bucket["operations"].items()))
        secrets_sorted = sorted(bucket["secrets"])
        codes_sorted = dict(sorted(bucket["statusCodes"].items()))
        caller_summaries.append(
            {
                "principalId": pid,
                "identity": ident,
                "totalCalls": int(bucket["totalCalls"]),
                "operations": ops_sorted,
                "secrets": secrets_sorted,
                "statusCodes": codes_sorted,
                "firstSeen": bucket["firstSeen"].isoformat(),
                "lastSeen": bucket["lastSeen"].isoformat(),
            }
        )

        if rule is None:
            _add_anomaly(
                "unexpected_caller",
                pid,
                "unexpected",
                f"unlisted caller {pid} invoked operations {sorted(ops_sorted)}",
            )
        elif bool(rule.get("forbidden", False)):
            _add_anomaly(
                "forbidden_workload_caller",
                pid,
                ident,
                f"forbidden workload {ident!r} ({pid}) invoked Key Vault operations "
                f"{sorted(ops_sorted)}",
            )
        else:
            for bad_op in sorted(bucket["disallowedOps"]):
                _add_anomaly(
                    "unexpected_operation",
                    pid,
                    ident,
                    f"caller {ident!r} ({pid}) invoked disallowed operation {bad_op!r}",
                )
            for bad_sec in sorted(bucket["outOfScopeSecrets"]):
                _add_anomaly(
                    "out_of_scope_secret",
                    pid,
                    ident,
                    f"caller {ident!r} ({pid}) accessed out-of-scope target {bad_sec!r}",
                )

        count_403 = int(codes_sorted.get("403", 0))
        count_401 = int(codes_sorted.get("401", 0))
        if count_403 >= 1 or count_401 >= denied_401_threshold:
            _add_anomaly(
                "denied_access_activity",
                pid,
                ident,
                f"denied responses for {pid}: 403={count_403}, 401={count_401} "
                f"(401 threshold {denied_401_threshold})",
            )

    anomalies.sort(
        key=lambda item: (str(item["kind"]), str(item["principalId"]), str(item["anomalyId"]))
    )

    w_start_iso = w_start_utc.isoformat()
    w_end_iso = w_end_utc.isoformat()
    audit_digest = _compute_audit_digest(
        vault_name=cleaned_vault,
        window_start=w_start_iso,
        window_end=w_end_iso,
        rbac_assignments=rbac_rows,
        caller_summaries=caller_summaries,
        system_notification_count=system_notification_count,
        anomalies=anomalies,
    )
    return {
        "vaultName": cleaned_vault,
        "windowStart": w_start_iso,
        "windowEnd": w_end_iso,
        "rbacAssignments": rbac_rows,
        "callerSummaries": caller_summaries,
        "systemNotificationCount": system_notification_count,
        "anomalies": anomalies,
        "outOfWindowEventCount": out_of_window_count,
        "denied401Threshold": denied_401_threshold,
        "auditDigest": audit_digest,
    }


def _validate_signing_key(signing_key: bytes, key_id: str) -> str:
    if not isinstance(signing_key, (bytes, bytearray)) or len(signing_key) < 32:
        raise SecretLifecycleError("signing_key must be at least 32 bytes")
    cleaned_id = key_id.strip() if isinstance(key_id, str) else ""
    if not _KEY_ID_TOKEN_RE.match(cleaned_id):
        raise SecretLifecycleError("key_id must be 3-128 token-safe characters")
    return cleaned_id


def create_signed_access_review_record(
    *,
    audit: Mapping[str, Any],
    decisions: Mapping[str, Any],
    reviewer: str,
    reviewed_at: dt.datetime,
    review_interval_days: int,
    signing_key: bytes,
    key_id: str,
    prev_entry: Mapping[str, Any] | None = None,
    min_window_days: int | None = None,
) -> dict[str, Any]:
    """Create an HMAC-SHA256 signed, SHA-256 hash-chained scheduled access review entry.

    `auditDigest` is a canonical SHA-256 integrity checksum over the audited snapshot bound
    under the human reviewer's `HMAC-SHA256` signature.
    """
    assert_no_secret_material(audit, path="$.audit")
    assert_no_secret_material(decisions, path="$.decisions")
    if prev_entry is not None:
        assert_no_secret_material(prev_entry, path="$.prevEntry")

    cleaned_reviewer = validate_human_reviewer(reviewer)
    cleaned_key_id = _validate_signing_key(signing_key, key_id)
    if (
        not isinstance(review_interval_days, int)
        or isinstance(review_interval_days, bool)
        or review_interval_days < 1
        or review_interval_days > 90
    ):
        raise SecretLifecycleError("review_interval_days must be between 1 and 90")
    if min_window_days is not None and (
        not isinstance(min_window_days, int)
        or isinstance(min_window_days, bool)
        or min_window_days < 1
    ):
        raise SecretLifecycleError("min_window_days must be a positive integer")
    if reviewed_at.tzinfo is None:
        raise SecretLifecycleError("reviewed_at must include an explicit timezone offset")
    reviewed_utc = reviewed_at.astimezone(dt.UTC)

    vault_name = str(audit.get("vaultName") or "").strip()
    if not _VAULT_NAME_RE.match(vault_name):
        raise SecretLifecycleError("audit.vaultName is missing or invalid")
    audit_digest = str(audit.get("auditDigest") or "").strip()
    if not _HEX64_RE.match(audit_digest):
        raise SecretLifecycleError("audit.auditDigest must be a 64-char lowercase hex SHA-256")

    w_start_dt = parse_time(str(audit.get("windowStart") or ""))
    w_end_dt = parse_time(str(audit.get("windowEnd") or ""))
    if w_end_dt <= w_start_dt:
        raise SecretLifecycleError("audit.windowEnd must be greater than audit.windowStart")
    if w_end_dt > reviewed_utc:
        raise SecretLifecycleError("audit.windowEnd cannot be after reviewed_at")
    if (reviewed_utc - w_end_dt) > dt.timedelta(days=review_interval_days):
        raise SecretLifecycleError(
            f"audit.windowEnd is stale by more than {review_interval_days} days before reviewed_at"
        )
    if prev_entry is None:
        req_window_days = review_interval_days if min_window_days is None else min_window_days
        if (w_end_dt - w_start_dt) < dt.timedelta(days=req_window_days):
            raise SecretLifecycleError(
                f"initial audit window is shorter than required {req_window_days} days"
            )
    else:
        prev_w_end_dt = parse_time(str(prev_entry.get("windowEnd") or ""))
        if w_start_dt > prev_w_end_dt:
            raise SecretLifecycleError(
                "audit.windowStart leaves an unreviewed gap after prev_entry.windowEnd"
            )
        if w_end_dt <= prev_w_end_dt:
            raise SecretLifecycleError("audit.windowEnd must advance past prev_entry.windowEnd")
        req_chained_days = 1 if min_window_days is None else min_window_days
        if (w_end_dt - w_start_dt) < dt.timedelta(days=req_chained_days):
            raise SecretLifecycleError(
                f"chained audit window is shorter than required {req_chained_days} days"
            )
    window_start = w_start_dt.isoformat()
    window_end = w_end_dt.isoformat()

    rbac_rows = audit.get("rbacAssignments", [])
    if not isinstance(rbac_rows, Sequence) or isinstance(rbac_rows, (str, bytes)) or not rbac_rows:
        raise SecretLifecycleError("audit must contain at least one RBAC assignment to review")
    if not all(isinstance(r, Mapping) and str(r.get("assignmentId") or "") for r in rbac_rows):
        raise SecretLifecycleError("audit.rbacAssignments must contain valid assignment objects")

    expected_asgn_ids = {str(r["assignmentId"]): r for r in rbac_rows if isinstance(r, Mapping)}
    if len(expected_asgn_ids) != len(rbac_rows):
        raise SecretLifecycleError("audit.rbacAssignments contains duplicate assignmentId values")

    anom_rows = audit.get("anomalies", [])
    if not isinstance(anom_rows, Sequence) or isinstance(anom_rows, (str, bytes)):
        raise SecretLifecycleError("audit.anomalies must be a list")
    if not all(isinstance(a, Mapping) and str(a.get("anomalyId") or "") for a in anom_rows):
        raise SecretLifecycleError("audit.anomalies must contain valid anomaly objects")
    expected_anom_ids = {str(a["anomalyId"]): a for a in anom_rows if isinstance(a, Mapping)}
    if len(expected_anom_ids) != len(anom_rows):
        raise SecretLifecycleError("audit.anomalies contains duplicate anomalyId values")

    raw_caller_summaries = audit.get("callerSummaries")
    if not isinstance(raw_caller_summaries, list) or not all(
        isinstance(c, Mapping) for c in raw_caller_summaries
    ):
        raise SecretLifecycleError("audit.callerSummaries must be a list of caller summary objects")
    sys_notif_count = audit.get("systemNotificationCount")
    if (
        not isinstance(sys_notif_count, int)
        or isinstance(sys_notif_count, bool)
        or sys_notif_count < 0
    ):
        raise SecretLifecycleError("audit.systemNotificationCount must be a non-negative integer")

    expected_audit_digest = _compute_audit_digest(
        vault_name=vault_name,
        window_start=str(audit.get("windowStart") or ""),
        window_end=str(audit.get("windowEnd") or ""),
        rbac_assignments=[r for r in rbac_rows if isinstance(r, Mapping)],
        caller_summaries=raw_caller_summaries,
        system_notification_count=sys_notif_count,
        anomalies=[a for a in anom_rows if isinstance(a, Mapping)],
    )
    if audit_digest != expected_audit_digest:
        raise SecretLifecycleError(
            "audit.auditDigest mismatch: audit payload has been modified since audit generation"
        )

    raw_asgn_decisions = decisions.get("assignments", {})
    if not isinstance(raw_asgn_decisions, Mapping):
        raise SecretLifecycleError("decisions.assignments must map assignmentId to decision object")
    if set(raw_asgn_decisions.keys()) != set(expected_asgn_ids.keys()):
        raise SecretLifecycleError(
            "decisions.assignments must cover every audited assignmentId 1-to-1"
        )

    recorded_assignments: list[dict[str, Any]] = []
    for asgn_id in sorted(expected_asgn_ids):
        src_row = expected_asgn_ids[asgn_id]
        dec_obj = raw_asgn_decisions[asgn_id]
        if isinstance(dec_obj, str):
            dec_val = dec_obj.strip()
            rationale = ""
        elif isinstance(dec_obj, Mapping):
            dec_val = str(dec_obj.get("decision") or "").strip()
            rationale = " ".join(str(dec_obj.get("rationale") or "").split())
        else:
            raise SecretLifecycleError(f"invalid decision payload for {asgn_id}")
        if dec_val not in VALID_ASSIGNMENT_DECISIONS:
            raise SecretLifecycleError(
                f"assignment {_safe_token(asgn_id, '<invalid-assignment>')} decision "
                "must be 'keep' or 'remove'"
            )
        needs_rationale = (
            dec_val == "remove"
            or str(src_row.get("access", "")).startswith("unclassified")
            or src_row.get("identity") == "unmapped"
        )
        if needs_rationale and not rationale:
            raise SecretLifecycleError(f"assignment {asgn_id} requires a non-empty human rationale")
        recorded_assignments.append(
            {
                "assignmentId": asgn_id,
                "principalId": src_row["principalId"],
                "identity": src_row["identity"],
                "role": src_row["role"],
                "access": src_row["access"],
                "scope": src_row["scope"],
                "decision": dec_val,
                "rationale": rationale,
            }
        )

    raw_anom_decisions = decisions.get("anomalies", {})
    if not isinstance(raw_anom_decisions, Mapping):
        raise SecretLifecycleError("decisions.anomalies must map anomalyId to disposition object")
    if set(raw_anom_decisions.keys()) != set(expected_anom_ids.keys()):
        raise SecretLifecycleError("decisions.anomalies must cover every audited anomalyId 1-to-1")

    recorded_anomalies: list[dict[str, Any]] = []
    for anom_id in sorted(expected_anom_ids):
        src_anom = expected_anom_ids[anom_id]
        disp_obj = raw_anom_decisions[anom_id]
        if not isinstance(disp_obj, Mapping):
            raise SecretLifecycleError(f"anomaly {anom_id} disposition must be an object")
        disp_val = str(disp_obj.get("disposition") or "").strip()
        rationale = " ".join(str(disp_obj.get("rationale") or "").split())
        if disp_val not in VALID_ANOMALY_DISPOSITIONS:
            raise SecretLifecycleError(
                f"anomaly {_safe_token(anom_id, '<invalid-anomaly>')} disposition must be one of "
                f"{sorted(VALID_ANOMALY_DISPOSITIONS)}"
            )
        if not rationale:
            raise SecretLifecycleError(
                f"anomaly {_safe_token(anom_id, '<invalid-anomaly>')} requires a "
                "non-empty human rationale"
            )
        recorded_anomalies.append(
            {
                "anomalyId": anom_id,
                "kind": src_anom["kind"],
                "principalId": src_anom["principalId"],
                "identity": src_anom["identity"],
                "disposition": disp_val,
                "rationale": rationale,
            }
        )

    prev_hash = GENESIS_HASH
    if prev_entry is not None:
        prev_vault = str(prev_entry.get("vaultName") or "")
        if prev_vault != vault_name:
            raise SecretLifecycleError(
                f"cannot chain vault {_safe_vault(vault_name)!r} onto ledger for "
                f"{_safe_vault(prev_vault)!r}"
            )
        prev_reviewed = parse_time(str(prev_entry.get("reviewedAt") or ""))
        if reviewed_utc <= prev_reviewed:
            raise SecretLifecycleError("reviewed_at must advance monotonically past prev_entry")
        raw_prev_hash = str(prev_entry.get("entryHash") or "")
        if not _HEX64_RE.match(raw_prev_hash):
            raise SecretLifecycleError("prev_entry.entryHash is missing or invalid")
        prev_hash = raw_prev_hash

    next_due = (reviewed_utc + dt.timedelta(days=review_interval_days)).date().isoformat()

    unsigned_entry: dict[str, Any] = {
        "schemaVersion": 1,
        "vaultName": vault_name,
        "windowStart": window_start,
        "windowEnd": window_end,
        "auditDigest": audit_digest,
        "reviewedAt": reviewed_utc.isoformat(),
        "reviewer": cleaned_reviewer,
        "reviewIntervalDays": review_interval_days,
        "nextReviewDue": next_due,
        "callerCount": len(raw_caller_summaries),
        "assignments": recorded_assignments,
        "anomalyDispositions": recorded_anomalies,
        "prevHash": prev_hash,
        "signatureAlgorithm": "hmac-sha256",
        "signingKeyId": cleaned_key_id,
    }
    entry_hash = _sha256_canonical(unsigned_entry)
    signature = hmac.new(signing_key, entry_hash.encode("ascii"), hashlib.sha256).hexdigest()
    return {
        **unsigned_entry,
        "entryHash": entry_hash,
        "signature": signature,
    }


def verify_access_review_ledger(
    entries: Sequence[Mapping[str, Any]],
    verification_keys: Mapping[str, bytes],
    *,
    now: dt.datetime,
    max_interval_days: int = 90,
    expected_vault_name: str | None = None,
    min_window_days: int | None = None,
) -> dict[str, Any]:
    """Verify hash-chain continuity, HMAC signatures, human decisions, and 90-day schedule."""
    assert_no_secret_material(entries, path="$.ledger")
    if expected_vault_name is not None:
        assert_no_secret_material(expected_vault_name, path="$.expectedVaultName")
    if min_window_days is not None and (
        not isinstance(min_window_days, int)
        or isinstance(min_window_days, bool)
        or min_window_days < 1
    ):
        raise SecretLifecycleError("min_window_days must be a positive integer")
    if now.tzinfo is None:
        raise SecretLifecycleError("now must include an explicit timezone offset")
    now_utc = now.astimezone(dt.UTC)

    problems: list[str] = []
    if not entries:
        return {
            "intact": False,
            "overdue": False,
            "entryCount": 0,
            "vaultName": expected_vault_name,
            "latestReviewedAt": None,
            "nextReviewDue": None,
            "problems": ["ledger contains no access review entries"],
        }

    for key_id, key_bytes in verification_keys.items():
        if not isinstance(key_bytes, (bytes, bytearray)) or len(key_bytes) < 32:
            problems.append(
                f"verification key {_safe_token(key_id, '<invalid-key-id>')!r} "
                "must be at least 32 bytes"
            )

    expected_prev = GENESIS_HASH
    ledger_vault: str | None = expected_vault_name.strip() if expected_vault_name else None
    if ledger_vault is not None and not _VAULT_NAME_RE.match(ledger_vault):
        problems.append("expectedVaultName must be 3-24 alphanumeric or hyphen characters")
        ledger_vault = None
    prev_reviewed_at: dt.datetime | None = None
    prev_window_end: dt.datetime | None = None
    latest_due: str | None = None
    latest_due_date: dt.date | None = None

    for idx, entry in enumerate(entries):
        prefix = f"entry[{idx}]"
        if not isinstance(entry, Mapping):
            problems.append(f"{prefix}: entry is not a JSON object")
            break

        vault_name = str(entry.get("vaultName") or "").strip()
        if not _VAULT_NAME_RE.match(vault_name):
            problems.append(f"{prefix}: invalid or missing vaultName")
        elif ledger_vault is None:
            ledger_vault = vault_name
        elif vault_name != ledger_vault:
            problems.append(
                f"{prefix}: vaultName {_safe_vault(vault_name)!r} does not match "
                f"ledger vault {_safe_vault(ledger_vault)!r}"
            )

        try:
            validate_human_reviewer(str(entry.get("reviewer") or ""))
        except SecretLifecycleError as exc:
            problems.append(f"{prefix}: {exc}")

        if not _HEX64_RE.match(str(entry.get("auditDigest") or "")):
            problems.append(f"{prefix}: missing or invalid auditDigest")

        raw_interval = entry.get("reviewIntervalDays")
        interval_ok = (
            isinstance(raw_interval, int)
            and not isinstance(raw_interval, bool)
            and 1 <= raw_interval <= max_interval_days
        )
        if not interval_ok:
            problems.append(
                f"{prefix}: reviewIntervalDays must be an integer between 1 and {max_interval_days}"
            )

        w_start: dt.datetime | None = None
        w_end: dt.datetime | None = None
        try:
            w_start = parse_time(str(entry.get("windowStart") or ""))
            w_end = parse_time(str(entry.get("windowEnd") or ""))
            if w_end <= w_start:
                problems.append(f"{prefix}: windowEnd must be after windowStart")
            else:
                if idx == 0:
                    eff_initial_days = (
                        (
                            raw_interval
                            if interval_ok and isinstance(raw_interval, int)
                            else max_interval_days
                        )
                        if min_window_days is None
                        else min_window_days
                    )
                    if (w_end - w_start) < dt.timedelta(days=eff_initial_days):
                        problems.append(
                            f"{prefix}: initial audit window is shorter than required "
                            f"{eff_initial_days}d coverage"
                        )
                else:
                    if prev_window_end is not None:
                        if w_start > prev_window_end:
                            problems.append(
                                f"{prefix}: windowStart leaves an unreviewed gap after "
                                "previous windowEnd"
                            )
                        if w_end <= prev_window_end:
                            problems.append(
                                f"{prefix}: windowEnd must advance past previous windowEnd"
                            )
                    eff_chained_days = 1 if min_window_days is None else min_window_days
                    if (w_end - w_start) < dt.timedelta(days=eff_chained_days):
                        problems.append(
                            f"{prefix}: chained audit window is shorter than required "
                            f"{eff_chained_days}d coverage"
                        )
                prev_window_end = w_end
        except (SecretLifecycleError, ValueError):
            problems.append(f"{prefix}: invalid windowStart/windowEnd timestamps")

        reviewed_at: dt.datetime | None = None
        try:
            reviewed_at = parse_time(str(entry.get("reviewedAt") or ""))
            if reviewed_at > now_utc:
                problems.append(f"{prefix}: reviewedAt is in the future relative to now")
            if w_end is not None:
                if w_end > reviewed_at:
                    problems.append(f"{prefix}: windowEnd cannot be after reviewedAt")
                elif (reviewed_at - w_end) > dt.timedelta(days=max_interval_days):
                    problems.append(
                        f"{prefix}: windowEnd is stale by more than "
                        f"{max_interval_days}d before reviewedAt"
                    )
            if prev_reviewed_at is not None:
                if reviewed_at <= prev_reviewed_at:
                    problems.append(f"{prefix}: reviewedAt is not strictly monotonic")
                elif (reviewed_at - prev_reviewed_at) > dt.timedelta(days=max_interval_days):
                    gap_days = (reviewed_at - prev_reviewed_at).days
                    problems.append(
                        f"{prefix}: schedule gap {gap_days}d exceeds {max_interval_days}d cadence"
                    )
            prev_reviewed_at = reviewed_at
        except (SecretLifecycleError, ValueError):
            problems.append(f"{prefix}: invalid reviewedAt timestamp")

        due_raw = str(entry.get("nextReviewDue") or "").strip()
        if not due_raw:
            problems.append(f"{prefix}: missing nextReviewDue")
        else:
            try:
                if len(due_raw) != 10:
                    raise ValueError("expected YYYY-MM-DD")
                parsed_due_date = dt.date.fromisoformat(due_raw)
                latest_due = due_raw
                latest_due_date = parsed_due_date
                if reviewed_at is not None and interval_ok:
                    assert isinstance(raw_interval, int)
                    expected_due = (
                        (reviewed_at.astimezone(dt.UTC) + dt.timedelta(days=raw_interval))
                        .date()
                        .isoformat()
                    )
                    if due_raw != expected_due:
                        problems.append(
                            f"{prefix}: nextReviewDue does not match "
                            f"reviewedAt + {raw_interval}d ({expected_due})"
                        )
            except (SecretLifecycleError, ValueError):
                problems.append(f"{prefix}: invalid nextReviewDue date")

        asgn_rows = entry.get("assignments", [])
        if (
            not isinstance(asgn_rows, Sequence)
            or isinstance(asgn_rows, (str, bytes))
            or not asgn_rows
        ):
            problems.append(f"{prefix}: no reviewed RBAC assignments recorded")
        else:
            seen_asgn: set[str] = set()
            for row in asgn_rows:
                if not isinstance(row, Mapping):
                    problems.append(f"{prefix}: invalid assignment row")
                    continue
                aid = str(row.get("assignmentId") or "")
                safe_aid = _safe_token(aid, "<invalid-assignment>")
                if not aid or aid in seen_asgn:
                    problems.append(f"{prefix}: missing or duplicate assignmentId")
                seen_asgn.add(aid)
                dec = row.get("decision")
                if dec not in VALID_ASSIGNMENT_DECISIONS:
                    problems.append(f"{prefix}: assignment {safe_aid} has invalid decision")
                needs_rat = (
                    dec == "remove"
                    or str(row.get("access", "")).startswith("unclassified")
                    or row.get("identity") == "unmapped"
                )
                if needs_rat and not str(row.get("rationale") or "").strip():
                    problems.append(f"{prefix}: assignment {safe_aid} missing required rationale")

        anom_rows = entry.get("anomalyDispositions", [])
        if not isinstance(anom_rows, Sequence) or isinstance(anom_rows, (str, bytes)):
            problems.append(f"{prefix}: anomalyDispositions must be a list")
        else:
            seen_anom: set[str] = set()
            for row in anom_rows:
                if not isinstance(row, Mapping):
                    problems.append(f"{prefix}: invalid anomaly disposition row")
                    continue
                anid = str(row.get("anomalyId") or "")
                safe_anid = _safe_token(anid, "<invalid-anomaly>")
                if not anid or anid in seen_anom:
                    problems.append(f"{prefix}: missing or duplicate anomalyId")
                seen_anom.add(anid)
                disp = row.get("disposition")
                if disp not in VALID_ANOMALY_DISPOSITIONS:
                    problems.append(f"{prefix}: anomaly {safe_anid} has invalid disposition")
                if not str(row.get("rationale") or "").strip():
                    problems.append(f"{prefix}: anomaly {safe_anid} missing required rationale")

        if entry.get("prevHash") != expected_prev:
            problems.append(f"{prefix}: prevHash mismatch, broken chain continuity")

        unsigned_copy = {k: v for k, v in entry.items() if k not in {"entryHash", "signature"}}
        expected_hash = _sha256_canonical(unsigned_copy)
        recorded_hash = str(entry.get("entryHash") or "")
        if recorded_hash != expected_hash:
            problems.append(f"{prefix}: entryHash mismatch, record tampered")

        if entry.get("signatureAlgorithm") != "hmac-sha256":
            problems.append(f"{prefix}: unsupported signatureAlgorithm")
        key_id = str(entry.get("signingKeyId") or "")
        recorded_sig = str(entry.get("signature") or "")
        key_material = verification_keys.get(key_id)
        if key_material is None:
            problems.append(
                f"{prefix}: unknown signingKeyId {_safe_token(key_id, '<invalid-key-id>')!r}"
            )
        elif isinstance(key_material, (bytes, bytearray)) and len(key_material) >= 32:
            expected_sig = hmac.new(
                key_material, recorded_hash.encode("ascii"), hashlib.sha256
            ).hexdigest()
            if not hmac.compare_digest(recorded_sig, expected_sig):
                problems.append(f"{prefix}: HMAC signature verification failed")

        expected_prev = recorded_hash

    overdue = False
    if latest_due is not None and latest_due_date is not None and now_utc.date() > latest_due_date:
        overdue = True
        problems.append(f"latest access review overdue since {latest_due}")

    return {
        "intact": len(problems) == 0,
        "overdue": overdue,
        "entryCount": len(entries),
        "vaultName": ledger_vault,
        "latestReviewedAt": prev_reviewed_at.isoformat() if prev_reviewed_at else None,
        "nextReviewDue": latest_due,
        "problems": problems,
    }
