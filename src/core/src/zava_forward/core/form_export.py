"""Read-only held draft export of a working form review; never a reviewed pack."""

import hashlib
import json
from copy import deepcopy
from typing import Any

from . import forms
from .doc_controls import DocumentUnavailable
from .form_review import NOTICE, _draft, _report

type Record = dict[str, Any]

EXPORT_NOTICE = (
    "Held draft export for human reading only. It is not a reviewed application or claim "
    "pack and does not submit anything or establish eligibility, approval, award, payment "
    "or cash. Finance review of a pack needs an approved template and rules."
)


BODY_KEYS = (
    "draft_id",
    "input_version",
    "schema_id",
    "schema_version",
    "schema_digest",
    "template",
    "rule_refs",
    "fields",
    "attachments",
    "stale_fields",
    "open_issues",
)


def _digest(body: Record) -> str:
    text = json.dumps(body, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(text.encode()).hexdigest()


def draft_export(store: Any, user: Record, case_id: str, draft_id: str) -> Record:
    """Return field values, evidence links and versions with a fixed Held status.

    The export holds no submission, eligibility or readiness claim, changes no
    record and has no reviewed state; the manual path is the working review itself.
    """
    with store.lock:
        forms._actor(store, user)
        case = store._case(case_id)
        draft = _draft(case, draft_id)
        try:
            report = _report(store, case, draft)
        except DocumentUnavailable:
            return dict(
                draft_id=draft_id,
                status="Unavailable",
                reviewed=False,
                notice="Working evidence is unavailable. Ask the document owner to recover it.",
            )
        fields = []
        for field in draft["schema"]["fields"]:
            row = report["fields"][field["id"]]
            evidence = row["evidence"]
            fields.append(
                dict(
                    field_id=field["id"],
                    value=deepcopy(row["value"]),
                    state=row["effective_state"],
                    source_id=None if evidence is None else evidence["source"]["id"],
                    source_version=None if evidence is None else evidence["source"]["version"],
                    document_hash=None
                    if evidence is None
                    else evidence["source"]["content_sha256"],
                    locator=None if evidence is None else deepcopy(evidence["locator"]),
                )
            )
        body = dict(
            draft_id=report["draft_id"],
            input_version=report["input_version"],
            schema_id=report["schema_id"],
            schema_version=report["schema_version"],
            schema_digest=report["schema_digest"],
            template=report["template"],
            rule_refs=report["rule_refs"],
            fields=fields,
            attachments=report["attachments"],
            stale_fields=report["stale_fields"],
            open_issues=report["issues"],
        )
        return dict(
            body,
            content_sha256=_digest(body),
            schema_impact=report["dependency_impact"]["schema"],
            status="Held",
            reviewed=False,
            submission="Not submitted",
            eligibility="Not assessed",
            notice=EXPORT_NOTICE,
            working_notice=NOTICE,
        )


def export_freshness(store: Any, user: Record, case_id: str, saved: Record) -> Record:
    """Compare a previously saved held export with the current working review.

    Only fields whose value, state or bound source changed, or that are stale
    now, are named. Nothing is written and a saved copy is never edited.
    """
    with store.lock:
        forms._actor(store, user)
        try:
            body = {key: saved[key] for key in BODY_KEYS}
            intact = saved["content_sha256"] == _digest(body)
            saved_rows = {row["field_id"]: row for row in body["fields"]}
        except (KeyError, TypeError, ValueError):
            intact = False
        if not intact:
            return dict(
                status="Invalid",
                stale_fields=[],
                reasons=["The saved export is incomplete or was edited after export."],
                action="Create a new held export from the working review.",
                reviewed=False,
            )
        try:
            current = draft_export(store, user, case_id, body["draft_id"])
        except KeyError:
            current = dict(
                status="Unavailable",
                notice="The working review for this export is missing or belongs to another case.",
            )
        if current["status"] == "Unavailable":
            return dict(
                status="Unavailable",
                stale_fields=[],
                reasons=[current["notice"]],
                action="Ask the document owner to recover the evidence.",
                reviewed=False,
            )
        reasons = []
        if body["schema_digest"] != current["schema_digest"]:
            reasons.append("The form schema or its rule references changed.")
        elif current["schema_impact"]["status"] == "Unknown":
            reasons.append("Schema lineage is missing or malformed.")
        elif current["schema_impact"]["affects_draft"]:
            reasons.append("A newer schema version changes this form.")
        if body["input_version"] != current["input_version"]:
            reasons.append("Reviewed field inputs changed after this export.")
        changed = {
            row["field_id"] for row in current["fields"] if saved_rows.get(row["field_id"]) != row
        }
        stale = sorted(changed | set(current["stale_fields"]))
        if stale and not reasons:
            reasons.append("A bound source or field state changed.")
        return dict(
            status="Stale" if reasons else "Current",
            stale_fields=stale,
            unaffected_fields=sorted(set(saved_rows) - set(stale)),
            reasons=reasons,
            action="Re-review the named fields and create a new held export." if reasons else None,
            reviewed=False,
        )
