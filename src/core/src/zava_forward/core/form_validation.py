"""Deterministic validation, version-linked review pack assembly, and stale propagation.

Nothing here approves a template, source policy, rule set, or reviewer. Rules and
approved sum calculations run only when both the registered schema row and the supplied
rule set carry recorded approval metadata bound to the exact schema digest, rule_refs,
evidenced funding route, and template version; otherwise validation reports Not evaluated.
Only current values confirmed in audit history by a registered human reviewer with intact
source evidence are ever passed to rule checks.
"""

import re
from copy import deepcopy
from decimal import Decimal
from typing import Any

from . import forms
from .doc_controls import DocumentUnavailable
from .form_export import _digest, _issues_by_field
from .form_review import (
    NOTICE,
    Digests,
    _draft,
    _equal,
    _report,
    _reviewer_confirmed,
    _schema,
    _valid,
)

type Record = dict[str, Any]

RULE_KINDS = frozenset({"min", "max", "max_length", "pattern", "equals", "one_of", "sum"})
SET_KEYS = frozenset({"id", "version", "approval", "bound", "rules"})
BOUND_KEYS = frozenset(
    {"schema_id", "schema_version", "schema_digest", "template_id", "template_version"}
)
APPROVAL_KEYS = frozenset({"status", "approver", "evidence_ref"})
RULE_KEYS = frozenset({"rule_id", "field_id", "kind", "param", "message"})
SUM_PARAM_KEYS = frozenset({"calc_id", "calc_version", "addends"})

PACK_BODY_KEYS = (
    "draft_id",
    "case_id",
    "form_type",
    "pack_status",
    "reviewed",
    "submission",
    "eligibility",
    "input_version",
    "template",
    "template_version",
    "schema_id",
    "schema_version",
    "schema_digest",
    "rule_refs",
    "fields",
    "evidence",
    "attachments",
    "history",
    "validation",
    "stale_fields",
)

NOT_EVALUATED = "Not evaluated"
UNAVAILABLE_NOTICE = "Working evidence is unavailable. Ask the document owner to recover it."
PACK_NOTICE = (
    "Review pack for human Finance review only. It records versioned links and deterministic "
    "validation; it is not an approval, submission, eligibility finding, award or payment."
)
_CALC_UNAVAILABLE = "Approved calculation is unavailable."
_DERIVED_REASONS = frozenset(
    {
        "Required confirmed input is missing.",
        "Conditional requirement is unknown.",
        _CALC_UNAVAILABLE,
    }
)


def _nonblank(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _dec(value: int | float) -> Decimal:
    return Decimal(str(value))


def _scalar_matches(left: object, right: object, ftype: str) -> bool:
    if ftype == "number":
        if type(left) not in (int, float) or type(right) not in (int, float):
            return False
        assert isinstance(left, (int, float)) and isinstance(right, (int, float))
        return _dec(left) == _dec(right)
    return _equal(left, right)


def _check_param(
    rule: Record, field: Record, known: dict[str, Record], seen_sums: set[str]
) -> None:
    kind: str = rule["kind"]
    param: Any = rule["param"]
    ftype: str = field["type"]
    fid: str = rule["field_id"]
    if kind in ("min", "max"):
        if ftype not in ("integer", "number") or type(param) not in (int, float):
            raise ValueError(f"Rule {rule['rule_id']} requires a numeric field and bound.")
        if not forms._scalar(param):
            raise ValueError(f"Rule {rule['rule_id']} bound must be finite.")
        return
    if kind == "max_length":
        if ftype != "string" or type(param) is not int or param < 0:
            raise ValueError(
                f"Rule {rule['rule_id']} requires a string field and non-negative int."
            )
        return
    if kind == "pattern":
        if ftype != "string" or not isinstance(param, str):
            raise ValueError(f"Rule {rule['rule_id']} requires a string field and regex pattern.")
        try:
            re.compile(param)
        except re.error as err:
            raise ValueError(f"Rule {rule['rule_id']} has an invalid regular expression.") from err
        return
    if kind == "equals":
        if not _valid(param, field):
            raise ValueError(f"Rule {rule['rule_id']} parameter does not match field {fid} type.")
        return
    if kind == "one_of":
        if not isinstance(param, list) or not param or not all(_valid(x, field) for x in param):
            raise ValueError(f"Rule {rule['rule_id']} requires a non-empty list of valid options.")
        return
    if fid in seen_sums:
        raise ValueError(f"Field {fid} cannot declare multiple sum rules.")
    cref = field.get("calculation_ref")
    if ftype not in ("integer", "number") or not isinstance(cref, dict):
        raise ValueError(f"Sum rule {rule['rule_id']} requires a numeric calculation_ref field.")
    if not isinstance(param, dict) or set(param) != SUM_PARAM_KEYS:
        raise ValueError(f"Sum rule {rule['rule_id']} requires calc_id, calc_version, and addends.")
    if param["calc_id"] != cref["id"] or param["calc_version"] != cref["version"]:
        raise ValueError(
            f"Sum rule {rule['rule_id']} must match field {fid} calculation_ref id and version."
        )
    addends = param["addends"]
    if not isinstance(addends, list) or not addends or len(set(addends)) != len(addends):
        raise ValueError(f"Sum rule {rule['rule_id']} requires unique non-empty addend fields.")
    for addend in addends:
        if (
            not isinstance(addend, str)
            or addend not in known
            or addend == fid
            or known[addend]["category"] in forms.HUMAN_ONLY
            or known[addend]["type"] not in ("integer", "number")
        ):
            raise ValueError(
                f"Sum rule {rule['rule_id']} addend {addend!r} must be another numeric data field."
            )
    seen_sums.add(fid)


def _check_rules(rules: object, schema: Record) -> Record:
    """Validate deterministic rule-set structure before checking approval metadata."""
    if not isinstance(rules, dict) or set(rules) != SET_KEYS:
        raise ValueError("Rule set must be a mapping with id, version, approval, bound, and rules.")
    if not _nonblank(rules["id"]) or not _nonblank(rules["version"]):
        raise ValueError("Rule set id and version must be non-empty strings.")
    approval = rules["approval"]
    if (
        not isinstance(approval, dict)
        or set(approval) != APPROVAL_KEYS
        or approval["status"] not in ("Approved", "Unapproved")
        or (approval["approver"] is not None and not isinstance(approval["approver"], str))
        or (approval["evidence_ref"] is not None and not isinstance(approval["evidence_ref"], str))
    ):
        raise ValueError("Rule set approval metadata is malformed.")
    bound = rules["bound"]
    if (
        not isinstance(bound, dict)
        or set(bound) != BOUND_KEYS
        or not _nonblank(bound["schema_id"])
        or type(bound["schema_version"]) is not int
        or bound["schema_version"] <= 0
        or not _nonblank(bound["schema_digest"])
        or not _nonblank(bound["template_id"])
        or not _nonblank(bound["template_version"])
    ):
        raise ValueError("Rule set schema/template binding metadata is malformed.")
    rule_list = rules["rules"]
    if not isinstance(rule_list, list) or not rule_list:
        raise ValueError("Rule set must declare at least one deterministic rule.")
    known: dict[str, Record] = {f["id"]: f for f in schema["fields"]}
    seen_ids: set[str] = set()
    seen_sums: set[str] = set()
    for rule in rule_list:
        if not isinstance(rule, dict) or set(rule) != RULE_KEYS:
            raise ValueError("Each rule requires rule_id, field_id, kind, param, and message.")
        rid = rule["rule_id"]
        fid = rule["field_id"]
        kind = rule["kind"]
        if not _nonblank(rid) or rid in seen_ids:
            raise ValueError(f"Rule identifier {rid!r} must be unique and non-empty.")
        if not isinstance(fid, str) or fid not in known:
            raise ValueError(f"Rule {rid} references unknown schema field {fid!r}.")
        target = known[fid]
        if target["category"] in forms.HUMAN_ONLY:
            raise ValueError(f"Rule {rid} cannot target human-only field {fid!r}.")
        if kind not in RULE_KINDS:
            raise ValueError(f"Rule {rid} uses unsupported rule kind {kind!r}.")
        if not _nonblank(rule["message"]):
            raise ValueError(f"Rule {rid} requires a non-empty diagnostic message.")
        _check_param(rule, target, known, seen_sums)
        seen_ids.add(rid)
    return rules


def _approval_gaps(row: Record, rules: Record, draft: Record) -> list[str]:
    """Return all missing authority or binding conditions; empty only when fully approved."""
    gaps: list[str] = []
    if row["approval"] != "Approved" or not _nonblank(row.get("approval_evidence")):
        gaps.append("The registered template schema has no recorded approval.")
    if row.get("source_policy_status") != "Approved":
        gaps.append("The source policy has no recorded approval.")
    schema = draft["schema"]
    if schema["form_type"] == "funding" and schema["funding"]["status"] != "Evidenced":
        gaps.append("The funding route is not evidenced for this funding form.")
    if row["digest"] != draft["schema_digest"]:
        gaps.append("The registered schema digest does not match the working review schema.")
    declared_refs = {(ref["id"], ref["version"]) for ref in schema["rule_refs"]}
    if (rules["id"], rules["version"]) not in declared_refs:
        gaps.append("The rule set id and version are not declared in the schema rule_refs.")
    approval = rules["approval"]
    if (
        approval["status"] != "Approved"
        or not _nonblank(approval["approver"])
        or not _nonblank(approval["evidence_ref"])
    ):
        gaps.append("The rule set has no recorded approval.")
    expected_bound = dict(
        schema_id=schema["id"],
        schema_version=schema["version"],
        schema_digest=draft["schema_digest"],
        template_id=schema["template"]["id"],
        template_version=schema["template"]["version"],
    )
    if rules["bound"] != expected_bound:
        gaps.append("The rule set is not bound to this schema digest and template version.")
    return gaps


def _provenance_confirmed(store: Any, draft: Record, fid: str, row: Record) -> bool:
    """Verify audit-history confirmation by a registered human reviewer with intact evidence."""
    if not _reviewer_confirmed(draft, fid, row):
        return False
    events = [e for e in draft["history"] if e["field_id"] == fid]
    if not events:
        return False
    last = events[-1]
    expected_decision = "accept" if row["state"] == "Accepted" else "correct"
    reviewer = last.get("reviewer")
    if (
        last.get("decision") != expected_decision
        or not _nonblank(reviewer)
        or forms._registered(store, str(reviewer)) is None
    ):
        return False
    evidence = row.get("evidence")
    recorded = last["new"].get("evidence")
    return (
        isinstance(evidence, dict)
        and evidence.get("source") is not None
        and evidence.get("locator") is not None
        and evidence == recorded
    )


def _confirmed_and_issues(
    store: Any,
    report: Record,
    draft: Record,
    approved_calcs: set[tuple[str, str, str]],
) -> tuple[dict[str, Any], list[Record]]:
    """Extract strictly reviewer-confirmed inputs and reconcile open validation issues."""
    schema = draft["schema"]
    confirmed: dict[str, Any] = {}
    base_issues: list[Record] = [
        deepcopy(issue) for issue in report["issues"] if issue.get("reason") not in _DERIVED_REASONS
    ]
    for field in schema["fields"]:
        fid: str = field["id"]
        row: Record = report["fields"][fid]
        if row["effective_state"] in ("Accepted", "Corrected"):
            if not _provenance_confirmed(store, draft, fid, row):
                unconfirmed_issue = dict(
                    field_id=fid, status="Fail", reason="Value lacks reviewer confirmation."
                )
                if unconfirmed_issue not in base_issues:
                    base_issues.append(unconfirmed_issue)
            elif _valid(row["value"], field):
                if not isinstance(row["value"], str) or bool(row["value"].strip()):
                    confirmed[fid] = row["value"]

    for field in schema["fields"]:
        fid = field["id"]
        conditions: list[Record] = field["required_when"]
        required = bool(field["required"]) or any(
            c["field_id"] in confirmed and _equal(confirmed[c["field_id"]], c["equals"])
            for c in conditions
        )
        if required and fid not in confirmed:
            base_issues.append(
                dict(field_id=fid, status="Unknown", reason="Required confirmed input is missing.")
            )
        elif not required and any(c["field_id"] not in confirmed for c in conditions):
            base_issues.append(
                dict(field_id=fid, status="Unknown", reason="Conditional requirement is unknown.")
            )
        cref = field["calculation_ref"]
        if cref is not None and (fid, cref["id"], cref["version"]) not in approved_calcs:
            base_issues.append(dict(field_id=fid, status="Unknown", reason=_CALC_UNAVAILABLE))
    return confirmed, base_issues


def _eval_scalar(rule: Record, value: Any, ftype: str) -> bool:
    kind: str = rule["kind"]
    param: Any = rule["param"]
    if kind == "min":
        assert isinstance(value, (int, float)) and isinstance(param, (int, float))
        return bool(_dec(value) >= _dec(param))
    if kind == "max":
        assert isinstance(value, (int, float)) and isinstance(param, (int, float))
        return bool(_dec(value) <= _dec(param))
    if kind == "max_length":
        assert isinstance(value, str) and isinstance(param, int)
        return len(value) <= param
    if kind == "pattern":
        assert isinstance(value, str) and isinstance(param, str)
        return re.fullmatch(param, value) is not None
    if kind == "equals":
        return _scalar_matches(value, param, ftype)
    assert isinstance(param, list)
    return any(_scalar_matches(value, option, ftype) for option in param)


def _overall_status(results: list[Record], open_issues: list[Record]) -> str:
    statuses = {r["status"] for r in results} | {i["status"] for i in open_issues}
    if "Fail" in statuses:
        return "Fail"
    if "Conflict" in statuses:
        return "Conflict"
    if "Unknown" in statuses:
        return "Unknown"
    return "Pass"


def _validate_from_report(store: Any, draft: Record, report: Record, rules: Record) -> Record:
    row = _schema(store, draft["schema"]["id"], draft["schema"]["version"])
    gaps = _approval_gaps(row, rules, draft)
    base = dict(draft_id=draft["id"], input_version=draft["version"], reviewed=False)
    if gaps:
        _confirmed_map, open_issues = _confirmed_and_issues(store, report, draft, set())
        return dict(
            base,
            status=NOT_EVALUATED,
            reasons=gaps,
            results=[],
            confirmed_fields=sorted(_confirmed_map),
            open_issues=open_issues,
            rule_set=None,
        )

    known: dict[str, Record] = {f["id"]: f for f in draft["schema"]["fields"]}
    approved_calcs = {
        (
            r["field_id"],
            r["param"]["calc_id"],
            r["param"]["calc_version"],
        )
        for r in rules["rules"]
        if r["kind"] == "sum"
    }
    confirmed, open_issues = _confirmed_and_issues(store, report, draft, approved_calcs)
    results: list[Record] = []
    for rule in rules["rules"]:
        fid: str = rule["field_id"]
        kind: str = rule["kind"]
        if kind == "sum":
            addends: list[str] = rule["param"]["addends"]
            missing = [f for f in (fid, *addends) if f not in confirmed]
            if missing:
                status = "Unknown"
                reason: str | None = (
                    f"Field or addend lacks reviewer-confirmed input: {', '.join(missing)}."
                )
            else:
                expected = sum((_dec(confirmed[a]) for a in addends), Decimal(0))
                if _dec(confirmed[fid]) == expected:
                    status, reason = "Pass", None
                else:
                    status, reason = "Fail", str(rule["message"])
        elif fid not in confirmed:
            status, reason = "Unknown", "Field lacks a current reviewer-confirmed value."
        elif _eval_scalar(rule, confirmed[fid], known[fid]["type"]):
            status, reason = "Pass", None
        else:
            status, reason = "Fail", str(rule["message"])
        results.append(
            dict(
                rule_id=rule["rule_id"],
                field_id=fid,
                kind=kind,
                param=deepcopy(rule["param"]),
                message=rule["message"],
                status=status,
                reason=reason,
            )
        )

    overall = _overall_status(results, open_issues)
    return dict(
        base,
        status=overall,
        reasons=[],
        results=results,
        confirmed_fields=sorted(confirmed),
        open_issues=open_issues,
        rule_set=dict(
            id=rules["id"],
            version=rules["version"],
            approval=deepcopy(rules["approval"]),
        ),
    )


def validate(store: Any, user: Record, case_id: str, draft_id: str, rules: object) -> Record:
    """Read-only deterministic validation on approved rules and reviewer-confirmed inputs."""
    with store.lock:
        forms._actor(store, user)
        case = store._case(case_id)
        draft = _draft(case, draft_id)
        try:
            digests: Digests = {}
            report = _report(store, case, draft, digests)
        except DocumentUnavailable:
            return dict(
                draft_id=draft["id"],
                input_version=draft["version"],
                status="Unavailable",
                reviewed=False,
                reasons=[UNAVAILABLE_NOTICE],
                results=[],
                confirmed_fields=[],
                open_issues=[],
                rule_set=None,
                notice=UNAVAILABLE_NOTICE,
            )
        checked = _check_rules(rules, draft["schema"])
        return _validate_from_report(store, draft, report, checked)


def review_pack(store: Any, user: Record, case_id: str, draft_id: str, rules: object) -> Record:
    """Assemble a version-linked Finance review pack from a single working-review report.

    Every field, deduplicated evidence link, and attachment carries the template
    version and the input version it was reviewed on. Source bytes are hashed at
    most once per distinct document. The pack is never itself approved or submitted.
    """
    with store.lock:
        forms._actor(store, user)
        case = store._case(case_id)
        draft = _draft(case, draft_id)
        try:
            digests: Digests = {}
            report = _report(store, case, draft, digests)
        except DocumentUnavailable:
            return dict(
                draft_id=draft["id"],
                case_id=case["id"],
                status="Unavailable",
                pack_status="Held",
                pack_ready_for_review=False,
                reviewed=False,
                submission="Not submitted",
                eligibility="Not assessed",
                notice=UNAVAILABLE_NOTICE,
            )
        checked = _check_rules(rules, draft["schema"])
        validation = _validate_from_report(store, draft, report, checked)
        template_version: str = report["template"]["version"]

        attachments: list[Record] = []
        att_by_source: dict[tuple[str, int], str] = {}
        for raw_att in report["attachments"]:
            att_id = f"{raw_att['id']}:v{raw_att['version']}"
            att_by_source[(raw_att["id"], raw_att["version"])] = att_id
            attachments.append(dict(deepcopy(raw_att), attachment_id=att_id))

        fields: list[Record] = []
        evidence_map: dict[tuple[str, int], Record] = {}
        for field_def in draft["schema"]["fields"]:
            fid: str = field_def["id"]
            row: Record = report["fields"][fid]
            ev: Record | None = row["evidence"]
            field_input_version = max(
                (e["input_version"] for e in report["history"] if e["field_id"] == fid),
                default=0,
            )
            source_id = None if ev is None else ev["source"]["id"]
            source_version = None if ev is None else ev["source"]["version"]
            doc_hash = None if ev is None else ev["source"]["content_sha256"]
            locator = None if ev is None else deepcopy(ev["locator"])
            fields.append(
                dict(
                    field_id=fid,
                    value=deepcopy(row["value"]),
                    state=row["effective_state"],
                    source_id=source_id,
                    source_version=source_version,
                    document_hash=doc_hash,
                    locator=locator,
                    template_version=template_version,
                    input_version=field_input_version,
                )
            )
            if source_id is not None and source_version is not None:
                key = (source_id, source_version)
                entry = evidence_map.get(key)
                if entry is None:
                    entry = dict(
                        source_id=source_id,
                        source_version=source_version,
                        document_hash=doc_hash,
                        attachment_id=att_by_source.get(key),
                        template_version=template_version,
                        input_version=field_input_version,
                        field_ids=[],
                        locators=[],
                    )
                    evidence_map[key] = entry
                else:
                    entry["input_version"] = max(entry["input_version"], field_input_version)
                entry["field_ids"].append(fid)
                entry["locators"].append(dict(field_id=fid, locator=deepcopy(locator)))

        ready = validation["status"] == "Pass" and not report["stale_fields"]
        pack_status = "Ready for Finance review" if ready else "Held"
        body: Record = dict(
            draft_id=report["draft_id"],
            case_id=case["id"],
            form_type=draft["schema"]["form_type"],
            pack_status=pack_status,
            reviewed=False,
            submission="Not submitted",
            eligibility="Not assessed",
            input_version=report["input_version"],
            template=deepcopy(report["template"]),
            template_version=template_version,
            schema_id=report["schema_id"],
            schema_version=report["schema_version"],
            schema_digest=report["schema_digest"],
            rule_refs=deepcopy(report["rule_refs"]),
            fields=fields,
            evidence=list(evidence_map.values()),
            attachments=attachments,
            history=deepcopy(report["history"]),
            validation=validation,
            stale_fields=list(report["stale_fields"]),
        )
        return dict(
            body,
            content_sha256=_digest(body),
            status=pack_status,
            pack_ready_for_review=ready,
            schema_impact=deepcopy(report["dependency_impact"]["schema"]),
            notice=PACK_NOTICE,
            working_notice=NOTICE,
        )


def _rule_map(validation: Record) -> dict[str, Record]:
    raw = validation.get("results")
    if not isinstance(raw, list):
        raise ValueError("Pack validation results must be a list.")
    mapped: dict[str, Record] = {}
    for item in raw:
        if (
            not isinstance(item, dict)
            or not _nonblank(item.get("rule_id"))
            or not isinstance(item.get("field_id"), str)
            or item.get("kind") not in RULE_KINDS
            or "param" not in item
            or not _nonblank(item.get("message"))
            or not isinstance(item.get("status"), str)
        ):
            raise ValueError("Pack validation rule result is malformed.")
        rid = str(item["rule_id"])
        if rid in mapped:
            raise ValueError("Duplicate rule_id in saved pack validation results.")
        mapped[rid] = item
    return mapped


def _rule_sig(item: Record) -> tuple[Any, ...]:
    return (
        item["field_id"],
        item["kind"],
        item["param"],
        item["message"],
        item["status"],
        item.get("reason"),
    )


def _sum_edges(results: dict[str, Record]) -> list[tuple[list[str], str]]:
    edges: list[tuple[list[str], str]] = []
    for item in results.values():
        if item["kind"] == "sum" and isinstance(item["param"], dict):
            addends = item["param"].get("addends")
            if isinstance(addends, list) and all(isinstance(a, str) for a in addends):
                edges.append(([str(a) for a in addends], str(item["field_id"])))
    return edges


def pack_freshness(store: Any, user: Record, case_id: str, saved: object, rules: object) -> Record:
    """Verify pack digest integrity and compute exact dependent-only field staleness."""
    with store.lock:
        forms._actor(store, user)
        intact = False
        saved_digest = ""
        saved_rows: dict[str, Record] = {}
        saved_issues: dict[str, list[Record]] = {}
        saved_results: dict[str, Record] = {}
        body: Record = {}
        if isinstance(saved, dict):
            try:
                body = {key: saved[key] for key in PACK_BODY_KEYS}
                digest_ok = isinstance(saved.get("content_sha256"), str) and saved[
                    "content_sha256"
                ] == _digest(body)
                case_ok = body["case_id"] == case_id and _nonblank(body["draft_id"])
                lists_ok = (
                    isinstance(body["fields"], list)
                    and isinstance(body["evidence"], list)
                    and isinstance(body["attachments"], list)
                    and isinstance(body["stale_fields"], list)
                    and isinstance(body["validation"], dict)
                    and isinstance(body["validation"].get("status"), str)
                )
                if digest_ok and case_ok and lists_ok:
                    saved_digest = str(saved["content_sha256"])
                    for f_row in body["fields"]:
                        if not isinstance(f_row, dict) or not _nonblank(f_row.get("field_id")):
                            raise ValueError("Saved field row is malformed.")
                        saved_rows[str(f_row["field_id"])] = f_row
                    saved_issues = _issues_by_field(body["validation"].get("open_issues", []))
                    saved_results = _rule_map(body["validation"])
                    intact = True
            except (KeyError, TypeError, ValueError):
                intact = False

        if not intact:
            return dict(
                status="Invalid",
                stale_fields=[],
                unaffected_fields=[],
                reasons=[
                    "The saved review pack is incomplete, belongs to another case, "
                    "or was edited after assembly."
                ],
                action="Assemble a new review pack from the working review.",
                reviewed=False,
            )

        try:
            case = store._case(case_id)
            draft = _draft(case, str(body["draft_id"]))
        except KeyError:
            return dict(
                status="Unavailable",
                stale_fields=[],
                unaffected_fields=[],
                reasons=["The working review for this pack is missing or belongs to another case."],
                action="Ask the document owner to recover the working review.",
                reviewed=False,
            )

        current = review_pack(store, user, case_id, str(body["draft_id"]), rules)
        if current["status"] == "Unavailable":
            return dict(
                status="Unavailable",
                stale_fields=[],
                unaffected_fields=[],
                reasons=[str(current["notice"])],
                action="Ask the document owner to recover the evidence.",
                reviewed=False,
            )

        active_fields = [str(r["field_id"]) for r in current["fields"]]
        active_set = set(active_fields)
        current_rows = {str(r["field_id"]): r for r in current["fields"]}
        stale_set: set[str] = set(current["stale_fields"]) & active_set
        reasons: list[str] = []

        if (
            body["schema_digest"] != current["schema_digest"]
            or body["template_version"] != current["template_version"]
        ):
            reasons.append("The bound form schema or template version changed.")
        elif current["schema_impact"]["status"] == "Unknown":
            reasons.append("Schema lineage is missing or malformed.")
        elif current["schema_impact"]["affects_draft"]:
            reasons.append("A newer registered schema version affects this review pack.")

        field_diffs = {
            fid
            for fid in (set(saved_rows) | active_set)
            if saved_rows.get(fid) != current_rows.get(fid)
        }
        stale_set.update(field_diffs & active_set)
        if body["input_version"] != current["input_version"] or field_diffs:
            reasons.append("Working field inputs or bound source evidence changed.")

        now_issues = _issues_by_field(current["validation"]["open_issues"])
        issue_diffs = {fid for fid in active_set if saved_issues.get(fid) != now_issues.get(fid)}
        stale_set.update(issue_diffs)
        if issue_diffs:
            reasons.append("Open field validation issues changed.")

        saved_val: Record = body["validation"]
        now_val: Record = current["validation"]
        now_results = _rule_map(now_val)
        was_unevaluated = saved_val["status"] == NOT_EVALUATED
        is_unevaluated = now_val["status"] == NOT_EVALUATED

        if was_unevaluated != is_unevaluated:
            if is_unevaluated:
                stale_set.update(active_set)
                reasons.append("Approved-rule authority or binding is no longer satisfied.")
            else:
                newly_evaluated = {
                    str(r["field_id"]) for r in now_results.values() if r["field_id"] in active_set
                }
                for f_def in draft["schema"]["fields"]:
                    if f_def["calculation_ref"] is not None and f_def["id"] in active_set:
                        newly_evaluated.add(str(f_def["id"]))
                stale_set.update(newly_evaluated)
                reasons.append("Approved rules became active after pack assembly.")
        else:
            rule_affected: set[str] = set()
            for rid in set(saved_results) | set(now_results):
                sr = saved_results.get(rid)
                nr = now_results.get(rid)
                if sr is None or nr is None or _rule_sig(sr) != _rule_sig(nr):
                    if sr is not None and sr["field_id"] in active_set:
                        rule_affected.add(str(sr["field_id"]))
                    if nr is not None and nr["field_id"] in active_set:
                        rule_affected.add(str(nr["field_id"]))
            if rule_affected:
                stale_set.update(rule_affected)
                reasons.append("Approved validation rules or rule outcomes changed.")
            elif saved_val.get("rule_set") != now_val.get("rule_set") or saved_val.get(
                "reasons"
            ) != now_val.get("reasons"):
                reasons.append("Rule-set approval metadata or evaluation reasons changed.")

        edges = [*_sum_edges(saved_results), *_sum_edges(now_results)]
        schema_fields: list[Record] = draft["schema"]["fields"]
        grew = True
        while grew:
            grew = False
            for f_def in schema_fields:
                fid = str(f_def["id"])
                if fid in stale_set or fid not in active_set:
                    continue
                if any(c["field_id"] in stale_set for c in f_def["required_when"]):
                    stale_set.add(fid)
                    grew = True
            for addends, target_fid in edges:
                if target_fid not in stale_set and target_fid in active_set:
                    if any(a in stale_set for a in addends):
                        stale_set.add(target_fid)
                        grew = True

        stale_list = sorted(stale_set & active_set)
        unaffected_list = sorted(active_set - stale_set)
        digest_changed = current["content_sha256"] != saved_digest
        if stale_list and not reasons:
            reasons.append("One or more dependent fields became stale.")
        if digest_changed and not reasons:
            reasons.append("Pack metadata or review history changed after assembly.")
        is_stale = bool(stale_list or reasons or digest_changed)
        return dict(
            status="Stale" if is_stale else "Current",
            stale_fields=stale_list,
            unaffected_fields=unaffected_list,
            reasons=reasons,
            action=(
                "Re-review the stale fields and assemble a new Finance review pack."
                if is_stale
                else None
            ),
            reviewed=False,
        )
