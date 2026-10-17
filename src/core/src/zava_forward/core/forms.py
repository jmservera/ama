"""Unapproved form definitions and source-linked candidates, never accepted fields."""

import csv
import hashlib
import io
import json
import math
import re
import uuid
from collections.abc import Callable
from contextlib import AbstractContextManager
from copy import deepcopy
from datetime import UTC, datetime
from typing import Any, Protocol

from . import ai_registry, projection
from .controls import RESIDENT_VIEW_ROLES
from .documents import ACCEPTED

type Record = dict[str, Any]
VERSION = "form-source-locator-1"
HUMAN_ONLY = ("declaration", "signature", "attestation", "consent", "approval")
TYPES = ("string", "integer", "number", "boolean", "date", "enum")
ROUTES = ("competitive", "allocation", "award-return", "claim")


class DocumentReader(Protocol):
    def get(self, case_id: str, doc_id: str) -> bytes: ...


class FormStore(Protocol):
    KINDS: tuple[str, ...]
    data: Record
    staff: dict[str, Record]
    lock: AbstractContextManager[Any]
    docstore: DocumentReader

    def _case(self, case_id: str) -> Record: ...
    def _doc_role(self, user: Record, what: str) -> None: ...
    def require_clean(self, doc: Record) -> None: ...
    def ensure_scanned(self, case_id: str, doc: Record, who: str) -> None: ...
    def audit(self, who: str, action: str, case_id: str, detail: str) -> None: ...
    def save(self) -> None: ...


def _fields(value: object, keys: set[str], label: str) -> Record:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"{label} must contain exactly: {', '.join(sorted(keys))}.")
    return value


def _text(value: object, label: str, limit: int = 200) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"Add {label}, at most {limit} characters.")
    return value


def _id(value: object) -> str:
    text = _text(value, "a stable identifier", 64)
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", text) is None:
        raise ValueError("Use letters, numbers, dot, underscore or hyphen for the identifier.")
    return text


def _positive(value: object) -> int:
    if type(value) is not int or not 1 <= value <= 2147483647:
        raise ValueError("Use a positive integer version or coordinate.")
    return value


def _scalar(value: object) -> bool:
    return type(value) in (str, int, bool) or type(value) is float and math.isfinite(value)


def _list(value: object, label: str, minimum: int = 0) -> list[Any]:
    if not isinstance(value, list) or not minimum <= len(value) <= 200:
        raise ValueError(f"{label} must be a list with {minimum} to 200 entries.")
    return value


def _reference(value: object) -> None:
    ref = _fields(value, {"id", "version", "evidence_ref"}, "Versioned reference")
    _id(ref["id"])
    _text(ref["version"], "the reference version", 80)
    _text(ref["evidence_ref"], "the evidence reference", 500)


def _registered(store: FormStore, email: str) -> Record | None:
    connect = getattr(store, "assistant_connection", None)
    if callable(connect):
        db = connect()
        try:
            row = db.execute("SELECT body FROM staff WHERE email=?", (email.lower(),)).fetchone()
        finally:
            db.close()
        if row is None:
            return None
        person: Record = json.loads(row[0])
        return person
    return store.staff.get(email.lower())


def _actor(store: FormStore, user: Record) -> Record:
    email = user.get("email")
    actor = _registered(store, email) if isinstance(email, str) else None
    if (
        actor is None
        or any(actor.get(k) != user.get(k) for k in ("code", "name", "role"))
        or actor.get("role") not in projection.FINANCE_VIEW
        or actor.get("role") not in RESIDENT_VIEW_ROLES
        or not projection.can_see_reason(actor)
    ):
        raise PermissionError(
            "Form collection requires current Finance, resident-record and reason-view rights."
        )
    store._doc_role(actor, "read")
    return actor


def _schema(value: object, store: FormStore) -> Record:
    row = _fields(
        value,
        {"id", "version", "form_type", "template", "reviewer", "funding", "rule_refs", "fields"},
        "Form schema",
    )
    _id(row["id"])
    _positive(row["version"])
    if row["form_type"] not in ("technical", "work-package", "invoice", "funding"):
        raise ValueError("Choose technical, work-package, invoice or funding form type.")
    _reference(row["template"])
    reviewer = _text(row["reviewer"], "a registered reviewer")
    if _registered(store, reviewer) is None:
        raise ValueError("Choose an existing registered reviewer; this records no approval.")
    funding = _fields(
        row["funding"], {"status", "scheme_id", "route", "evidence_ref"}, "Funding association"
    )
    if funding["status"] == "Evidenced":
        _id(funding["scheme_id"])
        if funding["route"] not in ROUTES:
            raise ValueError("Choose a declared funding route.")
        _text(funding["evidence_ref"], "the supplied funding-route evidence reference", 500)
    elif funding["status"] in ("Unknown", "Not applicable"):
        if any(funding[k] is not None for k in ("scheme_id", "route", "evidence_ref")):
            raise ValueError("Unknown/not-applicable funding associations have null references.")
        if row["form_type"] == "funding" and funding["status"] == "Not applicable":
            raise ValueError("Funding forms require an evidenced or explicitly unknown route.")
    else:
        raise ValueError("Funding association must be Evidenced, Unknown or Not applicable.")
    for ref in _list(row["rule_refs"], "Rule references"):
        _reference(ref)
    fields = _list(row["fields"], "Schema fields", 1)
    seen: set[str] = set()
    for field in fields:
        _fields(
            field,
            {
                "id",
                "section_id",
                "type",
                "unit",
                "options",
                "required",
                "required_when",
                "source_authority",
                "evidence_required",
                "calculation_ref",
                "category",
            },
            "Schema field",
        )
        fid = _id(field["id"])
        if fid in seen:
            raise ValueError("Schema field identifiers must be unique.")
        seen.add(fid)
        _id(field["section_id"])
        if field["type"] not in TYPES or type(field["required"]) is not bool:
            raise ValueError("Use a supported field type and a boolean required flag.")
        if field["category"] not in ("value", *HUMAN_ONLY):
            raise ValueError("Choose value or an explicit human-only field category.")
        if field["unit"] is not None:
            _text(field["unit"], "the unit", 80)
        options = _list(field["options"], "Field options")
        if (
            any(not _scalar(option) for option in options)
            or len({ai_registry.digest(option) for option in options}) != len(options)
            or (field["type"] == "enum") != bool(options)
        ):
            raise ValueError("Only enum fields have a nonempty unique scalar options list.")
        for item in _list(field["evidence_required"], "Evidence requirements", 1):
            _text(item, "an evidence requirement", 500)
        kinds: set[str] = set()
        ranks: set[int] = set()
        for policy in _list(field["source_authority"], "Source authority policy", 1):
            _fields(policy, {"kind", "rank", "evidence_ref"}, "Source authority policy")
            if policy["kind"] not in store.KINDS:
                raise ValueError("Choose an existing document kind for source policy.")
            rank = _positive(policy["rank"])
            if policy["kind"] in kinds or rank in ranks:
                raise ValueError("Source kinds and precedence ranks must be unique per field.")
            kinds.add(policy["kind"])
            ranks.add(rank)
            _text(policy["evidence_ref"], "the supplied source-policy evidence reference", 500)
        if field["calculation_ref"] is not None:
            _reference(field["calculation_ref"])
    for field in fields:
        for condition in _list(field["required_when"], "Required-field conditions"):
            _fields(condition, {"field_id", "equals"}, "Required-field condition")
            if (
                not isinstance(condition["field_id"], str)
                or condition["field_id"] not in seen
                or condition["field_id"] == field["id"]
                or not _scalar(condition["equals"])
            ):
                raise ValueError("A condition needs another declared field and a finite scalar.")
    return deepcopy(row)


def _commit(
    store: FormStore,
    actor: Record,
    action: str,
    case_id: str,
    detail: str,
    restore: Callable[[], None],
) -> None:
    discard = getattr(store, "_discard", None)
    if callable(discard):
        try:
            store.audit(actor["email"], action, case_id, detail)
            store.save()
        except BaseException:
            discard()
            raise
    else:
        saved = False
        try:
            store.save()
            saved = True
            store.audit(actor["email"], action, case_id, detail)
        except BaseException:
            restore()
            if saved:
                store.save()
            raise


def register_schema(store: FormStore, user: Record, body: object) -> Record:
    with store.lock:
        actor = _actor(store, user)
        definition = _schema(body, store)
        registry = store.data.get("form_schemas", [])
        versions = [r for r in registry if r["definition"]["id"] == definition["id"]]
        if definition["version"] != len(versions) + 1:
            raise ValueError("Register the next schema version; existing versions are immutable.")
        row = dict(
            definition=definition,
            digest=ai_registry.digest(definition),
            approval="Unapproved",
            approval_evidence=None,
            source_policy_status="Unapproved",
            recorded_by=actor["email"],
            recorded_at=datetime.now(UTC).isoformat(),
        )
        existed = "form_schemas" in store.data

        def restore() -> None:
            if existed:
                store.data["form_schemas"] = registry
            else:
                store.data.pop("form_schemas", None)

        store.data["form_schemas"] = registry + [row]
        _commit(
            store,
            actor,
            "form_schema_registered",
            "-",
            f"{definition['id']} version {definition['version']} digest {row['digest']}",
            restore,
        )
        return deepcopy(row)


def list_schemas(store: FormStore, user: Record) -> list[Record]:
    with store.lock:
        _actor(store, user)
        return deepcopy(store.data.get("form_schemas", []))


def _document(store: FormStore, case: Record, doc_id: str, actor: Record) -> Record:
    doc: Record | None = next((d for d in case["documents"] if d["id"] == doc_id), None)
    if doc is None:
        raise KeyError(doc_id)
    if doc.get("generated"):
        raise ValueError("Upload original source bytes; generated placeholders are not evidence.")
    store.ensure_scanned(case["id"], doc, actor["email"])
    store.require_clean(doc)
    return doc


def _processing(value: object) -> Record:
    row = _fields(
        value,
        {"kind", "parser", "parser_version", "model_version", "route_evidence", "error_record"},
        "Supplied processing lineage",
    )
    if row["kind"] not in ("text", "csv", "ocr"):
        raise ValueError("Choose text, csv or a supplied OCR import.")
    for key in ("parser", "parser_version"):
        _text(row[key], key, 160)
    for key in ("model_version", "route_evidence", "error_record"):
        if row[key] is not None:
            _text(row[key], key, 500)
    if row["kind"] == "ocr" and any(row[k] is None for k in ("route_evidence", "error_record")):
        raise ValueError("OCR imports need supplied route evidence and an error record.")
    return dict(deepcopy(row), assertion_status="Supplied, unverified")


def _source_cells(data: bytes, mime: str, kind: str) -> tuple[object, str | None]:
    if kind == "ocr":
        if mime not in (ACCEPTED["pdf"], ACCEPTED["png"], ACCEPTED["jpg"]):
            return None, "The supplied OCR route does not support this source type."
        return None, None
    if mime not in (ACCEPTED["txt"], ACCEPTED["csv"]):
        return None, "This source type needs an approved parser or manual transcription."
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return None, "The source cannot be read as UTF-8; use manual transcription."
    if kind == "text":
        return text, None
    try:
        return list(csv.reader(io.StringIO(text, newline=""), strict=True)), None
    except csv.Error:
        return None, "The CSV structure cannot be read; correct it or use manual transcription."


def _locator(value: object, kind: str, cells: Any, raw: str) -> Record:
    if kind == "text":
        loc = _fields(value, {"start", "end"}, "Text locator")
        start, end = loc["start"], loc["end"]
        if (
            type(start) is not int
            or type(end) is not int
            or not 0 <= start < end <= len(cells)
            or cells[start:end] != raw
        ):
            raise ValueError("Text locator must match the exact supplied raw source span.")
    elif kind == "csv":
        loc = _fields(value, {"row", "column"}, "CSV locator")
        row, column = _positive(loc["row"]), _positive(loc["column"])
        if row > len(cells) or column > len(cells[row - 1]) or cells[row - 1][column - 1] != raw:
            raise ValueError("CSV locator must match the exact supplied raw source cell.")
    else:
        loc = _fields(value, {"page", "region"}, "Supplied OCR locator")
        _positive(loc["page"])
        _text(loc["region"], "the supplied page region", 300)
    return deepcopy(loc)


def stage_candidates(store: FormStore, user: Record, case_id: str, body: object) -> Record:
    with store.lock:
        actor = _actor(store, user)
        request = _fields(
            body,
            {"schema_id", "schema_version", "document_id", "processing", "candidates"},
            "Candidate batch",
        )
        sid, version = _id(request["schema_id"]), _positive(request["schema_version"])
        schema_row = next(
            (
                r
                for r in store.data.get("form_schemas", [])
                if r["definition"]["id"] == sid and r["definition"]["version"] == version
            ),
            None,
        )
        if schema_row is None:
            raise ValueError("Register the exact schema version before collecting candidates.")
        definition = schema_row["definition"]
        fields = {f["id"]: f for f in definition["fields"]}
        processing = _processing(request["processing"])
        proposals = _list(request["candidates"], "Candidates", 1)
        case = store._case(case_id)
        doc = _document(store, case, _id(request["document_id"]), actor)
        data = store.docstore.get(case_id, doc["id"])
        actual_hash = hashlib.sha256(data).hexdigest()
        if actual_hash != doc.get("content_sha256") or type(doc.get("version")) is not int:
            raise ValueError("Source hash/version is missing or changed; resolve its evidence.")
        if doc["version"] < 1:
            raise ValueError("Source version must be positive.")
        for proposal in proposals:
            _fields(proposal, {"field_id", "raw_value", "locator"}, "Candidate")
            fid = _id(proposal["field_id"])
            if fid not in fields:
                raise ValueError("Choose a declared schema field.")
            if fields[fid]["category"] in HUMAN_ONLY:
                raise PermissionError("Declarations and authority-bearing fields are human-only.")
            if doc["kind"] not in [policy["kind"] for policy in fields[fid]["source_authority"]]:
                raise PermissionError("Source kind is not permitted by this field's schema policy.")
            _text(proposal["raw_value"], "the raw source value", 16000)
        cells, reason = _source_cells(data, doc["mime"], processing["kind"])
        candidates = []
        if reason is None:
            for proposal in proposals:
                candidates.append(
                    dict(
                        id=uuid.uuid4().hex,
                        field_id=proposal["field_id"],
                        raw_value=proposal["raw_value"],
                        locator=_locator(
                            proposal["locator"], processing["kind"], cells, proposal["raw_value"]
                        ),
                        review_state="Not reviewed",
                    )
                )
        row = dict(
            id=uuid.uuid4().hex,
            schema_id=sid,
            schema_version=version,
            schema_digest=schema_row["digest"],
            schema_approval=schema_row["approval"],
            case_id=case_id,
            source=dict(
                id=doc["id"],
                content_sha256=actual_hash,
                version=doc["version"],
                date=doc["at"],
                kind=doc["kind"],
                authority="Not established",
            ),
            processing=processing,
            verification=dict(
                verifier=VERSION,
                status=(
                    "Not verified"
                    if reason
                    else "Unverified OCR import"
                    if processing["kind"] == "ocr"
                    else "Exact source match"
                ),
            ),
            candidates=candidates,
            status="Manual recovery required" if reason else "Staged candidates only",
            recovery=(
                dict(
                    owner=definition["reviewer"],
                    reason=reason,
                    next_action="Correct the source or arrange authorized manual transcription.",
                )
                if reason
                else None
            ),
            recorded_by=actor["email"],
            recorded_at=datetime.now(UTC).isoformat(),
        )
        existed = "form_staging" in case
        previous = case.get("form_staging", [])

        def restore() -> None:
            if existed:
                case["form_staging"] = previous
            else:
                case.pop("form_staging", None)

        case["form_staging"] = previous + [row]
        _commit(
            store,
            actor,
            "form_candidates_staged",
            case_id,
            f"{row['id']} schema {sid}/{version} source {doc['id']} "
            f"hash {actual_hash} candidates {len(candidates)}",
            restore,
        )
        return deepcopy(row)


def list_candidates(store: FormStore, user: Record, case_id: str) -> list[Record]:
    with store.lock:
        _actor(store, user)
        case = store._case(case_id)
        visible = {
            d["id"]
            for d in case["documents"]
            if not d.get("generated") and d.get("scan", {}).get("status") == "clean"
        }
        return deepcopy(
            [batch for batch in case.get("form_staging", []) if batch["source"]["id"] in visible]
        )
