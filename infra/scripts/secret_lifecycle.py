"""Key Vault secret lifecycle checks: inventory, staged rotation verification and signed reviews.

Reads Azure CLI / Log Analytics JSON metadata from files so it can be tested offline.
Fails closed on any raw secret material and never reads or prints secret values.

  secret_lifecycle.py check --inventory infra/secret-inventory.json --secrets secrets.json
      secrets.json is `az keyvault secret list --vault-name V -o json`.
  secret_lifecycle.py review --inventory infra/secret-inventory.json --assignments roles.json
      roles.json is `az role assignment list --scope <vault id> --include-inherited -o json`.
  secret_lifecycle.py rotation-plan --vault V --app-id ID
      prints the ordered, zero-downtime rotation steps (no secret is created).
  secret_lifecycle.py rotation-simulate
      offline model of the rotation order; exits 1 if sign-in would fail at any step.
  secret_lifecycle.py rotation-verify --evidence rotation-evidence.json [--out receipt.json]
      verifies dual-secret overlap, Key Vault version switchover, probes, and rollback gates.
  secret_lifecycle.py review-status --record review.json [--now ISO]
      exits 1 unless every decision is keep or remove, a reviewer is named and not overdue.
  secret_lifecycle.py rbac-merge --vault-id ID --inherited inh.json --all all.json [--out roles.json]
      merges `--scope <vault-id> --include-inherited` ancestors with child `<vault-id>/secrets/*`.
  secret_lifecycle.py access-audit --vault-name V --assignments roles.json --diagnostics diag.json
      audits Key Vault RBAC assignments and AzureDiagnostics data-plane logs against policy.
  secret_lifecycle.py review-sign --audit audit.json --decisions dec.json --reviewer NAME ...
      signs and hash-chains a completed access review record using an outside-repo 0600 key file.
  secret_lifecycle.py ledger-verify --ledger ledger.jsonl --keys-file keys.json [--vault-name V]
      verifies hash-chain continuity, HMAC-SHA256 signatures, human decisions, and 90-day cadence.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any

REPO_ROOT = Path(__file__).resolve().parents[2]
_CORE_SRC = str(REPO_ROOT / "src" / "core" / "src")
_CORE_PKG = str(REPO_ROOT / "src" / "core" / "src" / "zava_forward" / "core")
if _CORE_SRC not in sys.path:
    sys.path.insert(0, _CORE_SRC)
_existing_core_pkg = sys.modules.get("zava_forward.core")
if _existing_core_pkg is not None and hasattr(_existing_core_pkg, "__path__"):
    _pkg_paths = list(_existing_core_pkg.__path__)
    if _CORE_PKG not in _pkg_paths:
        _existing_core_pkg.__path__ = [_CORE_PKG, *_pkg_paths]

if TYPE_CHECKING:
    from zava_forward.core.secret_lifecycle import (
        DATA_ROLES,
        GENESIS_HASH,
        REQUIRED,
        SAFE_ORDER,
        SecretExposureError,
        SecretLifecycleError,
        access_review,
        assert_no_secret_material,
        audit_keyvault_data_plane_access,
        check_secrets,
        create_signed_access_review_record,
        default_expected_caller_policy,
        merge_vault_role_assignments,
        parse_time,
        review_status,
        rotation_plan,
        rotation_timeline,
        unwrap_arm_list_envelope,
        validate_human_reviewer,
        validate_inventory,
        verify_access_review_ledger,
        verify_staged_entra_rotation,
    )
else:
    from zava_forward.core.secret_lifecycle import (
        DATA_ROLES,
        GENESIS_HASH,
        REQUIRED,
        SAFE_ORDER,
        SecretExposureError,
        SecretLifecycleError,
        access_review,
        assert_no_secret_material,
        audit_keyvault_data_plane_access,
        check_secrets,
        create_signed_access_review_record,
        default_expected_caller_policy,
        merge_vault_role_assignments,
        parse_time,
        review_status,
        rotation_plan,
        rotation_timeline,
        unwrap_arm_list_envelope,
        validate_human_reviewer,
        validate_inventory,
        verify_access_review_ledger,
        verify_staged_entra_rotation,
    )

__all__ = [
    "DATA_ROLES",
    "GENESIS_HASH",
    "REQUIRED",
    "SAFE_ORDER",
    "SecretExposureError",
    "SecretLifecycleError",
    "access_review",
    "assert_no_secret_material",
    "audit_keyvault_data_plane_access",
    "check_secrets",
    "create_signed_access_review_record",
    "default_expected_caller_policy",
    "load",
    "load_ledger_entries",
    "main",
    "merge_vault_role_assignments",
    "parse_time",
    "review_status",
    "rotation_plan",
    "rotation_timeline",
    "unwrap_arm_list_envelope",
    "validate_human_reviewer",
    "validate_inventory",
    "verify_access_review_ledger",
    "verify_staged_entra_rotation",
]


_ENV_VAR_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_KEY_ID_RE = re.compile(r"^[A-Za-z0-9._:-]{3,128}$")


def _reject_json_constant(_token: str) -> Any:
    raise SecretLifecycleError("JSON input contains non-standard numeric constant")


def _strict_json_loads(raw_text: str, *, label: str) -> Any:
    try:
        return json.loads(raw_text, parse_constant=_reject_json_constant)
    except json.JSONDecodeError as exc:
        raise SecretLifecycleError(f"{label} must contain valid UTF-8 JSON") from exc


def load(path: str | Path) -> Any:
    """Load strict UTF-8 JSON from disk rejecting NaN/Infinity constants."""
    try:
        raw_text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise SecretLifecycleError("JSON input file could not be read as UTF-8") from exc
    return _strict_json_loads(raw_text, label="JSON input")


def _write_json(path: str | Path, payload: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_owner_only_key_bytes(path_str: str, *, flag_name: str) -> bytes:
    candidate = Path(path_str)
    if candidate.is_symlink():
        raise SecretLifecycleError(f"{flag_name} must not be a symbolic link")
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise SecretLifecycleError(f"{flag_name} does not exist or cannot be opened") from exc
    if not resolved.is_file():
        raise SecretLifecycleError(f"{flag_name} must be a regular file")
    if resolved.is_relative_to(REPO_ROOT):
        raise SecretLifecycleError(f"{flag_name} must reside outside the Git repository worktree")
    if os.name == "posix":
        mode = resolved.stat().st_mode
        if (mode & 0o077) != 0:
            raise SecretLifecycleError(f"{flag_name} must have owner-only permissions (0600)")
    return resolved.read_bytes()


def _load_signing_key(path_str: str) -> bytes:
    raw = _read_owner_only_key_bytes(path_str, flag_name="--key-file").strip()
    if len(raw) < 32:
        raise SecretLifecycleError("--key-file must contain at least 32 key bytes")
    return raw


def _resolve_rotation_signing_key(
    signing_key_env: str | None, signing_key_file: str | None
) -> bytes | None:
    env_name = (signing_key_env or "").strip()
    file_path = (signing_key_file or "").strip()
    if env_name and file_path:
        raise SecretLifecycleError("specify at most one of --signing-key-env or --signing-key-file")
    if env_name:
        if not _ENV_VAR_NAME_RE.match(env_name):
            raise SecretLifecycleError(
                "--signing-key-env must be a valid environment variable identifier"
            )
        env_val = os.environ.get(env_name, "").strip()
        if not env_val:
            raise SecretLifecycleError(
                "--signing-key-env target environment variable is unset or empty"
            )
        encoded = env_val.encode("utf-8")
        if len(encoded) < 32:
            raise SecretLifecycleError(
                "--signing-key-env target environment variable must provide at least "
                "32 UTF-8 key bytes"
            )
        return encoded
    if file_path:
        raw = _read_owner_only_key_bytes(file_path, flag_name="--signing-key-file").strip()
        if len(raw) < 32:
            raise SecretLifecycleError("--signing-key-file must contain at least 32 key bytes")
        return raw
    return None


def _load_verification_keys(path_str: str) -> dict[str, bytes]:
    raw = _read_owner_only_key_bytes(path_str, flag_name="--keys-file")
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SecretLifecycleError("--keys-file must contain valid UTF-8 JSON") from exc
    parsed = _strict_json_loads(decoded, label="--keys-file")
    if not isinstance(parsed, Mapping) or not parsed:
        raise SecretLifecycleError("--keys-file must be a non-empty JSON object mapping keyId")
    keys: dict[str, bytes] = {}
    for key_id, secret_str in parsed.items():
        if not isinstance(key_id, str) or not isinstance(secret_str, str):
            raise SecretLifecycleError("--keys-file entries must map string keyId to string key")
        cleaned_id = key_id.strip()
        if not _KEY_ID_RE.match(cleaned_id):
            raise SecretLifecycleError(
                "--keys-file keyId must be 3-128 alphanumeric, '.', '_', ':' or '-' characters"
            )
        encoded = secret_str.strip().encode("utf-8")
        if len(encoded) < 32:
            raise SecretLifecycleError(f"verification key {cleaned_id!r} must be at least 32 bytes")
        keys[cleaned_id] = encoded
    return keys


def load_ledger_entries(path: str | Path) -> list[dict[str, Any]]:
    """Read signed review ledger entries from JSONL or a JSON array."""
    try:
        raw_text = Path(path).read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError) as exc:
        raise SecretLifecycleError("ledger file could not be read as UTF-8") from exc
    if not raw_text:
        return []
    if raw_text.startswith("["):
        parsed = _strict_json_loads(raw_text, label="ledger JSON array")
        if not isinstance(parsed, list) or not all(isinstance(r, Mapping) for r in parsed):
            raise SecretLifecycleError("ledger JSON array must contain entry objects")
        return [dict(r) for r in parsed]
    entries: list[dict[str, Any]] = []
    for line_no, line in enumerate(raw_text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        parsed_line = _strict_json_loads(stripped, label=f"ledger line {line_no}")
        if not isinstance(parsed_line, Mapping):
            raise SecretLifecycleError(f"ledger line {line_no} is not a JSON object")
        entries.append(dict(parsed_line))
    return entries


def _ensure_jsonl_ledger_target(path: str | Path) -> None:
    target = Path(path)
    if not target.exists():
        return
    if target.read_text(encoding="utf-8").lstrip().startswith("["):
        raise SecretLifecycleError(
            "--ledger must be JSONL (.jsonl) for append; JSON array ledgers are read-only"
        )


def _append_jsonl_entry(path: str | Path, record: Mapping[str, Any]) -> None:
    target = Path(path)
    _ensure_jsonl_ledger_target(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    prefix = ""
    if target.exists() and target.stat().st_size > 0:
        with target.open("rb") as existing_handle:
            existing_handle.seek(-1, os.SEEK_END)
            if existing_handle.read(1) != b"\n":
                prefix = "\n"
    serialized = prefix + json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
    with target.open("a", encoding="utf-8") as handle:
        handle.write(serialized)


def _resolve_default_path(rel_path: str) -> str:
    local_candidate = Path(rel_path)
    if local_candidate.exists():
        return str(local_candidate)
    repo_candidate = REPO_ROOT / rel_path
    if repo_candidate.exists():
        return str(repo_candidate)
    return rel_path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "command",
        choices=[
            "check",
            "review",
            "rotation-plan",
            "rotation-simulate",
            "rotation-verify",
            "review-status",
            "rbac-merge",
            "access-audit",
            "review-sign",
            "ledger-verify",
        ],
    )
    parser.add_argument("--inventory", default="infra/secret-inventory.json")
    parser.add_argument("--role-matrix", default="infra/role-assignments.json")
    parser.add_argument("--secrets")
    parser.add_argument("--assignments")
    parser.add_argument("--inherited")
    parser.add_argument("--all", dest="all_assignments")
    parser.add_argument("--vault-id", default="")
    parser.add_argument("--diagnostics")
    parser.add_argument("--expected-principals")
    parser.add_argument("--evidence")
    parser.add_argument("--audit")
    parser.add_argument("--decisions")
    parser.add_argument("--record")
    parser.add_argument("--ledger")
    parser.add_argument("--key-file")
    parser.add_argument("--key-id")
    parser.add_argument("--keys-file")
    parser.add_argument("--signing-key-env")
    parser.add_argument("--signing-key-file")
    parser.add_argument("--allow-non-browser-mode", action="store_true")
    parser.add_argument("--out")
    parser.add_argument("--reviewer", default="")
    parser.add_argument("--vault", default="<vault>")
    parser.add_argument("--vault-name", default="")
    parser.add_argument("--app-id", default="<app id>")
    parser.add_argument("--min-overlap-minutes", type=int, default=60)
    parser.add_argument("--min-probe-samples", type=int, default=3)
    parser.add_argument("--min-probe-span-seconds", type=int, default=60)
    parser.add_argument("--max-probe-gap-seconds", type=int, default=60)
    parser.add_argument("--window-days", type=int, default=90)
    parser.add_argument("--min-window-days", type=int, default=None)
    parser.add_argument("--denied-401-threshold", type=int, default=5)
    parser.add_argument("--now", default=None)
    args = parser.parse_args(argv)

    try:
        now = parse_time(args.now) if args.now else dt.datetime.now(dt.UTC)

        if args.command == "rotation-plan":
            print("\n".join(rotation_plan(args.vault, args.app_id)))
            return 0

        if args.command == "rotation-simulate":
            timeline = rotation_timeline(SAFE_ORDER)
            for row in timeline:
                print(
                    f"{row['step']}: presented={row['presented']} "
                    f"valid={row['valid']} signInOk={row['signInOk']}"
                )
            return 0 if all(bool(row["signInOk"]) for row in timeline) else 1

        if args.command == "rotation-verify":
            if not args.evidence:
                print("--evidence is required", file=sys.stderr)
                return 2
            raw_evidence = load(args.evidence)
            if not isinstance(raw_evidence, Mapping):
                print("--evidence must contain a JSON object", file=sys.stderr)
                return 2
            rot_signing_key = _resolve_rotation_signing_key(
                args.signing_key_env, args.signing_key_file
            )
            receipt = verify_staged_entra_rotation(
                raw_evidence,
                now=now,
                min_overlap_minutes=args.min_overlap_minutes,
                require_browser_mode=not bool(args.allow_non_browser_mode),
                signing_key=rot_signing_key,
                min_probe_samples=args.min_probe_samples,
                min_probe_span_seconds=args.min_probe_span_seconds,
                max_probe_gap_seconds=args.max_probe_gap_seconds,
            )
            if args.out:
                _write_json(args.out, receipt)
            print(json.dumps(receipt, indent=2, sort_keys=True))
            return 0 if bool(receipt["ok"]) else 1

        if args.command == "rbac-merge":
            if not args.vault_id.strip() or not args.inherited or not args.all_assignments:
                print("--vault-id, --inherited, and --all are required", file=sys.stderr)
                return 2
            merged = merge_vault_role_assignments(
                load(args.inherited),
                load(args.all_assignments),
                vault_resource_id=args.vault_id,
            )
            if args.out:
                _write_json(args.out, merged)
            print(json.dumps(merged, indent=2, sort_keys=True))
            return 0

        if args.command == "review-status":
            if not args.record:
                print("--record is required", file=sys.stderr)
                return 2
            problems = review_status(load(args.record), now)
            print("\n".join(problems) if problems else "review record complete and current")
            return 1 if problems else 0

        inventory_path = _resolve_default_path(args.inventory)
        inventory = load(inventory_path)
        inv_problems = validate_inventory(inventory)
        if inv_problems:
            print("\n".join(inv_problems), file=sys.stderr)
            return 2

        if args.command == "check":
            if not args.secrets:
                print("--secrets is required", file=sys.stderr)
                return 2
            listed = unwrap_arm_list_envelope(load(args.secrets), label="$.secrets")
            findings = check_secrets(inventory, listed, now)
            for name, kind, detail in findings:
                print(f"{name}: {kind}: {detail}")
            return 1 if findings else 0

        if args.command == "review":
            if not args.reviewer:
                print("--reviewer is required", file=sys.stderr)
                return 2
            if not args.assignments:
                print("--assignments is required", file=sys.stderr)
                return 2
            assignments = unwrap_arm_list_envelope(load(args.assignments), label="$.assignments")
            print(json.dumps(access_review(inventory, assignments, args.reviewer, now), indent=2))
            return 0

        if args.command == "access-audit":
            vault_name = (
                args.vault_name.strip()
                if args.vault_name.strip()
                else ("" if args.vault == "<vault>" else args.vault.strip())
            )
            if not vault_name:
                print("--vault-name is required", file=sys.stderr)
                return 2
            if not args.assignments or not args.diagnostics:
                print("--assignments and --diagnostics are required", file=sys.stderr)
                return 2
            role_matrix = load(_resolve_default_path(args.role_matrix))
            principal_map: Mapping[str, str] = {}
            if args.expected_principals:
                loaded_map = load(args.expected_principals)
                if not isinstance(loaded_map, Mapping):
                    print("--expected-principals must be a JSON object", file=sys.stderr)
                    return 2
                principal_map = {str(k): str(v) for k, v in loaded_map.items()}
            expected_callers = default_expected_caller_policy(role_matrix, principal_map)
            assignments = unwrap_arm_list_envelope(load(args.assignments), label="$.assignments")
            diagnostics = unwrap_arm_list_envelope(load(args.diagnostics), label="$.diagnostics")
            window_start = now - dt.timedelta(days=args.window_days)
            audit_report = audit_keyvault_data_plane_access(
                vault_name=vault_name,
                inventory=inventory,
                assignments=assignments,
                diagnostics=diagnostics,
                expected_callers=expected_callers,
                window_start=window_start,
                window_end=now,
                denied_401_threshold=args.denied_401_threshold,
                max_window_days=max(95, args.window_days),
            )
            if args.out:
                _write_json(args.out, audit_report)
            print(json.dumps(audit_report, indent=2, sort_keys=True))
            return 0

        if args.command == "review-sign":
            if (
                not args.audit
                or not args.decisions
                or not args.reviewer
                or not args.key_file
                or not args.key_id
            ):
                print(
                    "--audit, --decisions, --reviewer, --key-file, and --key-id are required",
                    file=sys.stderr,
                )
                return 2
            signing_key = _load_signing_key(args.key_file)
            audit_data = load(args.audit)
            decisions_data = load(args.decisions)
            if not isinstance(audit_data, Mapping) or not isinstance(decisions_data, Mapping):
                print("--audit and --decisions must contain JSON objects", file=sys.stderr)
                return 2
            prev_entry: Mapping[str, Any] | None = None
            if args.ledger:
                _ensure_jsonl_ledger_target(args.ledger)
                if Path(args.ledger).exists():
                    existing_entries = load_ledger_entries(args.ledger)
                    if existing_entries:
                        prev_entry = existing_entries[-1]
            try:
                signed_record = create_signed_access_review_record(
                    audit=audit_data,
                    decisions=decisions_data,
                    reviewer=args.reviewer,
                    reviewed_at=now,
                    review_interval_days=int(inventory["reviewIntervalDays"]),
                    signing_key=signing_key,
                    key_id=args.key_id,
                    prev_entry=prev_entry,
                    min_window_days=args.min_window_days,
                )
            except SecretExposureError:
                raise
            except SecretLifecycleError as exc:
                print(str(exc), file=sys.stderr)
                return 1
            if args.ledger:
                _append_jsonl_entry(args.ledger, signed_record)
            print(json.dumps(signed_record, indent=2, sort_keys=True))
            return 0

        if not args.ledger or not args.keys_file:
            print("--ledger and --keys-file are required", file=sys.stderr)
            return 2
        verification_keys = _load_verification_keys(args.keys_file)
        entries = load_ledger_entries(args.ledger)
        expected_vault = args.vault_name.strip() or None
        verification = verify_access_review_ledger(
            entries,
            verification_keys,
            now=now,
            max_interval_days=int(inventory["reviewIntervalDays"]),
            expected_vault_name=expected_vault,
            min_window_days=args.min_window_days,
        )
        print(json.dumps(verification, indent=2, sort_keys=True))
        return 0 if bool(verification["intact"]) else 1

    except SecretExposureError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (SecretLifecycleError, json.JSONDecodeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
