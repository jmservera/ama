"""Unapproved working reviews and held diagnostics, never financial authority."""

import hashlib
import re
import uuid
from copy import deepcopy
from datetime import UTC, date, datetime
from typing import Any

from . import forms
from .change_provenance import controlled
from .doc_controls import DocumentUnavailable
from .store import ConflictError

type Record = dict[str, Any]
type Digests = dict[str, str | None]

NOTICE = (
    "Unapproved working notes only. Not a reviewed application or claim pack; "
    "no eligibility, approval, submission, award, payment or cash is established."
)
HOLD_DEFINITIONS = (
    (
        "template-rules",
        "Finance and template owner",
        "Supply approved template, source policy, rules, funding route and reviewer authority.",
    ),
    (
        "OD-12",
        "Finance and Board",
        "Supply the approved investment envelope, asset plan, liquidity and covenant model.",
    ),
    (
        "OD-15",
        "Board and control owners",
        "Supply approved downside tolerances, pause conditions and restart authority.",
    ),
)


def _equal(left: object, right: object) -> bool:
    return type(left) is type(right) and left == right


def _valid(value: object, field: Record) -> bool:
    kind = field["type"]
    if kind == "enum":
        return any(_equal(value, option) for option in field["options"])
    if kind == "integer":
        return type(value) is int
    if kind == "number":
        return type(value) in (int, float) and forms._scalar(value)
    if kind == "boolean":
        return type(value) is bool
    if kind == "date":
        if not isinstance(value, str) or re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) is None:
            return False
        try:
            date.fromisoformat(value)
        except ValueError:
            return False
        return True
    return kind == "string" and isinstance(value, str)


def _schema(store: Any, sid: object, version: object) -> Record:
    forms._id(sid)
    forms._positive(version)
    registry: list[Record] = store.data.get("form_schemas", [])
    for row in registry:
        if row["definition"]["id"] == sid and row["definition"]["version"] == version:
            return row
    raise ValueError("Register the exact supplied schema version first; it remains unapproved.")


def _draft(case: Record, value: object) -> Record:
    did = forms._id(value)
    drafts: list[Record] = case.get("form_reviews", [])
    for draft in drafts:
        if draft["id"] == did:
            return draft
    raise KeyError(did)


def _document(store: Any, case: Record, did: str) -> Record:
    documents: list[Record] = case["documents"]
    doc = next((d for d in documents if d["id"] == did), None)
    if doc is None or doc.get("generated"):
        raise DocumentUnavailable(
            "Working evidence is unavailable. Ask the document owner to recover its source."
        )
    store.require_clean(doc)
    return doc


def _source_document(store: Any, case: Record, field: Record, source: Record) -> Record:
    doc = _document(store, case, source["id"])
    if doc["kind"] not in {p["kind"] for p in field["source_authority"]}:
        raise DocumentUnavailable("Source policy changed. Ask the evidence owner to review it.")
    return doc


def _digest(store: Any, case: Record, did: str, digests: Digests) -> str:
    if did not in digests:
        try:
            data = store.docstore.get(case["id"], did)
        except KeyError:
            digests[did] = None
        else:
            digests[did] = hashlib.sha256(data).hexdigest()
    digest = digests[did]
    if digest is None:
        raise DocumentUnavailable(
            "Working evidence is unavailable. Ask the document owner to recover its source."
        )
    return digest


def _visible(store: Any, case: Record, draft: Record, digests: Digests) -> None:
    fields = {f["id"]: f for f in draft["schema"]["fields"]}

    def check(fid: str, row: Record) -> None:
        evidence = row["evidence"]
        if evidence is not None:
            source = evidence["source"]
            _source_document(store, case, fields[fid], source)
            _digest(store, case, source["id"], digests)

    for report in (draft, *draft["diagnostics"]):
        for fid, row in report["fields"].items():
            check(fid, row)
        for event in report["history"]:
            for side in ("prior", "new"):
                check(event["field_id"], event[side])
        for source in report.get("attachments", []):
            _document(store, case, source["id"])
            _digest(store, case, source["id"], digests)


def _current(store: Any, case: Record, evidence: Record, digests: Digests | None = None) -> bool:
    source = evidence["source"]
    doc = _document(store, case, source["id"])
    return (
        all(doc.get(key) == source[key] for key in ("version", "content_sha256", "kind"))
        and _digest(store, case, doc["id"], {} if digests is None else digests)
        == source["content_sha256"]
    )


def _candidate(
    store: Any, case: Record, draft: Record, fid: str, batch_id: object, candidate_id: object
) -> Record:
    forms._id(batch_id)
    forms._id(candidate_id)
    batch = next((b for b in case.get("form_staging", []) if b["id"] == batch_id), None)
    if (
        batch is None
        or batch["case_id"] != case["id"]
        or batch["schema_id"] != draft["schema"]["id"]
        or batch["schema_version"] != draft["schema"]["version"]
        or batch["schema_digest"] != draft["schema_digest"]
    ):
        raise ValueError("Choose a candidate from this case and exact working schema.")
    candidate = next((c for c in batch["candidates"] if c["id"] == candidate_id), None)
    if candidate is None or candidate["field_id"] != fid:
        raise ValueError("Choose a candidate for this field.")
    evidence = dict(
        batch_id=batch["id"],
        candidate_id=candidate["id"],
        raw_value=candidate["raw_value"],
        locator=deepcopy(candidate["locator"]),
        source=deepcopy(batch["source"]),
        processing=deepcopy(batch["processing"]),
        verification=deepcopy(batch["verification"]),
    )
    field = next(f for f in draft["schema"]["fields"] if f["id"] == fid)
    _source_document(store, case, field, evidence["source"])
    if not _current(store, case, evidence):
        raise ValueError("The candidate source changed. Restage and review its current evidence.")
    return evidence


def _holds(case: Record, draft: Record, actor: Record) -> None:
    ledger = case.setdefault("finance_decision_holds", [])
    for decision, owner, next_action in HOLD_DEFINITIONS:
        scope = draft["id"] if decision == "template-rules" else None
        if any(h["decision_id"] == decision and h["draft_id"] == scope for h in ledger):
            continue
        ledger.append(
            dict(
                decision_id=decision,
                draft_id=scope,
                status="Held",
                owner_role=owner,
                next_action=next_action,
                approved_input=None,
                approval_evidence=None,
                recorded_by=actor["email"],
                recorded_at=datetime.now(UTC).isoformat(),
            )
        )


def _report(store: Any, case: Record, draft: Record, digests: Digests | None = None) -> Record:
    hashes = {} if digests is None else digests
    _visible(store, case, draft, hashes)
    schema = draft["schema"]
    latest = max(
        (
            r["definition"]["version"]
            for r in store.data.get("form_schemas", [])
            if r["definition"]["id"] == schema["id"]
        ),
        default=0,
    )
    schema_current = latest == schema["version"]
    fields = deepcopy(draft["fields"])
    issues: list[Record] = []
    confirmed: Record = {}
    stale = []
    freshness: dict[tuple[str, int, str, str], bool] = {}

    def current(evidence: Record) -> bool:
        source = evidence["source"]
        key = (source["id"], source["version"], source["content_sha256"], source["kind"])
        if key not in freshness:
            freshness[key] = _current(store, case, evidence, hashes)
        return freshness[key]

    for field in schema["fields"]:
        fid = field["id"]
        row = fields[fid]
        evidence = row["evidence"]
        source_current = True
        if schema_current and evidence is not None:
            source_current = current(evidence)
        if not schema_current or not source_current:
            row["effective_state"] = "Stale"
            stale.append(fid)
        else:
            row["effective_state"] = row["state"]
        if row["effective_state"] in ("Accepted", "Corrected"):
            if _valid(row["value"], field):
                if not isinstance(row["value"], str) or row["value"].strip():
                    confirmed[fid] = row["value"]
            else:
                issues.append(dict(field_id=fid, status="Fail", reason="Wrong schema value type."))
        elif row["effective_state"] == "Stale":
            issues.append(
                dict(field_id=fid, status="Unknown", reason="Bound source/schema changed.")
            )
        elif row["state"] == "Unknown" and field["category"] not in forms.HUMAN_ONLY:
            alternatives: set[str] = set()
            for batch in case.get("form_staging", []):
                if (
                    batch["case_id"] != case["id"]
                    or batch["schema_id"] != schema["id"]
                    or batch["schema_version"] != schema["version"]
                    or batch["schema_digest"] != draft["schema_digest"]
                ):
                    continue
                candidates = [c for c in batch["candidates"] if c["field_id"] == fid]
                if not candidates:
                    continue
                try:
                    _source_document(store, case, field, batch["source"])
                    if not current(batch):
                        continue
                except DocumentUnavailable:
                    continue
                alternatives.update(c["raw_value"] for c in candidates)
            if len(alternatives) > 1:
                issues.append(
                    dict(field_id=fid, status="Conflict", reason="Unreviewed source alternatives.")
                )
    for field in schema["fields"]:
        fid = field["id"]
        conditions = field["required_when"]
        required = field["required"] or any(
            c["field_id"] in confirmed and _equal(confirmed[c["field_id"]], c["equals"])
            for c in conditions
        )
        if required and fid not in confirmed:
            issues.append(
                dict(field_id=fid, status="Unknown", reason="Required confirmed input is missing.")
            )
        elif not required and any(c["field_id"] not in confirmed for c in conditions):
            issues.append(
                dict(field_id=fid, status="Unknown", reason="Conditional requirement is unknown.")
            )
        if field["calculation_ref"] is not None:
            issues.append(
                dict(field_id=fid, status="Unknown", reason="Approved calculation is unavailable.")
            )
    attachments = {
        (
            event["new"]["evidence"]["source"]["id"],
            event["new"]["evidence"]["source"]["version"],
        ): deepcopy(event["new"]["evidence"]["source"])
        for event in draft["history"]
        if event["new"]["evidence"] is not None
    }
    return dict(
        draft_id=draft["id"],
        input_version=draft["version"],
        schema_id=schema["id"],
        schema_version=schema["version"],
        schema_digest=draft["schema_digest"],
        template=deepcopy(schema["template"]),
        rule_refs=deepcopy(schema["rule_refs"]),
        funding=deepcopy(schema["funding"]),
        fields=fields,
        history=deepcopy(draft["history"]),
        attachments=list(attachments.values()),
        stale_fields=sorted(stale),
        issues=issues,
        approved_rule_validation="Not evaluated",
        unit_currency_verification="Not evaluated",
        reviewed_ready=False,
        status="Held",
        acceleration=dict(
            signal="Pause for human decision",
            scope="Diagnostic only; not a programme-wide release or live-activity hold",
            approved_envelope=None,
            approved_tolerances=None,
            breach_assessment="Not evaluated",
        ),
        notice=NOTICE,
    )


def view(store: Any, user: Record, case_id: str) -> Record:
    with store.lock:
        forms._actor(store, user)
        case = store._case(case_id)
        drafts = []
        for draft in case.get("form_reviews", []):
            try:
                report = dict(
                    _report(store, case, draft),
                    recorded_diagnostics=deepcopy(draft["diagnostics"]),
                )
            except DocumentUnavailable:
                report = dict(
                    draft_id=draft["id"],
                    status="Unavailable",
                    notice=(
                        "Working evidence is unavailable. "
                        "Ask the document owner to recover its source."
                    ),
                )
            drafts.append(report)
        return dict(
            drafts=drafts,
            decision_holds=deepcopy(case.get("finance_decision_holds", [])),
            notice=NOTICE,
        )


def action(store: Any, user: Record, case_id: str, body: object) -> Record:
    if not isinstance(body, dict):
        raise ValueError("Supply a single working-review action.")
    step = body.get("action")
    keys = {
        "open": {"action", "schema_id", "schema_version"},
        "review": {
            "action",
            "draft_id",
            "expected_version",
            "field_id",
            "decision",
            "batch_id",
            "candidate_id",
            "value",
            "reason",
        },
        "diagnose": {"action", "draft_id", "expected_version"},
    }
    if not isinstance(step, str) or step not in keys:
        raise ValueError(
            "Choose open, review or diagnose; approvals and reviewed exports are held."
        )
    forms._fields(body, keys[step], "Working review")
    with controlled(store, user, case_id) as (case, actor):
        forms._actor(store, user)
        digests: Digests = {}
        if step == "open":
            row = _schema(store, body["schema_id"], body["schema_version"])
            definition = row["definition"]
            draft = dict(
                id=uuid.uuid4().hex,
                version=1,
                schema=deepcopy(definition),
                schema_digest=row["digest"],
                status="Unapproved working notes",
                fields={
                    f["id"]: dict(value=None, state="Unknown", evidence=None)
                    for f in definition["fields"]
                },
                history=[],
                diagnostics=[],
                recorded_by=actor["email"],
                recorded_at=datetime.now(UTC).isoformat(),
            )
            case.setdefault("form_reviews", []).append(draft)
        else:
            draft = _draft(case, body["draft_id"])
            expected = forms._positive(body["expected_version"])
            if expected != draft["version"]:
                raise ConflictError("The working review changed. Reload before retrying.")
            _visible(store, case, draft, digests)
            if step == "review":
                _review(store, case, draft, actor, body)
            draft["version"] += 1
        _holds(case, draft, actor)
        report = _report(store, case, draft, digests)
        if step == "diagnose":
            draft["diagnostics"].append(deepcopy(report))
        store.audit(actor["email"], f"form_review_{step}", case_id, draft["id"])
        store.save()
        return deepcopy(report)


def _review(store: Any, case: Record, draft: Record, actor: Record, body: Record) -> None:
    fid = forms._id(body["field_id"])
    field = next((f for f in draft["schema"]["fields"] if f["id"] == fid), None)
    if field is None:
        raise ValueError("Choose a field in this working schema.")
    if field["category"] in forms.HUMAN_ONLY:
        raise PermissionError("Authority-bearing fields cannot be accepted by working review.")
    reason = forms._text(body["reason"], "a review reason", 500)
    decision = body["decision"]
    evidence = None
    value = None
    if decision in ("accept", "correct"):
        evidence = _candidate(store, case, draft, fid, body["batch_id"], body["candidate_id"])
        if decision == "accept":
            if body["value"] is not None:
                raise ValueError(
                    "Acceptance copies raw text; use an explicit correction to change it."
                )
            value = evidence["raw_value"]
        else:
            value = body["value"]
            if not forms._scalar(value) or isinstance(value, str) and len(value) > 16000:
                raise ValueError("Supply a finite scalar correction, at most 16000 characters.")
    elif decision != "reject":
        raise ValueError("Choose accept, correct or reject.")
    elif any(body[key] is not None for key in ("batch_id", "candidate_id", "value")):
        raise ValueError(
            "A rejection has no new candidate or value; prior evidence stays in history."
        )
    new = dict(
        value=value,
        state={"accept": "Accepted", "correct": "Corrected", "reject": "Rejected"}[decision],
        evidence=evidence,
    )
    draft["history"].append(
        dict(
            field_id=fid,
            input_version=draft["version"] + 1,
            prior=deepcopy(draft["fields"][fid]),
            new=deepcopy(new),
            decision=decision,
            reviewer=actor["email"],
            reason=reason,
            at=datetime.now(UTC).isoformat(),
        )
    )
    draft["fields"][fid] = new
