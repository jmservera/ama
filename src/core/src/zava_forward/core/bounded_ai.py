"""Cross-capability bounded-AI invariant enforcement and audit contract (Issue #104).

Enforces and verifies the two programme-wide engineering invariants across every
registered AI capability in `zava_forward.core.ai_registry`:

1. AI never approves, executes, ranks, or mutates controlled records.
2. No registered AI capability is enabled beyond the exercise without finite
   call, token, and budget limits approved by a named human (and an owned alert).
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from typing import Any

from . import ai as _untyped_ai
from . import ai_consumption, rai_release
from . import ai_registry as _untyped_registry
from . import assistants as _untyped_assistants
from . import ranking as _untyped_ranking

ai_mod: Any = _untyped_ai
ai_registry: Any = _untyped_registry
assistants_mod: Any = _untyped_assistants
ranking_mod: Any = _untyped_ranking

ASSISTANT_CAPABILITIES: frozenset[str] = frozenset(
    {
        "stock-prioritisation",
        "assessment-preparation",
        "funding-evidence",
        "works-resident-coordination",
        "quality-evidence",
    }
)
RETAINED_CAPABILITIES: frozenset[str] = frozenset(
    {
        "briefing",
        "message",
        "summary",
        "priority",
        "funding_draft",
        "read_document",
    }
)
EXPECTED_CAPABILITIES: frozenset[str] = (
    ASSISTANT_CAPABILITIES
    | RETAINED_CAPABILITIES
    | frozenset({"chat-case-conversation", "aftercare-concern-pack"})
)

CONTROLLED_CASE_FIELDS: tuple[str, ...] = (
    "stage",
    "closed",
    "resident",
    "hazards",
    "signoffs",
    "grants",
    "procurement",
    "finance",
    "quality",
    "appointments",
    "service_requests",
    "handoff",
    "technical",
    "measures",
    "survey",
    "home",
)

FORBIDDEN_MUTATION_KEYS: frozenset[str] = frozenset(
    {
        "stage_transition",
        "approved_by",
        "executed",
        "executed_at",
        "rank_override",
        "ranking_override",
        "consent_granted",
        "payment_released",
        "grant_submitted",
        "hazard_cleared",
    }
)

UNAPPROVED_STATES: frozenset[str | None] = frozenset(
    {None, "Not reviewed", "pending", "pending_owner_review"}
)


class BoundedAiViolation(PermissionError):
    """Raised when an AI capability output or configuration violates an Issue #104 invariant."""


def _canonical_digest(value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def capability_inventory() -> dict[str, dict[str, Any]]:
    """Return the canonical registered capability map and verify exact registry parity."""
    tasks_raw = ai_registry.tasks()
    if not isinstance(tasks_raw, Mapping):
        raise BoundedAiViolation("ai_registry.tasks() did not return a mapping.")
    tasks: dict[str, dict[str, Any]] = {str(k): dict(v) for k, v in tasks_raw.items()}
    registered_ids = frozenset(tasks)
    if registered_ids != EXPECTED_CAPABILITIES:
        missing = sorted(EXPECTED_CAPABILITIES - registered_ids)
        extra = sorted(registered_ids - EXPECTED_CAPABILITIES)
        raise BoundedAiViolation(
            f"Registered capability drift: missing={missing}, unexpected={extra}"
        )
    assistant_ids = frozenset(str(k) for k in assistants_mod.REGISTRY)
    if assistant_ids != ASSISTANT_CAPABILITIES:
        raise BoundedAiViolation("assistants.REGISTRY drifted from canonical assistant set.")
    legacy_ids = frozenset(str(k) for k in ai_registry.LEGACY)
    if legacy_ids != RETAINED_CAPABILITIES:
        raise BoundedAiViolation("ai_registry.LEGACY drifted from canonical retained set.")
    return tasks


def snapshot_controlled_records(store: Any, *, aftercare: Any = None) -> dict[str, Any]:
    """Capture partitioned digests of controlled records vs. capability-scoped draft slots."""
    sync_fn = getattr(store, "_sync", None)
    if callable(sync_fn):
        sync_fn()
    cases_attr = getattr(store, "cases", None)
    if callable(cases_attr):
        loaded = cases_attr()
        raw_cases = list(loaded.values()) if isinstance(loaded, Mapping) else list(loaded)
    elif isinstance(cases_attr, Mapping):
        raw_cases = list(cases_attr.values())
    elif isinstance(cases_attr, Sequence):
        raw_cases = list(cases_attr)
    else:
        raise TypeError("Store must expose a cases mapping, sequence, or cases() method.")

    strict_cases: dict[str, str] = {}
    funding_workspace: dict[str, dict[str, Any]] = {}
    document_summaries: dict[str, str] = {}

    for case in sorted(raw_cases, key=lambda item: str(item.get("id", ""))):
        cid = str(case["id"])
        funding = dict(case.get("funding") or {})
        controlled_funding = {k: v for k, v in funding.items() if k not in ("draft", "status")}
        docs = [
            {
                k: v
                for k, v in dict(doc).items()
                if k not in ("summary", "summary_from_exception", "necessity_exception")
            }
            for doc in (case.get("documents") or [])
        ]
        strict_payload = {
            "fields": {field: case.get(field) for field in CONTROLLED_CASE_FIELDS},
            "funding_ok": bool(case.get("funding_ok")),
            "funding_controlled": controlled_funding,
            "documents_controlled": docs,
        }
        strict_cases[cid] = _canonical_digest(strict_payload)
        funding_workspace[cid] = {
            "draft_digest": _canonical_digest(funding.get("draft")),
            "status": funding.get("status"),
            "approved_by": funding.get("approved_by"),
        }
        doc_notes = [
            {
                "id": doc.get("id"),
                "summary": doc.get("summary"),
                "summary_from_exception": doc.get("summary_from_exception"),
                "necessity_exception": doc.get("necessity_exception"),
            }
            for doc in (case.get("documents") or [])
        ]
        document_summaries[cid] = _canonical_digest(doc_notes)

    rank_fn = getattr(store, "_ranking", None)
    if callable(rank_fn):
        ranking_digest = _canonical_digest(ranking_mod.canonical(rank_fn()))
    else:
        ranking_digest = _canonical_digest(ranking_mod.canonical(ranking_mod.rank_cases(raw_cases)))

    sql_cases_digest: str | None = None
    conn_fn = getattr(store, "assistant_connection", None)
    if callable(conn_fn):
        db = conn_fn()
        try:
            rows = db.execute(
                "SELECT id, stage, closed, hazard, rkey, decision, priority_correction "
                "FROM cases ORDER BY id"
            ).fetchall()
            sql_cases_digest = _canonical_digest([list(row) for row in rows])
        finally:
            db.close()

    aftercare_digest: str | None = None
    if aftercare is not None:
        aftercare_digest = _canonical_digest(
            {
                "concerns": getattr(aftercare, "concerns", None),
                "closures": getattr(aftercare, "closures", None),
            }
        )

    return {
        "strict_cases": strict_cases,
        "sql_cases": sql_cases_digest,
        "funding_workspace": funding_workspace,
        "document_summaries": document_summaries,
        "ranking": ranking_digest,
        "aftercare": aftercare_digest,
    }


def assert_controlled_records_unchanged(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    *,
    capability: str | None = None,
) -> None:
    """Raise BoundedAiViolation if any controlled record, approval, or ranking changed."""
    if before.get("strict_cases") != after.get("strict_cases"):
        raise BoundedAiViolation(
            f"Controlled case fields mutated during capability={capability!r}."
        )
    if before.get("sql_cases") != after.get("sql_cases"):
        raise BoundedAiViolation(
            f"Persisted SQL controlled case columns mutated during capability={capability!r}."
        )
    if before.get("ranking") != after.get("ranking"):
        raise BoundedAiViolation(
            f"Deterministic stock ranking mutated during capability={capability!r}."
        )
    if before.get("aftercare") != after.get("aftercare"):
        raise BoundedAiViolation(
            f"Controlled aftercare concerns/closures mutated during capability={capability!r}."
        )

    before_funding = before.get("funding_workspace")
    after_funding = after.get("funding_workspace")
    if capability == "funding_draft":
        if not isinstance(before_funding, Mapping) or not isinstance(after_funding, Mapping):
            raise BoundedAiViolation("Missing funding workspace snapshot.")
        if set(before_funding) != set(after_funding):
            raise BoundedAiViolation("Case set changed during funding_draft.")
        for cid, prev in before_funding.items():
            curr = after_funding[cid]
            if prev.get("approved_by") != curr.get("approved_by"):
                raise BoundedAiViolation(f"funding.approved_by mutated on {cid}.")
            if prev != curr:
                prev_status = prev.get("status")
                curr_status = curr.get("status")
                allowed_draft_move = (
                    prev_status in ("Not started", "To prepare", "Draft ready")
                    and curr_status == "Draft ready"
                ) or curr_status == prev_status
                if not allowed_draft_move:
                    raise BoundedAiViolation(
                        f"Illegal funding status transition {prev_status!r} -> {curr_status!r}."
                    )
    elif before_funding != after_funding:
        raise BoundedAiViolation(
            f"Unapproved funding draft workspace mutated by non-funding capability={capability!r}."
        )

    if capability != "read_document" and before.get("document_summaries") != after.get(
        "document_summaries"
    ):
        raise BoundedAiViolation(
            f"Document summary workspace mutated by non-document capability={capability!r}."
        )


def _iter_strings(value: object) -> list[str]:
    found: list[str] = []
    if isinstance(value, str):
        found.append(value)
    elif isinstance(value, Mapping):
        for k, v in value.items():
            if k != "ai_text":
                found.extend(_iter_strings(v))
    elif isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        for item in value:
            found.extend(_iter_strings(item))
    return found


def _iter_mapping_keys(value: object) -> set[str]:
    found: set[str] = set()
    if isinstance(value, Mapping):
        for k, v in value.items():
            found.add(str(k))
            found.update(_iter_mapping_keys(v))
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for item in value:
            found.update(_iter_mapping_keys(item))
    return found


def enforce_proposal_only(task_id: str, payload: Mapping[str, Any]) -> None:
    """Verify an AI capability envelope or proposal output remains strictly propose-only."""
    if not ai_registry.is_registered(task_id):
        raise BoundedAiViolation(f"Unregistered AI capability: {task_id!r}")
    if payload.get("approved") is True:
        raise BoundedAiViolation(f"Capability {task_id!r} emitted approved=True.")
    approval = payload.get("approval")
    if not (approval is None or (isinstance(approval, str) and approval in UNAPPROVED_STATES)):
        raise BoundedAiViolation(
            f"Capability {task_id!r} emitted approved/reviewed status {approval!r}."
        )
    status = payload.get("status")
    if isinstance(status, str) and status.casefold() in {
        "approved",
        "executed",
        "submitted",
        "awarded",
        "closed",
        "signed_off",
    }:
        raise BoundedAiViolation(f"Capability {task_id!r} emitted controlled status {status!r}.")
    bad_keys = FORBIDDEN_MUTATION_KEYS & _iter_mapping_keys(payload)
    if bad_keys:
        raise BoundedAiViolation(
            f"Capability {task_id!r} injected controlled mutation keys: {sorted(bad_keys)}"
        )
    for text in _iter_strings(payload):
        if ai_mod.FORBIDDEN.search(text):
            raise BoundedAiViolation(
                f"Capability {task_id!r} output matched forbidden approval/execution claim."
            )


def verify_non_exercise_enablement(
    task_id: str,
    *,
    env: Mapping[str, str] | None = None,
    task_entry: Mapping[str, Any] | None = None,
    release_record: Mapping[str, Any] | None = None,
    binding: Mapping[str, Any] | None = None,
    bound_keys: Sequence[str] = (),
    now: float | None = None,
    ledger: ai_consumption.Consumption | None = None,
    configuration: str | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    """Fail-closed cross-capability gate for enabling any AI capability beyond the exercise."""
    reasons: list[str] = []
    if not ai_registry.is_registered(task_id):
        return {
            "allowed": False,
            "capability": task_id,
            "consumption_capability": None,
            "reasons": ["unregistered-capability"],
        }

    consumption_cap = str(ai_registry.consumption_capability(task_id))
    entry: Mapping[str, Any] = (
        dict(ai_registry.get(task_id) or {}) if task_entry is None else task_entry
    )
    missing = list(ai_registry.missing_fields(entry))
    if missing:
        reasons.append(f"missing-registry-fields:{','.join(missing)}")
    if ai_registry.demo_activation_honoured(task_id, env):
        reasons.append("demo-activation-is-exercise-only")
    if entry.get("enabled") is False:
        reasons.append("capability-disabled-in-registry")
    if not rai_release.named_human(entry.get("accountable_individual")):
        reasons.append("accountable-individual-not-named-human")
    if not rai_release.named(entry.get("delegation")):
        reasons.append("delegation-missing")
    if entry.get("approval_state") in (None, "", ai_registry.UNAPPROVED, ai_registry.UNKNOWN):
        reasons.append("registry-approval-unapproved")
    authorities = entry.get("authority")
    if not isinstance(authorities, Mapping) or not authorities:
        reasons.append("registry-authorities-missing")
    elif not all(rai_release.named_human(holder) for holder in authorities.values()):
        reasons.append("registry-authority-holder-not-named-human")

    if release_record is None or binding is None or now is None:
        reasons.append("live-rai-release-missing")
    else:
        contract_gaps = rai_release.missing_contract(release_record, entry)
        if contract_gaps:
            reasons.extend(f"release-contract:{gap}" for gap in contract_gaps)
        if not rai_release.named_human(release_record.get("accountable_owner")):
            reasons.append("release-accountable-owner-not-named-human")
        consumption_cfg = release_record.get("consumption")
        if not isinstance(consumption_cfg, Mapping) or not rai_release.valid_consumption(
            dict(consumption_cfg)
        ):
            reasons.append("release-consumption-limits-invalid")
        binding_gaps = rai_release.missing_binding(
            release_record, binding, bound_keys, now, live=True
        )
        if binding_gaps:
            reasons.extend(f"release-binding:{gap}" for gap in binding_gaps)

    if ledger is None:
        reasons.append("consumption-ledger-missing")
    else:
        status = ledger.non_exercise_status(
            consumption_cap,
            configuration=configuration,
            model=model,
            now=now,
        )
        if not status["allowed"]:
            reasons.extend(f"consumption:{r}" for r in status["reasons"])

    return {
        "allowed": not reasons,
        "capability": task_id,
        "consumption_capability": consumption_cap,
        "reasons": reasons,
    }


def audit_registered_capabilities(
    env: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Audit all 13 registered capabilities against Issue #104 Invariants 1 and 2."""
    effective_env: Mapping[str, str] = {} if env is None else env
    tasks = capability_inventory()
    report: dict[str, dict[str, Any]] = {}
    violations: list[str] = []

    for task_id in sorted(tasks):
        entry = tasks[task_id]
        env_record = ai_registry.envelope(
            task_id,
            case_ids=["CASE-AUDIT"],
            source_versions={"case": "v1"},
            result={"source": "template", "text": "Template fallback"},
        )
        propose_only = True
        try:
            enforce_proposal_only(task_id, env_record)
        except BoundedAiViolation as exc:
            propose_only = False
            violations.append(f"{task_id}: {exc}")

        if not rai_release.strings(list(entry.get("prohibited_uses") or [])):
            propose_only = False
            violations.append(f"{task_id}: missing prohibited_uses")
        if not rai_release.strings(list(entry.get("limits") or [])):
            propose_only = False
            violations.append(f"{task_id}: missing limits")
        if "no write, send, approve or rank" not in json.dumps(entry).casefold():
            propose_only = False
            violations.append(f"{task_id}: missing propose-only boundary declaration")

        non_exercise = verify_non_exercise_enablement(task_id, env=effective_env)
        if non_exercise["allowed"]:
            violations.append(
                f"{task_id}: unexpectedly enabled beyond exercise without explicit owner limits"
            )

        report[task_id] = {
            "kind": entry.get("kind"),
            "consumption_capability": str(ai_registry.consumption_capability(task_id)),
            "dispatch_enabled": bool(ai_registry.is_dispatch_enabled(task_id, effective_env)),
            "demo_activation": bool(ai_registry.demo_activation_honoured(task_id, effective_env)),
            "propose_only": propose_only,
            "non_exercise_enabled": bool(non_exercise["allowed"]),
            "non_exercise_block_reasons": list(non_exercise["reasons"]),
        }

    return {
        "ok": not violations,
        "count": len(report),
        "capabilities": report,
        "violations": violations,
    }
