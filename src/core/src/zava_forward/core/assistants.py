"""Five proposal-only assistants. SQL owns claims, liability and review, not inference.

Exercise rules deliberately describe gaps, not company approvals. All captured
fields are safe for every reader of a capability. No domain write is available
to the provider or this service.
"""

import hashlib
import json
import logging
import math
import os
import threading
import time
import uuid
from collections.abc import Mapping
from copy import deepcopy
import contextvars
from datetime import date, datetime, timezone
from contextlib import contextmanager
from typing import Any

from . import assistant_release as rel
from . import recovery
from .forecast_reads import ForecastReads, ForecastTimeout
from .ai import may_carry_captured_readings
from .doc_controls import is_available_case_document
from .mssqlstore import driver_sqlstate, is_write_lock_busy
from . import (
    ai_consumption,
    challenges,
    continuity,
    controls,
    identity,
    monitoring_coverage,
    projection,
    rai_metrics,
    quality,
    ranking,
    rai_release,
    sensor_map,
    sensor_view,
    task_contracts,
    telemetry,
)
from zava_forward.core.ai import FORBIDDEN, Ai
from zava_forward.core.regulatory_output_guard import (
    GuardDecision,
    GuardTelemetry,
    ViolationCategory,
    inspect_regulatory_output,
)
from .store import ConflictError
from .synthetic.sensor_identity import demo_homes

LOG = logging.getLogger(__name__)


class ReleaseDenied(PermissionError):
    """Release admission denial; the transaction commits so a recorded invalidation persists."""


PM = "Retrofit Programme Manager"
RC = "Retrofit Coordinator"
VERSION = "1.0.0"
SCHEMA_VERSION = "evidence-proposal-v1"
RULE_VERSION = "synthetic-gaps-2026-10-13-v1"
PURPOSE = "service:retrofit-evidence-proposals"
REGISTRY = {
    "stock-prioritisation": dict(
        roles=(RC, PM),
        categories=("home", "survey", "ranking"),
        purpose="Explain stock facts and prepare a data-owner query",
    ),
    "assessment-preparation": dict(
        roles=(RC, PM),
        categories=("home", "survey", "measures", "technical", "documents"),
        purpose="Prepare a survey/design evidence checklist",
    ),
    "funding-evidence": dict(
        roles=("Grants and Evidence Officer", PM),
        categories=("home", "measures", "funding", "finance", "grants", "documents"),
        purpose="Prepare application/claim evidence gaps",
    ),
    "works-resident-coordination": dict(
        roles=(RC, "Resident Liaison Officer", PM),
        categories=(
            "home",
            "measures",
            "preferences",
            "appointments",
            "handoff",
            "capacity",
            "requests",
        ),
        purpose="Draft an update or committed-capacity option",
    ),
    "quality-evidence": dict(
        roles=("Quality Inspector", PM),
        categories=("home", "measures", "quality", "checklists", "documents", "sensor"),
        purpose="Assemble per-measure quality evidence discrepancies and review-flag retained indoor readings",
    ),
}
RULES = {
    "stock-prioritisation": "Missing/unknown home.epc, home.type or home.built; supplied survey.epc/type/built conflicts with home.",
    "assessment-preparation": "Missing Survey/Design metadata/content hash or technical.design_version; relevant permitted source signature changes.",
    "funding-evidence": "Missing measures, funding.route/reference, grants or budget amount; incomplete supplied invoice ref/lines/milestone inputs; claim-phase grant lacks sourced history or hashed Funding evidence metadata; relevant permitted terms/evidence signature changes.",
    "works-resident-coordination": "handoff.state=Offered/Received/Escalated; past appointment.date with missing/Booked/Planned/No access/Missed outcome; past open service_request.next_update.",
    "quality-evidence": "Missing/unknown measures; not exactly one active (non-Superseded) quality record per measure; current work not Accepted/Handed over; missing/conflicting checklist item evidence or checklist version mismatch; current evidence version or relevant permitted signature changes; retained consented synthetic readings captured for a case with a quality record, one proposal per six-hour bucket of the latest reading (a review flag only, not a threshold, defect or acceptance).",
}
# One provider call per attempt, one agent, no tools or sub-agents (#107, #432). Attempts per request
# are the configured ZF_ASSIST_ATTEMPTS, never above ATTEMPT_CEILING.
MODEL_CALLS_PER_ATTEMPT = 1
AGENT_DEPTH = 1
ATTEMPT_CEILING = 3
PERMIT_LEASE_MARGIN = 38.0  # seconds of lease a permit needs: 2 permit + 8 dispatch + 15 provider + 10 post, plus margin
PERMIT_WINDOW = 2.0  # price and authority must stay valid this long after the permit
PERMIT_REQUEST = (
    "body_sha256",
    "model",
    "deployment",
    "temperature",
    "configuration",
    "max_tokens",
    "input_bound",
)
OUTPUT_SCHEMA = dict(
    required=("summary", "findings", "unknowns"),
    summary_chars=1200,
    findings_count=12,
    finding_chars=800,
    citations_per_finding=8,
    unknowns_count=80,
    unknown_chars=240,
    absolute_output_chars=16000,
    citations="captured source IDs only; non-empty on every finding",
)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


WITHHELD_OUTPUT = dict(
    summary="Withheld: this output was built with retained readings and monitoring consent is not granted now.",
    findings=[],
    unknowns=[],
)
WITHHELD_NOTE = (
    "Withheld: this note may refer to retained readings and monitoring consent is not granted now."
)
ROLE_WITHHELD_OUTPUT = dict(summary=projection.NOTE_HELD, findings=[], unknowns=[])
ASSISTANT_CHALLENGE_ACTIONS = ("open", "update", "reopen", "escalate", "resolve")
ASSISTANT_CHALLENGE_CHANNELS = (
    "Digital", "Phone", "Letter", "In person", "Assisted visit", "Trusted intermediary"
)
ASSISTANT_CHALLENGE_SUBMITTERS = ("The resident", "Their representative", "Nominee")
ASSISTANT_CHALLENGE_TARGETS = ("proposal", "source", "policy")
ASSISTANT_CHALLENGE_RESOLUTIONS = ("Explanation recorded", "Correction recorded")
TRANSIENT_VIEW_KEYS = (
    "history_next_offset",
    "history_count",
    "display_state",
    "stale",
    "actionable",
    "suspension",
    "release_denial",
    "epoch_current",
    "relied_on",
    "review_flag",
    "sensor_withheld",
    "role_withheld",
    "non_retaliation_assurance",
    "hazard_clock_preserved",
)


def _output_violates_visibility(
    output: Any,
    withheld: Any,
    *,
    guard_telemetry: GuardTelemetry | None = None,
) -> bool:
    if not isinstance(output, Mapping):
        return False
    texts = [output.get("summary")]
    for f in output.get("findings") or ():
        if isinstance(f, Mapping):
            texts.append(f.get("text"))
            texts.extend(f.get("citations") or ())
    texts.extend(output.get("unknowns") or ())
    for t in texts:
        if not isinstance(t, str):
            continue
        if FORBIDDEN.search(t) or projection.contains_withheld_value(t, withheld):
            return True
        dec = inspect_regulatory_output(t, on_violation="reject")
        if not dec.passed:
            if guard_telemetry is not None:
                guard_telemetry.record_decision(dec)
            return True
    return False


def signature(snapshot):
    """Identity and staleness digest of the exact capture, retained readings, context and citations included."""
    return digest(snapshot)


def scheduling_signature(snapshot):
    """Rate-limit key for proactive scans only. It never decides identity or staleness: sensor evidence
    enters as a coarse six-hour value so one five-minute reading does not start new model work."""
    sensors = snapshot["sources"].get("sensors")
    if sensors is None:
        return digest(snapshot)
    coarse = dict(
        snapshot,
        sources=dict(snapshot["sources"], sensors=sensor_view.signature(sensors)),
        citations={
            k: v
            for k, v in snapshot["citations"].items()
            if not k.startswith("sensor:") and k != "source:sensors"
        },
    )
    return digest(coarse)


def _sensor_bucket_key(snapshot):
    """Six-hour sensor bucket ignoring provenance-class additions so same-bucket conflicts stay visible."""
    if not isinstance(snapshot, Mapping):
        return None
    sources = snapshot.get("sources") or {}
    sensors = sources.get("sensors")
    if not isinstance(sensors, Mapping):
        return None
    sig = sensor_view.signature(sensors)
    if not isinstance(sig, dict):
        return None
    coarse_sig = dict(sig, classes=[])
    citations = snapshot.get("citations") or {}
    coarse = dict(
        snapshot,
        sources=dict(sources, sensors=coarse_sig),
        citations={
            k: v
            for k, v in citations.items()
            if not k.startswith("sensor:") and k != "source:sensors"
        },
    )
    return digest(coarse)


def proposal_identity(capability):
    return dict(capability=capability, purpose=REGISTRY[capability]["purpose"])


def pick(value, keys):
    value = value if isinstance(value, dict) else {}
    result = {}
    for key in keys:
        item = value.get(key)
        result[key] = (
            item
            if (
                item is None
                or type(item) in (str, int, bool)
                or (type(item) is float and math.isfinite(item))
            )
            else None
        )
    return result


def measures(c):
    value = c.get("measures")
    values = (
        value if isinstance(value, list) else value.split(",") if isinstance(value, str) else []
    )
    return [m.strip() for m in values if isinstance(m, str) and m.strip()]


def capture(capability, c, procurement=None, sensors=None):
    """Closed field allowlists, never whole records, notes, vulnerability or AI summaries."""
    source = {
        "home": pick(
            c.get("home"), ("address", "town", "postcode", "type", "built", "epc", "tenure")
        )
    }
    # Role-independent so the source signature is stable: outcomes only when every role of the assistant has a recorded need.
    need_ok = all(projection.can_see_reason(dict(role=r)) for r in REGISTRY[capability]["roles"])
    if "measures" in REGISTRY[capability]["categories"]:
        source["measures"] = measures(c)
    if capability in ("stock-prioritisation", "assessment-preparation"):
        source["survey"] = pick(
            c.get("survey"), ("epc", "type", "built", "version", "status", "evidence_hash")
        )
    if capability == "stock-prioritisation":
        # Only the public portion of the deterministic reasons crosses this audience.
        policy = ranking.describe(ranking.CURRENT)
        policy.pop("versions", None)
        public = pick(
            dict(stage=c.get("stage"), waiting_days=c.get("days_in_stage")),
            ("stage", "waiting_days"),
        )
        reasons = []
        if type(public["waiting_days"]) in (int, float):
            reasons.append(
                dict(
                    code="waiting_days", text=f"Waiting {public['waiting_days']} days in this stage"
                )
            )
        if public["stage"]:
            reasons.append(dict(code="stage_order", text=f"At '{public['stage']}'"))
        source["ranking"] = dict(
            policy=policy,
            **public,
            reasons=reasons,
            disclosure="Resident support and safety ranking inputs are not disclosed to this audience.",
        )
    if capability == "assessment-preparation":
        source["technical"] = pick(c.get("technical"), ("design_version",))
    if capability in ("assessment-preparation", "funding-evidence", "quality-evidence"):
        kinds = {
            "assessment-preparation": ("EPC", "Survey", "Design"),
            "funding-evidence": ("EPC", "Survey", "Design", "Funding evidence"),
            "quality-evidence": ("Photo", "Design", "Other"),
        }[capability]
        source["documents"] = sorted(
            [
                pick(d, ("id", "kind", "version", "content_sha256", "at"))
                for d in c.get("documents", [])
                if d.get("kind") in kinds and is_available_case_document(d)
            ],
            key=lambda d: str(d.get("id")),
        )
    if capability == "funding-evidence":
        source["funding"] = pick(
            c.get("funding"), ("route", "status", "reference", "terms_version", "terms_hash")
        )
        fx = c.get("finance") or {}
        source["finance"] = {
            "budget": pick(fx.get("budget"), ("amount", "status")),
            "commitments": [
                pick(
                    x,
                    (
                        "id",
                        "supplier",
                        "contract",
                        "work_order",
                        "measure",
                        "amount",
                        "quantity",
                        "status",
                    ),
                )
                for x in fx.get("commitments", [])
            ],
            "invoices": [
                dict(
                    pick(
                        x,
                        (
                            "id",
                            "kind",
                            "supplier",
                            "work_order",
                            "ref",
                            "status",
                            "version",
                            "evidence_hash",
                        ),
                    ),
                    lines=[
                        pick(line, ("measure", "quantity", "amount", "milestone_ref"))
                        for line in x.get("lines", [])
                    ],
                )
                for x in fx.get("invoices", [])
            ],
        }
        source["grants"] = [
            dict(
                pick(g, ("id", "scheme", "state")),
                evidence=[
                    pick(x, ("state", "source", "amount", "at")) for x in g.get("history", [])
                ],
            )
            for g in c.get("grants", [])
        ]
    if capability == "works-resident-coordination":
        source["preferences"] = pick(c.get("resident"), ("preferred", "unavailable"))
        source["appointments"] = [
            dict(
                pick(a, ("type", "date", "slot", "outcome")),
                **({} if need_ok else {"outcome": projection.status_only(a.get("outcome"))}),
            )
            for a in c.get("appointments", [])
        ]
        source["handoff"] = pick(c.get("handoff"), ("state", "to_code", "at"))
        source["requests"] = [
            pick(r, ("id", "status", "next_update")) for r in c.get("service_requests", [])
        ]
        name = (c.get("contractor") or {}).get("name")
        source["capacity"] = []
        for p in (procurement or {}).get("packages", []):
            cap = (p.get("capacity") or {}).get(name)
            if cap:
                source["capacity"].append(
                    dict(
                        package=p.get("id"),
                        period_from=p.get("period_from"),
                        period_to=p.get("period_to"),
                        contractor=name,
                        **pick(cap, ("committed", "evidence")),
                    )
                )
    if capability == "quality-evidence":
        source["quality"] = [
            dict(
                pick(q, ("measure", "state", "checklist_version", "evidence_version")),
                items=[pick(i, ("label", "evidence")) for i in q.get("items", [])],
            )
            for q in quality.active_records(c.get("quality", []))
        ]
        source["checklists"] = {m: quality.checklist_for(m) for m in measures(c)}
        if sensors is not None:
            source["sensors"] = sensors
    unknowns = []

    def missing(value, path):
        if value is None or value == "" or value == []:
            unknowns.append(path)
        elif isinstance(value, dict):
            for key, child in value.items():
                missing(child, f"{path}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                missing(child, f"{path}.{index}")

    missing(source, "source")
    citations = {
        f"source:{key}": dict(locator=f"case:{c['id']}/{key}", content_hash=digest(value))
        for key, value in source.items()
    }
    if source.get("sensors"):
        for key, reading in sensor_view.citations(source["sensors"]).items():
            citations[key] = dict(
                locator=f"sensor_reading/{reading['sensor_id']}/{reading['reading_id']}",
                content_hash=digest(reading),
            )
    return dict(
        sources=source,
        citations=citations,
        unknowns=unknowns,
        schema=SCHEMA_VERSION,
        rules=RULE_VERSION,
        registry=VERSION,
        registry_hash=digest(
            dict(version=VERSION, capability=capability, contract=REGISTRY[capability])
        ),
        schema_hash=digest(dict(version=SCHEMA_VERSION, schema=OUTPUT_SCHEMA)),
        rule_hash=digest(dict(version=RULE_VERSION, predicate=RULES[capability])),
        exercise_predicate=RULES[capability],
        exercise_rule="Selected synthetic gap predicates, not approved company rules.",
    )


def eligible(capability, snapshot, now_date, changed=False, known=False):
    s = snapshot["sources"]
    if capability == "stock-prioritisation":
        h, survey = s["home"], s["survey"]
        return any(h.get(k) in (None, "", "Unknown") for k in ("epc", "type", "built")) or any(
            survey.get(k) not in (None, "") and survey[k] != h.get(k)
            for k in ("epc", "type", "built")
        )
    if capability == "assessment-preparation":
        kinds = {d["kind"] for d in s["documents"]}
        return (
            changed
            or not {"Survey", "Design"} <= kinds
            or not s["technical"]["design_version"]
            or any(not d["content_sha256"] for d in s["documents"])
        )
    if capability == "funding-evidence":
        f = s["funding"]
        basic = (
            not s["measures"]
            or f["route"] in (None, "", "Not decided")
            or not f["reference"]
            or not s["grants"]
            or not s["finance"]["budget"]["amount"]
        )
        invoices_missing = any(
            not inv["ref"]
            or not inv["lines"]
            or any(
                any(
                    line.get(k) in (None, "")
                    for k in ("measure", "quantity", "amount", "milestone_ref")
                )
                for line in inv["lines"]
            )
            for inv in s["finance"]["invoices"]
        )
        claim_missing = any(
            g["state"] in ("Claimable", "Submitted", "Accepted", "Cash received")
            and (
                not any(e.get("source") for e in g["evidence"])
                or not any(
                    d["kind"] == "Funding evidence" and d["content_sha256"] for d in s["documents"]
                )
            )
            for g in s["grants"]
        )
        return changed or basic or invoices_missing or claim_missing
    if capability == "works-resident-coordination":
        return (
            s["handoff"]["state"] in ("Offered", "Received", "Escalated")
            or any(
                a["date"]
                and a["date"] < now_date
                and a["outcome"] in (None, "", "Booked", "Planned", "No access", "Missed")
                for a in s["appointments"]
            )
            or any(
                r["next_update"]
                and r["next_update"] < now_date
                and r["status"] not in ("Closed", "Resolved")
                for r in s["requests"]
            )
        )
    if not s["measures"]:
        return True
    active = quality.active_records(s["quality"])
    if any(q["measure"] not in s["measures"] for q in active):
        return True
    for m in s["measures"]:
        records = [q for q in active if q["measure"] == m]
        if len(records) != 1:
            return True
        q = records[0]
        if q["state"] not in (quality.ACCEPTED, quality.HANDED):
            return True
        labels = s["checklists"][m]["items"]
        if q["checklist_version"] != s["checklists"][m]["version"]:
            return True
        if any(
            not any(i["label"] == label and i["evidence"] for i in q["items"]) for label in labels
        ):
            return True
        if any(
            len({i["evidence"] for i in q["items"] if i["label"] == label}) > 1 for label in labels
        ):
            return True
    sensors = s.get("sensors") or {}
    return changed or bool(
        sensors.get("state") == "ok"
        and sensors.get("readings")
        and not sensors.get("conflicting_readings")
        and not sensors.get("implausible_readings")
        and s["quality"]
        and not known
    )


def review_flag(
    task, provenance=(), actionable=True, withheld=False, newer_readings=False, current=None
):
    """Projection of a returned quality-evidence output. Only a proactive, current, returned model finding
    that cites captured sensor readings is an autonomous L4 review flag; every other state is named as such."""
    envelope, output = task.get("envelope") or {}, task.get("output")
    if (
        task.get("capability") != "quality-evidence"
        or not output
        or envelope.get("source") != "ai"
        or envelope.get("outcome") != "returned"
    ):
        return None
    if withheld:
        return dict(
            level=None,
            status="withheld",
            autonomous=False,
            unapproved=True,
            task_state=task.get("state"),
            effect="Monitoring consent is not granted now, so retained readings, citations and findings built on them are withheld. "
            "The stored record is kept.",
        )
    snap = task.get("snapshot") or {}
    snap_sources = snap.get("sources") or {}
    snap_citations = snap.get("citations") or {}
    sensors = snap_sources.get("sensors") or {}
    prov_map = sensors.get("provenance") or {}
    known = sensor_view.citations(sensors)
    cited = sorted({x for finding in output["findings"] for x in finding["citations"]})
    sensor_cited = [x for x in cited if x in known]
    proactive = (task.get("dispatch") or {}).get("trigger") == "proactive"
    state = task.get("state")
    now_sensors = ((current or {}).get("sources") or {}).get("sensors") or {}
    # Only a successful observation may call a cited reading missing; an unavailable or consent-withheld
    # capture is unknown, never an empty one.
    observed = current is not None and now_sensors.get("state") in ("ok", "no-readings")
    captured_conflicts = list(sensors.get("conflicting_readings") or [])
    captured_implausible = list(sensors.get("implausible_readings") or [])
    # A corrected row keeps its id, so a cited reading may be impossible now although it was valid at capture.
    if observed and not captured_implausible:
        captured_implausible = [
            e
            for e in sensor_view.implausible(sensor_view.citations(now_sensors).values())
            if e["citation_key"] in known
        ]
    current_conflicts = list(now_sensors.get("conflicting_readings") or []) if observed else []
    same_bucket_conflict = bool(
        current_conflicts
        and (actionable or _sensor_bucket_key(current) == _sensor_bucket_key(snap))
    )
    clashes = (
        captured_conflicts
        if (actionable and captured_conflicts)
        else (current_conflicts if same_bucket_conflict else [])
    )
    if state == "rejected":
        status = "rejected"
    elif state == "accepted":
        status = "reviewed"
    elif state == "ready" and clashes:
        status = "conflicting-readings"
    elif state == "ready" and captured_implausible:
        status = "implausible-readings"
    elif not actionable or state != "ready":
        status = "not-current"
    elif not proactive:
        status = "manual-proposal"
    elif not sensor_cited:
        status = "uncited"
    else:
        status = "review-suggested"
    autonomous = status == "review-suggested"
    as_of = (task.get("dispatch") or {}).get("as_of")
    timing = sensor_view.as_of_state(sensors, as_of) if isinstance(as_of, (int, float)) else {}
    newer = bool(newer_readings and autonomous)
    now_rows = sensor_view.citations(now_sensors) if observed else None
    # missing_ids means absent from the current bounded capture (a newest-window selection). Rotation out of
    # that window is not a deletion; the stored rows may still exist.
    comparison = dict(
        state="unknown",
        changed_ids=[],
        missing_ids=[],
        basis="current bounded capture; a missing citation may still be stored",
    )
    if now_rows is not None and sensor_cited:
        # Content, not identity: a corrected row keeps its id. Only cited rows decide; extra rows are counted apart.
        comparison["changed_ids"] = sorted(
            k
            for k in sensor_cited
            if k in now_rows and canonical(now_rows[k]) != canonical(known[k])
        )
        comparison["missing_ids"] = sorted(k for k in sensor_cited if k not in now_rows)
        comparison["state"] = (
            "changed" if comparison["changed_ids"] or comparison["missing_ids"] else "match"
        )
    changed = {"match": False, "changed": True}.get(comparison["state"])

    def _reading_entry(k):
        row = known[k]
        pclass = str(row.get("provenance_class") or "synthetic-unclassified")
        stext = str(
            prov_map.get(pclass)
            or sensor_view.CLASSES.get(pclass, sensor_view.CLASSES["synthetic-unclassified"])
        )
        meta = snap_citations.get(k) or {}
        return dict(
            sensor_id=row["sensor_id"],
            reading_id=row["reading_id"],
            citation=k,
            observed_at=row["observed_at"],
            temperature_c=row["temperature_c"],
            humidity_pct=row["humidity_pct"],
            provenance_class=pclass,
            source_text=stext,
            locator=meta.get("locator"),
            content_hash=meta.get("content_hash"),
            text=sensor_view.reading_text(row),
        )

    def _source_entry(k):
        meta = snap_citations.get(k) or {}
        if k in known:
            row = known[k]
            pclass = str(row.get("provenance_class") or "synthetic-unclassified")
            stext = str(
                prov_map.get(pclass)
                or sensor_view.CLASSES.get(pclass, sensor_view.CLASSES["synthetic-unclassified"])
            )
            return dict(
                citation=k,
                kind="sensor-reading",
                locator=meta.get("locator"),
                content_hash=meta.get("content_hash"),
                sensor_id=row["sensor_id"],
                reading_id=row["reading_id"],
                observed_at=row["observed_at"],
                provenance_class=pclass,
                source_text=stext,
            )
        return dict(
            citation=k,
            kind="case-evidence",
            locator=meta.get("locator"),
            content_hash=meta.get("content_hash"),
        )

    conflict_notice = (
        (
            sensors.get("conflict_notice")
            or (now_sensors.get("conflict_notice") if observed else None)
        )
        if clashes
        else None
    )
    effect = (
        "Retained sensor readings conflict for the same sensor and time, so no automatic review flag is raised. "
        "Do not choose between conflicting readings; use the ordinary quality check."
        if status == "conflicting-readings"
        else "A retained sensor reading is missing a value or outside the possible range, so no automatic review flag is raised. "
        "Do not rely on it; use the ordinary quality check."
        if status == "implausible-readings"
        else "Suggests a person review the cited readings. It does not accept work, close a defect, authorise payment or consent, "
        "diagnose a hazard or change any ranking."
        + (
            " Retained readings changed after this finding was captured; review the current readings and request a new proposal if needed."
            if newer
            else ""
        )
    )
    out = dict(
        changed_since_capture=changed,
        cited_comparison=comparison,
        newer_reading_count=None if now_rows is None else len(set(now_rows) - set(known)),
        level="L4" if autonomous else None,
        status=status,
        autonomous=autonomous,
        unapproved=True,
        newer_readings=newer,
        evidence_as_of=timing.get("request_as_of"),
        freshness=timing.get("freshness"),
        age_minutes=timing.get("age_minutes"),
        task_state=state,
        trigger="proactive" if proactive else "requested",
        invocation_modes=[
            str(e.get("mode"))
            for e in (provenance or ())
            if isinstance(e, Mapping) and e.get("kind") == "invocation" and e.get("mode")
        ],
        model=dict(
            provider=envelope.get("provider"),
            deployment=envelope.get("deployment"),
            model=envelope.get("model"),
            task_version=envelope.get("task_version"),
            release=task.get("release"),
        ),
        cited_ids=cited,
        sensor_cited_ids=sensor_cited,
        readings=[_reading_entry(k) for k in sensor_cited],
        source_provenance=[_source_entry(k) for k in cited],
        origin="generative_model",
        origin_text="Origin: generative_model. The finding is model-written; the cited retained values are decision_rule evidence.",
        not_retained=list(sensor_view.NOT_RETAINED),
        sensor_grounded=bool(sensor_cited),
        provenance_classes=sorted(prov_map),
        cited_provenance_classes=sorted(
            {
                str(known[k]["provenance_class"])
                for k in sensor_cited
                if known[k].get("provenance_class")
            }
        ),
        source_time=datetime.fromtimestamp(task["created_at"], timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        if isinstance(task.get("created_at"), (int, float))
        else None,
        delivery="No named recipient or delivery of a request is recorded.",
        effect=effect,
    )
    if clashes:
        out["conflicting_readings"] = clashes
        if conflict_notice:
            out["conflict_notice"] = conflict_notice
    if status == "implausible-readings":
        out["implausible_readings"] = captured_implausible
        out["implausible_notice"] = sensors.get("implausible_notice")
    return out


def validate_output(
    value: Any,
    snapshot: Mapping[str, Any],
    max_chars: int,
    *,
    guard_telemetry: GuardTelemetry | None = None,
) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {"summary", "findings", "unknowns"}:
        raise ValueError("Expected summary, findings and unknowns.")
    if (
        len(canonical(value)) > max_chars
        or not isinstance(value["summary"], str)
        or not value["summary"].strip()
        or not 1 <= len(value["summary"]) <= 1200
    ):
        raise ValueError("Summary/output bounds exceeded.")
    if not isinstance(value["findings"], list) or not 1 <= len(value["findings"]) <= 12:
        raise ValueError("Cited findings required.")
    if (
        not isinstance(value["unknowns"], list)
        or len(value["unknowns"]) > 80
        or any(not isinstance(x, str) or len(x) > 240 for x in value["unknowns"])
    ):
        raise ValueError("Unknowns must be bounded strings.")
    for item in value["findings"]:
        if (
            not isinstance(item, dict)
            or set(item) != {"text", "citations"}
            or not isinstance(item["text"], str)
            or not 1 <= len(item["text"]) <= 800
        ):
            raise ValueError("Invalid finding.")
        if (
            not isinstance(item["citations"], list)
            or not 1 <= len(item["citations"]) <= 8
            or any(
                not isinstance(x, str) or x not in snapshot["citations"] for x in item["citations"]
            )
        ):
            raise ValueError("Missing/unsupported citation.")
    # Deterministic unknowns cannot disappear merely because a model omitted them.
    value["unknowns"] = sorted(set(value["unknowns"] + snapshot["unknowns"]))
    if (
        len(value["unknowns"]) > 80
        or len(canonical(value)) > max_chars
        or FORBIDDEN.search(canonical(value))
    ):
        raise ValueError("Output bounds exceeded after unknown reconciliation.")
    violations: list[ViolationCategory] = []
    reasons: list[str] = []
    for candidate_text in (
        value["summary"],
        *[item["text"] for item in value["findings"]],
        *value["unknowns"],
    ):
        dec = inspect_regulatory_output(candidate_text, on_violation="reject")
        if not dec.passed:
            for v in dec.violations:
                if v not in violations:
                    violations.append(v)
            for r in dec.reasons:
                if r not in reasons:
                    reasons.append(r)
    if violations:
        if guard_telemetry is not None:
            guard_telemetry.record_decision(
                GuardDecision(
                    checked=True,
                    passed=False,
                    action="rejected",
                    violations=tuple(violations),
                    reasons=tuple(reasons),
                    rewritten_text=None,
                )
            )
        raise ValueError("Regulatory non-advice or future-law output guard rejected proposal.")
    if guard_telemetry is not None:
        guard_telemetry.record_decision(
            GuardDecision(
                checked=True,
                passed=True,
                action="passed",
                violations=(),
                reasons=(),
                rewritten_text=None,
            )
        )
    return value


def model_bounds(limits=None):
    """Stated per-request model-call and agent-depth bounds shared by the five assistants."""
    attempts = (
        Limits.DEFAULTS["attempts"] if limits is None or not limits.valid else limits.attempts
    )
    return dict(
        calls_per_attempt=MODEL_CALLS_PER_ATTEMPT,
        max_attempts=attempts,
        max_calls_per_request=MODEL_CALLS_PER_ATTEMPT * attempts,
        max_agent_depth=AGENT_DEPTH,
        tools=0,
        attempt_ceiling=ATTEMPT_CEILING,
    )


class Limits:
    DEFAULTS = dict(
        scan_interval=60,
        scan_size=20,
        input_chars=12000,
        output_chars=8000,
        output_tokens=600,
        timeout=20,
        active_calls=2,
        attempts=2,
        backoff=30,
        lease=60,
    )

    def __init__(self, env: Mapping[str, str] | None = None) -> None:
        env = os.environ if env is None else env
        self.authority = env.get("ZF_ASSIST_AUTHORITY", "")
        self.proactive = env.get("ZF_ASSIST_PROACTIVE", "0") == "1"
        self.expiry = None
        self.valid = False
        self.error = "Operator authority, finite allowance and expiry are required."
        try:
            for key, default in self.DEFAULTS.items():
                setattr(self, key, int(env.get(f"ZF_ASSIST_{key.upper()}", default)))
            self.calls = int(env.get("ZF_ASSIST_CALL_ALLOWANCE", "0"))
            self.tokens = int(env.get("ZF_ASSIST_TOKEN_ALLOWANCE", "0"))
            expiry = datetime.fromisoformat(env.get("ZF_ASSIST_EXPIRES", "").replace("Z", "+00:00"))
            if expiry.tzinfo is None:
                raise ValueError("Explicit expiry timezone required.")
            self.expiry = expiry.timestamp()
            bounds = dict(
                scan_interval=(5, 3600),
                scan_size=(1, 100),
                input_chars=(1000, 24000),
                output_chars=(1000, 16000),
                output_tokens=(100, 2000),
                timeout=(1, 40),
                active_calls=(1, 4),
                attempts=(1, ATTEMPT_CEILING),
                backoff=(1, 3600),
                lease=(10, 120),
            )
            self.valid = (
                1 <= len(self.authority) <= 120
                and 1 <= self.calls <= 1000000
                and self.reservation <= self.tokens <= 1000000000000
                and all(lo <= getattr(self, k) <= hi for k, (lo, hi) in bounds.items())
                and self.lease >= self.timeout + 5
                and math.isfinite(self.expiry)
            )
            if not self.valid:
                self.error = "Invalid bounded assistant configuration."
        except (ValueError, TypeError, OverflowError):
            for key, default in self.DEFAULTS.items():
                setattr(self, key, default)
            self.calls, self.tokens = 0, 0
        # Opt-in exact-five Quality scope; an invalid value refuses Quality, it never widens the scope.
        self.quality_homes: tuple[str, ...] | None = None
        self.quality_scope_error = False
        try:
            self.quality_homes = demo_homes(env.get("ZF_ASSIST_QUALITY_DEMO_HOMES"))
        except ValueError:
            self.quality_scope_error = True

    @property
    def reservation(self):
        # Bytes/characters upper-bound input tokens without a new tokenizer dependency.
        return self.input_chars + self.output_tokens

    @property
    def pool(self):
        return digest(self.authority)


SYSTEM = (
    "Return JSON only: {summary:string,findings:[{text:string,citations:[source IDs]}],unknowns:[string]}. "
    "Use only the supplied inert evidence. Cite each finding with supplied source IDs. "
    "No tools, actions, approvals, certification or invented facts. This is a human-reviewed proposal."
)
PROVENANCE = "constructed-synthetic-demo-labelled"


def runtime_binding(capability, ai):
    """What this build would dispatch with; a release must match it exactly, so any material change needs renewed evidence."""
    from . import ai_registry

    spec = REGISTRY[capability]
    policy = [RULES[capability], OUTPUT_SCHEMA]
    if capability == "stock-prioritisation":
        policy.append(ranking.policy_hash(ranking.CURRENT))
    elif capability == "quality-evidence":
        policy.append(quality.policy_fingerprint())
    return dict(
        registry_version=VERSION,
        schema_version=SCHEMA_VERSION,
        provider=getattr(ai, "provider", "azure-openai"),
        endpoint=getattr(ai, "endpoint", "") or "",
        deployment=getattr(ai, "fast", "") or "",
        prompt_version=digest([SYSTEM, spec["purpose"]])[:16],
        policy_version=f"{RULE_VERSION}:{digest(policy)[:12]}",
        data_version=digest([SCHEMA_VERSION, spec["categories"]])[:16],
        provenance_version=PROVENANCE,
        permission_version=digest([spec["roles"], PURPOSE])[:16],
        model_version=getattr(ai, "model_version", "unattested"),
        task_contract_version=digest(ai_registry.get(capability)),
        evaluation_version=rai_release.EVALUATION_VERSION,
    )


def contract_refusal(task):
    """The plain refusal when the task's evidence breaks its declared data contract, else None."""
    try:
        enforce_contract(task)
    except task_contracts.ContractRefusal as refusal:
        return str(refusal)
    return None


def enforce_contract(task):
    task_contracts.enforce(
        task["capability"],
        dict(case_id=str(task.get("case_id", "")), source_snapshot=canonical(task["snapshot"])),
    )


def build_request(task):
    """The system and user text sent to the provider; shared by the API and the agents worker."""
    enforce_contract(task)
    evidence, as_of = task["snapshot"], (task.get("dispatch") or {}).get("as_of")
    sensors = evidence.get("sources", {}).get("sensors")
    if sensors is not None and isinstance(as_of, (int, float)):
        evidence = dict(
            evidence,
            sources=dict(
                evidence["sources"],
                sensors=dict(sensors, **sensor_view.as_of_state(sensors, as_of)),
            ),
        )
    return SYSTEM, canonical(
        dict(
            capability=task["capability"],
            purpose=REGISTRY[task["capability"]]["purpose"],
            evidence=evidence,
        )
    )


def sanitize_identity(envelope: dict[str, Any]) -> dict[str, Any]:
    """A copy whose provider, deployment and model are safe identifiers, whatever path produced the envelope."""
    clean = dict(envelope)
    for key in ("provider", "deployment", "model"):
        clean[key] = ai_consumption.safe_identity(clean.get(key))
    return clean


def shape_result(
    task: dict[str, Any],
    result: Any,
    limits: Limits,
    *,
    guard_telemetry: GuardTelemetry | None = None,
) -> tuple[dict[str, Any], Any, Any]:
    """Reduce a raw provider result to (envelope, output, failure). Only safe, known fields survive; text is never saved on failure."""
    if not isinstance(result, dict):
        result = dict(
            outcome="malformed-provider-envelope", usage=None, source="unverified", text=None
        )
    envelope = pick(result, ("provider", "deployment", "model", "outcome", "source"))
    envelope["usage"] = result.get("usage")
    envelope.update(
        task=task["capability"],
        task_version=task["version"],
        case_id=task["case_id"],
        source_signature=task["source_signature"],
        approved=False,
    )
    for key in ("outcome", "source"):
        envelope[key] = envelope[key][:120] if isinstance(envelope[key], str) else None
    envelope = sanitize_identity(envelope)
    usage = envelope["usage"]
    valid = ai_consumption.usage(usage)
    envelope["usage"] = valid if valid and valid["prompt_tokens"] > 0 else None
    for key in ("meter_id", "meter_root", "configuration", "prompt_hash"):
        value = result.get(key)
        if (
            isinstance(value, str)
            and len(value) == 64
            and all(c in "0123456789abcdef" for c in value)
        ):
            envelope[key] = value
    output, failure = None, None
    try:
        if result.get("source") != "ai" or result.get("outcome") != "returned":
            raise ValueError("AI unavailable/unverified; use the manual route.")
        text = result.get("text")
        if not isinstance(text, str) or len(text) > limits.output_chars:
            raise ValueError("Output exceeds bounds.")
        output = validate_output(
            json.loads(text),
            task["snapshot"],
            limits.output_chars,
            guard_telemetry=guard_telemetry,
        )
    except (ValueError, TypeError, KeyError):
        failure = "Failed or malformed evidence proposal; human/manual work required."
        envelope["source"] = "unverified"
    return envelope, output, failure


HOLD_GRACE = 5.0
PAUSED = "Readings kept changing before the model ran; automatic review is paused briefly. Request review manually or wait."
SQLITE_DDL = (
    "CREATE TABLE IF NOT EXISTS continuity_gate_state (id INTEGER PRIMARY KEY CHECK (id = 1), gate_version TEXT NOT NULL, epoch INTEGER NOT NULL DEFAULT 0)",
    "CREATE TABLE IF NOT EXISTS continuity_open_holds (scope TEXT PRIMARY KEY, incident_id TEXT NOT NULL, epoch INTEGER NOT NULL)",
    "CREATE TABLE IF NOT EXISTS assistant_tasks (id TEXT PRIMARY KEY, capability TEXT NOT NULL, case_id TEXT NOT NULL, signature TEXT NOT NULL, body TEXT NOT NULL, state TEXT NOT NULL, fence INTEGER NOT NULL, owner TEXT NOT NULL, lease_until REAL NOT NULL, attempts INTEGER NOT NULL, not_before REAL NOT NULL, revision INTEGER NOT NULL, dispatched REAL NOT NULL DEFAULT 0, review_gate_version TEXT NOT NULL DEFAULT '', reviewed_revision INTEGER NOT NULL DEFAULT 0)",
    "CREATE TABLE IF NOT EXISTS assistant_allowance (id TEXT PRIMARY KEY, calls INTEGER NOT NULL, tokens INTEGER NOT NULL, expires REAL NOT NULL, used_calls INTEGER NOT NULL, reserved_tokens INTEGER NOT NULL)",
    "CREATE TABLE IF NOT EXISTS assistant_attempts (id TEXT PRIMARY KEY, task_id TEXT NOT NULL, fence INTEGER NOT NULL, pool TEXT NOT NULL, reserved INTEGER NOT NULL, actual INTEGER, outcome TEXT NOT NULL, active_until REAL NOT NULL DEFAULT 0, capability TEXT NOT NULL DEFAULT '', gate_version TEXT NOT NULL DEFAULT '', send_gate_version TEXT NOT NULL DEFAULT '')",
    "CREATE TABLE IF NOT EXISTS assistant_events (id TEXT PRIMARY KEY, task_id TEXT NOT NULL, at REAL NOT NULL, body TEXT NOT NULL)",
    "CREATE INDEX IF NOT EXISTS ix_assistant_pending ON assistant_tasks (state, not_before, lease_until)",
    "CREATE TABLE IF NOT EXISTS assistant_schedule (capability TEXT NOT NULL, case_id TEXT NOT NULL, scope TEXT NOT NULL, signature TEXT NOT NULL, task_id TEXT NOT NULL, at REAL NOT NULL, replaced INTEGER NOT NULL DEFAULT 0, seen TEXT NOT NULL DEFAULT '', paused_at REAL NOT NULL DEFAULT 0, PRIMARY KEY (capability, case_id))",
    "CREATE INDEX IF NOT EXISTS ix_assistant_case ON assistant_tasks (capability, case_id)",
    "CREATE TABLE IF NOT EXISTS assistant_dispatch_gate (home_id TEXT NOT NULL, task_id TEXT NOT NULL, fence INTEGER NOT NULL, expires_at REAL NOT NULL, PRIMARY KEY (home_id, task_id, fence))",
) + rel.SQLITE_DDL
MSSQL_DDL = (
    "CREATE TABLE continuity_gate_state (id INT PRIMARY KEY CHECK (id = 1), gate_version VARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL, epoch BIGINT NOT NULL DEFAULT 0)",
    "CREATE TABLE continuity_open_holds (scope VARCHAR(64) COLLATE Latin1_General_100_BIN2 PRIMARY KEY, incident_id VARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL, epoch BIGINT NOT NULL)",
    "CREATE TABLE assistant_tasks (id VARCHAR(64) PRIMARY KEY, capability VARCHAR(64) NOT NULL, case_id NVARCHAR(64) NOT NULL, signature VARCHAR(64) NOT NULL, body NVARCHAR(MAX) NOT NULL, state VARCHAR(24) NOT NULL, fence BIGINT NOT NULL, owner VARCHAR(64) NOT NULL, lease_until FLOAT NOT NULL, attempts INT NOT NULL, not_before FLOAT NOT NULL, revision BIGINT NOT NULL, dispatched FLOAT NOT NULL DEFAULT 0, review_gate_version VARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL DEFAULT '', reviewed_revision BIGINT NOT NULL DEFAULT 0)",
    "CREATE TABLE assistant_allowance (id VARCHAR(64) PRIMARY KEY, calls BIGINT NOT NULL, tokens BIGINT NOT NULL, expires FLOAT NOT NULL, used_calls BIGINT NOT NULL, reserved_tokens BIGINT NOT NULL)",
    "CREATE TABLE assistant_attempts (id VARCHAR(100) PRIMARY KEY, task_id VARCHAR(64) NOT NULL, fence BIGINT NOT NULL, pool VARCHAR(64) NOT NULL, reserved BIGINT NOT NULL, actual BIGINT NULL, outcome VARCHAR(40) NOT NULL, active_until FLOAT NOT NULL DEFAULT 0, capability VARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL DEFAULT '', gate_version VARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL DEFAULT '', send_gate_version VARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL DEFAULT '')",
    "CREATE TABLE assistant_events (id VARCHAR(64) PRIMARY KEY, task_id VARCHAR(64) NOT NULL, at FLOAT NOT NULL, body NVARCHAR(MAX) NOT NULL)",
    "CREATE TABLE assistant_schedule (capability VARCHAR(64) NOT NULL, case_id NVARCHAR(64) NOT NULL, scope VARCHAR(64) NOT NULL, signature VARCHAR(64) NOT NULL, task_id VARCHAR(64) NOT NULL, at FLOAT NOT NULL, replaced INT NOT NULL DEFAULT 0, seen VARCHAR(64) NOT NULL DEFAULT '', paused_at FLOAT NOT NULL DEFAULT 0, PRIMARY KEY (capability, case_id))",
    "CREATE TABLE assistant_dispatch_gate (home_id NVARCHAR(128) NOT NULL, task_id VARCHAR(64) NOT NULL, fence BIGINT NOT NULL, expires_at FLOAT NOT NULL, PRIMARY KEY (home_id, task_id, fence))",
) + rel.MSSQL_DDL

SQLITE_ATTEMPT_TRIGGERS = (
    "CREATE TRIGGER IF NOT EXISTS continuity_gate_no_delete BEFORE DELETE ON continuity_gate_state "
    "BEGIN SELECT RAISE(ABORT, 'continuity gate state cannot be deleted'); END",
    "CREATE TRIGGER IF NOT EXISTS continuity_gate_monotonic BEFORE UPDATE ON continuity_gate_state WHEN NEW.epoch < OLD.epoch "
    "BEGIN SELECT RAISE(ABORT, 'continuity gate epoch is monotonic'); END",
    "CREATE TRIGGER IF NOT EXISTS assistant_attempts_gate_insert BEFORE INSERT ON assistant_attempts "
    "WHEN (NEW.outcome = 'reserved' AND (NEW.capability = '' OR NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = NEW.gate_version))) "
    "OR (NEW.outcome = 'sending' AND (NEW.capability = '' OR NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = NEW.gate_version AND g.gate_version = NEW.send_gate_version))) "
    "BEGIN SELECT RAISE(ABORT, 'continuity SQL gate mismatch'); END",
    "CREATE TRIGGER IF NOT EXISTS assistant_attempts_hold_insert BEFORE INSERT ON assistant_attempts "
    "WHEN NEW.outcome IN ('reserved', 'sending') AND EXISTS (SELECT 1 FROM continuity_open_holds h WHERE h.scope = 'all' OR h.scope = NEW.capability) "
    "BEGIN SELECT RAISE(ABORT, 'continuity scope is suspended'); END",
    "CREATE TRIGGER IF NOT EXISTS assistant_attempts_gate_update BEFORE UPDATE ON assistant_attempts "
    "WHEN (NEW.active_until > 0 OR NEW.outcome <> OLD.outcome) AND ("
    "(NEW.outcome = 'reserved' AND (NEW.capability = '' OR NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = NEW.gate_version))) "
    "OR (NEW.outcome = 'sending' AND (NEW.capability = '' OR NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = NEW.gate_version AND g.gate_version = NEW.send_gate_version)))) "
    "BEGIN SELECT RAISE(ABORT, 'continuity SQL gate mismatch'); END",
    "CREATE TRIGGER IF NOT EXISTS assistant_attempts_hold_update BEFORE UPDATE ON assistant_attempts "
    "WHEN NEW.outcome IN ('reserved', 'sending') "
    "AND EXISTS (SELECT 1 FROM continuity_open_holds h WHERE h.scope = 'all' OR h.scope = NEW.capability) "
    "BEGIN SELECT RAISE(ABORT, 'continuity scope is suspended'); END",
    "CREATE TRIGGER IF NOT EXISTS assistant_tasks_gate_insert BEFORE INSERT ON assistant_tasks "
    "WHEN NEW.state = 'accepted' AND (NEW.reviewed_revision <> NEW.revision OR NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = NEW.review_gate_version)) "
    "BEGIN SELECT RAISE(ABORT, 'continuity SQL gate mismatch'); END",
    "CREATE TRIGGER IF NOT EXISTS assistant_tasks_hold_insert BEFORE INSERT ON assistant_tasks "
    "WHEN NEW.state = 'accepted' AND EXISTS (SELECT 1 FROM continuity_open_holds h WHERE h.scope = 'all' OR h.scope = NEW.capability) "
    "BEGIN SELECT RAISE(ABORT, 'continuity scope is suspended'); END",
    "CREATE TRIGGER IF NOT EXISTS assistant_tasks_gate_update "
    "BEFORE UPDATE OF state, body, capability, review_gate_version, reviewed_revision ON assistant_tasks "
    "WHEN ((NEW.state = 'accepted' AND (OLD.state <> 'accepted' OR NEW.revision <> OLD.revision OR NEW.body <> OLD.body)) "
    "OR (OLD.state = 'ready' AND NEW.state = 'ready' AND NEW.revision <> OLD.revision)) "
    "AND (NEW.reviewed_revision <> NEW.revision OR NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = NEW.review_gate_version)) "
    "BEGIN SELECT RAISE(ABORT, 'continuity SQL gate mismatch'); END",
    "CREATE TRIGGER IF NOT EXISTS assistant_tasks_hold_update "
    "BEFORE UPDATE OF state, body, capability, review_gate_version, reviewed_revision ON assistant_tasks "
    "WHEN ((NEW.state = 'accepted' AND (OLD.state <> 'accepted' OR NEW.revision <> OLD.revision OR NEW.body <> OLD.body)) "
    "OR (OLD.state = 'ready' AND NEW.state = 'ready' AND NEW.revision <> OLD.revision)) "
    "AND EXISTS (SELECT 1 FROM continuity_open_holds h WHERE h.scope = 'all' OR h.scope = NEW.capability) "
    "BEGIN SELECT RAISE(ABORT, 'continuity scope is suspended'); END",
)

MSSQL_ATTEMPT_TRIGGERS = (
    "IF OBJECT_ID(N'continuity_gate_no_delete', N'TR') IS NULL EXEC(N'CREATE TRIGGER continuity_gate_no_delete ON continuity_gate_state "
    "INSTEAD OF DELETE AS IF EXISTS (SELECT 1 FROM deleted) THROW 50004, ''continuity gate state cannot be deleted'', 1')",
    "IF OBJECT_ID(N'continuity_gate_monotonic', N'TR') IS NULL EXEC(N'CREATE TRIGGER continuity_gate_monotonic ON continuity_gate_state "
    "AFTER UPDATE AS IF EXISTS (SELECT 1 FROM inserted i JOIN deleted d ON d.id = i.id WHERE i.epoch < d.epoch) "
    "THROW 50004, ''continuity gate epoch is monotonic'', 1')",
    "IF OBJECT_ID(N'assistant_attempts_gate_insert', N'TR') IS NULL EXEC(N'CREATE TRIGGER assistant_attempts_gate_insert ON assistant_attempts "
    "AFTER INSERT AS "
    "IF EXISTS (SELECT 1 FROM inserted i WHERE (i.outcome = ''reserved'' AND (i.capability = '''' OR NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = i.gate_version))) "
    "OR (i.outcome = ''sending'' AND (i.capability = '''' OR NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = i.gate_version AND g.gate_version = i.send_gate_version)))) "
    "THROW 50004, ''continuity SQL gate mismatch'', 1; "
    "IF EXISTS (SELECT 1 FROM inserted i WHERE i.outcome IN (''reserved'', ''sending'') AND EXISTS (SELECT 1 FROM continuity_open_holds h WHERE h.scope = ''all'' OR h.scope = i.capability)) "
    "THROW 50004, ''continuity scope is suspended'', 1')",
    "IF OBJECT_ID(N'assistant_attempts_gate_update', N'TR') IS NULL EXEC(N'CREATE TRIGGER assistant_attempts_gate_update ON assistant_attempts "
    "AFTER UPDATE AS "
    "IF EXISTS (SELECT 1 FROM inserted i JOIN deleted d ON d.id = i.id WHERE (i.active_until > 0 OR i.outcome <> d.outcome) AND ("
    "(i.outcome = ''reserved'' AND (i.capability = '''' OR NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = i.gate_version))) "
    "OR (i.outcome = ''sending'' AND (i.capability = '''' OR NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = i.gate_version AND g.gate_version = i.send_gate_version))))) "
    "THROW 50004, ''continuity SQL gate mismatch'', 1; "
    "IF EXISTS (SELECT 1 FROM inserted i WHERE i.outcome IN (''reserved'', ''sending'') "
    "AND EXISTS (SELECT 1 FROM continuity_open_holds h WHERE h.scope = ''all'' OR h.scope = i.capability)) "
    "THROW 50004, ''continuity scope is suspended'', 1')",
    "IF OBJECT_ID(N'assistant_tasks_gate_insert', N'TR') IS NULL EXEC(N'CREATE TRIGGER assistant_tasks_gate_insert ON assistant_tasks "
    "AFTER INSERT AS "
    "IF EXISTS (SELECT 1 FROM inserted i WHERE i.state = ''accepted'' AND (i.reviewed_revision <> i.revision OR NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = i.review_gate_version))) "
    "THROW 50004, ''continuity SQL gate mismatch'', 1; "
    "IF EXISTS (SELECT 1 FROM inserted i WHERE i.state = ''accepted'' AND EXISTS (SELECT 1 FROM continuity_open_holds h WHERE h.scope = ''all'' OR h.scope = i.capability COLLATE Latin1_General_100_BIN2)) "
    "THROW 50004, ''continuity scope is suspended'', 1')",
    "IF OBJECT_ID(N'assistant_tasks_gate_update', N'TR') IS NULL EXEC(N'CREATE TRIGGER assistant_tasks_gate_update ON assistant_tasks "
    "AFTER UPDATE AS "
    "IF (UPDATE(state) OR UPDATE(body) OR UPDATE(capability) OR UPDATE(review_gate_version) OR UPDATE(reviewed_revision)) "
    "BEGIN "
    "IF EXISTS (SELECT 1 FROM inserted i JOIN deleted d ON d.id = i.id WHERE ((i.state = ''accepted'' AND (d.state <> ''accepted'' OR i.revision <> d.revision OR i.body <> d.body)) "
    "OR (d.state = ''ready'' AND i.state = ''ready'' AND i.revision <> d.revision)) "
    "AND (i.reviewed_revision <> i.revision OR NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = i.review_gate_version))) "
    "THROW 50004, ''continuity SQL gate mismatch'', 1; "
    "IF EXISTS (SELECT 1 FROM inserted i JOIN deleted d ON d.id = i.id WHERE ((i.state = ''accepted'' AND (d.state <> ''accepted'' OR i.revision <> d.revision OR i.body <> d.body)) "
    "OR (d.state = ''ready'' AND i.state = ''ready'' AND i.revision <> d.revision)) "
    "AND EXISTS (SELECT 1 FROM continuity_open_holds h WHERE h.scope = ''all'' OR h.scope = i.capability COLLATE Latin1_General_100_BIN2)) "
    "THROW 50004, ''continuity scope is suspended'', 1; "
    "END')",
)


class DispatchGate:
    """Per-attempt consent re-check for a carrier that declares it sends no bytes.

    Calling it commits the final consent check and a fenced gate row together, so a withdrawal for that home
    waits for the row. Direct SQL control writes for the home are rejected by the guard trigger while a row
    is live. This is NOT a guarantee about physical transmission: a process suspended between this check and
    a real send could still transmit. For that reason a real Ai client is never given captured readings
    (see `ai.may_carry_captured_readings`); this gate only covers carriers that cannot transmit them."""

    def __init__(self, service, task):
        self.service, self.task, self.written = service, task, False

    def __call__(self):
        service, task = self.service, self.task
        with service.transaction() as db:
            granted = service._sensors_granted(db, task)
            if granted and service._captured_sensors(task):
                key = (task["case_id"], task["id"], task["fence"])
                db.execute(
                    "DELETE FROM assistant_dispatch_gate WHERE home_id=? AND task_id=? AND fence=?",
                    key,
                )
                db.execute(
                    "INSERT INTO assistant_dispatch_gate (home_id,task_id,fence,expires_at) VALUES (?,?,?,?)",
                    (*key, service.now(db) + service.limits.timeout + HOLD_GRACE),
                )
                self.written = True
        if not granted:
            raise ai_consumption.DispatchWithdrawn("consent-withdrawn")

    def release(self):
        if not self.written:
            return
        try:
            with self.service.transaction() as db:
                db.execute(
                    "DELETE FROM assistant_dispatch_gate WHERE home_id=? AND task_id=? AND fence=?",
                    (self.task["case_id"], self.task["id"], self.task["fence"]),
                )
        except Exception:
            pass  # The row expires on the database clock and the send-by deadline has passed.


class CallTicket:
    """One admitted direct call. end() settles the durable reservation once and releases the physical slot once."""

    def __init__(self, service, attempt, reason, capability=None):
        self.service, self.attempt, self.reason, self.capability = (
            service,
            attempt,
            reason,
            capability,
        )
        self.lock, self.done = threading.Lock(), attempt is None

    def send_fence(self):
        """Raises DispatchWithdrawn unless this admission is still valid to send now (see Assistants.fence_send)."""
        self.service.fence_send(self.attempt, self.capability)

    def end(self, envelope):
        with self.lock:
            if self.done:
                return
            self.done = True
            try:
                with self.service.transaction() as db:
                    actual, reserved = self.service._settle(db, self.attempt, envelope)
                    self.service.event(
                        db,
                        self.attempt.split(":")[0],
                        kind="direct-call-completed",
                        outcome=str(envelope.get("outcome", "unknown"))[:40],
                        actual_tokens=actual,
                        reservation_liability=reserved if actual is None else actual,
                    )
            finally:
                # An unsettled attempt keeps its durable slot and reservation until its lease expires.
                self.service.call_slots.release()


class Affected(list):
    """Affected proposals with the full count, so a capped list is never mistaken for the whole set."""

    def __init__(self, items=(), total=None):
        super().__init__(items)
        self.total = len(self) if total is None else total
        self.truncated = self.total > len(self)


class _ForecastJob:
    def __init__(self):
        self.done = threading.Event()
        self.result: dict | None = None
        self.error: BaseException | None = None


class Assistants:
    def __init__(
        self,
        store,
        env=None,
        provider=None,
        transport=None,
        *,
        guard_telemetry: GuardTelemetry | None = None,
    ):
        self.store, self.limits = store, Limits(env)
        self.guard_telemetry: GuardTelemetry = (
            guard_telemetry if guard_telemetry is not None else GuardTelemetry()
        )
        self._guard_local = threading.local()
        # Resolves the object that physically carries the request bytes, when the provider hides it behind a wrapper.
        self.transport = transport
        # The provider port: (system, prompt, max_tokens, timeout) -> raw envelope. The default late-binds to the store's AI client.
        self.provider = provider or self._default_provider
        self.sql = hasattr(store, "assistant_connection")
        self.mssql = hasattr(store, "_env")
        self.stop_event = threading.Event()
        self.dispatch_lock = threading.Lock()
        self.threads = []
        self.scan_lock = threading.Lock()
        self.call_slots = threading.BoundedSemaphore(
            self.limits.active_calls if self.limits.valid else 1
        )
        self.scan_cursor = ""
        self._forecasts: dict[tuple, tuple[float, dict]] = {}
        self._forecast_jobs: dict[tuple, "_ForecastJob"] = {}
        self._forecast_lock = threading.Lock()
        self.incomplete = set()
        self.approvers = {
            x.strip().lower()
            for x in (env or os.environ).get("ZF_ASSIST_RELEASE_APPROVERS", "").split(",")
            if x.strip()
        }
        self.schema_error = None
        if self.sql:
            try:
                self.migrate()
            except Exception:
                self.sql = False
                self.schema_error = "Assistant schema unavailable; operator migration required. Continue ordinary case work manually."
        self.consumption = ai_consumption.Consumption(self)
        if isinstance(store.ai, Ai) and self.sql:
            store.ai.consumption = self.consumption

    def migrate(self):
        with self.transaction() as db:
            ledger = False
            if self.mssql:
                ledger = bool(
                    db.execute(
                        "SELECT is_ledger_on FROM sys.databases WHERE name=DB_NAME()"
                    ).fetchone()[0]
                )
                for ddl in MSSQL_DDL:
                    name = ddl.split()[2]
                    if ledger and name == "assistant_events":
                        ddl += " WITH (LEDGER = ON (APPEND_ONLY = ON))"
                    db.execute(f"IF OBJECT_ID(N'{name}', N'U') IS NULL {ddl}")
                db.execute(
                    "IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name='ix_assistant_pending' AND object_id=OBJECT_ID(N'assistant_tasks')) CREATE INDEX ix_assistant_pending ON assistant_tasks (state, not_before, lease_until)"
                )
                db.execute(
                    "IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name='ix_assistant_case' AND object_id=OBJECT_ID(N'assistant_tasks')) CREATE INDEX ix_assistant_case ON assistant_tasks (capability, case_id)"
                )
                if ledger:
                    kind = db.execute(
                        "SELECT ledger_type_desc FROM sys.tables WHERE name=N'assistant_events'"
                    ).fetchone()[0]
                    if kind != "APPEND_ONLY_LEDGER_TABLE":
                        raise ValueError(
                            "Assistant events must be an append-only ledger table; operator schema repair required."
                        )
                else:
                    db.execute(
                        "IF OBJECT_ID(N'assistant_events_immutable', N'TR') IS NULL EXEC(N'CREATE TRIGGER assistant_events_immutable ON assistant_events INSTEAD OF UPDATE, DELETE AS THROW 50001, ''assistant evidence is append-only'', 1')"
                    )
            else:
                for ddl in SQLITE_DDL:
                    db.execute(ddl)
                for action in ("UPDATE", "DELETE"):
                    db.execute(
                        f"CREATE TRIGGER IF NOT EXISTS assistant_events_no_{action.lower()} BEFORE {action} ON assistant_events BEGIN SELECT RAISE(ABORT, 'assistant evidence is append-only'); END"
                    )
            self._upgrade(db)
            if not (self.mssql and ledger):
                for trigger in (MSSQL_ATTEMPT_TRIGGERS if self.mssql else SQLITE_ATTEMPT_TRIGGERS):
                    db.execute(trigger)
            continuity.sync_sql_gate(db, read_meta=True, mssql=self.mssql)
            try:
                from .sensor_consumer import ensure_control_home

                ensure_control_home(db, self.mssql)
            except Exception:
                # Readers fail closed on a missing or partial index; assistants keep working.
                LOG.warning(
                    "Sensor consent index could not be reconciled; retained readings stay withheld."
                )

    def _add_column(self, db, table, column, ddl):
        """Idempotently add a column to an existing table; True when it was added now."""
        if self.mssql:
            present = (
                db.execute(f"SELECT COL_LENGTH(N'{table}', N'{column}')").fetchone()[0] is not None
            )
        else:
            present = column in [r[1] for r in db.execute(f"PRAGMA table_info({table})").fetchall()]
        if not present:
            if self.mssql:
                row = db.execute("SELECT ledger_type FROM sys.tables WHERE object_id = OBJECT_ID(?)", (table,)).fetchone()
                if row and isinstance(row[0], int) and row[0] != 0:
                    sqltype, default = ddl.split(" NOT NULL DEFAULT ", 1)
                    db.execute(f"ALTER TABLE {table} ADD {column} {sqltype} NULL")
                    db.execute(f"UPDATE {table} SET {column} = {default} WHERE {column} IS NULL")
                    db.execute(f"ALTER TABLE {table} ADD CONSTRAINT ck_{table}_{column}_nn CHECK ({column} IS NOT NULL)")
                    db.execute(f"ALTER TABLE {table} ADD CONSTRAINT df_{table}_{column} DEFAULT {default} FOR {column}")
                    return True
            db.execute(f"ALTER TABLE {table} ADD {'' if self.mssql else 'COLUMN '}{column} {ddl}")
        return not present

    def _upgrade(self, db):
        """In-place upgrade of C5 schedule/task tables, keeping their rows. `dispatched` backfills from the
        recorded claim events, so legacy serviced ordering is the actual claim time; unrecorded history
        stays 0 and is never treated as approved."""
        self._add_column(
            db,
            "assistant_schedule",
            "replaced",
            "INT NOT NULL DEFAULT 0" if self.mssql else "INTEGER NOT NULL DEFAULT 0",
        )
        self._add_column(
            db,
            "assistant_schedule",
            "seen",
            "VARCHAR(64) NOT NULL DEFAULT ''" if self.mssql else "TEXT NOT NULL DEFAULT ''",
        )
        self._add_column(
            db,
            "assistant_schedule",
            "paused_at",
            "FLOAT NOT NULL DEFAULT 0" if self.mssql else "REAL NOT NULL DEFAULT 0",
        )
        gate_col_ddl = (
            "VARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL DEFAULT ''"
            if self.mssql
            else "TEXT NOT NULL DEFAULT ''"
        )
        for col in ("capability", "gate_version", "send_gate_version"):
            self._add_column(db, "assistant_attempts", col, gate_col_ddl)
        self._add_column(db, "assistant_tasks", "review_gate_version", gate_col_ddl)
        self._add_column(
            db,
            "assistant_tasks",
            "reviewed_revision",
            "BIGINT NOT NULL DEFAULT 0" if self.mssql else "INTEGER NOT NULL DEFAULT 0",
        )
        if self._add_column(
            db,
            "assistant_tasks",
            "dispatched",
            "FLOAT NOT NULL DEFAULT 0" if self.mssql else "REAL NOT NULL DEFAULT 0",
        ):
            db.execute(
                "UPDATE assistant_tasks SET dispatched=COALESCE((SELECT MAX(e.at) FROM assistant_events e"
                ' WHERE e.task_id=assistant_tasks.id AND e.body LIKE \'%"kind":"claimed"%\'),0) WHERE attempts>0'
            )
        index = "CREATE INDEX ix_assistant_dispatched ON assistant_tasks (capability, case_id, dispatched, revision)"
        if self.mssql:
            db.execute(
                f"IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name='ix_assistant_dispatched' AND object_id=OBJECT_ID(N'assistant_tasks')) {index}"
            )
        else:
            db.execute(index.replace("CREATE INDEX", "CREATE INDEX IF NOT EXISTS"))

    @contextmanager
    def transaction(self):
        with telemetry.operation("db.transaction") as observation:
            if observation.span is not None:
                observation.span.set_attribute("db.system.name", "microsoft.sql_server" if self.mssql else "sqlite")
            with self._transaction() as db:
                yield db

    @contextmanager
    def _transaction(self):
        db = self.store.assistant_connection()
        try:
            if self.mssql:
                db.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.execute("COMMIT")
        except ReleaseDenied:
            # Only release invalidation, which must outlive the denied operation, precedes this raise.
            db.execute("COMMIT")
            raise
        except BaseException:
            db.execute("ROLLBACK")
            raise
        finally:
            try:
                if self.mssql:
                    db.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")
            finally:
                db.close()

    @contextmanager
    def _read_connection(self):
        """A lock-free autocommit connection for estimates that write nothing.

        `_transaction` holds the application-wide exclusive lock, so a long read inside it blocks every other writer and the map."""
        db = self.store.assistant_connection()
        try:
            yield db
        finally:
            db.close()

    def now(self, db):
        query = (
            "SELECT DATEDIFF_BIG(MILLISECOND, CONVERT(datetime2,'1970-01-01'), SYSUTCDATETIME()) / 1000.0"
            if self.mssql
            else "SELECT (julianday('now')-2440587.5)*86400.0"
        )
        return float(db.execute(query).fetchone()[0])

    def event(self, db, tid, **body):
        if correlation := telemetry.correlation():
            body["trace_context"] = correlation
        db.execute("INSERT INTO assistant_events (id, task_id, at, body) VALUES (?,?,?,?)",
                   (uuid.uuid4().hex, tid, self.now(db), canonical(body)))

    def authorize(self, db, user, capability, case_id=None):
        if capability not in REGISTRY:
            raise ValueError("Unknown assistant.")
        if user.get("role") not in REGISTRY[capability]["roles"]:
            raise PermissionError(
                "This assistant belongs to a different role. Use the manual owner route."
            )
        if identity.is_entra(user):
            # An unbound Entra principal has no roster row, so its verified tenant/object keys are
            # the authority. A roster-bound one is re-read from its row (matched on the immutable
            # keys), so the row's scope and revocation apply to it as to any roster staff.
            current = identity.verified(user)
            if current is not None and current.get("view_only"):
                raise PermissionError("View-only access cannot use assistants.")
            bound = current.get("bound") if current else None
            if bound:
                row = db.execute(
                    "SELECT body FROM staff WHERE email=?", (str(bound.get("email")).lower(),)
                ).fetchone()
                staff = json.loads(row[0]) if row else None
                current = (
                    staff
                    if staff
                    and staff.get("oid") == user.get("oid")
                    and identity.row_tenant_ok(self.store, staff, user.get("tid"))
                    else None
                )
        else:
            row = db.execute(
                "SELECT body FROM staff WHERE email=?", (user.get("email", "").lower(),)
            ).fetchone()
            current = json.loads(row[0]) if row else None
        if (
            not current
            or current.get("role") != user.get("role")
            or current.get("disabled")
            or current.get("active") is False
            or (current.get("email", "").lower() != user.get("email", "").lower())
        ):
            raise PermissionError("Current staff role has changed or been revoked.")
        for field in ("case_ids", "areas"):
            values = current.get(field)
            if values is not None and (
                not isinstance(values, list)
                or len(values) > 1000
                or any(not isinstance(x, str) or not 1 <= len(x) <= 128 for x in values)
            ):
                raise PermissionError("Current staff scope is malformed; resolve it manually.")
        if case_id is not None:
            ids = current.get("case_ids")
            if ids is not None and case_id not in ids:
                raise PermissionError("Case is outside your current scope.")
            row = db.execute("SELECT body FROM cases WHERE id=?", (case_id,)).fetchone()
            if row is None:
                raise KeyError(case_id)
            c = json.loads(row[0])
            areas = current.get("areas")
            if areas is not None and c.get("home", {}).get("area") not in areas:
                raise PermissionError("Case area is outside your current scope.")
            return c
        return current

    def snapshot(self, db, capability, c):
        proc = {}
        if capability == "works-resident-coordination":
            row = db.execute("SELECT value FROM meta WHERE key='procurement'").fetchone()
            proc = json.loads(row[0]) if row else {}
        sensors = None
        if capability == "quality-evidence":
            sensors = sensor_view.capture_source(
                db, c["id"], sensor_view.reference_for(c.get("quality")), self.now(db), self.mssql
            )
        return capture(capability, c, proc, sensors)

    def continuity(self, db):
        """The persisted suspension state, read on the caller's own SQL connection so no process caches it."""
        row = db.execute("SELECT value FROM meta WHERE key='continuity'").fetchone()
        return continuity.load(row[0] if row else None)

    def suspended(self, db, capability):
        hold = continuity.gate_hold(db, mssql=self.mssql)
        if hold is not None:
            return continuity.reason_text(hold)
        s = self.open_suspension(db, capability)
        return continuity.reason_text(s) if s else None

    def open_suspension(self, db, capability):
        """The open suspension covering this task; the owner-directed demo override skips the hold, never the record."""
        if continuity.demo_owner_override():
            return None
        return continuity.active(
            self.continuity(db), capability, constructed=not isinstance(self.store.ai, Ai)
        )

    def admission(self, db, capability):
        """The retained denial for this task, or None when a matching release is in force. Read on the caller's connection."""
        ai = self.store.ai
        return rel.admission(
            db, capability, runtime_binding(capability, ai), self.now(db), live=isinstance(ai, Ai)
        )

    def authorize_user(self, user, capability):
        with self.transaction() as db:
            self.authorize(db, user, capability)

    def dispatch_hold(self, capability):
        """The suspension or release denial for a capability, read now on a fresh connection, or None."""
        with self.transaction() as db:
            return self.suspended(db, capability) or (self.admission(db, capability) or {}).get(
                "reason"
            )

    def release_reference(self, db, capability):
        def read():
            selected, _ = rel.assessment(
                db,
                capability,
                runtime_binding(capability, self.store.ai),
                self.now(db),
                live=isinstance(self.store.ai, Ai),
            )
            return rai_release.reference(selected) if selected else None

        # The forecast's view is one frozen read, so the answer is the same for every case (issue #2304).
        return db.once(("release_reference", capability), read) if isinstance(db, ForecastReads) else read()

    def record_release(self, user, body):
        from . import rai_control_plane

        live_intent = rai_control_plane.is_live_release_intent(body)
        try:
            if not self.sql:
                if live_intent:
                    task_candidate = body.get("task") if isinstance(body, dict) else None
                    check = rai_control_plane.validate_live_task_approval(
                        task_candidate,
                        body if isinstance(body, dict) else None,
                    )
                    if not check["valid"]:
                        raise rai_control_plane.LiveActivationApprovalError(
                            check["task_id"],
                            check["reasons"],
                        )
                raise ValueError(self.disabled())
            with self.transaction() as db:
                self.authorize(db, user, "funding-evidence")
                from .ai_registry import LEGACY

                rid = rel.record(
                    db,
                    self.now(db),
                    user,
                    body,
                    self.approvers,
                    set(REGISTRY) | {f"legacy:{t}" for t in LEGACY},
                )
        except (PermissionError, ValueError) as exc:
            if live_intent:
                task_candidate = body.get("task") if isinstance(body, dict) else None
                reasons = (
                    list(exc.reasons)
                    if isinstance(exc, rai_control_plane.LiveActivationApprovalError)
                    else [str(exc)]
                )
                rai_control_plane.emit_live_activation_rejection_audit(
                    self.store,
                    actor=user,
                    task_id=task_candidate,
                    reasons=reasons,
                    assistants_service=self,
                )
            raise
        return dict(
            id=rid,
            status="active",
            note="Permits bounded proposals only; no approval, domain write or live-use authority.",
        )

    def change_release(self, user, rid, status, reason):
        if not self.sql:
            raise ValueError(self.disabled())
        with self.transaction() as db:
            self.authorize(db, user, "funding-evidence")
            recovery.record_release_change(self.store, db, rid, status)
            rel.change(db, self.now(db), user, rid, status, reason)
        return dict(id=rid, status=status)

    def affected(self, scope, limit=500):
        """Queued, leased and ready proposals a suspension of this scope covers; `.truncated` says whether the limit cut the list."""
        if not self.sql:
            return Affected()
        with self.transaction() as db:
            rows = db.execute(
                "SELECT id,capability,state,body FROM assistant_tasks WHERE state IN ('pending','leased','ready') ORDER BY id"
            ).fetchall()
        found = [
            dict(id=i, task=c, version=json.loads(b).get("version"), state=s)
            for i, c, s, b in rows
            if scope in (continuity.ALL, c)
        ]
        return Affected(found[:limit], total=len(found))

    def export(self, limit=5000, release_limit=5000, event_limit=5000):
        """Proposals with append-only provenance for the supplier-independent export, and whether the limit cut them off."""
        if self.schema_error:
            return dict(
                proposals=[],
                total=None,
                truncated=True,
                supported=True,
                source_status="unavailable",
                note=self.schema_error,
            )
        if not self.sql:
            return dict(
                proposals=[],
                total=0,
                truncated=False,
                supported=False,
                source_status="unsupported",
                note="Assistant proposals are durable SQL only; this JSON store holds none, so none are exported.",
            )
        with self.transaction() as db:
            ids = [
                r[0] for r in db.execute("SELECT id FROM assistant_tasks ORDER BY id").fetchall()
            ]
            out = []
            for tid in ids[:limit]:
                body = self._row(db, tid)
                events = [
                    json.loads(r[0])
                    for r in db.execute(
                        "SELECT body FROM assistant_events WHERE task_id=? ORDER BY at,id", (tid,)
                    ).fetchall()
                ]
                capability = continuity.record_task(body)
                s = continuity.gate_hold(db, mssql=self.mssql) or self.open_suspension(
                    db, capability
                )
                current = continuity.epoch_current(body, self.continuity(db))
                row = db.execute("SELECT body FROM cases WHERE id=?", (body["case_id"],)).fetchone()
                stale = (
                    capability not in REGISTRY
                    or row is None
                    or signature(self.snapshot(db, capability, json.loads(row[0])))
                    != body["source_signature"]
                )
                actionable = (
                    current
                    and not stale
                    and body["state"] in ("ready", "accepted")
                    and not s
                    and not self.admission(db, capability)
                    and body.get("release") == self.release_reference(db, capability)
                )
                if self._withhold_sensors(db, body):
                    events = self._scrub_events(events)
                out.append(
                    dict(
                        body,
                        provenance=events,
                        epoch_current=current,
                        stale=stale,
                        actionable=bool(actionable),
                        relied_on=bool(actionable and body["state"] == "accepted"),
                        suspension=s["id"] if s else None,
                    )
                )
            releases = []
            rows = db.execute(
                "SELECT id,capability,status,body,revision FROM assistant_releases ORDER BY id"
            ).fetchall()
            for rid, cap, status, raw, revision in rows[:release_limit]:
                events = db.execute(
                    "SELECT id,at,body FROM assistant_events WHERE task_id=? ORDER BY at,id", (rid,)
                ).fetchall()
                releases.append(
                    dict(
                        id=rid,
                        task=cap,
                        current_status=status,
                        revision=revision,
                        snapshot=dict(json.loads(raw), id=rid, status="active"),
                        events=[
                            dict(id=eid, release_id=rid, at=at, body=json.loads(body))
                            for eid, at, body in events[:event_limit]
                        ],
                        event_total=len(events),
                        truncated=len(events) > event_limit,
                    )
                )
            return dict(
                proposals=out,
                total=len(ids),
                truncated=len(ids) > limit,
                supported=True,
                source_status="available",
                limit=limit,
                epoch=self.continuity(db)["epoch"],
                task_releases=dict(
                    supported=True,
                    records=releases,
                    total=len(rows),
                    exported=len(releases),
                    truncated=len(rows) > release_limit,
                ),
            )

    def disabled(self, db=None, capability=None, capacity=True):
        """The reason new work is refused, or None. With capacity=False only the authority conditions that can
        end an already admitted call are checked (not the room for a further reservation)."""
        l = self.limits
        if self.schema_error:
            return self.schema_error
        if not self.sql:
            return "Durable SQL is required; use the ordinary case/manual route."
        if not l.valid:
            return l.error
        if db is not None and (
            held := self.suspended(db, continuity.ALL if capability is None else capability)
        ):
            return held
        if db is not None and capability and (denied := self.admission(db, capability)):
            return denied["reason"]
        if db is not None and self.now(db) >= l.expiry:
            return "Operator authority/allowance has expired."
        if not self.store.ai.configured:
            return "AI is not configured; use the manual owner route."
        if db is not None:
            pool = self._pool(db)
            if pool and (
                pool[2] <= self.now(db)
                or capacity
                and (
                    pool[3] >= min(pool[0], l.calls)
                    or pool[4] + l.reservation > min(pool[1], l.tokens)
                )
            ):
                return "Shared durable allowance exhausted/expired; use the manual owner route."
        return None

    def registry(self, user):
        from . import rai_control_plane

        if user.get("role") not in projection.STAFF_ROLES:
            raise PermissionError("Staff assistance only.")
        if not self.sql:
            readiness = rai_control_plane.exercise_acceptance_report(
                self.store,
                user=user,
                assistants_service=self,
            )
            return dict(
                assistants=[
                    dict(id=k, version=VERSION, model_bounds=model_bounds(), **v)
                    for k, v in REGISTRY.items()
                    if user.get("role") in v["roles"]
                ],
                disabled=self.disabled(),
                proactive=False,
                quality_scope=self.quality_scope(),
                manual="Use the ordinary case controls.",
                **readiness,
            )
        with self.transaction() as db:
            from . import ai_registry

            result = []
            for k, v in REGISTRY.items():
                if user.get("role") in v["roles"]:
                    self.authorize(db, user, k)
                    denied = self.admission(db, k)
                    result.append(
                        dict(
                            id=k,
                            version=VERSION,
                            release="in force" if not denied else denied,
                            binding=runtime_binding(k, self.store.ai),
                            model_bounds=model_bounds(self.limits),
                            **v,
                        )
                    )
            registered = []
            for task, spec in ai_registry.tasks().items():
                if user.get("role") not in spec["roles"]:
                    continue
                if spec.get("enabled") is False:
                    registered.append(
                        dict(
                            spec,
                            binding=None,
                            release_denial=dict(
                                missing=[
                                    "Task is disabled and has no runtime binding or release evidence."
                                ]
                            ),
                            release=None,
                            authority_gap=rai_release.AUTHORITY_GAP,
                            status=monitoring_coverage.disabled_task_status(spec),
                            monitoring_status=monitoring_coverage.check_monitoring_declaration(
                                spec.get("monitoring_declaration"),
                                task_enabled=False,
                                live=False,
                            ),
                        )
                    )
                    continue
                if task in REGISTRY:
                    live = isinstance(self.store.ai, Ai)
                    binding = runtime_binding(task, self.store.ai)
                    selected, denied = rel.assessment(
                        db, task, binding, self.now(db), live=live
                    )
                else:
                    live = True
                    dep = (
                        getattr(self.store.ai, "fast", "")
                        if task in ("message", "summary", "briefing")
                        else getattr(self.store.ai, "strong", "")
                    )
                    binding = ai_registry.legacy_binding(task, self.store.ai, dep)
                    selected, denied = rel.assessment(
                        db, f"legacy:{task}", binding, self.now(db), live=live
                    )
                active_decl = (selected or spec).get("monitoring_declaration")
                registered.append(
                    dict(
                        spec,
                        binding=binding,
                        release_denial=denied,
                        release=rai_release.reference(selected) if selected else None,
                        authority_gap=rai_release.AUTHORITY_GAP,
                        monitoring_status=monitoring_coverage.check_monitoring_declaration(
                            active_decl,
                            task_enabled=True,
                            live=live,
                        ),
                    )
                )
            payload = dict(
                assistants=result,
                registered_tasks=registered,
                disabled=self.disabled(db),
                proactive=self.limits.proactive,
                quality_scope=self.quality_scope(),
                principal=PURPOSE,
                rule=RULE_VERSION,
                limits=Limits.DEFAULTS
                if not self.limits.valid
                else {k: getattr(self.limits, k) for k in Limits.DEFAULTS},
                manual="Use the ordinary case controls; proposals never approve or change the case.",
            )
        # The report verifies the audit ledger under the store lock, which a writer holds while it waits for the
        # SQLite write lock this transaction held; reading on its own connection after commit avoids that deadlock.
        payload.update(
            rai_control_plane.exercise_acceptance_report(
                self.store,
                user=user,
                assistants_service=self,
            )
        )
        return payload

    def _task_id(self, db, capability, c, signature):
        return digest(
            [
                capability,
                VERSION,
                c["id"],
                signature,
                proposal_identity(capability),
                self.release_reference(db, capability),
                self.continuity(db)["epoch"],
            ]
        )

    def quality_scope_denial(self, capability, case_id, requested=True):
        """The reason Quality may not work on this case under the demo scope, or None.

        Unset scope allows everything; a configured scope allows only the five homes and only on a person's request."""
        l = self.limits
        if capability != "quality-evidence":
            return None
        if l.quality_scope_error or (
            l.quality_homes is not None and (case_id not in l.quality_homes or not requested)
        ):
            return "Quality analysis is limited to the configured five-home demo set and a person's request; use the manual route."
        return None

    def quality_scope(self):
        """The effective Quality scope for operator evidence; reads configuration only and never calls a model."""
        l = self.limits
        if l.quality_scope_error:
            mode, homes = "invalid-refused", []
        elif l.quality_homes is None:
            mode, homes = "unrestricted", []
        else:
            mode, homes = "demo-homes", list(l.quality_homes)
        scoped = mode != "unrestricted"
        return dict(
            mode=mode,
            homes=homes,
            trigger="operator-requested-only" if scoped else "any",
            background_scan="skips-quality" if scoped else "includes-quality",
            per_reading_calls="none",
            model_call_authority_present=bool(l.authority) and l.valid,
        )

    def _enqueue(self, db, capability, c, mode, actor, replaced=None):
        with telemetry.operation("messaging.publish", backend="other_sql"):
            return self._enqueue_task(db, capability, c, mode, actor, replaced)

    def _enqueue_task(self, db, capability, c, mode, actor, replaced=None):
        if denial := self.quality_scope_denial(capability, c["id"], mode != "proactive"):
            raise ValueError(denial)
        snapshot = self.snapshot(db, capability, c)
        signature_ = signature(snapshot)
        identity = proposal_identity(capability)
        release = self.release_reference(db, capability)
        epoch = self.continuity(db)["epoch"]
        tid = self._task_id(db, capability, c, signature_)
        row = db.execute("SELECT body FROM assistant_tasks WHERE id=?", (tid,)).fetchone()
        if row is None:
            reason = self.disabled(db, capability)
            body = dict(id=tid, capability=capability, version=VERSION, case_id=c["id"], proposal_identity=identity,
                        source_signature=signature_, snapshot=snapshot, output=None, verification=None, review=None, envelope=None,
                        manual=f"Review the ordinary case with {', '.join(REGISTRY[capability]['roles'])}.",
                        release=release, reason=reason, continuity_epoch=epoch, created_at=self.now(db),
                        manual_requested=mode != "proactive")
            if traceparent := telemetry.carrier():
                body["traceparent"] = traceparent
            state = "disabled" if reason else "pending"
            if self.limits.valid and len(canonical(snapshot)) > self.limits.input_chars - 1500:
                state, body["reason"] = (
                    "failed",
                    "Source capture exceeds bounded input. Review manually.",
                )
            db.execute(
                "INSERT INTO assistant_tasks (id,capability,case_id,signature,body,state,fence,owner,lease_until,attempts,not_before,revision) VALUES (?,?,?,?,?,?,0,'',0,0,0,1)",
                (tid, capability, c["id"], scheduling_signature(snapshot), canonical(body), state),
            )
        elif not self.disabled(db, capability):
            task = self._row(db, tid)
            # The exact evidence is current again, so a never-dispatched stale or disabled task is runnable work.
            if task["state"] in ("disabled", "stale") and task["attempts"] < self.limits.attempts:
                was = task["state"]
                task["reason"] = None
                db.execute(
                    "UPDATE assistant_tasks SET state='pending',body=?,revision=revision+1 WHERE id=?",
                    (canonical(task), tid),
                )
                if was == "stale":
                    self.event(
                        db,
                        tid,
                        kind="requeued",
                        reason="The exact source evidence is current again.",
                    )
        # A person's request for another exact capture never rewrites the autonomous Quality slot: the proactive
        # call for this schedule was already made, and a later reading must not make a second one.
        if mode == "proactive" or not self._serviced_proactive_slot(db, capability, c["id"]):
            self._occupy(
                db,
                capability,
                c["id"],
                scheduling_signature(snapshot),
                tid,
                replaced,
                touch=mode == "proactive",
                seen=signature_ if mode == "proactive" else None,
            )
        if row is not None and mode != "proactive":
            self._mark_requested(db, tid)
        denied = self.admission(db, capability)
        self.event(
            db,
            tid,
            kind="invocation",
            mode=mode,
            actor=actor,
            purpose=PURPOSE if mode == "proactive" else None,
            rules=RULE_VERSION,
            release=release,
            release_denial=denied,
        )
        return tid

    def _serviced_proactive_slot(self, db, capability, case_id):
        """True when a Quality slot of the current scope is held by a task the assistant already dispatched on its own."""
        if capability != "quality-evidence":
            return False
        slot = db.execute(
            "SELECT scope,task_id FROM assistant_schedule WHERE capability=? AND case_id=?",
            (capability, case_id),
        ).fetchone()
        if slot is None or slot[0] != self._scope(db, capability):
            return False
        held = db.execute(
            "SELECT attempts,body FROM assistant_tasks WHERE id=?", (slot[1],)
        ).fetchone()
        return (
            held is not None
            and held[0] > 0
            and (json.loads(held[1]).get("dispatch") or {}).get("trigger") == "proactive"
        )

    def _mark_requested(self, db, tid):
        """A person's request is durable on the task, so attribution never depends on an event window.
        It governs the next claim only; an executing or returned dispatch keeps the trigger frozen at its claim."""
        task = self._row(db, tid)
        if task["state"] not in ("pending", "leased", "disabled"):
            return
        task["manual_requested"] = True
        db.execute(
            "UPDATE assistant_tasks SET body=?,revision=revision+1 WHERE id=?",
            (canonical(task), tid),
        )

    def invoke(self, user, capability, case_id):
        if not isinstance(case_id, str) or not 1 <= len(case_id) <= 64:
            raise ValueError("Choose a bounded case ID.")
        if not self.sql:
            raise ValueError(self.disabled())
        with self.transaction() as db:
            c = self.authorize(db, user, capability, case_id)
            tid = self._enqueue(db, capability, c, "reactive", user["email"])
        return self.detail(user, tid)

    def _row(self, db, tid):
        row = db.execute(
            "SELECT body,state,fence,owner,lease_until,attempts,not_before,revision FROM assistant_tasks WHERE id=?",
            (tid,),
        ).fetchone()
        if row is None:
            raise KeyError(tid)
        body = json.loads(row[0])
        body.update(
            state=row[1],
            fence=row[2],
            owner=row[3],
            lease_until=row[4],
            attempts=row[5],
            not_before=row[6],
            revision=row[7],
        )
        return body

    def _view(self, db, user, tid, history_offset=0):
        body = self._row(db, tid)
        c = self.authorize(db, user, body["capability"], body["case_id"])
        viewer = self.authorize(db, user, body["capability"])
        current = self.snapshot(db, body["capability"], c)
        source_stale = signature(current) != body["source_signature"]
        challenged_stale = bool(body.get("challenged_stale"))
        body["stale"] = source_stale or challenged_stale
        newer = (
            source_stale
            and not challenged_stale
            and scheduling_signature(current) == scheduling_signature(body["snapshot"])
        )
        history_limit = 50
        query = "SELECT body FROM assistant_events WHERE task_id=? ORDER BY at DESC,id DESC"
        query += " OFFSET ? ROWS FETCH NEXT ? ROWS ONLY" if self.mssql else " LIMIT ? OFFSET ?"
        args = (
            (tid, history_offset, history_limit)
            if self.mssql
            else (tid, history_limit, history_offset)
        )
        body["provenance"] = list(
            reversed([json.loads(r[0]) for r in db.execute(query, args).fetchall()])
        )
        total = db.execute(
            "SELECT COUNT(*) FROM assistant_events WHERE task_id=?", (tid,)
        ).fetchone()[0]
        body["history_next_offset"] = (
            history_offset + history_limit if total > history_offset + history_limit else None
        )
        body["history_count"] = total
        body["display_state"] = "stale" if body["stale"] else body["state"]
        held = continuity.gate_hold(db, mssql=self.mssql) or self.open_suspension(
            db, body["capability"]
        )
        body["epoch_current"] = continuity.epoch_current(body, self.continuity(db))
        body["release_denial"] = self.admission(db, body["capability"])
        if not body["release_denial"] and body.get("release") != self.release_reference(
            db, body["capability"]
        ):
            body["release_denial"] = rel.denial(
                "activation release changed", ["original activation release"], body["capability"]
            )
        body["actionable"] = (
            body["epoch_current"]
            and not body["stale"]
            and held is None
            and body["state"] in ("ready", "accepted")
            and not body["release_denial"]
        )
        body["relied_on"] = body["actionable"] and body["state"] == "accepted"
        body["suspension"] = held["id"] if held else None
        if held:
            body["display_state"] = "suspended"
        elif body["release_denial"]:
            body["display_state"] = "release-denied"
        elif not body["epoch_current"]:
            body["display_state"] = "epoch-stale"
        raw_challenges = body.get("challenges")
        if isinstance(raw_challenges, list) and raw_challenges:
            flagged = any(r.get("hazard_referral") is not None for r in raw_challenges)
            routed = any(
                (r.get("hazard_referral") or {}).get("routed_hazard_index") is not None
                for r in raw_challenges
            )
            body["hazard_clock_preserved"] = True
            body["non_retaliation_assurance"] = challenges.build_non_retaliation_assurance(
                hazard_concern=flagged, independent_hazard_routed=routed
            )
            if not projection.appointment_evidence_visible(viewer):
                body.pop("challenges", None)
                body["provenance"] = [
                    dict(ev, note=projection.NOTE_HELD)
                    if ev.get("kind") == "challenge" and ev.get("note")
                    else ev
                    for ev in body["provenance"]
                ]
        withheld = self._withhold_sensors(db, body)
        if withheld:
            body["provenance"] = self._scrub_events(body["provenance"])
        role_withheld = tuple(
            dict.fromkeys(
                list(
                    projection.withheld_case_values(c, projection.project_case_visibility(user, c))
                )
                + list(projection.withheld_scope_values(self.store, user, [body["case_id"]]))
            )
        )
        reason_ok = projection.can_see_reason(user)
        if body.get("output") and _output_violates_visibility(
            body["output"], role_withheld, guard_telemetry=self.guard_telemetry
        ):
            body["output"] = dict(ROLE_WITHHELD_OUTPUT)
            body["role_withheld"] = True
            body["actionable"] = False
            body["relied_on"] = False
        if not withheld and not reason_ok:
            for key in ("verification", "review"):
                if (body.get(key) or {}).get("note"):
                    body[key] = dict(body[key], note=projection.NOTE_HELD)
        if not withheld and (not reason_ok or role_withheld):
            scrubbed_events = []
            for e in body["provenance"]:
                ev = dict(e)
                if not reason_ok and ev.get("note"):
                    ev["note"] = projection.NOTE_HELD
                for okey in ("output", "edited_output"):
                    if ev.get(okey) and _output_violates_visibility(
                        ev[okey], role_withheld, guard_telemetry=self.guard_telemetry
                    ):
                        ev[okey] = dict(ROLE_WITHHELD_OUTPUT)
                scrubbed_events.append(ev)
            body["provenance"] = scrubbed_events
        keeps = (
            newer
            and (body.get("dispatch") or {}).get("trigger") == "proactive"
            and body["epoch_current"]
            and held is None
            and body["state"] == "ready"
            and not body["release_denial"]
        )
        live_conflicts = bool(
            (((current or {}).get("sources") or {}).get("sensors") or {}).get(
                "conflicting_readings"
            )
        )
        conflict_current = (
            source_stale
            and not challenged_stale
            and live_conflicts
            and _sensor_bucket_key(current) == _sensor_bucket_key(body["snapshot"])
            and body["epoch_current"]
            and held is None
            and body["state"] == "ready"
            and not body["release_denial"]
        )
        body["review_flag"] = review_flag(
            body,
            body["provenance"],
            body["actionable"] or keeps or conflict_current,
            withheld,
            newer_readings=newer,
            current=current,
        )
        return body

    @staticmethod
    def _captured_sensors(body):
        sensors = (body.get("snapshot") or {}).get("sources", {}).get("sensors")
        return body.get("capability") == "quality-evidence" and bool(
            sensor_view.citations(sensors or {})
        )

    def _sensors_granted(self, db, body):
        """True when the captured readings may still be shown or sent: none captured, or consent is granted now."""
        sensors = (body.get("snapshot") or {}).get("sources", {}).get("sensors")
        captured = sensor_view.citations(sensors or {})
        if body.get("capability") != "quality-evidence" or not captured:
            return True
        ids = {r["sensor_id"] for r in captured.values()}
        try:
            return sensor_view.consent(db, body["case_id"], ids, self.mssql) == "granted"
        except Exception:
            return False

    def _withhold_sensors(self, db, body):
        """Current-consent projection: stored records stay, but values, citations and derived text are not disclosed."""
        if self._sensors_granted(db, body):
            return False
        note = "Monitoring consent is not granted now; retained readings are withheld."
        stub = dict(
            state="consent-withheld",
            detail=note,
            readings=[],
            before=[],
            after=[],
            latest=None,
            citation_keys=[],
        )
        body["snapshot"] = dict(
            body["snapshot"],
            sources=dict(body["snapshot"]["sources"], sensors=stub),
            citations={
                k: v
                for k, v in body["snapshot"]["citations"].items()
                if not k.startswith("sensor:")
            },
        )
        if body.get("output"):
            body["output"] = dict(WITHHELD_OUTPUT)
        for key in ("verification", "review"):
            if (body.get(key) or {}).get("note"):
                body[key] = dict(body[key], note=WITHHELD_NOTE)
        if isinstance(body.get("challenges"), list):
            scrubbed = []
            for rec in body["challenges"]:
                item = deepcopy(rec)
                for field in ("request", "explanation"):
                    if item.get(field):
                        item[field] = WITHHELD_NOTE
                if isinstance(item.get("resolution"), dict) and item["resolution"].get("explanation"):
                    item["resolution"] = dict(item["resolution"], explanation=WITHHELD_NOTE)
                if isinstance(item.get("updates"), list):
                    item["updates"] = [
                        dict(u, detail=WITHHELD_NOTE) if u.get("detail") else u
                        for u in item["updates"]
                    ]
                if isinstance(item.get("previous_resolutions"), list):
                    item["previous_resolutions"] = [
                        dict(pr, explanation=WITHHELD_NOTE) if pr.get("explanation") else pr
                        for pr in item["previous_resolutions"]
                    ]
                scrubbed.append(item)
            body["challenges"] = scrubbed
        body["sensor_withheld"] = True
        return True

    @staticmethod
    def _scrub_events(events):
        """The model and any editor saw the withheld capture, so every output-bearing event field is withheld."""
        return [
            dict(
                e,
                **{k: dict(WITHHELD_OUTPUT) for k in ("output", "edited_output") if e.get(k)},
                **({"note": WITHHELD_NOTE} if e.get("note") else {}),
            )
            for e in events
        ]

    def sensors(self, user, case_id):
        """Bounded retained indoor readings for one authorised case; the same source the quality snapshot captures."""
        if not isinstance(case_id, str) or not 1 <= len(case_id) <= 64:
            raise ValueError("Choose a bounded case ID.")
        if not self.sql:
            raise ValueError(self.disabled())
        with self._read_connection() as db:
            c = self.authorize(db, user, "quality-evidence", case_id)
            out = sensor_view.view(
                db, case_id, sensor_view.reference_for(c.get("quality")), self.now(db), self.mssql
            )
        return dict(out, case_id=case_id)

    def map_sensors(self, user, case_ids):
        """Latest bounded sensor summary per mapped home, projected for this user's role and scope.

        A role outside quality evidence, or a case outside the current staff scope, gets a fixed
        state with no values. Without SQL no readings exist, so the state says so."""
        ids = [i for i in case_ids if isinstance(i, str) and 1 <= len(i) <= 64]
        if user.get("role") not in REGISTRY["quality-evidence"]["roles"]:
            return {i: sensor_map.fixed("restricted") for i in ids}
        if not self.sql:
            return {i: sensor_map.fixed("not-connected") for i in ids}
        out = {}
        try:
            with self._read_connection() as db:
                now = self.now(db)
                allowed = []
                for i in ids[: sensor_map.HOME_CAP]:
                    try:
                        self.authorize(db, user, "quality-evidence", i)
                        allowed.append(i)
                    except (PermissionError, KeyError):
                        out[i] = sensor_map.fixed("restricted")
                out.update(sensor_map.summaries(db, allowed, now, self.mssql))
        except Exception as exc:
            # The sensor overlay is optional: a database failure here must not fail the whole map (issue 2257).
            cause = "sql-write-lock-busy" if is_write_lock_busy(exc) else "other"
            state = driver_sqlstate(exc)
            LOG.warning(
                "map sensor summary unavailable exc=%s cause=%s sqlstate=%s",
                type(exc).__name__,
                cause,
                state or "none",
            )
            out = {i: sensor_map.fixed("unavailable") for i in ids[: sensor_map.HOME_CAP]}
        out.update({i: sensor_map.fixed("not-loaded") for i in ids[sensor_map.HOME_CAP :]})
        return out

    def detail(self, user, tid, history_offset=0):
        if not self.sql:
            raise ValueError(self.disabled())
        if type(history_offset) is not int or not 0 <= history_offset <= 1000000:
            raise ValueError("Invalid bounded history offset.")
        with self.transaction() as db:
            return self._view(db, user, tid, history_offset)

    def listing(self, user, case_id=None, after=""):
        if case_id is not None and (not isinstance(case_id, str) or not 1 <= len(case_id) <= 64):
            raise ValueError("Choose a bounded case ID.")
        if not isinstance(after, str) or (
            after and (len(after) != 64 or any(c not in "0123456789abcdef" for c in after))
        ):
            raise ValueError("Invalid proposal cursor.")
        if user.get("role") not in projection.STAFF_ROLES:
            raise PermissionError("Staff assistance only.")
        if not self.sql:
            return dict(proposals=[], disabled=self.disabled())
        with self.transaction() as db:
            permitted = [k for k, v in REGISTRY.items() if user.get("role") in v["roles"]]
            current = None
            for cap in permitted:
                current = self.authorize(db, user, cap)
            if not permitted:
                return dict(proposals=[], disabled="No assistant belongs to this role.")
            where = "WHERE capability IN (" + ",".join("?" for _ in permitted) + ")"
            args = tuple(permitted)
            if case_id:
                where += " AND case_id=?"
                args += (case_id,)
            for field in ("case_ids", "areas"):
                values = current.get(field)
                if values is not None:
                    if not values:
                        return dict(proposals=[], disabled=self.disabled(db), next_after=None)
                    if field == "case_ids":
                        where += " AND case_id IN (" + ",".join("?" for _ in values) + ")"
                    else:
                        where += (
                            " AND case_id IN (SELECT id FROM cases WHERE area IN ("
                            + ",".join("?" for _ in values)
                            + "))"
                        )
                    args += tuple(values)
            if after:
                where += " AND id>?"
                args += (after,)
            query = f"SELECT id,capability FROM assistant_tasks {where} ORDER BY id"
            if self.mssql:
                query += " OFFSET 0 ROWS FETCH NEXT 50 ROWS ONLY"
            else:
                query += " LIMIT 50"
            results = []
            rows = db.execute(query, args).fetchall()
            for tid, cap in rows:
                if cap in permitted:
                    try:
                        results.append(self._view(db, user, tid))
                    except PermissionError:
                        continue
            return dict(
                proposals=results,
                disabled=self.disabled(db),
                manual="Open the case for ordinary human work.",
                next_after=rows[-1][0] if len(rows) == 50 else None,
            )

    def rai_metrics(self, user, window_start, window_end, replay=None):
        """RAI metric counts rebuilt from the persisted audit events, so a restart needs no in-memory state.

        Persisted event ids are the prior ids of the window; a replayed telemetry batch is deduplicated
        against them. Content-free: counts and opaque event ids only."""
        if user.get("role") not in {r for v in REGISTRY.values() for r in v["roles"]}:
            raise PermissionError("Staff assistance only.")
        if not self.sql:
            raise ValueError(self.disabled())
        bounds = rai_metrics.parse_window(window_start, window_end)
        if bounds is None:
            return rai_metrics.reconstruct([], window_start=window_start, window_end=window_end)
        with self.transaction() as db:
            rows = db.execute(
                "SELECT id,task_id,at,body FROM assistant_events WHERE at>=? AND at<? ORDER BY at,id",
                (bounds[0].timestamp(), bounds[1].timestamp()),
            ).fetchall()
        persisted = [
            dict(
                json.loads(body),
                event_id=eid,
                task_id=tid,
                observed_at=datetime.fromtimestamp(at, timezone.utc).isoformat(),
            )
            for eid, tid, at, body in rows
        ]
        return rai_metrics.reconstruct(
            persisted, window_start=window_start, window_end=window_end, replay=replay
        )

    FORECAST_BUDGET_SECONDS = 120.0  # cap on the background computation
    FORECAST_WAIT_SECONDS = 8.0  # longest a request waits, connection time included
    FORECAST_STALE_SECONDS = 900.0  # oldest last-good answer served when a fresh one is late

    def forecast(self, user, period_seconds=86400):
        """Read-only per-period call forecast for each proactive predicate; enqueues nothing and holds no case content.

        The computation runs in a background job that is not cut off when this request stops waiting. A request waits at
        most FORECAST_WAIT_SECONDS (connection time included): a quiet system answers with fresh figures; a slow one
        answers with the last good figures marked `stale_seconds` for up to FORECAST_STALE_SECONDS; with none to show it
        raises ForecastTimeout, and the job keeps running so the retry is answered from its result."""
        started = time.monotonic()
        if not isinstance(period_seconds, int) or not 60 <= period_seconds <= 2592000:
            raise ValueError("Choose a period between 60 seconds and 30 days.")
        if not self.sql:
            raise ValueError(self.disabled())
        if user.get("role") not in {r for v in REGISTRY.values() for r in v["roles"]}:
            raise PermissionError("Staff assistance only.")
        key = (
            str(user.get("email", "")).lower(),
            user.get("role"),
            user.get("oid"),
            user.get("tid"),
            period_seconds,
        )
        with self._forecast_lock:
            job = self._forecast_jobs.get(key)
            if job is None or job.done.is_set():
                job = self._forecast_jobs[key] = _ForecastJob()
                threading.Thread(
                    target=self._forecast_job, args=(key, job, dict(user), period_seconds), daemon=True
                ).start()
        remaining = max(0.0, self.FORECAST_WAIT_SECONDS - (time.monotonic() - started))
        finished = job.done.wait(remaining)
        if finished and job.error is None:
            return deepcopy(job.result)
        if finished and not isinstance(job.error, ForecastTimeout):
            raise job.error
        with self._forecast_lock:
            cached = self._forecasts.get(key)
        if cached and time.monotonic() - cached[0] <= self.FORECAST_STALE_SECONDS:
            return {**deepcopy(cached[1]), "stale_seconds": int(time.monotonic() - cached[0])}
        raise ForecastTimeout("The forecast is still being prepared.")

    def _forecast_job(self, key, job, user, period_seconds):
        try:
            job.result = self._forecast_compute(user, period_seconds)
            with self._forecast_lock:
                self._forecasts[key] = (time.monotonic(), job.result)
        except BaseException as exc:
            job.error = exc
        finally:
            job.done.set()

    def _forecast_compute(self, user, period_seconds):
        if not isinstance(period_seconds, int) or not 60 <= period_seconds <= 2592000:
            raise ValueError("Choose a period between 60 seconds and 30 days.")
        if not self.sql:
            raise ValueError(self.disabled())
        if self.limits.scan_interval <= 0:
            raise ValueError(
                "The scan interval must be greater than zero seconds, so no forecast can be given. Set a valid interval or continue ordinary case work manually."
            )
        bounds = model_bounds(self.limits)
        cycles = period_seconds // self.limits.scan_interval
        with self._read_connection() as raw, rel.read_only():
            db = ForecastReads(raw, self.mssql, self.FORECAST_BUDGET_SECONDS)
            allowed = [k for k, v in REGISTRY.items() if user.get("role") in v["roles"]]
            if not allowed:
                raise PermissionError("Staff assistance only.")
            current = {cap: self.authorize(db, user, cap) for cap in allowed}
            today = datetime.fromtimestamp(self.now(db), timezone.utc).date().isoformat()
            rows = db.execute("SELECT id,body FROM cases WHERE closed=0 ORDER BY id").fetchall()
            cases = [json.loads(raw) for _, raw in rows]
            result = []
            for cap in allowed:
                staff = current[cap]
                ids, areas = staff.get("case_ids"), staff.get("areas")
                scoped = [
                    c
                    for c in cases
                    if (ids is None or c["id"] in ids)
                    and (areas is None or c.get("home", {}).get("area") in areas)
                ]
                held = self.suspended(db, cap)
                eligible_now = new = 0
                snapshots = []
                for c in scoped:
                    db.check()
                    snapshots.append((c, self.snapshot(db, cap, c)))
                db.load_tasks(
                    db.slot_task_ids()
                    | {self._task_id(db, cap, c, signature(s)) for c, s in snapshots}
                )
                db.prefetch_adoptions(
                    [c["id"] for c, _ in snapshots if not db.has_slot(cap, c["id"])],
                    self.ADOPT_ROWS * self.ADOPT_PAGES,
                )
                for c, s in snapshots:
                    if self._due(db, cap, c, s, today, observe=False):
                        eligible_now += 1
                        found = db.execute(
                            "SELECT state,attempts FROM assistant_tasks WHERE id=?",
                            (self._task_id(db, cap, c, signature(s)),),
                        ).fetchone()
                        if found is None or (
                            found[0] == "stale" and found[1] < self.limits.attempts
                        ):
                            new += 1
                result.append(
                    dict(
                        id=cap,
                        rule=RULES[cap],
                        open_cases_in_scope=len(scoped),
                        eligible_cases=eligible_now,
                        new_proposals=new,
                        max_calls_per_request=bounds["max_calls_per_request"],
                        max_calls_this_period=new * bounds["max_calls_per_request"],
                        held=held,
                    )
                )
        reach = self.limits.scan_size * cycles
        return dict(
            period_seconds=period_seconds,
            proactive=self.limits.proactive,
            rule=RULE_VERSION,
            scan_interval=self.limits.scan_interval,
            scan_size=self.limits.scan_size,
            cases_reachable_per_period=reach,
            call_allowance=self.limits.calls if self.limits.valid else 0,
            assistants=result,
            max_calls_this_period=sum(r["max_calls_this_period"] for r in result),
            cost="Unknown: no price source is set (BRD OD-51).",
            basis="Upper bound from current case state; routine case edits can add proposals later. Read-only.",
            manual="Proactive scans stay off unless an operator enables them; use the ordinary case controls.",
        )

    def _scope(self, db, cap):
        return digest([self.release_reference(db, cap), self.continuity(db)["epoch"]])

    def _occupy(self, db, cap, case_id, coarse, tid, replaced=None, touch=True, seen=None):
        """Record the task that holds this case's proactive schedule slot; one row per (assistant, case).
        `replaced` counts consecutive replacements without a dispatch; it is kept within one schedule and
        reset when the schedule changes, when a proactive dispatch happens, or by `_due` when the evidence
        stayed unchanged for a quiet interval or the pause reached its hard limit. `seen` is the full evidence
        signature last observed, and `paused_at` when the limit was reached. A person's request does not
        refresh the slot time."""
        scope = self._scope(db, cap)
        slot = db.execute(
            "SELECT scope,signature,replaced,at,seen,paused_at FROM assistant_schedule WHERE capability=? AND case_id=?",
            (cap, case_id),
        ).fetchone()
        now = self.now(db)
        if replaced is None:
            replaced = slot[2] if slot is not None and slot[0] == scope and slot[1] == coarse else 0
        paused_at = (
            0
            if replaced < self.REPLACEMENTS
            else (slot[5] if slot is not None and slot[2] >= self.REPLACEMENTS and slot[5] else now)
        )
        at = now if touch or slot is None else slot[3]
        seen = seen if seen is not None else (slot[4] if slot is not None else "")
        values = (scope, coarse, tid, at, replaced, seen, paused_at, cap, case_id)
        if slot is None:
            db.execute(
                "INSERT INTO assistant_schedule (scope,signature,task_id,at,replaced,seen,paused_at,capability,case_id) VALUES (?,?,?,?,?,?,?,?,?)",
                values,
            )
        else:
            db.execute(
                "UPDATE assistant_schedule SET scope=?,signature=?,task_id=?,at=?,replaced=?,seen=?,paused_at=? WHERE capability=? AND case_id=?",
                values,
            )

    ADOPT_ROWS = 5
    ADOPT_PAGES = 20
    COALESCE_QUIET = 300.0
    COALESCE_MAX = 1800.0
    INCOMPLETE = "incomplete-history"

    def _adopt(self, db, cap, case_id, cursor=None):
        """Pre-upgrade stores have tasks but no schedule row. Adopt, once per case, the newest dispatched task
        of the current release and epoch that was not a person's request, recording that task's OWN schedule
        signature so a later assessment or funding change is still new work. Unrecorded history is never
        treated as approved. Pure: it reads and returns a slot `(scope, signature, task_id, at, replaced, seen,
        paused_at)` and writes nothing. The first read is the newest ADOPT_ROWS x ADOPT_PAGES dispatched
        tasks. When that bound is reached first the slot is INCOMPLETE and stores a durable cursor, the last
        task id examined; later scans walk the remaining history by immutable task id (retries rewrite
        `dispatched`, so that is not a stable key), adopting the first qualifying task, so a long history
        completes in bounded scans without a larger cap or a model call. After the first window the adopted
        task is the first qualifying by id, which is not necessarily the newest. Nothing qualifying after a
        complete read is an empty slot, never an approval."""
        epoch = self.continuity(db)["epoch"]
        release = self.release_reference(db, cap)
        now = self.now(db)

        def qualifies(raw):
            task = json.loads(raw)
            if task.get("release") != release or task.get("continuity_epoch") != epoch:
                return False
            trigger = (task.get("dispatch") or {}).get("trigger")
            return not (
                trigger == "requested" or (trigger is None and task.get("manual_requested"))
            )

        if cursor is None:
            query = (
                "SELECT id,body,signature FROM assistant_tasks WHERE capability=? AND case_id=? AND attempts>0"
                " ORDER BY dispatched DESC, revision DESC, id"
            )
            query += " OFFSET ? ROWS FETCH NEXT ? ROWS ONLY" if self.mssql else " LIMIT ? OFFSET ?"
            for page in range(self.ADOPT_PAGES):
                args = (
                    (self.ADOPT_ROWS, page * self.ADOPT_ROWS)
                    if not self.mssql
                    else (page * self.ADOPT_ROWS, self.ADOPT_ROWS)
                )
                rows = db.execute(query, (cap, case_id, *args)).fetchall()
                for tid, raw, own in rows:
                    if qualifies(raw):
                        return (self._scope(db, cap), own, tid, now, 0, "", 0)
                if len(rows) < self.ADOPT_ROWS:
                    return ("", "", "", now, 0, "", 0)
            return ("", self.INCOMPLETE, "", now, 0, "", 0)
        query = (
            "SELECT id,body,signature FROM assistant_tasks WHERE capability=? AND case_id=? AND attempts>0"
            " AND id>? ORDER BY id"
        )
        query += " OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY" if self.mssql else " LIMIT ?"
        for _ in range(self.ADOPT_PAGES):
            rows = db.execute(query, (cap, case_id, cursor, self.ADOPT_ROWS)).fetchall()
            for tid, raw, own in rows:
                if qualifies(raw):
                    return (self._scope(db, cap), own, tid, now, 0, "", 0)
            if len(rows) < self.ADOPT_ROWS:
                return ("", "", "", now, 0, "", 0)
            cursor = rows[-1][0]
        return ("", self.INCOMPLETE, cursor, now, 0, "", 0)

    def _write_slot(self, db, cap, case_id, slot, exists):
        if exists:
            db.execute(
                "UPDATE assistant_schedule SET scope=?,signature=?,task_id=?,at=?,replaced=?,seen=?,paused_at=? WHERE capability=? AND case_id=?",
                (*slot, cap, case_id),
            )
        else:
            db.execute(
                "INSERT INTO assistant_schedule (scope,signature,task_id,at,replaced,seen,paused_at,capability,case_id) VALUES (?,?,?,?,?,?,?,?,?)",
                (*slot, cap, case_id),
            )

    def _due(self, db, cap, c, snapshot, today, observe=True):
        """Whether a proactive scan may start work. The coarse signature throttles every eligible branch,
        gaps included, only within the current release and continuity scope and only while the slot's task
        is serviced; any other change or a manual request is never suppressed. A dispatched task is a
        person's request only when its frozen dispatch says so. Reads are by primary key. Only an observing
        scan persists adoption or the history cursor; a forecast computes the same result in memory."""
        coarse = scheduling_signature(snapshot)
        columns = "SELECT scope,signature,task_id,at,replaced,seen,paused_at FROM assistant_schedule WHERE capability=? AND case_id=?"
        slot = db.execute(columns, (cap, c["id"])).fetchone()
        if slot is None or slot[1] == self.INCOMPLETE:
            if slot is not None and not observe:
                return False
            stored = slot is not None
            slot = self._adopt(db, cap, c["id"], slot[2] if stored else None)
            if observe:
                self._write_slot(db, cap, c["id"], slot, stored)
            if slot[1] == self.INCOMPLETE:
                if observe:
                    self.incomplete.add((cap, c["id"]))
                return False
        scoped = slot is not None and slot[0] == self._scope(db, cap)
        known = False
        if scoped and slot[1] == coarse:
            held = db.execute(
                "SELECT state,attempts,body FROM assistant_tasks WHERE id=?", (slot[2],)
            ).fetchone()
            if held is not None:
                body = json.loads(held[2])
                dispatched = held[1] > 0
                manual = (
                    ((body.get("dispatch") or {}).get("trigger") == "requested")
                    if dispatched
                    else bool(body.get("manual_requested"))
                )
                if held[0] == "stale" and not dispatched:
                    if (
                        not manual
                        and slot[4] >= self.REPLACEMENTS
                        and not self._resumes(db, cap, c, snapshot, slot, observe)
                    ):
                        return False
                else:
                    # A person's request services a non-sensor schedule but never the autonomous Quality flag.
                    known = not manual or cap != "quality-evidence"
        if not eligible(cap, snapshot, today, scoped and not known, known):
            return False
        exact = self._task_id(db, cap, c, signature(snapshot))
        exists = db.execute("SELECT 1 FROM assistant_tasks WHERE id=?", (exact,)).fetchone()
        if known and exists is not None and cap == "quality-evidence" and exact != slot[2]:
            # The exact capture already belongs to a person's request; the serviced autonomous slot is not rewritten.
            return False
        return exists is not None or not known

    def _resumes(self, db, cap, c, snapshot, slot, observe):
        """While the replacement limit holds a stale, undispatched slot, readings still arriving keep it paused
        only until COALESCE_MAX after the pause began, so work is never starved. A change observed by a scan
        restarts the quiet interval; automatic review resumes after COALESCE_QUIET without an observed change.
        Changes that revert between two scans are not observed. Resuming resets the replacement count."""
        now, full = self.now(db), signature(snapshot)
        at, started = slot[3], slot[6] or slot[3]
        if full != slot[5]:
            at = now
            if observe:
                db.execute(
                    "UPDATE assistant_schedule SET seen=?,at=?,paused_at=? WHERE capability=? AND case_id=?",
                    (full, now, started, cap, c["id"]),
                )
        if now - at < self.COALESCE_QUIET and now - started < self.COALESCE_MAX:
            return False
        if observe:
            db.execute(
                "UPDATE assistant_schedule SET replaced=0,paused_at=0 WHERE capability=? AND case_id=?",
                (cap, c["id"]),
            )
        return True

    def scan(self):
        if not self.sql or not self.limits.proactive:
            return dict(enqueued=[], disabled="Proactive assistance is off.")
        if not self.scan_lock.acquire(blocking=False):
            return dict(enqueued=[], disabled="Scan already in progress.")
        try:
            with self.transaction() as db:
                reason = self.disabled(db)
                if reason:
                    return dict(enqueued=[], disabled=reason)
                query = "SELECT id,body FROM cases WHERE id>? AND closed=0 ORDER BY id"
                query += " OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY" if self.mssql else " LIMIT ?"
                rows = db.execute(query, (self.scan_cursor, self.limits.scan_size)).fetchall()
                self.scan_cursor = rows[-1][0] if len(rows) == self.limits.scan_size else ""
                today = datetime.fromtimestamp(self.now(db), timezone.utc).date().isoformat()
                result = []
                for cid, raw in rows:
                    c = json.loads(raw)
                    for cap in REGISTRY:
                        if self.suspended(db, cap):
                            continue
                        # Demo scope: Quality runs only when a person requests it, never from the background scan.
                        if cap == "quality-evidence" and (
                            self.limits.quality_homes is not None or self.limits.quality_scope_error
                        ):
                            continue
                        s = self.snapshot(db, cap, c)
                        if self._due(db, cap, c, s, today):
                            result.append(self._enqueue(db, cap, c, "proactive", PURPOSE))
                held = sorted(f"{cap}:{cid}" for cap, cid in self.incomplete)
                self.incomplete.clear()
                return dict(enqueued=result, disabled=None, incomplete_history=held)
        finally:
            self.scan_lock.release()

    def claim(self, tid, owner):
        with self.transaction() as db:
            task, now, l = self._row(db, tid), self.now(db), self.limits
            if (
                task["state"] not in ("pending", "leased")
                or task["not_before"] > now
                or (task["state"] == "leased" and task["lease_until"] > now)
            ):
                return None
            if "permitted" in self._markers(db, tid):
                task["reason"] = (
                    "A provider call may already have been permitted for this task; Finance or the manual route resolves it."
                )
                db.execute(
                    "UPDATE assistant_tasks SET state='failed',body=?,lease_until=0,revision=revision+1 WHERE id=?",
                    (canonical(task), tid),
                )
                self.event(db, tid, kind="blocked-reclaim", reason="permitted-marker")
                return None
            if task["attempts"] >= l.attempts:
                task["reason"] = "Attempts exhausted; use the manual owner route."
                db.execute(
                    "UPDATE assistant_tasks SET state='failed',body=?,revision=revision+1 WHERE id=?",
                    (canonical(task), tid),
                )
                self.event(db, tid, kind="exhausted", outcome="attempts-exhausted")
                return None
            reason = self.disabled(db, task["capability"]) or self.quality_scope_denial(
                task["capability"], task["case_id"], task.get("manual_requested") is True
            )
            if not reason and not continuity.epoch_current(task, self.continuity(db)):
                reason = "Proposal epoch changed or is unavailable; request fresh work or use the manual route."
            if not reason and task.get("release") != self.release_reference(db, task["capability"]):
                reason = rel.denial(
                    "activation release changed",
                    ["original activation release"],
                    task["capability"],
                )["reason"]
            if reason:
                task["reason"] = reason
                db.execute(
                    "UPDATE assistant_tasks SET state='disabled',body=?,revision=revision+1 WHERE id=?",
                    (canonical(task), tid),
                )
                self.event(db, tid, kind="disabled", reason=reason)
                return None
            row = db.execute("SELECT body FROM cases WHERE id=?", (task["case_id"],)).fetchone()
            current = self.snapshot(db, task["capability"], json.loads(row[0])) if row else None
            if current is None or signature(current) != task["source_signature"]:
                replace = current is not None and self._replaceable(db, task, current)
                paused = current is not None and not replace and self._paused(db, task, current)
                task["reason"] = (
                    PAUSED
                    if paused
                    else "Permitted source changed; request a new proposal or work manually."
                )
                db.execute(
                    "UPDATE assistant_tasks SET state='stale',body=?,revision=revision+1 WHERE id=?",
                    (canonical(task), tid),
                )
                self.event(db, tid, kind="stale", reason=task["reason"])
                if replace:
                    # Newer readings in the same coarse schedule: the current capture is its own task with its own
                    # evidence identity, so a person's later request for it reuses it instead of duplicating it.
                    slot = db.execute(
                        "SELECT replaced FROM assistant_schedule WHERE capability=? AND case_id=?",
                        (task["capability"], task["case_id"]),
                    ).fetchone()
                    self._enqueue(
                        db,
                        task["capability"],
                        json.loads(row[0]),
                        "proactive",
                        PURPOSE,
                        (slot[0] if slot else 0) + 1,
                    )
                return None
            fence = task["fence"] + 1
            refusal = self._reserve(db, now, f"{tid}:{fence}", tid, fence, task["capability"])
            if refusal == "active":
                reason = "Waiting for a shared active-call slot; ordinary manual case work remains available."
                if task["reason"] != reason:
                    task["reason"] = reason
                    db.execute(
                        "UPDATE assistant_tasks SET body=?,revision=revision+1 WHERE id=?",
                        (canonical(task), tid),
                    )
                    self.event(db, tid, kind="throttled", reason=reason)
                return None
            if refusal == "pool":
                task["reason"] = "Shared durable allowance exhausted/expired; use manual route."
                db.execute(
                    "UPDATE assistant_tasks SET state='disabled',body=?,revision=revision+1 WHERE id=?",
                    (canonical(task), tid),
                )
                self.event(
                    db,
                    tid,
                    kind="disabled",
                    reason="Shared durable allowance exhausted/expired; use manual route.",
                )
                return None
            task["reason"] = None
            task["claim_epoch"] = self.continuity(db)["epoch"]
            # Only an explicit absence of a person's request is proactive; legacy or unclear tasks are not.
            task["dispatch"] = dict(
                trigger="proactive" if task.get("manual_requested") is False else "requested",
                fence=fence,
                as_of=now,
            )
            if task["dispatch"]["trigger"] == "proactive":
                db.execute(
                    "UPDATE assistant_schedule SET replaced=0,paused_at=0 WHERE capability=? AND case_id=? AND task_id=?",
                    (task["capability"], task["case_id"], tid),
                )
            task["claim_binding"] = digest(runtime_binding(task["capability"], self.store.ai))
            result = db.execute(
                "UPDATE assistant_tasks SET state='leased',body=?,owner=?,fence=?,lease_until=?,attempts=attempts+1,dispatched=?,revision=revision+1 WHERE id=? AND fence=? AND revision=?",
                (
                    canonical(task),
                    owner,
                    fence,
                    now + l.lease,
                    now,
                    tid,
                    task["fence"],
                    task["revision"],
                ),
            )
            if result.rowcount != 1:
                raise ConflictError(tid)
            self.event(
                db,
                tid,
                kind="claimed",
                owner=owner,
                fence=fence,
                reservation=l.reservation,
                authority_reference=l.authority,
                trigger=task["dispatch"]["trigger"],
            )
            return self._row(db, tid)

    def _pool(self, db):
        """The allowance row for the current authority. A changed or rotated authority token has no row of its own, so
        it inherits the most constrained persisted ledger (lowest ceilings, highest consumption) instead of a fresh pool.
        Returns None only when no authority has ever been admitted."""
        l = self.limits
        pool = db.execute(
            "SELECT calls,tokens,expires,used_calls,reserved_tokens FROM assistant_allowance WHERE id=?",
            (l.pool,),
        ).fetchone()
        if pool is not None:
            return tuple(pool)
        # Owner-directed demo override: an expired earlier exercise cannot poison a newly authorised finite one.
        live_only = (
            " WHERE expires>?" if continuity.demo_owner_override() else ""
        )
        prior = db.execute(
            "SELECT MIN(calls),MIN(tokens),MIN(expires),MAX(used_calls),MAX(reserved_tokens) FROM assistant_allowance"
            + live_only,
            (self.now(db),) if live_only else (),
        ).fetchone()
        if prior[0] is None:
            return None
        return (
            min(prior[0], l.calls),
            min(prior[1], l.tokens),
            min(prior[2], l.expiry),
            prior[3],
            prior[4],
        )

    def _reserve(self, db, now, attempt, tid, fence, capability):
        """Inside the caller's transaction: take one durable active-call slot and debit one call plus its token
        reservation from the shared allowance. Returns None on success, else "active" or "pool"."""
        l = self.limits
        active = db.execute(
            "SELECT COUNT(*) FROM assistant_attempts WHERE active_until>?", (now,)
        ).fetchone()[0]
        if active >= l.active_calls:
            return "active"
        pool = self._pool(db)
        if pool is None:
            pool = (l.calls, l.tokens, l.expiry, 0, 0)
        if db.execute("SELECT 1 FROM assistant_allowance WHERE id=?", (l.pool,)).fetchone() is None:
            db.execute(
                "INSERT INTO assistant_allowance (id,calls,tokens,expires,used_calls,reserved_tokens) VALUES (?,?,?,?,?,?)",
                (l.pool, *pool),
            )
        # Same authority cannot extend expiry or increase allowance by restarting/config changes.
        calls, tokens, expiry = (
            min(pool[0], l.calls),
            min(pool[1], l.tokens),
            min(pool[2], l.expiry),
        )
        db.execute(
            "UPDATE assistant_allowance SET calls=?,tokens=?,expires=? WHERE id=?",
            (calls, tokens, expiry, l.pool),
        )
        if expiry <= now or pool[3] >= calls or pool[4] + l.reservation > tokens:
            return "pool"
        db.execute(
            "UPDATE assistant_allowance SET used_calls=used_calls+1,reserved_tokens=reserved_tokens+? WHERE id=?",
            (l.reservation, l.pool),
        )
        db.execute(
            "INSERT INTO assistant_attempts (id,task_id,fence,pool,reserved,actual,outcome,active_until,capability,gate_version,send_gate_version) VALUES (?,?,?,?,?,NULL,'reserved',?,?,?,'')",
            (
                attempt,
                tid,
                fence,
                l.pool,
                l.reservation,
                now + l.lease,
                capability,
                continuity.GATE_VERSION,
            ),
        )
        return None

    def _settle(self, db, attempt, envelope):
        """Inside the caller's transaction: settle an attempt from its provider envelope. Known usage within the
        reservation refunds the difference; otherwise the whole reservation stays as liability. The durable slot is
        released unless the outcome is uncertain (timeout or provider unavailable). Returns (actual, reserved)."""
        usage = envelope.get("usage")
        actual = usage.get("total_tokens") if isinstance(usage, dict) else None
        row = db.execute(
            "SELECT pool,reserved FROM assistant_attempts WHERE id=?", (attempt,)
        ).fetchone()
        # A finance hold taken before any meter reservation means no request, token or socket existed, so the
        # whole call is returned and a held capability cannot drain the shared allowance for the others.
        unsent = envelope.get("outcome") == "financial-held" and not envelope.get("meter_id")
        if unsent:
            db.execute(
                "UPDATE assistant_allowance SET used_calls=used_calls-1,reserved_tokens=reserved_tokens-? WHERE id=?",
                (row[1], row[0]),
            )
            actual = 0
        elif type(actual) is int and 0 <= actual <= row[1]:
            db.execute(
                "UPDATE assistant_allowance SET reserved_tokens=reserved_tokens-? WHERE id=?",
                (row[1] - actual, row[0]),
            )
        else:
            actual = None
        db.execute(
            "UPDATE assistant_attempts SET actual=?,outcome=? WHERE id=?",
            (actual, str(envelope.get("outcome", "unknown"))[:40], attempt),
        )
        if envelope.get("outcome") not in ("timeout", "provider-unavailable"):
            db.execute("UPDATE assistant_attempts SET active_until=0 WHERE id=?", (attempt,))
        return actual, row[1]

    def begin_call(self, capability, chars, call_id):
        """Admit one bounded direct provider call under the same operator authority, durable allowance and
        active-call slots as ordinary assistant tasks. The physical slot is taken first without waiting; then one
        transaction applies the disabled/expiry/schema/release checks and the atomic reserve and debit. A refusal
        happens before any meter, token or socket and carries a reason; otherwise the ticket must be ended."""
        if not self.call_slots.acquire(blocking=False):
            return CallTicket(
                self, None, "Waiting for a shared active-call slot; use the manual route."
            )
        attempt = f"{call_id}:1"
        try:
            with self.transaction() as db:
                reason = self.disabled(db, capability)
                if not reason and chars > self.limits.input_chars:
                    reason = "Input exceeds limit; use the manual route."
                if not reason:
                    refusal = self._reserve(db, self.now(db), attempt, call_id, 1, capability)
                    reason = {
                        "active": "Waiting for a shared active-call slot; use the manual route.",
                        "pool": "Shared durable allowance exhausted/expired; use the manual route.",
                    }.get(refusal)
                if not reason:
                    self.event(
                        db,
                        call_id,
                        kind="direct-call-claimed",
                        capability=capability,
                        reservation=self.limits.reservation,
                        authority_reference=self.limits.authority,
                    )
        except (self.store.dberror, OSError):
            self.call_slots.release()
            return CallTicket(
                self, None, "Operator authority store unavailable; use the manual route."
            )
        except BaseException:
            self.call_slots.release()
            raise
        if reason:
            self.call_slots.release()
            return CallTicket(self, None, reason)
        return CallTicket(self, attempt, None, capability)

    def fence_send(self, attempt, capability):
        """The last durable decision before a request byte, in one transaction: the same operator authority,
        suspension, release and allowance-expiry conditions as admission, and an attempt that is still live. It
        then restamps the attempt to cover the bounded send, so another caller cannot reuse the slot while this
        send is in flight. A refusal raises DispatchWithdrawn and sends nothing. A process suspended after this
        returns, outside user space, can still transmit late; the send window and socket deadline bound it."""
        with self.transaction() as db:
            refused = self._fence_in(db, attempt, capability)
        if refused:
            raise ai_consumption.DispatchWithdrawn(refused)

    def _fence_in(self, db, attempt, capability):
        """The fence decision in the caller's transaction: a refusal reason (after a `send-refused` event),
        or None after restamping the attempt to `sending`. Shared by `fence_send` and `issue_permit`."""
        window = self.limits.timeout + HOLD_GRACE
        now = self.now(db)
        held = self.disabled(db, capability, capacity=False)
        row = db.execute(
            "SELECT outcome,active_until FROM assistant_attempts WHERE id=?", (attempt,)
        ).fetchone()
        if held or row is None or row[0] not in ("reserved", "sending") or row[1] <= now:
            refused = held or "The admission lease ended before the request was sent."
            self.event(db, attempt.split(":")[0], kind="send-refused", reason=refused[:120])
            return refused
        db.execute(
            "UPDATE assistant_attempts SET outcome='sending',send_gate_version=?,active_until=? WHERE id=?",
            (continuity.GATE_VERSION, max(row[1], now + window), attempt),
        )
        return None

    REPLACEMENTS = 3

    def _paused(self, db, task, current):
        """An unrequested proactive task whose schedule is unchanged but whose consecutive-replacement limit is
        reached: automatic review waits for a quiet interval, and a person can still request it."""
        slot = db.execute(
            "SELECT replaced,task_id FROM assistant_schedule WHERE capability=? AND case_id=?",
            (task["capability"], task["case_id"]),
        ).fetchone()
        return (
            task.get("manual_requested") is False
            and scheduling_signature(current) == scheduling_signature(task["snapshot"])
            and slot is not None
            and slot[1] == task["id"]
            and slot[0] >= self.REPLACEMENTS
        )

    def _replaceable(self, db, task, current):
        """Only an unrequested proactive task whose coarse schedule is unchanged, within the input bound and
        within the consecutive no-dispatch replacement limit, which keeps churn from creating unbounded tasks."""
        slot = db.execute(
            "SELECT replaced,task_id FROM assistant_schedule WHERE capability=? AND case_id=?",
            (task["capability"], task["case_id"]),
        ).fetchone()
        # Only the task that owns the slot may spend its replacement budget; an older task goes stale alone.
        return (
            task.get("manual_requested") is False
            and scheduling_signature(current) == scheduling_signature(task["snapshot"])
            and not (self.limits.valid and len(canonical(current)) > self.limits.input_chars - 1500)
            and slot is not None
            and slot[1] == task["id"]
            and slot[0] < self.REPLACEMENTS
        )

    def renew(self, tid, owner, fence):
        with self.transaction() as db:
            now = self.now(db)
            renewed = (
                db.execute(
                    "UPDATE assistant_tasks SET lease_until=? WHERE id=? AND owner=? AND fence=? AND state='leased' AND lease_until>?",
                    (now + self.limits.lease, tid, owner, fence, now),
                ).rowcount
                == 1
            )
            if renewed:
                db.execute(
                    "UPDATE assistant_attempts SET active_until=? WHERE id=?",
                    (now + self.limits.lease, f"{tid}:{fence}"),
                )
            return renewed

    def complete_result(self, tid, owner, fence, envelope, output, failure=None):
        """Post-back completion: the stored task, not the caller, supplies the snapshot and release.

        Returns False for an unknown, unleased, wrong-owner or wrong-fence task, without any mutation.
        `complete` then re-checks lease, release, epoch, admission and source binding under the transaction.
        """
        if (
            not isinstance(envelope, dict)
            or not isinstance(tid, str)
            or not isinstance(owner, str)
            or type(fence) is not int
        ):
            raise ValueError("Malformed result.")
        if (output is not None and not isinstance(output, dict)) or (
            failure is not None and not isinstance(failure, str)
        ):
            raise ValueError("Malformed result.")
        if not self.sql:
            raise ValueError(self.disabled())
        with self.transaction() as db:
            try:
                task = self._row(db, tid)
            except KeyError:
                return False
            marker = self._markers(db, tid).get("permitted")
            matches = task["owner"] == owner and task["fence"] == fence
            if marker is not None:
                root = self._permitted_root(db, marker["meter_id"])
                if (
                    marker["owner"] != owner
                    or marker["fence"] != fence
                    or root is None
                    or envelope.get("meter_id") not in (None, marker["meter_id"])
                    or envelope.get("meter_root") not in (None, root)
                ):
                    self.event(db, tid, kind="result-rejected", reason="not-the-permitted-attempt")
                    return False
                envelope = dict(envelope, meter_id=marker["meter_id"], meter_root=root)
                self._settle_meter(db, marker, envelope)
            elif matches:
                self.event(db, tid, kind="closed-without-permit", fence=fence)
        if task["state"] != "leased" or not matches:
            return False
        return self.complete(task, envelope, output, failure)

    def _permitted_root(self, db, meter_id):
        """The attribution root the server reserved under; the caller never supplies it."""
        return next(
            (
                r["root"]
                for r in self.consumption._read(db)
                if r["kind"] == "reserved" and r["id"] == meter_id
            ),
            None,
        )

    def _settle_meter(self, db, marker, envelope):
        usage, outcome = envelope.get("usage"), envelope.get("outcome")
        if outcome in ("returned", "model-mismatch") and ai_consumption.usage(usage):
            model = envelope.get("model")
            # A rewritten or oversized identity cannot match the reservation, so the spend stays held.
            self.consumption.complete_in(
                db,
                marker["meter_id"],
                usage,
                model if ai_consumption.bounded_model(model) == model else None,
                "returned",
            )
        else:
            self.consumption.complete_in(
                db,
                marker["meter_id"],
                None,
                None,
                "timeout" if outcome == "timeout" else "provider-unavailable",
            )

    def _markers(self, db, tid):
        found = {}
        for (body,) in db.execute(
            "SELECT body FROM assistant_events WHERE task_id=? ORDER BY at", (tid,)
        ).fetchall():
            event = json.loads(body)
            if event.get("kind") in ("permitted", "closed-without-permit"):
                found.setdefault(event["kind"], event)
        return found

    def _permit_block(self, db, task):
        """Why a permit must not be issued now; every unresolved or unreadable condition fails closed to manual."""
        capability = task["capability"]
        epoch = self.continuity(db)
        if self.quality_scope_denial(
            capability, task["case_id"], (task.get("dispatch") or {}).get("trigger") == "requested"
        ):
            return "demo-scope"
        if self.suspended(db, capability):
            return "suspended"
        if self.admission(db, capability):
            return "not-admitted"
        if not continuity.epoch_current(task, epoch) or not continuity.epoch_current(
            dict(capability=capability, continuity_epoch=task.get("claim_epoch")), epoch
        ):
            return "epoch-changed"
        if digest(runtime_binding(capability, self.store.ai)) != task.get("claim_binding"):
            return "binding-changed"
        if task.get("release") != self.release_reference(db, capability):
            return "release-changed"
        row = db.execute("SELECT body FROM cases WHERE id=?", (task["case_id"],)).fetchone()
        if (
            row is None
            or digest(self.snapshot(db, capability, json.loads(row[0]))) != task["source_signature"]
        ):
            return "source-changed"
        if not self._sensors_granted(db, task):
            return "consent-not-granted"
        if contract_refusal(task):
            return "data-contract"
        if self._captured_sensors(task):
            # A queued worker is not the in-process carrier, so no existing contract lets it carry captured readings.
            return "captured-readings"
        return None

    def _refuse_attempt(self, db, task, state, reason):
        now = self.now(db)
        task["reason"] = f"Permit denied ({reason}); use the manual route."
        db.execute(
            "UPDATE assistant_tasks SET state=?,body=?,lease_until=0,revision=revision+1 WHERE id=? AND owner=? AND fence=?",
            (state, canonical(task), task["id"], task["owner"], task["fence"]),
        )
        attempt = db.execute(
            "SELECT pool,reserved,outcome FROM assistant_attempts WHERE id=?",
            (f"{task['id']}:{task['fence']}",),
        ).fetchone()
        # Nothing was sent: a refusal in this transaction also releases an attempt the fence had restamped to sending.
        if attempt is not None and attempt[2] in ("reserved", "sending"):
            db.execute(
                "UPDATE assistant_allowance SET used_calls=used_calls-1,reserved_tokens=reserved_tokens-? WHERE id=?",
                (attempt[1], attempt[0]),
            )
            db.execute(
                "UPDATE assistant_attempts SET outcome='permit-denied',actual=0,active_until=0 WHERE id=?",
                (f"{task['id']}:{task['fence']}",),
            )
        self.event(
            db, task["id"], kind="permit-denied", fence=task["fence"], reason=reason, at_time=now
        )

    def issue_permit(self, tid, owner, fence, request):
        """One transaction: task-first lock, DB time after the lock, exact request, send fence, ledger reservation,
        never-overwritten marker.

        A deadlock or storage error propagates and rolls everything back; a refusal commits at most one task outcome and one refund.
        """
        if (
            not isinstance(tid, str)
            or not isinstance(owner, str)
            or type(fence) is not int
            or not isinstance(request, dict)
        ):
            raise ValueError("Malformed permit request.")
        if not self.sql or not self.limits.valid:
            raise ValueError(self.disabled())

        def deny(reason):
            return dict(permit=False, reason=reason)

        with self.transaction() as db:
            if (
                db.execute(
                    "UPDATE assistant_tasks SET revision=revision+1 WHERE id=? AND owner=? AND fence=? AND state='leased'",
                    (tid, owner, fence),
                ).rowcount
                != 1
            ):
                return deny("task-not-leased")
            now = self.now(db)  # read after the possibly blocking update, never before it
            task, marks = self._row(db, tid), self._markers(db, tid)
            if "closed-without-permit" in marks:
                return deny("task-closed")
            if task["lease_until"] <= now + PERMIT_LEASE_MARGIN:
                return deny("lease-expiring")
            attempt = ai_consumption.reference(f"{tid}:{fence}")
            if "permitted" in marks or any(
                r["kind"] == "reserved" and r["attempt"] == attempt
                for r in self.consumption._read(db)
            ):
                return deny("duplicate-permit")
            blocked = self._permit_block(db, task)
            if blocked:
                self._refuse_attempt(db, task, "disabled", blocked)
                return deny(blocked)
            ai, system_prompt = self.store.ai, build_request(task)
            planner = getattr(ai, "request_plan", None)
            plan = (
                planner(*system_prompt, ai.fast, 0, self.limits.output_tokens)
                if planner and sum(map(len, system_prompt)) <= self.limits.input_chars
                else None
            )
            if plan is None or any(request.get(key) != plan[key] for key in PERMIT_REQUEST):
                return deny("request-mismatch")
            fenced = self._fence_in(db, f"{tid}:{fence}", task["capability"])
            if fenced:
                self._refuse_attempt(db, task, "disabled", "send-fence-refused")
                return deny("send-fence-refused")
            context = ai_consumption.CallContext(
                ai_consumption.reference(tid),
                attempt,
                task["capability"],
                "retrofit-case",
                plan["configuration"],
                ai_consumption.reference(runtime_binding(task["capability"], ai)["prompt_version"]),
                retry=task["attempts"] - 1,
            )
            meter, held = self.consumption.reserve_in(
                db,
                context,
                plan["model"],
                plan["input_bound"],
                plan["max_tokens"],
                live=ai.is_live(task["capability"]),
                min_window=PERMIT_WINDOW,
            )
            if meter is None or held:
                self._refuse_attempt(db, task, "failed", held or "permit-held")
                return deny(held or "permit-held")
            self.event(
                db,
                tid,
                kind="permitted",
                owner=owner,
                fence=fence,
                attempt=attempt,
                meter_id=meter,
                body_sha256=plan["body_sha256"],
                issued_at=now,
            )
            window = self.consumption.dispatch_window_ms(db, meter)
            if window < 1:
                raise ValueError("A permit without a dispatch window cannot be issued.")
            return dict(
                permit=True,
                meter_id=meter,
                issued_at=now,
                lease_remaining=task["lease_until"] - now,
                dispatch_within_ms=window,
            )

    def complete(self, task, envelope, output, failure=None):
        envelope = sanitize_identity(envelope)
        already_guarded = bool(getattr(self._guard_local, "already_guarded", False))
        if output is not None:
            try:
                if envelope.get("source") != "ai" or envelope.get("outcome") != "returned":
                    raise ValueError("Unverified provider outcome.")
                output = validate_output(
                    output,
                    task["snapshot"],
                    self.limits.output_chars,
                    guard_telemetry=None if already_guarded else self.guard_telemetry,
                )
            except (ValueError, TypeError, KeyError):
                output, failure = None, "Invalid/unverified proposal; use manual work."
        with self.transaction() as db:
            current, now = self._row(db, task["id"]), self.now(db)
            if (
                current["state"] != "leased"
                or current["owner"] != task["owner"]
                or current["fence"] != task["fence"]
                or current["lease_until"] <= now
            ):
                return False
            if output is not None:
                row_c = db.execute(
                    "SELECT body FROM cases WHERE id=?", (current["case_id"],)
                ).fetchone()
                c = json.loads(row_c[0]) if row_c else self.store.cases.get(current["case_id"])
                if c is not None:
                    cap_roles = REGISTRY.get(current["capability"], {}).get("roles", ())
                    per_role = [
                        set(
                            projection.withheld_case_values(
                                c,
                                projection.project_case_visibility(
                                    dict(role=role, code=c.get("owner_code", ""), email=""), c
                                ),
                            )
                        )
                        for role in cap_roles
                    ]
                    cap_withheld = set.intersection(*per_role) if per_role else set()
                    if _output_violates_visibility(output, cap_withheld):
                        output = None
                        failure = "Model output withheld by role visibility check; use manual work."
            epoch = self.continuity(db)["epoch"]
            denied = self.admission(db, current["capability"])
            binding = digest(runtime_binding(current["capability"], self.store.ai))
            quarantined = (
                not continuity.epoch_current(current, self.continuity(db))
                or not continuity.epoch_current(
                    dict(
                        capability=current["capability"],
                        continuity_epoch=current.get("claim_epoch"),
                    ),
                    self.continuity(db),
                )
                or bool(self.suspended(db, current["capability"]))
                or bool(denied)
                or binding != current.get("claim_binding", binding)
                or current.get("release") != self.release_reference(db, current["capability"])
            )
            if envelope.get("outcome") in ("returned", "model-mismatch"):
                # A deployment alias is not immutable, so the model the provider returned is compared with the released
                # serving model and the result is kept on the task. Only an exact match leaves a proposal eligible.
                released = [
                    r
                    for r in rel.releases(db, current["capability"])
                    if r["id"] == current["release"]["id"]
                ]
                attestation = (
                    rai_release.attest_serving(released[0], envelope.get("model"))
                    if released
                    else dict(expected=None, returned=None, outcome="unattested")
                )
                if (
                    envelope.get("outcome") == "model-mismatch"
                    and attestation["outcome"] == "matched"
                ):
                    attestation["outcome"] = "mismatch"
                current["serving_attestation"] = dict(attestation, at=now)
                if attestation["outcome"] != "matched":
                    quarantined = True
                    for r in released:
                        if r["status"] == "active":
                            recovery.record_release_change(self.store, db, r["id"], "suspended")
                            rel.change(
                                db,
                                now,
                                None,
                                r["id"],
                                "suspended",
                                f"Serving-version attestation {attestation['outcome']}; results quarantined and release suspended.",
                                system=True,
                            )
                    current["fallback"] = dict(
                        route="manual",
                        release="suspended",
                        reason=f"Serving-version attestation {attestation['outcome']}; use manual work.",
                    )
                    detail = dict(
                        kind="serving-attestation",
                        outcome=attestation["outcome"],
                        expected=attestation["expected"],
                        returned=ai_consumption.bounded_model(attestation["returned"]),
                    )
                    rel.event(db, now, current["release"]["id"], task=task["id"], **detail)
                    self.event(db, task["id"], **detail)
            held_output = output
            if quarantined:
                # The call may have been charged; its result is kept as a digest only and never becomes a proposal.
                output = None
                failure = (
                    failure
                    or "Late result quarantined after a suspension, restart, release change or serving-version mismatch; use manual work."
                )
                current["quarantine"] = dict(
                    epoch=epoch,
                    claim_epoch=current.get("claim_epoch"),
                    output_digest=digest(held_output) if held_output is not None else None,
                )
            envelope["release"] = current.get("release")
            state = (
                "quarantined"
                if quarantined
                else "ready"
                if output is not None and not failure
                else (
                    "pending"
                    if envelope.get("outcome") in ("timeout", "provider-unavailable")
                    and current["attempts"] < self.limits.attempts
                    else "failed"
                )
            )
            if envelope.get("meter_root") and state != "pending":
                held = self.consumption.publish_output(
                    envelope["meter_root"], task["id"], eligible=state == "ready", db=db
                )
                if held:
                    current["financial_attribution"] = held
                    output = None
                    failure = (
                        failure
                        or f"Financial attribution held ({held['reason']}); use manual work."
                    )
                    if not quarantined:
                        state = "failed"
            current.update(
                envelope=envelope, output=output, reason=failure, verification=None, review=None
            )
            delay = self.limits.backoff * current["attempts"] if state == "pending" else 0
            result = db.execute(
                "UPDATE assistant_tasks SET body=?,state=?,not_before=?,lease_until=0,revision=revision+1 WHERE id=? AND owner=? AND fence=? AND state='leased' AND lease_until>?",
                (
                    canonical(current),
                    state,
                    now + delay,
                    task["id"],
                    task["owner"],
                    task["fence"],
                    now,
                ),
            )
            if result.rowcount != 1:
                return False
            actual, reserved = self._settle(db, f"{task['id']}:{task['fence']}", envelope)
            self.event(
                db,
                task["id"],
                kind="completed",
                state=state,
                fence=task["fence"],
                envelope=envelope,
                actual_tokens=actual,
                reservation_liability=reserved if actual is None else actual,
                output=output,
                source_signature=task["source_signature"],
                capability=task["capability"],
                version=task["version"],
                financial_attribution=current.get("financial_attribution"),
            )
            return True

    def _carrier(self):
        """The object that physically carries the request bytes."""
        if self.transport is not None:
            return self.transport()
        owner = getattr(self.provider, "__self__", None)
        return self.store.ai if owner is self else (owner if owner is not None else self.provider)

    def _default_provider(self, *args):
        return self.store.ai.evidence(*args)

    def _dispatch_gate(self, task):
        return DispatchGate(self, task)

    def execute(self, tid):
        if self.stop_event.is_set():
            return False
        if not self.call_slots.acquire(blocking=False):
            return False
        owner = uuid.uuid4().hex
        try:
            try:
                task = self.claim(tid, owner)
            except Exception:
                # Lookup, never replay a possibly acknowledged reservation.
                with self.transaction() as db:
                    task = self._row(db, tid)
                    if (
                        task["owner"] != owner
                        or task["state"] != "leased"
                        or task["lease_until"] <= self.now(db)
                    ):
                        raise
        except BaseException:
            self.call_slots.release()
            raise
        if task is None:
            self.call_slots.release()
            return False
        with telemetry.operation("invoke_workflow", parent=task.get("traceparent"),
                                 capability=task["capability"]) as observation:
            return self._execute_claimed(task, observation)

    def _execute_claimed(self, task, observation):
        refusal = contract_refusal(task)
        if refusal:
            observation.fail("rejected")
            self.call_slots.release()
            return self.complete(
                task,
                dict(outcome="data-contract-refused", usage=None, source="unverified"),
                None,
                refusal + " Manual review required.",
            )
        system, prompt = build_request(task)
        if len(system) + len(prompt) > self.limits.input_chars:
            observation.fail("rejected")
            self.call_slots.release()
            return self.complete(
                task,
                dict(outcome="input-too-large", usage=None, source="unverified"),
                None,
                "Input exceeds limit; manual review required.",
            )
        started = time.perf_counter()
        returned, values = threading.Event(), []

        captured = self._captured_sensors(task)

        def call():
            gate = self._dispatch_gate(task)
            if task["capability"] == "quality-evidence":
                from . import chat_demo_meter  # deferred: ai_registry imports this module

                chat_demo_meter.ensure_quality(self.store, self.limits.output_tokens)
            try:
                context = ai_consumption.CallContext(
                    ai_consumption.reference(task["id"]),
                    ai_consumption.reference(f"{task['id']}:{task['fence']}"),
                    task["capability"],
                    "retrofit-case",
                    task["claim_binding"],
                    ai_consumption.reference(
                        runtime_binding(task["capability"], self.store.ai)["prompt_version"]
                    ),
                    retry=task["attempts"] - 1,
                )
                with (
                    ai_consumption.call_context(context),
                    ai_consumption.captured_readings(captured),
                    ai_consumption.send_fence(
                        lambda: self.fence_send(f"{task['id']}:{task['fence']}", task["capability"])
                    ),
                ):
                    gate()
                    values.append(
                        self.provider(
                            system, prompt, self.limits.output_tokens, self.limits.timeout
                        )
                    )
            except ai_consumption.DispatchWithdrawn:
                values.append(
                    dict(
                        outcome="suspended-before-dispatch",
                        usage=None,
                        source="unverified",
                        text=None,
                    )
                )
            except Exception:
                values.append(
                    dict(outcome="provider-unavailable", usage=None, source="unverified", text=None)
                )
            finally:
                gate.release()
                # A timed-out physical call continues owning its local slot until it returns.
                self.call_slots.release()
                returned.set()

        with self.transaction() as db:
            held = self.suspended(db, task["capability"]) or (
                self.admission(db, task["capability"]) or {}
            ).get("reason")
            if not held and not continuity.epoch_current(task, self.continuity(db)):
                held = "Epoch changed before dispatch; use the manual route."
            if not held and task.get("release") != self.release_reference(db, task["capability"]):
                held = "Release changed before dispatch; use the manual route."
            if not held and not self._sensors_granted(db, task):
                held = "Monitoring consent is not granted now; readings were not sent. Use the manual route."
            if not held and captured and not may_carry_captured_readings(self._carrier()):
                held = (
                    "Captured sensor readings cannot be sent to a real AI model in this release; they were "
                    "not sent. Use the manual route."
                )
        if held:
            observation.fail("rejected")
            self.call_slots.release()
            return self.complete(
                task,
                dict(outcome="suspended-before-dispatch", usage=None, source="unverified"),
                None,
                held,
            )
        try:
            with self.dispatch_lock:
                stopped = self.stop_event.is_set()
                if not stopped:
                    thread_context = contextvars.copy_context()
                    threading.Thread(target=thread_context.run, args=(call,), daemon=True, name="retrofit-provider").start()
        except RuntimeError:
            observation.fail()
            self.call_slots.release()
            return self.complete(
                task,
                dict(outcome="provider-unavailable", usage=None, source="unverified"),
                None,
                "Provider dispatch unavailable; use manual work.",
            )
        if stopped:
            observation.fail("cancelled")
            self.call_slots.release()
            return self.complete(
                task,
                dict(outcome="shutdown", usage=None, source="unverified"),
                None,
                "Assistance stopped before dispatch; use manual work.",
            )
        while not returned.wait(0.1):
            if self.stop_event.is_set() or time.perf_counter() - started >= self.limits.timeout:
                break
        result = (
            values[0]
            if returned.is_set() and time.perf_counter() - started <= self.limits.timeout
            else dict(outcome="timeout", usage=None, source="unverified", text=None)
        )
        envelope, output, failure = shape_result(
            task, result, self.limits, guard_telemetry=self.guard_telemetry
        )
        if failure:
            observation.fail("timeout" if result.get("outcome") == "timeout" else "error")
        try:
            self._guard_local.already_guarded = True
            try:
                return self.complete(task, envelope, output, failure)
            finally:
                self._guard_local.already_guarded = False
        except Exception:
            # Completion acknowledgement may have been lost. Never dispatch the provider again here.
            with self.transaction() as db:
                current = self._row(db, task["id"])
                return current["fence"] == task["fence"] and current["state"] in ("ready", "failed", "pending")

    def review(self, user, tid, action, revision, note="", output=None, source_verified=False):
        if not self.sql:
            raise ValueError(self.disabled())
        if action not in ("verify", "accept", "edit-accept", "reject"):
            raise ValueError("Choose verify, accept, edit-accept or reject.")
        if not isinstance(note, str) or not 1 <= len(note.strip()) <= 1000:
            raise ValueError("Record a bounded source verification/review note.")
        with self.transaction() as db:
            task = self._view(db, user, tid)
            if type(revision) is not int or revision != task["revision"]:
                raise ConflictError(tid)
            # The view may be a consent projection. Checks use it; the write uses the stored record.
            stored = self._row(db, tid)
            if action != "reject":
                if task.get("sensor_withheld"):
                    raise PermissionError(
                        "Monitoring consent is not granted now, so the readings cannot be verified. Use the manual route or reject."
                    )
                if not task["epoch_current"]:
                    raise PermissionError(
                        "Proposal epoch changed or is unavailable; request fresh work or use the manual route."
                    )
                if task["suspension"]:
                    raise PermissionError(self.suspended(db, task["capability"]))
                if task["release_denial"]:
                    raise ReleaseDenied(task["release_denial"]["reason"])
                if (
                    task["stale"]
                    or task["state"] != "ready"
                    or task["output"] is None
                    or task["envelope"].get("source") != "ai"
                ):
                    raise ValueError(
                        "Only current, valid AI proposals can be verified/accepted. Use manual work or reject."
                    )
                validate_output(task["output"], task["snapshot"], self.limits.output_chars)
                c = self.authorize(db, user, task["capability"], task["case_id"])
                if task["capability"] == "quality-evidence":
                    current_actor = self.authorize(db, user, task["capability"])
                    for rec in quality.active_records(c.get("quality", [])):
                        self.store._independent(rec, current_actor, "review quality evidence")
                if action == "verify":
                    if source_verified is not True:
                        raise ValueError("Explicit human source verification is required.")
                    stored["verification"] = dict(
                        by=user["email"],
                        signature=task["source_signature"],
                        note=note,
                        at=self.now(db),
                    )
                else:
                    verification = task.get("verification")
                    if (
                        not verification
                        or verification["by"] != user["email"]
                        or verification["signature"] != task["source_signature"]
                    ):
                        raise ValueError(
                            "Record your human source verification before accept/edit."
                        )
                    if action == "edit-accept":
                        stored["output"] = validate_output(
                            output,
                            task["snapshot"],
                            self.limits.output_chars,
                            guard_telemetry=self.guard_telemetry,
                        )
                    stored["review"] = dict(
                        action=action, by=user["email"], note=note, at=self.now(db)
                    )
            else:
                stored["review"] = dict(action=action, by=user["email"], note=note, at=self.now(db))
            state = (
                task["state"]
                if action == "verify"
                else ("rejected" if action == "reject" else "accepted")
            )
            for key in TRANSIENT_VIEW_KEYS:
                stored.pop(key, None)
            if action != "verify" and (task.get("envelope") or {}).get("meter_root"):
                try:
                    self.consumption.review(
                        tid,
                        action,
                        db=db,
                        root=task["envelope"]["meter_root"] if action == "reject" else None,
                    )
                except ai_consumption.DispatchHeld as error:
                    if action != "reject":
                        raise
                    self.consumption.review_unresolved(
                        task["envelope"]["meter_root"],
                        tid,
                        str(error),
                        revision=revision + 1,
                        db=db,
                    )
                    stored["financial_attribution"] = dict(
                        status="unresolved", reason=str(error), action=action
                    )
            if action == "reject":
                res = db.execute(
                    "UPDATE assistant_tasks SET body=?,state=?,revision=revision+1 WHERE id=? AND revision=?",
                    (canonical(stored), state, tid, revision),
                )
            else:
                res = db.execute(
                    "UPDATE assistant_tasks SET body=?,state=?,review_gate_version=?,reviewed_revision=revision+1,revision=revision+1 WHERE id=? AND revision=?",
                    (canonical(stored), state, continuity.GATE_VERSION, tid, revision),
                )
            if res.rowcount != 1:
                raise ConflictError(tid)
            self.event(
                db,
                tid,
                kind="review",
                action=action,
                reviewer=user["email"],
                note=note,
                source_verified=action == "verify",
                source_signature=task["source_signature"],
                edited_output=stored["output"] if action == "edit-accept" else None,
                financial_attribution=stored.get("financial_attribution"),
            )
        return self.detail(user, tid)

    def _authorize_challenge_staff(self, db, user, case_id):
        entra = identity.is_entra(user)
        if entra:
            verified = identity.verified(user)
            if verified is None or verified.get("view_only"):
                raise PermissionError("Current staff role has changed or been revoked.")
        row = db.execute("SELECT body FROM staff WHERE email=?", (user.get("email", "").lower(),)).fetchone()
        current = json.loads(row[0]) if row else None
        if (not current or current.get("role") != user.get("role") or current.get("disabled")
                or (entra and (current.get("oid") != user.get("oid")
                               or not identity.row_tenant_ok(self.store, current, user.get("tid"))))
                or current.get("active") is False
                or current.get("email", "").lower() != user.get("email", "").lower()):
            raise PermissionError("Current staff role has changed or been revoked.")
        if not projection.appointment_evidence_visible(current):
            raise PermissionError(
                "Challenge records need current resident-workflow and recorded-reason rights."
            )
        for field in ("case_ids", "areas"):
            values = current.get(field)
            if values is not None and (
                not isinstance(values, list) or len(values) > 1000
                or any(not isinstance(x, str) or not 1 <= len(x) <= 128 for x in values)
            ):
                raise PermissionError("Current staff scope is malformed; resolve it manually.")
        ids = current.get("case_ids")
        if ids is not None and case_id not in ids:
            raise PermissionError("Case is outside your current scope.")
        crow = db.execute("SELECT body FROM cases WHERE id=?", (case_id,)).fetchone()
        if crow is None:
            raise KeyError(case_id)
        case = json.loads(crow[0])
        areas = current.get("areas")
        if areas is not None and case.get("home", {}).get("area") not in areas:
            raise PermissionError("Case area is outside your current scope.")
        return current, case

    @staticmethod
    def _challenge_staff_identity(person):
        return dict(email=person["email"], name=person["name"], role=person["role"],
                    code=person.get("code", ""))

    @staticmethod
    def _iso_date(value, label):
        if not isinstance(value, str):
            raise ValueError(f"Enter {label} as YYYY-MM-DD.")
        cleaned = value.strip()
        try:
            return date.fromisoformat(cleaned).isoformat()
        except ValueError:
            raise ValueError(f"Enter {label} as YYYY-MM-DD.") from None

    @staticmethod
    def _submitter_meta(case, body):
        submitted_by = controls.choice(
            body.get("submitted_by", "The resident"),
            ASSISTANT_CHALLENGE_SUBMITTERS,
            "who submitted the challenge",
        )
        raw_ref = body.get("representative_ref")
        if submitted_by == "The resident":
            if raw_ref is not None and str(raw_ref).strip():
                raise ValueError(
                    "Do not supply representative_ref when the resident submitted directly."
                )
            return dict(submitted_by=submitted_by, representative_ref=None,
                        representative_authority_status="Direct resident submission")
        rep_ref = controls.evidence_text(raw_ref, "the representative or nominee reference")
        auth_status = "Unverified representative; challenge accepted without inferring consent"
        raw_auths = case.get("representative_authorities")
        if isinstance(raw_auths, dict):
            versions = raw_auths.get(rep_ref)
            if isinstance(versions, list) and versions and isinstance(versions[-1], dict):
                state = str(versions[-1].get("status") or "Recorded")
                if state in ("Confirmed", "Verified"):
                    auth_status = f"Verified representative authority ({rep_ref})"
        elif isinstance(raw_auths, list):
            for auth in raw_auths:
                if isinstance(auth, dict) and rep_ref in (
                    auth.get("id"), auth.get("representative"), auth.get("evidence_ref"),
                    auth.get("representative_ref"),
                ):
                    state = str(auth.get("status") or "Recorded")
                    if state in ("Confirmed", "Verified"):
                        auth_status = f"Verified representative authority ({rep_ref})"
                    break
        return dict(submitted_by=submitted_by, representative_ref=rep_ref,
                    representative_authority_status=auth_status)

    def challenge(self, user, tid, body):
        if not self.sql:
            raise ValueError(self.disabled())
        if not isinstance(body, dict):
            raise ValueError("Challenge request must be a JSON object.")
        controls.refuse_bulk(body)
        challenges.reject_adverse_mapping(body, "Assistant proposal challenge")
        sub_action = body.get("action")
        if sub_action not in ASSISTANT_CHALLENGE_ACTIONS:
            raise ValueError("Choose open, update, reopen, escalate or resolve.")
        revision = body.get("revision")
        if type(revision) is not int or revision < 1:
            raise ValueError("Supply the integer proposal revision.")
        schemas = {
            "open": (
                {"action", "revision", "target_kind", "channel", "source", "request",
                 "explanation", "owner", "non_digital_route", "next_update"},
                {"submitted_by", "representative_ref", "hazard_concern", "hazard_intake"},
            ),
            "update": (
                {"action", "revision", "id", "expected_version", "detail", "source", "next_update"},
                {"channel", "submitted_by", "representative_ref", "hazard_concern", "hazard_intake"},
            ),
            "reopen": (
                {"action", "revision", "id", "expected_version", "reason", "source", "next_update"},
                {"channel", "submitted_by", "representative_ref", "owner",
                 "hazard_concern", "hazard_intake"},
            ),
            "escalate": (
                {"action", "revision", "id", "expected_version", "reason", "escalated_to",
                 "next_update"},
                set(),
            ),
            "resolve": (
                {"action", "revision", "id", "expected_version", "resolution", "resolution_ref",
                 "explanation", "next_update"},
                set(),
            ),
        }
        req_keys, opt_keys = schemas[sub_action]
        if not (req_keys <= set(body) <= req_keys | opt_keys):
            raise ValueError(
                "Supply only the permitted assistant challenge fields; server fields are automatic."
            )
        flag = body.get("hazard_concern", False)
        if not isinstance(flag, bool):
            raise ValueError("hazard_concern must be true or false.")
        intake = body.get("hazard_intake")
        if intake is not None and not flag:
            raise ValueError("Set hazard_concern to true when supplying hazard_intake.")
        if intake is not None:
            if not isinstance(intake, dict):
                raise ValueError("hazard_intake must be an object.")
            in_req = {"category", "priority", "source", "aware_at"}
            if not (in_req <= set(intake) <= in_req | {"note"}):
                raise ValueError(
                    "Supply category, priority, source, aware_at and optional note for hazard_intake."
                )
            challenges.reject_adverse_mapping(intake, "Assistant challenge hazard_intake")
        with self.transaction() as db:
            pre = self._row(db, tid)
            actor, case_snapshot = self._authorize_challenge_staff(db, user, pre["case_id"])
            if revision != pre["revision"]:
                raise ConflictError(tid)
            owner_person = None
            if "owner" in body and body["owner"] is not None:
                orow = db.execute(
                    "SELECT body FROM staff WHERE email=?",
                    (str(body["owner"]).strip().lower(),),
                ).fetchone()
                owner_person = json.loads(orow[0]) if orow else None
                if (not owner_person or owner_person.get("disabled")
                        or owner_person.get("active") is False
                        or not projection.appointment_evidence_visible(owner_person)):
                    raise ValueError(
                        "Choose an active named owner with resident-workflow and recorded-reason rights."
                    )
            escalated_person = None
            if sub_action == "escalate":
                erow = db.execute(
                    "SELECT body FROM staff WHERE email=?",
                    (str(body["escalated_to"]).strip().lower(),),
                ).fetchone()
                escalated_person = json.loads(erow[0]) if erow else None
                if (not escalated_person or escalated_person.get("disabled")
                        or escalated_person.get("active") is False
                        or not projection.appointment_evidence_visible(escalated_person)):
                    raise ValueError(
                        "Choose an active escalation owner with resident-workflow and recorded-reason rights."
                    )
            existing_list = pre.get("challenges") or []
            if sub_action != "open":
                cid_req = controls.text(body.get("id"), "a recorded challenge ID", 24)
                exp_ver = body.get("expected_version")
                if type(exp_ver) is not int or exp_ver < 1:
                    raise ValueError("Supply the integer expected_version for the challenge.")
                matched = next((r for r in existing_list if r.get("id") == cid_req), None)
                if matched is None:
                    raise ValueError("Choose a recorded challenge on this assistant proposal.")
                if exp_ver != matched.get("version"):
                    raise ConflictError(cid_req)
                if sub_action == "reopen" and matched.get("status") != "Resolved":
                    raise ValueError("Only a resolved challenge can be reopened.")
                if sub_action in ("update", "escalate", "resolve") and matched.get("status") == "Resolved":
                    raise ValueError("Reopen a resolved challenge before updating, escalating or resolving it.")
            if sub_action == "open":
                target_kind = controls.choice(
                    body.get("target_kind"), ASSISTANT_CHALLENGE_TARGETS, "proposal, source or policy"
                )
                channel = controls.choice(
                    body.get("channel"), ASSISTANT_CHALLENGE_CHANNELS, "a challenge channel"
                )
                submitter = self._submitter_meta(case_snapshot, body)
                source = controls.evidence_text(body.get("source"), "the challenge evidence reference")
                request_txt = controls.text(body.get("request"), "the person's supplied request", 300)
                explanation_txt = controls.text(body.get("explanation"), "the plain-language explanation", 300)
                non_digital = controls.text(body.get("non_digital_route"), "the accessible non-digital route", 240)
                next_upd = self._iso_date(body.get("next_update"), "the next update date")
            elif sub_action == "update":
                detail_txt = controls.text(body.get("detail"), "the challenge update detail", 300)
                source = controls.evidence_text(body.get("source"), "the update evidence reference")
                next_upd = self._iso_date(body.get("next_update"), "the next update date")
                upd_channel = (
                    controls.choice(body.get("channel"), ASSISTANT_CHALLENGE_CHANNELS, "a challenge channel")
                    if body.get("channel") is not None else None
                )
                upd_submitter = (
                    self._submitter_meta(case_snapshot, body)
                    if ("submitted_by" in body or "representative_ref" in body) else None
                )
            elif sub_action == "reopen":
                reason_txt = controls.text(body.get("reason"), "the reason to reopen", 300)
                source = controls.evidence_text(body.get("source"), "the reopen evidence reference")
                next_upd = self._iso_date(body.get("next_update"), "the next update date")
                reopen_channel = (
                    controls.choice(body.get("channel"), ASSISTANT_CHALLENGE_CHANNELS, "a challenge channel")
                    if body.get("channel") is not None else None
                )
                reopen_submitter = (
                    self._submitter_meta(case_snapshot, body)
                    if ("submitted_by" in body or "representative_ref" in body) else None
                )
            elif sub_action == "escalate":
                reason_txt = controls.text(body.get("reason"), "the escalation reason", 300)
                next_upd = self._iso_date(body.get("next_update"), "the next update date")
            else:
                res_outcome = controls.choice(
                    body.get("resolution"), ASSISTANT_CHALLENGE_RESOLUTIONS, "the human resolution"
                )
                res_ref = controls.evidence_text(body.get("resolution_ref"), "the resolution evidence reference")
                explanation_txt = controls.text(body.get("explanation"), "the resolution explanation", 300)
                next_upd = self._iso_date(body.get("next_update"), "the next update date")
        case_id = pre["case_id"]
        capability = pre["capability"]
        with self.store.lock:
            before_case = deepcopy(self.store._case(case_id))
            self.store._ranks = None
            before_ranking = self.store._ranking()
        routed_idx = None
        if intake is not None:
            routed_idx = self.store.raise_hazard(
                actor,
                case_id,
                intake["category"],
                intake["priority"],
                str(intake.get("note") or ""),
                dict(source=intake["source"], aware_at=intake["aware_at"]),
            )
        with self.store.lock:
            after_case = deepcopy(self.store._case(case_id))
            self.store._ranks = None
            after_ranking = self.store._ranking()
            challenges.assert_no_adverse_challenge_effects(
                before_case,
                after_case,
                allow_new_independent_hazard=routed_idx is not None,
            )
            b_rank = before_ranking.get(case_id)
            a_rank = after_ranking.get(case_id)
            lowered = b_rank is not None and a_rank is not None and a_rank["rank"] > b_rank["rank"]
            if lowered or (routed_idx is None and after_ranking != before_ranking):
                raise challenges.ChallengeSafeguardError(
                    "Assistant proposal challenge lowered or altered case priority ranking."
                )
        at_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
        actor_ident = self._challenge_staff_identity(actor)
        with self.transaction() as db:
            stored = self._row(db, tid)
            if revision != stored["revision"]:
                raise ConflictError(tid)
            for key in TRANSIENT_VIEW_KEYS:
                stored.pop(key, None)
            items = list(stored.get("challenges") or [])
            if sub_action == "open":
                assert owner_person is not None
                target_id = (
                    tid if target_kind == "proposal"
                    else (f"case:{case_id}" if target_kind == "source" else f"rule:{RULE_VERSION}")
                )
                record = dict(
                    id=controls.next_id(items, "ACH"),
                    version=1,
                    status="Open",
                    proposal_id=tid,
                    proposal_kind="assistant_task",
                    capability=capability,
                    case_id=case_id,
                    source_signature=stored["source_signature"],
                    target=dict(kind=target_kind, id=target_id, version=stored["source_signature"]),
                    channel=channel,
                    source=source,
                    request=request_txt,
                    explanation=explanation_txt,
                    owner=self._challenge_staff_identity(owner_person),
                    non_digital_route=non_digital,
                    next_update=next_upd,
                    recorded_by=actor_ident,
                    opened_at=at_iso,
                    updated_at=at_iso,
                    updates=[],
                    escalations=[],
                    resolution=None,
                    hazard_referral=None,
                    **submitter,
                )
                items.append(record)
                event_note = request_txt
            else:
                cid_req = str(body["id"]).strip()
                record = next(r for r in items if r["id"] == cid_req)
                if record["version"] != body["expected_version"]:
                    raise ConflictError(cid_req)
                record["version"] += 1
                record["updated_at"] = at_iso
                record["next_update"] = next_upd
                if sub_action == "update":
                    if upd_channel is not None:
                        record["channel"] = upd_channel
                    if upd_submitter is not None:
                        record.update(upd_submitter)
                    record.setdefault("updates", []).append(dict(
                        kind="update", detail=detail_txt, source=source,
                        recorded_by=actor_ident, recorded_at=at_iso, next_update=next_upd,
                        channel=record["channel"], submitted_by=record.get("submitted_by", "The resident"),
                    ))
                    event_note = detail_txt
                elif sub_action == "reopen":
                    prior = record.get("resolution")
                    if isinstance(prior, dict):
                        record.setdefault("previous_resolutions", []).append(deepcopy(prior))
                        if prior.get("outcome") == "Correction recorded":
                            record["prior_correction_preserved"] = True
                    record["resolution"] = None
                    record["status"] = "Open"
                    if reopen_channel is not None:
                        record["channel"] = reopen_channel
                    if reopen_submitter is not None:
                        record.update(reopen_submitter)
                    if owner_person is not None:
                        record["owner"] = self._challenge_staff_identity(owner_person)
                    record.setdefault("updates", []).append(dict(
                        kind="reopen", detail=reason_txt, source=source,
                        recorded_by=actor_ident, recorded_at=at_iso, next_update=next_upd,
                        channel=record["channel"], submitted_by=record.get("submitted_by", "The resident"),
                    ))
                    event_note = reason_txt
                elif sub_action == "escalate":
                    assert escalated_person is not None
                    esc_ident = self._challenge_staff_identity(escalated_person)
                    record["status"] = "Escalated"
                    record["owner"] = esc_ident
                    record.setdefault("escalations", []).append(dict(
                        reason=reason_txt, escalated_to=esc_ident,
                        recorded_by=actor_ident, recorded_at=at_iso, next_update=next_upd,
                    ))
                    event_note = reason_txt
                else:
                    record["status"] = "Resolved"
                    record["resolution"] = dict(
                        outcome=res_outcome, reference=res_ref, explanation=explanation_txt,
                        recorded_by=actor_ident, recorded_at=at_iso, next_update=next_upd,
                    )
                    if res_outcome == "Correction recorded":
                        stored["challenged_stale"] = dict(
                            challenge_id=record["id"],
                            target_kind=record["target"]["kind"],
                            source_signature=stored["source_signature"],
                            recorded_at=at_iso,
                            recorded_by=actor["email"],
                            reference=res_ref,
                        )
                    event_note = explanation_txt
            if flag:
                existing_ref = record.get("hazard_referral")
                if existing_ref is None:
                    existing_ref = dict(
                        status="referred_on_receipt",
                        received_at=at_iso,
                        route="emergency_or_statutory_hazard_triage",
                        independent_intake=True,
                        waits_for_challenge_review=False,
                        hazard_clock_preserved=True,
                    )
                else:
                    existing_ref = dict(
                        existing_ref,
                        independent_intake=True,
                        waits_for_challenge_review=False,
                        hazard_clock_preserved=True,
                    )
                if routed_idx is not None:
                    existing_ref["routed_hazard_index"] = routed_idx
                record["hazard_referral"] = existing_ref
            ref_now = record.get("hazard_referral")
            record["safeguards"] = dict(challenges.SAFEGUARDS)
            record["hazard_clock_preserved"] = True
            record["non_retaliation_assurance"] = challenges.build_non_retaliation_assurance(
                hazard_concern=ref_now is not None,
                independent_hazard_routed=(ref_now or {}).get("routed_hazard_index") is not None,
            )
            stored["challenges"] = items
            state = stored.get("state", "ready")
            for key in ("state", "fence", "owner", "lease_until", "attempts", "not_before", "revision"):
                stored.pop(key, None)
            res = db.execute(
                "UPDATE assistant_tasks SET body=?,state=?,review_gate_version=?,"
                "reviewed_revision=revision+1,revision=revision+1 WHERE id=? AND revision=?",
                (canonical(stored), state, continuity.GATE_VERSION, tid, revision),
            )
            if res.rowcount != 1:
                raise ConflictError(tid)
            self.event(
                db, tid, kind="challenge", action=sub_action, challenge_id=record["id"],
                actor=actor["email"], note=event_note,
                non_retaliation_assurance="verified", hazard_clock_preserved=True,
            )
            updated_revision = revision + 1
            challenged_stale_flag = bool(stored.get("challenged_stale"))
            projected_challenges = deepcopy(items)
        self.store.audit(
            actor["email"],
            f"assistant_challenge_{sub_action}",
            case_id,
            f"{tid[:12]} {record['id']}; non_retaliation_assurance=verified; hazard_clock_preserved=true",
        )
        if user.get("role") in REGISTRY[capability]["roles"]:
            return self.detail(user, tid)
        any_flagged = any(r.get("hazard_referral") is not None for r in projected_challenges)
        any_routed = any(
            (r.get("hazard_referral") or {}).get("routed_hazard_index") is not None
            for r in projected_challenges
        )
        return dict(
            id=tid,
            capability=capability,
            case_id=case_id,
            revision=updated_revision,
            stale=challenged_stale_flag,
            actionable=False if challenged_stale_flag else None,
            challenges=projected_challenges,
            hazard_clock_preserved=True,
            non_retaliation_assurance=challenges.build_non_retaliation_assurance(
                hazard_concern=any_flagged, independent_hazard_routed=any_routed
            ),
        )

    def _worker(self):
        while not self.stop_event.is_set():
            delay = 1
            try:
                with self.transaction() as db:
                    now = self.now(db)
                    query = "SELECT id FROM assistant_tasks WHERE (state='pending' AND not_before<=?) OR (state='leased' AND lease_until<=?) ORDER BY id"
                    query += " OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY" if self.mssql else " LIMIT 1"
                    row = db.execute(query, (now, now)).fetchone()
                if row:
                    if self.execute(row[0]):
                        continue
            except Exception:
                LOG.warning(
                    "Retrofit assistant worker failed; manual work remains available; bounded retry pending."
                )
                delay = self.limits.backoff
            self.stop_event.wait(delay)

    def _scanner(self):
        while not self.stop_event.is_set():
            try:
                self.scan()
            except Exception:
                LOG.warning(
                    "Retrofit assistant scan failed; manual work remains available; next bounded scan pending."
                )
            self.stop_event.wait(self.limits.scan_interval)

    def start(self):
        if self.threads or not self.sql or not self.limits.valid:
            return
        self.stop_event.clear()
        for target in [self._worker] * self.limits.active_calls + (
            [self._scanner] if self.limits.proactive else []
        ):
            t = threading.Thread(target=target, daemon=True, name="retrofit-assistant")
            self.threads.append(t)
            t.start()

    def stop(self):
        with self.dispatch_lock:
            self.stop_event.set()
        for t in self.threads:
            t.join(timeout=0.2)
        # A bounded network call may still finish; SQL fencing/expiry owns correctness.
