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
            status="Held",
            reviewed=False,
            submission="Not submitted",
            eligibility="Not assessed",
            notice=EXPORT_NOTICE,
            working_notice=NOTICE,
        )
