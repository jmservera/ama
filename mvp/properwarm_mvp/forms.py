"""Source-bound fictional exercise forms, with no submission or approval powers.

Callers supply authenticated actors and independently authorized source metadata;
neither document text nor model output is an authorization input. Operations
return new JSON-compatible dictionaries. Persist them atomically on the owning
case and apply ``last_invalidation`` to external dependency references.
"""

from __future__ import annotations

import csv
from copy import deepcopy
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext
import hashlib
import io
import json
import re
from typing import TypeAlias

JSON: TypeAlias = None | bool | int | float | str | list["JSON"] | dict[str, "JSON"]
State: TypeAlias = dict[str, JSON]

SCHEME_ID: str = "proper-warm-exercise-fund"
SCHEMA_VERSION: str = "exercise-1"
RULE_VERSION: str = "exercise-fund-1"
PARSER_VERSION: str = "labelled-text-csv-1"
FIELD_REVIEW_ROLES: tuple[str, ...] = (
    "Grants and Evidence Officer", "Retrofit Coordinator",
    "Retrofit Programme Manager", "Programme Support Officer",
)
PACK_REVIEW_ROLES: tuple[str, ...] = (
    "Retrofit Programme Manager", "Programme Support Officer",
)
PROTECTED_FIELDS: tuple[str, ...] = (
    "declaration", "signature", "certification", "resident_decision",
    "controlled_approval", "match_budget_approved",
)
__all__: tuple[str, ...] = (
    "JSON", "State", "SCHEMAS", "SCHEME_ID", "SCHEMA_VERSION", "RULE_VERSION",
    "PARSER_VERSION", "FIELD_REVIEW_ROLES", "PACK_REVIEW_ROLES", "PROTECTED_FIELDS",
    "create_draft", "register_source", "update_source", "extract_candidates",
    "select_candidate", "review_field", "human_field_action", "validate_draft",
    "recalculate", "update_versions", "set_attachments", "link_downstream",
    "review_pack", "export_pack",
)
_MONEY = re.compile(r"^\d+(?:\.\d{1,2})?$")
_NUMBER = re.compile(r"^\d+(?:\.\d+)?$")
_HASH = re.compile(r"^[0-9a-f]{64}$")


def _field(kind: str, *, required: bool = True, unit: str | None = None,
           options: tuple[str, ...] = (), dependencies: tuple[str, ...] = (),
           authority: tuple[str, ...] = ("technical", "finance", "funding", "survey", "human"),
           protected: bool = False, roles: tuple[str, ...] = FIELD_REVIEW_ROLES,
           conditional: dict[str, JSON] | None = None, rule: bool = False) -> State:
    return {
        "type": kind, "required": required, "unit": "GBP" if kind == "money" else unit,
        "currency": "GBP" if kind in ("money", "calculated_money") else None, "options": list(options),
        "dependencies": list(dict.fromkeys([*dependencies, *(
            [conditional["field"]] if conditional else [])])), "authority": list(authority),
        "protected": protected, "reviewer_roles": list(roles),
        "conditional": conditional, "rule": RULE_VERSION if rule else None,
    }


def _schemas() -> dict[str, State]:
    identity = {"home_ids": _field("home_ids")}
    protected = {
        "signature": _field("text", required=False, protected=True, roles=PACK_REVIEW_ROLES,
                            dependencies=("declaration",)),
        "resident_decision": _field("text", required=False, protected=True, roles=("Resident",)),
        "controlled_approval": _field("text", required=False, protected=True,
                                     roles=PACK_REVIEW_ROLES),
    }
    funding = {
        **identity,
        "epc_band": _field("enum", options=tuple("ABCDEFG"), authority=("survey", "technical")),
        "eligibility": _field("enum", options=("eligible", "ineligible", "unknown"),
                              authority=("funding", "finance"), rule=True),
        "eligible_cost": _field("money", authority=("finance", "funding"), rule=True),
        "total_cost": _field("money", authority=("finance",)),
        "co_funding": _field("money", authority=("finance",)),
        "grant_amount": _field("calculated_money", unit="GBP",
                              dependencies=("eligible_cost", "eligibility"), rule=True),
        "provider_cost": _field("calculated_money", unit="GBP",
                               dependencies=("total_cost", "grant_amount"), rule=True),
        "match_budget_approved": _field(
            "bool", protected=True, roles=PACK_REVIEW_ROLES,
            dependencies=("co_funding", "provider_cost")),
        "declaration": _field(
            "bool", protected=True, roles=PACK_REVIEW_ROLES,
            dependencies=("home_ids", "epc_band", "eligibility", "eligible_cost",
                          "total_cost", "co_funding", "grant_amount", "provider_cost",
                          "match_budget_approved")),
        **deepcopy(protected),
    }
    variants = {
        "competitive": {**deepcopy(funding), "narrative": _field("text", authority=("funding", "human"))},
        "allocation": {**deepcopy(funding), "allocation_reference": _field("text", authority=("funding",))},
        "award_return": {**deepcopy(funding), "award_reference": _field("text", authority=("funding",))},
        "claim": {
            **deepcopy(funding),
            "award_reference": _field("text", authority=("funding",)),
            "awarded_amount": _field("money", authority=("funding",)),
            "claim_amount": _field("money", authority=("finance",)),
            "completed": _field("bool", authority=("technical",)),
            "invoice_reference": _field("text", required=False, authority=("finance",),
                                        conditional={"field": "completed", "equals": True}),
        },
        "technical": {
            **identity,
            "epc_band": _field("enum", options=tuple("ABCDEFG"), authority=("survey", "technical")),
            "floor_area": _field("number", unit="m2", authority=("survey", "technical")),
            "assessment_notes": _field("text", authority=("survey", "technical", "human")),
            "certification": _field("bool", protected=True, roles=("Retrofit Coordinator",),
                                    dependencies=("epc_band", "floor_area", "assessment_notes")),
            **deepcopy(protected),
        },
        "invoice": {
            **identity,
            "invoice_reference": _field("text", authority=("finance",)),
            "quantity": _field("number", unit="count", authority=("finance",)),
            "unit_cost": _field("money", authority=("finance",)),
            "invoice_total": _field("calculated_money", unit="GBP",
                                   dependencies=("quantity", "unit_cost")),
            "declaration": _field("bool", protected=True, roles=PACK_REVIEW_ROLES,
                                  dependencies=("invoice_reference", "quantity", "unit_cost",
                                                "invoice_total")),
            **deepcopy(protected),
        },
    }
    for kind in ("competitive", "allocation", "award_return", "claim"):
        extras = tuple(key for key in variants[kind] if key not in funding)
        variants[kind]["declaration"]["dependencies"].extend(extras)
    variants["technical"]["signature"]["dependencies"] = ["certification"]
    for kind in ("competitive", "allocation", "award_return", "claim"):
        variants[kind]["grant_amount"]["calculation"] = "min(7500, eligible_cost * 0.5)"
        variants[kind]["provider_cost"]["calculation"] = "total_cost - grant_amount"
    variants["invoice"]["invoice_total"]["calculation"] = "quantity * unit_cost"
    variants["invoice"]["invoice_total"]["rule"] = "exercise-invoice-1"
    return {
        kind: {"id": kind, "version": SCHEMA_VERSION, "approved": True,
               "fictional": True, "funding": kind not in ("technical", "invoice"),
               "rule_version": RULE_VERSION if kind not in ("technical", "invoice")
               else "exercise-invoice-1" if kind == "invoice" else None,
               "route": kind if kind not in ("technical", "invoice") else "not_applicable",
               "reviewer_roles": list(PACK_REVIEW_ROLES), "fields": deepcopy(fields)}
        for kind, fields in variants.items()
    }


SCHEMAS: dict[str, State] = _schemas()


def _copy(value: State) -> State:
    json.dumps(value, allow_nan=False)
    return deepcopy(value)


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty supplied string.")
    return value


def _actor(actor: State, roles: list[str] | tuple[str, ...]) -> State:
    identity = actor.get("id") or actor.get("email")
    _text(identity, "Human identity")
    _text(actor.get("name"), "Human name")
    if actor.get("role") not in roles:
        raise PermissionError("This human role is not authorized for the form action.")
    return {"id": identity, "name": actor["name"], "role": actor["role"]}


def _definition(draft: State, field_id: str) -> State:
    _text(field_id, "Field ID")
    if field_id not in draft["schema"]["fields"]:
        raise ValueError("Field is not in the approved form schema.")
    return draft["schema"]["fields"][field_id]


def _authorized_source(draft: State, source: State, *, check_routes: bool = True) -> State:
    # These attributes come from the caller's evidence authorization, not bytes.
    if (source.get("authorized") is not True or source.get("case_id") != draft["case_id"]
            or (source.get("scheme_id") not in (None, draft["funding"]["scheme_id"]))):
        raise PermissionError("Source is unavailable for this case/form.")
    for key in ("id", "version", "authority", "media_type"):
        _text(source.get(key), f"Source {key}")
    if not isinstance(source.get("hash"), str) or not _HASH.fullmatch(source["hash"]):
        raise ValueError("Source hash must be the SHA-256 of the authorized raw bytes.")
    allowed = source.get("field_ids")
    if not isinstance(allowed, list) or not all(isinstance(item, str) for item in allowed):
        raise ValueError("Source field_ids must be an explicit field allowlist.")
    if any(item not in draft["schema"]["fields"] for item in allowed):
        raise ValueError("Source field allowlist includes a field outside this schema.")
    if source.get("routes") is not None and (
            not isinstance(source["routes"], list)
            or not all(isinstance(route, str) for route in source["routes"])):
        raise ValueError("Source routes must be an explicit list of permitted route IDs.")
    if (check_routes and draft["schema"]["funding"] and source.get("routes") is not None
            and draft["funding"]["route"] not in source["routes"]):
        raise PermissionError("Source is unavailable for this case/form.")
    return _copy(source)


def _evidence(draft: State, ids: list[str], *, field_id: str | None = None) -> list[State]:
    if not isinstance(ids, list) or not all(isinstance(source_id, str) for source_id in ids):
        raise ValueError("Evidence must be a list of authorized source IDs.")
    if not ids:
        raise ValueError("Supply authorized evidence; otherwise record an unresolved correction.")
    refs = []
    for source_id in ids:
        source = draft["sources"].get(source_id)
        if source is None:
            raise PermissionError("Evidence is unavailable for this case/form.")
        _authorized_source(draft, source)
        if field_id is not None:
            definition = _definition(draft, field_id)
            if (field_id not in source["field_ids"]
                    or source["authority"] not in definition["authority"]):
                raise PermissionError("Evidence is unavailable for this field.")
        refs.append({key: source[key] for key in ("id", "version", "hash")})
    return refs


def create_draft(case_id: str, form_type: str, *, route: State | None = None,
                 sources: list[State] | None = None,
                 schema_version: str = SCHEMA_VERSION) -> State:
    """Open an approved draft; unknown funding routes remain visibly blocked.

    Route requires scheme_id, route, version and source_id. Sources require id,
    case_id, version, hash, authorized=True, authority, media_type and field_ids.
    Funding route evidence additionally declares scheme_id and permitted routes.
    """
    _text(case_id, "Case ID")
    if form_type not in SCHEMAS or schema_version != SCHEMA_VERSION:
        raise ValueError("Unapproved form schema/version; ask the template owner to correct it.")
    schema = deepcopy(SCHEMAS[form_type])
    funding = {"scheme_id": SCHEME_ID if schema["funding"] else None,
               "route": route.get("route") if route else None,
               "version": route.get("version") if route else None,
               "source_id": route.get("source_id") if route else None,
               "status": "unknown" if schema["funding"] else "not_applicable"}
    draft = {
        "case_id": case_id, "form_type": form_type, "schema": schema,
        "schema_version": schema_version, "rule_version": schema["rule_version"],
        "input_version": 1, "funding": funding, "sources": {}, "source_history": [],
        "fields": {
            key: {"value": None, "unit": None, "currency": None, "state": "unknown",
                  "stale": False, "input_version": 1, "candidates": [],
                  "proposal": None, "proposal_state": "unknown", "proposal_history": [],
                  "current_review": None}
            for key in schema["fields"]
        },
        "reviews": [], "pack_reviews": [], "stale_reviews": [], "exports": [],
        "attachments": [], "manual_tasks": [], "history": [], "downstream": {},
        "last_invalidation": {"fields": [], "calculations": [], "proposals": [],
                              "reviews": [], "downstream": []},
    }
    for source in sources or []:
        checked = _authorized_source(draft, source)
        if checked["id"] in draft["sources"]:
            raise ValueError("Duplicate source ID; update the existing source explicitly.")
        draft["sources"][checked["id"]] = checked
    if not schema["funding"]:
        if route is not None and route.get("route") != "not_applicable":
            raise ValueError("This non-funding template requires a not-applicable association.")
        funding["route"] = "not_applicable"
    elif route and route.get("scheme_id") == SCHEME_ID:
        funding["status"] = "evidenced" if _route_ok(draft) else "unknown"
    return draft


def _route_ok(draft: State) -> bool:
    funding = draft["funding"]
    source = draft["sources"].get(funding["source_id"])
    return bool(
        source and source.get("authorized") is True and source["case_id"] == draft["case_id"]
        and source.get("scheme_id") == SCHEME_ID and source["authority"] == "funding"
        and funding["route"] == draft["schema"]["route"]
        and funding["route"] in source.get("routes", [])
        and isinstance(funding["version"], str) and funding["version"].strip()
        and source["version"] == funding["version"]
    )


def _prepare(draft: State) -> None:
    if draft["schema"]["funding"] and (
            draft["funding"]["status"] != "evidenced" or not _route_ok(draft)):
        raise ValueError("Unknown/stale funding route blocks preparation; Finance must correct its evidence.")


def _closure(draft: State, roots: set[str]) -> set[str]:
    affected = set(roots)
    while True:
        following = {key for key, definition in draft["schema"]["fields"].items()
                     if set(definition["dependencies"]) & affected}
        expanded = affected | following
        if expanded == affected:
            return affected
        affected = expanded


def _invalidate(draft: State, roots: set[str], *, keep: set[str] | None = None,
                pack_only: bool = False, pack_review_ids: set[str] | None = None) -> None:
    changed = _closure(draft, roots)
    affected = changed - (keep or set())
    stale_reviews = set()
    proposals = []
    calculations = []
    for key in sorted(affected):
        field = draft["fields"][key]
        field["stale"] = True
        if field["value"] is not None:
            field["state"] = "stale"
        if field["current_review"]:
            stale_reviews.add(field["current_review"])
        if field["proposal"] is not None:
            proposals.append(key)
        if draft["schema"]["fields"][key]["type"] == "calculated_money":
            calculations.append(key)
    if changed or pack_only:
        stale_reviews.update(review["id"] for review in draft["pack_reviews"]
                             if changed or pack_review_ids is None or review["id"] in pack_review_ids)
    downstream = []
    for key, reference in draft["downstream"].items():
        if set(reference["depends_on"]) & changed:
            reference["stale"] = True
            downstream.append(key)
    draft["stale_reviews"] = sorted(set(draft["stale_reviews"]) | stale_reviews)
    draft["last_invalidation"] = {
        "fields": sorted(affected), "calculations": sorted(calculations),
        "proposals": sorted(proposals), "reviews": sorted(stale_reviews),
        "downstream": sorted(downstream),
    }
    draft["input_version"] += 1


def register_source(draft: State, source: State) -> State:
    """Register independently authorized evidence for manual completion."""
    result = _copy(draft)
    checked = _authorized_source(result, source)
    if checked["id"] in result["sources"]:
        raise ValueError("Source already exists; use update_source for a changed version.")
    result["sources"][checked["id"]] = checked
    return result


def update_source(draft: State, source: State) -> State:
    """Replace source metadata, invalidating only its exact dependent lineage."""
    result = _copy(draft)
    # Revocation must be representable without permitting access to its bytes.
    check = dict(source, authorized=True)
    checked = _authorized_source(result, check, check_routes=False)
    checked["authorized"] = source.get("authorized") is True
    old = result["sources"].get(checked["id"])
    if old is None:
        raise ValueError("Missing source; register authorized evidence before updating it.")
    if old == checked:
        return result
    result["source_history"].append(deepcopy(old))
    result["sources"][checked["id"]] = checked
    roots = set()
    lineage_changed = any(old.get(key) != checked.get(key) for key in (
        "version", "hash", "authorized", "authority", "media_type", "scheme_id", "routes"))
    scope_changed = set(old["field_ids"]) ^ set(checked["field_ids"])
    for key, field in result["fields"].items():
        if not lineage_changed and key not in scope_changed:
            continue
        for candidate in field["candidates"]:
            if candidate["source_id"] == checked["id"]:
                candidate["stale"] = True
                roots.add(key)
        review = next((entry for entry in result["reviews"]
                       if entry["id"] == field["current_review"]), None)
        if review and any(ref["id"] == checked["id"] for ref in review["evidence"]):
            roots.add(key)
    route_changed = checked["id"] == result["funding"]["source_id"] and any(
        old.get(key) != checked.get(key) for key in
        ("version", "hash", "authorized", "authority", "scheme_id", "routes"))
    if route_changed:
        result["funding"]["status"] = "stale"
        roots.update(key for key, definition in result["schema"]["fields"].items()
                     if definition["rule"])
    bound_pack_reviews = {
        review["id"] for review in result["pack_reviews"]
        if any(ref["id"] == checked["id"] for ref in review["evidence"])
        or any(ref["id"] == checked["id"] for ref in review["snapshot"]["sources"])
    }
    _invalidate(result, roots, pack_only=checked["id"] in result["attachments"]
                or route_changed or bool(bound_pack_reviews), pack_review_ids=bound_pack_reviews)
    return result


def _parse_value(raw: str, definition: State, unit: str | None,
                 currency: str | None) -> tuple[JSON, str | None, str | None]:
    text = raw.strip()
    kind = definition["type"]
    if kind in ("money", "number"):
        parts = text.split()
        if len(parts) == 2:
            text, labelled_unit = parts
            unit = unit or labelled_unit
            if kind == "money":
                currency = currency or labelled_unit
        if kind == "money" and _MONEY.fullmatch(text):
            return _amount(Decimal(text)), unit, currency
        if kind == "number" and _NUMBER.fullmatch(text):
            return float(text), unit, currency
    if kind == "bool" and text in ("true", "false"):
        return text == "true", unit, currency
    if kind == "home_ids":
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            value = text
        return value, unit, currency
    return text, unit, currency


def _rows(text: str, media_type: str) -> list[tuple[str, str, str | None, str | None, State]]:
    rows = []
    if media_type == "text/csv":
        reader = csv.DictReader(io.StringIO(text, newline=""), strict=True)
        headers = reader.fieldnames or []
        if len(headers) != len(set(headers)) or not {"field_id", "value"} <= set(headers):
            raise ValueError("CSV requires unique field_id,value headers; use a manual evidence task.")
        for index, row in enumerate(reader, 2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError("CSV row width does not match its headers; correct the source.")
            rows.append((row["field_id"], row["value"], row.get("unit") or None,
                         row.get("currency") or None,
                         {"kind": "csv", "row": index, "line_end": reader.line_num,
                          "column": "value", "case_id": row.get("case_id")}))
    else:
        for number, line in enumerate(text.splitlines(), 1):
            if ":" in line:
                field_id, raw = line.split(":", 1)
                rows.append((field_id.strip(), raw, None, None,
                             {"kind": "text", "line": number,
                              "column": line.index(":") + 2}))
    return rows


def extract_candidates(draft: State, source: State, data: bytes) -> State:
    """Extract only allowlisted labels/CSV cells from authorized raw UTF-8 bytes.

    Unsupported scans and invalid UTF-8 yield no values, only manual tasks.
    Conflicts remain as alternatives; text never controls permissions or actions.
    """
    if not isinstance(data, bytes):
        raise TypeError("Extraction requires the original source bytes.")
    _prepare(draft)
    result = _copy(draft)
    checked = _authorized_source(result, source)
    if hashlib.sha256(data).hexdigest() != checked["hash"]:
        raise ValueError("Source bytes do not match the authorized SHA-256; refresh the evidence.")
    old = result["sources"].get(checked["id"])
    source_invalidation = None
    if old is None:
        result = register_source(result, checked)
    elif old != checked:
        result = update_source(result, checked)
        source_invalidation = deepcopy(result["last_invalidation"])
    manual_reason = None
    if checked["media_type"] not in ("text/plain", "text/csv"):
        manual_reason = "Unsupported or scanned input; provide readable text/CSV or human evidence."
    else:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            manual_reason = "Unreadable UTF-8; provide readable text/CSV or human evidence."
    if manual_reason:
        result["manual_tasks"].append({
            "source_id": checked["id"], "source_version": checked["version"],
            "reason": manual_reason, "owner": "Evidence owner", "state": "manual_required",
        })
        return result
    try:
        rows = _rows(text, checked["media_type"])
    except csv.Error as error:
        raise ValueError("Malformed CSV; correct the source or use manual evidence.") from error
    touched = set()
    for field_id, raw, unit, currency, locator in rows:
        if locator.get("case_id") not in (None, "", result["case_id"]):
            raise PermissionError("Source row is unavailable for this case/form.")
        if field_id == "case_id" and raw.strip() != result["case_id"]:
            raise PermissionError("Source row is unavailable for this case/form.")
        if field_id not in checked["field_ids"]:
            continue
        definition = _definition(result, field_id)
        if definition["protected"] or definition["type"] == "calculated_money":
            continue
        if checked["authority"] not in definition["authority"]:
            continue
        value, unit, currency = _parse_value(raw, definition, unit, currency)
        if field_id == "home_ids" and isinstance(value, list):
            if any(home != result["case_id"] for home in value):
                raise PermissionError("Source row is unavailable for this case/form.")
        payload = {
            "case_id": result["case_id"], "field_id": field_id, "value": value,
            "raw_value": raw, "source_id": checked["id"], "source_version": checked["version"],
            "source_hash": checked["hash"], "locator": locator,
            "parser": PARSER_VERSION, "media_type": checked["media_type"],
            "unit": unit, "currency": currency, "stale": False,
        }
        candidate_id = hashlib.sha256(
            json.dumps(payload, sort_keys=True, allow_nan=False).encode()).hexdigest()
        payload["id"] = candidate_id
        field = result["fields"][field_id]
        if any(candidate["id"] == candidate_id for candidate in field["candidates"]):
            continue
        field["candidates"].append(payload)
        touched.add(field_id)
    if touched:
        _invalidate(result, touched)
        if source_invalidation:
            for key, items in source_invalidation.items():
                result["last_invalidation"][key] = sorted(
                    set(items) | set(result["last_invalidation"][key]))
        for key in touched:
            field = result["fields"][key]
            field["proposal_state"] = _candidate_state(field)
            if field["current_review"] is None:
                field["stale"] = False
                field["state"] = _candidate_state(field)
    return result


def _candidate_state(field: State) -> str:
    candidates = [candidate for candidate in field["candidates"] if not candidate["stale"]]
    values = {json.dumps([entry["value"], entry["unit"], entry["currency"]], sort_keys=True)
              for entry in candidates}
    return "conflict" if len(values) > 1 else "proposed" if values else "unknown"


def select_candidate(draft: State, field_id: str, candidate_id: str | None) -> State:
    """Stage a supplied authorized candidate or explicit no-match, never a value."""
    definition = _definition(draft, field_id)
    _prepare(draft)
    if definition["protected"] or definition["type"] == "calculated_money":
        raise PermissionError("This field requires a separate human action or calculation.")
    result = _copy(draft)
    field = result["fields"][field_id]
    field["proposal_history"].append(
        {"candidate_id": field["proposal"], "state": field["proposal_state"]})
    if candidate_id is not None:
        candidate = _candidate(result, field_id, candidate_id)
        field["proposal"] = candidate["id"]
        field["proposal_state"] = _candidate_state(field)
        field["state"] = field["proposal_state"]
    else:
        field["proposal"] = None
        field["proposal_state"] = "no_match"
        field["state"] = "no_match"
    # Suggestions do not overwrite confirmed values or invalidate human reviews.
    if field["current_review"] is not None:
        field["state"] = "stale" if field["stale"] else "confirmed"
    return result


def _candidate(draft: State, field_id: str, candidate_id: str) -> State:
    candidate = next((entry for entry in draft["fields"][field_id]["candidates"]
                      if entry["id"] == candidate_id), None)
    if candidate is None or candidate["stale"] or candidate["case_id"] != draft["case_id"]:
        raise PermissionError("Candidate is unavailable for this case/field.")
    source = draft["sources"].get(candidate["source_id"])
    if (source is None or source["version"] != candidate["source_version"]
            or source["hash"] != candidate["source_hash"]):
        raise PermissionError("Candidate source has changed; extract and review the current version.")
    _evidence(draft, [source["id"]], field_id=field_id)
    return candidate


def _review(draft: State, field_id: str, action: str, actor: State, *, value: JSON,
            unit: str | None, currency: str | None, evidence: list[str], reason: str,
            unresolved: bool, human_only: bool) -> State:
    definition = _definition(draft, field_id)
    _prepare(draft)
    if definition["type"] == "calculated_money":
        raise PermissionError("Calculated fields cannot be manually overridden.")
    if bool(definition["protected"]) != human_only:
        raise PermissionError("Protected fields require the separate human_field_action.")
    human = _actor(actor, definition["reviewer_roles"])
    _text(reason, "Individual field review reason")
    if action not in ("accept", "correct", "reject") or (human_only and action == "accept"):
        raise ValueError("Use individual accept/correct/reject; protected fields require supplied values.")
    result = _copy(draft)
    field = result["fields"][field_id]
    candidate = None
    if action == "accept":
        if field["proposal"] is None:
            raise ValueError("Select a supplied candidate before accepting this individual field.")
        candidate = _candidate(result, field_id, field["proposal"])
        value, unit, currency = candidate["value"], candidate["unit"], candidate["currency"]
        evidence = list(dict.fromkeys([candidate["source_id"], *evidence]))
    refs = _evidence(result, evidence, field_id=field_id) if evidence else []
    if action != "reject" and not unresolved and not refs:
        raise ValueError("A confirmed field requires authorized source evidence.")
    json.dumps(value, allow_nan=False)
    prior = {key: deepcopy(field[key]) for key in ("value", "unit", "currency", "state", "input_version")}
    review_id = f"field-review-{len(result['reviews']) + 1}"
    result["reviews"].append({
        "id": review_id, "field_id": field_id, "action": action, "actor": human,
        "prior": prior, "value": None if action == "reject" else value,
        "unit": unit, "currency": currency, "evidence": refs, "reason": reason,
        "candidate_id": candidate["id"] if candidate else None,
        "candidate": deepcopy(candidate),
        "input_version": field["input_version"] + 1, "schema_version": result["schema_version"],
        "rule_version": result["rule_version"], "human_only": human_only,
        "unresolved": unresolved,
    })
    field.update(value=None if action == "reject" else value, unit=unit, currency=currency,
                 state="rejected" if action == "reject" else "unknown" if unresolved else "confirmed",
                 stale=False, current_review=review_id)
    field["input_version"] += 1
    _invalidate(result, {field_id}, keep={field_id})
    # The replaced field review is historical, never silently rewritten.
    if prior["state"] == "confirmed":
        old_id = draft["fields"][field_id]["current_review"]
        result["stale_reviews"] = sorted(set(result["stale_reviews"]) | {old_id})
    return result


def review_field(draft: State, field_id: str, action: str, actor: State, *,
                 value: JSON = None, unit: str | None = None, currency: str | None = None,
                 evidence: list[str] | None = None, reason: str,
                 unresolved: bool = False) -> State:
    """Accept/correct/reject one ordinary field without modifying any source."""
    return _review(draft, field_id, action, actor, value=value, unit=unit, currency=currency,
                   evidence=evidence or [], reason=reason, unresolved=unresolved, human_only=False)


def human_field_action(draft: State, field_id: str, actor: State, *, value: JSON,
                       evidence: list[str], reason: str, action: str = "correct") -> State:
    """Record one explicitly supplied human-only statement, not an external approval.

    No prefilled signature, inferred consent or batch acceptance is supported.
    The caller must authorize the actual declaration/decision separately.
    """
    return _review(draft, field_id, action, actor, value=value, unit=None, currency=None,
                   evidence=evidence, reason=reason, unresolved=False, human_only=True)


def _money(value: JSON) -> Decimal | None:
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        return None
    text = str(value)
    if not _MONEY.fullmatch(text):
        return None
    try:
        amount = Decimal(text)
    except InvalidOperation:
        return None
    return amount if amount.is_finite() and amount >= 0 else None


def _valid_type(value: JSON, definition: State, case_id: str) -> bool:
    kind = definition["type"]
    if kind == "text":
        return isinstance(value, str) and bool(value.strip())
    if kind == "bool":
        return type(value) is bool
    if kind == "enum":
        return isinstance(value, str) and value in definition["options"]
    if kind == "money":
        return _money(value) is not None
    if kind == "number":
        return (not isinstance(value, bool) and isinstance(value, (int, float))
                and Decimal(str(value)).is_finite() and value > 0)
    if kind == "home_ids":
        return (isinstance(value, list) and value == [case_id])
    return False


def _issue(issues: list[State], field_id: str, code: str, reason: str) -> None:
    issues.append({"field_id": field_id, "code": code, "reason": reason,
                   "owner": "Finance reviewer" if field_id == "funding_route" else "Field reviewer",
                   "next_action": "Correct evidence/input and explicitly re-review the affected field."})


def validate_draft(draft: State) -> State:
    """Return deterministic errors and calculations from current confirmed inputs."""
    issues: list[State] = []
    calculated: State = {}
    if draft["schema"] != SCHEMAS.get(draft["form_type"]):
        _issue(issues, "schema", "unapproved_schema", "Template content does not match the approved registry.")
    if draft["schema_version"] != SCHEMA_VERSION:
        _issue(issues, "schema", "unapproved_version", "Template version is not approved.")
    if draft["schema"]["rule_version"] and draft["rule_version"] != draft["schema"]["rule_version"]:
        _issue(issues, "rule", "unapproved_version", "Calculation/eligibility rule version is not approved.")
    if draft["schema"]["funding"] and (
            draft["funding"]["status"] != "evidenced" or not _route_ok(draft)):
        _issue(issues, "funding_route", "unknown_route", "An evidenced approved exercise route is required.")
    valid = set()
    for source_id in draft["attachments"]:
        source = draft["sources"].get(source_id)
        if (source is None or source.get("authorized") is not True
                or source["case_id"] != draft["case_id"]):
            _issue(issues, "attachments", "missing_source", "Attachment is missing or unavailable for this case.")
    for key, definition in draft["schema"]["fields"].items():
        field = draft["fields"][key]
        if definition["type"] == "calculated_money":
            continue
        conditional = definition["conditional"]
        required = definition["required"] or bool(
            conditional and draft["fields"][conditional["field"]]["value"] == conditional["equals"])
        if not required and field["value"] is None and field["state"] in ("unknown", "rejected"):
            continue
        if field["stale"]:
            _issue(issues, key, "stale", "The bound evidence/input changed; previous review is stale.")
        if field["state"] != "confirmed":
            _issue(issues, key, field["state"], "Required input is unknown, conflicting or not human reviewed.")
            continue
        if not _valid_type(field["value"], definition, draft["case_id"]):
            _issue(issues, key, "type", "Value does not match the approved type/options or single-home scope.")
            continue
        if field["unit"] != definition["unit"]:
            _issue(issues, key, "unit", "Unit does not match the template.")
            continue
        if field["currency"] != definition["currency"]:
            _issue(issues, key, "currency", "Currency does not match the template.")
            continue
        review = next((entry for entry in draft["reviews"]
                       if entry["id"] == field["current_review"]), None)
        if review is None or not review["evidence"]:
            _issue(issues, key, "missing_source", "A confirmed field requires current authorized evidence.")
            continue
        evidence_current = all(
            (source := draft["sources"].get(ref["id"])) is not None
            and source.get("authorized") is True and source["case_id"] == draft["case_id"]
            and source["version"] == ref["version"] and source["hash"] == ref["hash"]
            and key in source["field_ids"] and source["authority"] in definition["authority"]
            for ref in review["evidence"])
        if not evidence_current:
            _issue(issues, key, "missing_source", "Reviewed evidence is missing, restricted or superseded.")
            continue
        if not field["stale"]:
            valid.add(key)
    value = lambda key: draft["fields"][key]["value"]
    if draft["schema"]["funding"]:
        if "eligibility" in valid and value("eligibility") != "eligible":
            _issue(issues, "eligibility", "eligibility", "Eligibility is unknown or not eligible.")
        if {"eligible_cost", "total_cost"} <= valid and _money(value("eligible_cost")) > _money(value("total_cost")):
            _issue(issues, "eligible_cost", "cost_total", "Eligible cost cannot exceed total cost.")
        if {"eligible_cost", "eligibility"} <= valid and value("eligibility") == "eligible":
            calculated["grant_amount"] = _amount(min(
                Decimal("7500"), _arithmetic(_money(value("eligible_cost")), Decimal("0.5"), multiply=True)))
        if "total_cost" in valid and "grant_amount" in calculated:
            total, grant = _money(value("total_cost")), Decimal(calculated["grant_amount"])
            if total >= grant:
                calculated["provider_cost"] = _amount(_arithmetic(total, grant))
            else:
                _issue(issues, "total_cost", "grant_exceeds_cost", "Grant cannot exceed confirmed total cost.")
        if "co_funding" in valid and "provider_cost" in calculated:
            if _money(value("co_funding")) < Decimal(calculated["provider_cost"]):
                _issue(issues, "co_funding", "match_budget", "Confirmed co-funding does not cover the provider cost.")
        for key in ("match_budget_approved", "declaration"):
            if key in valid and value(key) is not True:
                _issue(issues, key, "human_required", "An explicit evidenced human statement is required.")
        if draft["form_type"] == "claim":
            if "completed" in valid and value("completed") is not True:
                _issue(issues, "completed", "not_completed", "Claim evidence must show completed work.")
            if {"claim_amount", "awarded_amount"} <= valid and "grant_amount" in calculated:
                ceiling = min(_money(value("awarded_amount")), Decimal(calculated["grant_amount"]))
                if _money(value("claim_amount")) > ceiling:
                    _issue(issues, "claim_amount", "award_ceiling", "Claim exceeds the evidenced award/rule ceiling.")
    elif draft["form_type"] == "invoice" and {"quantity", "unit_cost"} <= valid:
        calculated["invoice_total"] = _amount(_arithmetic(
            Decimal(str(value("quantity"))), _money(value("unit_cost")), multiply=True))
    elif draft["form_type"] == "technical":
        if "certification" in valid and value("certification") is not True:
            _issue(issues, "certification", "human_required", "Explicit human certification evidence is required.")
    for key, definition in draft["schema"]["fields"].items():
        if definition["type"] != "calculated_money":
            continue
        if key not in calculated:
            _issue(issues, key, "unknown_calculation", "Calculation needs current confirmed dependent inputs.")
        elif draft["fields"][key]["value"] != calculated[key]:
            _issue(issues, key, "changed_total", "Stored total differs from the deterministic calculation.")
        elif draft["fields"][key]["stale"]:
            _issue(issues, key, "stale", "Calculated input version changed; explicitly recalculate.")
    return {"ready": not issues, "issues": issues, "calculations": calculated,
            "schema_version": draft["schema_version"], "rule_version": draft["rule_version"],
            "input_version": draft["input_version"]}


def _amount(value: Decimal) -> str:
    with localcontext() as context:
        context.prec = max(28, len(value.as_tuple().digits) + abs(value.as_tuple().exponent) + 3)
        return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _arithmetic(left: Decimal, right: Decimal, *, multiply: bool = False) -> Decimal:
    with localcontext() as context:
        context.prec = max(28, sum(len(item.as_tuple().digits) + abs(item.as_tuple().exponent)
                                   for item in (left, right)) + 3)
        return left * right if multiply else left - right


def recalculate(draft: State) -> State:
    """Refresh derived totals only from current human-confirmed typed inputs."""
    _prepare(draft)
    result = _copy(draft)
    calculations = validate_draft(result)["calculations"]
    changed = {key for key, value in calculations.items()
               if result["fields"][key]["value"] != value or result["fields"][key]["stale"]}
    if changed:
        _invalidate(result, changed, keep=set(calculations))
    for key, value in calculations.items():
        field = result["fields"][key]
        if key in changed:
            field["input_version"] += 1
        field.update(value=value, unit="GBP", currency="GBP", state="calculated", stale=False)
    return result


def update_versions(draft: State, *, schema_version: str | None = None,
                    rule_version: str | None = None,
                    input_versions: dict[str, int] | None = None,
                    route: State | None = None) -> State:
    """Invalidate exact dependent version changes; unknown contracts block review.

    A template version binds every field. A funding rule binds only declared
    rule inputs/calculations and their transitive dependents. Supplied input
    versions bind only those fields. No update activates an unapproved rule.
    """
    result = _copy(draft)
    roots = set()
    for key, version in (input_versions or {}).items():
        _definition(result, key)
        if type(version) is not int or version <= result["fields"][key]["input_version"]:
            raise ValueError("Input version must be an increasing positive integer.")
        result["history"].append({"kind": "input_version", "field_id": key,
                                  "prior": result["fields"][key]["input_version"], "new": version})
        result["fields"][key]["input_version"] = version
        roots.add(key)
    for key, version in (("schema_version", schema_version), ("rule_version", rule_version)):
        if version is None or version == result[key]:
            continue
        if key == "rule_version" and result["schema"]["rule_version"] is None:
            raise ValueError("This template has no independently versioned calculation rule.")
        _text(version, key)
        result["history"].append({"kind": key, "prior": result[key], "new": version})
        result[key] = version
        roots.update(
            field_id for field_id, definition in result["schema"]["fields"].items()
            if key == "schema_version" or definition["rule"])
    if route is not None:
        if not result["schema"]["funding"] or route.get("scheme_id") != SCHEME_ID:
            raise ValueError("Route does not match the approved fictional funding scheme.")
        result["history"].append({"kind": "route", "prior": deepcopy(result["funding"])})
        result["funding"].update({key: route.get(key) for key in ("route", "version", "source_id")})
        result["funding"]["status"] = "evidenced" if _route_ok(result) else "unknown"
        roots.update(key for key, definition in result["schema"]["fields"].items() if definition["rule"])
    if roots:
        _invalidate(result, roots)
    return result


def set_attachments(draft: State, source_ids: list[str]) -> State:
    """Bind authorized attachments; changing only links stales pack review only."""
    result = _copy(draft)
    _evidence(result, source_ids)
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("Attachment source IDs must be unique.")
    if result["attachments"] != source_ids:
        result["attachments"] = list(source_ids)
        _invalidate(result, set(), pack_only=True)
    return result


def link_downstream(draft: State, reference_id: str, field_ids: list[str], *,
                    evidence_reference: str) -> State:
    """Link an existing external decision for invalidation, never create approval."""
    _text(reference_id, "Downstream reference ID")
    _text(evidence_reference, "External evidence reference")
    result = _copy(draft)
    if not field_ids:
        raise ValueError("An external reference requires explicit field dependencies.")
    for field_id in field_ids:
        _definition(result, field_id)
    if reference_id in result["downstream"]:
        raise ValueError("External reference already exists; preserve its prior dependency binding.")
    result["downstream"][reference_id] = {
        "depends_on": sorted(set(field_ids)), "evidence_reference": evidence_reference, "stale": False,
    }
    return result


def _pack(draft: State, calculations: State, finance_evidence: list[State]) -> State:
    fields = {
        key: {"value": calculations.get(key, field["value"]),
              "unit": "GBP" if key in calculations else field["unit"],
              "currency": "GBP" if key in calculations else field["currency"],
              "input_version": field["input_version"], "review_id": field["current_review"]}
        for key, field in draft["fields"].items()
    }
    review_ids = {field["current_review"] for field in draft["fields"].values()
                  if field["current_review"] is not None}
    reviews = [deepcopy(entry) for entry in draft["reviews"] if entry["id"] in review_ids]
    source_ids = set(draft["attachments"])
    source_ids.update(ref["id"] for ref in finance_evidence)
    source_ids.update(ref["id"] for review in reviews for ref in review["evidence"])
    if draft["funding"]["source_id"]:
        source_ids.add(draft["funding"]["source_id"])
    for source_id in source_ids:
        source = draft["sources"].get(source_id)
        if source is None:
            raise ValueError("Pack evidence is missing; restore authorized evidence and re-review.")
        _authorized_source(draft, source)
    return {
        "case_id": draft["case_id"], "form_type": draft["form_type"], "fictional": True,
        "schema": deepcopy(draft["schema"]), "schema_version": draft["schema_version"],
        "rule_version": draft["rule_version"], "input_version": draft["input_version"],
        "funding": deepcopy(draft["funding"]), "fields": fields, "field_reviews": reviews,
        "pack_evidence": deepcopy(finance_evidence),
        "sources": [deepcopy(draft["sources"][key]) for key in sorted(source_ids)],
        "attachments": [deepcopy(draft["sources"][key]) for key in draft["attachments"]],
        "event": "reviewed_export_only", "external_submission": False,
    }


def _digest(pack: State) -> str:
    return hashlib.sha256(json.dumps(pack, sort_keys=True, separators=(",", ":"),
                                    allow_nan=False).encode("utf-8")).hexdigest()


def review_pack(draft: State, actor: State, *, evidence: list[str], reason: str) -> State:
    """Snapshot a complete pack with a distinct authorized Finance reviewer."""
    human = _actor(actor, PACK_REVIEW_ROLES)
    _text(reason, "Finance review reason")
    if any(review["actor"]["id"] == human["id"] for review in draft["reviews"]
           if review["id"] in {field["current_review"] for field in draft["fields"].values()}):
        raise PermissionError("Finance pack reviewer must be distinct from every current field reviewer.")
    checked = validate_draft(draft)
    if not checked["ready"]:
        raise ValueError("Pack is not ready; resolve deterministic field/route errors and re-review.")
    result = _copy(draft)
    refs = _evidence(result, evidence)
    pack = _pack(result, checked["calculations"], refs)
    result["pack_reviews"].append({
        "id": f"pack-review-{len(result['pack_reviews']) + 1}", "actor": human,
        "evidence": refs, "reason": reason, "digest": _digest(pack), "snapshot": pack,
    })
    return result


def export_pack(draft: State) -> State:
    """Append an exact reviewed export snapshot; no financial/operational event."""
    checked = validate_draft(draft)
    if not checked["ready"] or not draft["pack_reviews"]:
        raise ValueError("Reviewed export requires a complete current Finance-reviewed pack.")
    result = _copy(draft)
    review = result["pack_reviews"][-1]
    for ref in review["evidence"]:
        source = result["sources"].get(ref["id"])
        if (source is None or source.get("authorized") is not True
                or source["version"] != ref["version"] or source["hash"] != ref["hash"]):
            raise ValueError("Finance review evidence changed; restore evidence and explicitly re-review.")
    pack = _pack(result, checked["calculations"], review["evidence"])
    if review["id"] in result["stale_reviews"] or _digest(pack) != review["digest"]:
        raise ValueError("Pack review is stale; a distinct Finance reviewer must re-review.")
    export = deepcopy(review["snapshot"])
    export["finance_review"] = {key: deepcopy(review[key])
                                for key in ("id", "actor", "evidence", "reason", "digest")}
    export["id"] = f"export-{len(result['exports']) + 1}"
    result["exports"].append(export)
    return result
