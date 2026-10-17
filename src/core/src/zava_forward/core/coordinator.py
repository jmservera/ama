"""Current authorized populations and partial observed flow; never inferred history."""

import logging
import math
from collections.abc import Mapping
from typing import Any

from . import insights, progress, projection, ranking, taskqueues
from .export_fields import scalars

Record = dict[str, Any]
UNKNOWN = "Unknown (not recorded)"
FILTERS = frozenset({"stage", "area", "wave", "owner", "contractor", "flag", "queue"})
METRICS = frozenset(
    {
        "current",
        "entries",
        "exits",
        "returns",
        "reopens",
        "stopped",
        "unknown_history",
        "missing_geocode",
        "priority",
        "filtered_out",
    }
)
PARAMETERS = FILTERS | {
    "view",
    "q",
    "as_of",
    "start",
    "group_by",
    "group",
    "metric",
    "metric_stage",
    "limit",
    "offset",
    "zoom",
    "bbox",
}
DEFINITIONS = {
    "population": "Current authorized open records; not reconstructed at the event cutoff.",
    "denominator": "Source-filtered current cases, before group or metric drill selection.",
    "current": "Current stage occupancy, not stage occupancy at the event cutoff.",
    "entries": "Distinct cases with a trusted recorded transition into this stage in the period.",
    "exits": "Distinct cases with a trusted recorded transition out of this stage in the period.",
    "returns": "Distinct cases with a recorded return into this stage; not event occurrences.",
    "reopens": "Distinct cases with a recorded reopen into this stage; not case completion.",
    "stopped": "Current paused stage or an existing task blocker marked current_stop; cases once.",
    "priority": "Existing owner-approved policy only; a draft rule order is not approved priority.",
    "unknown_history": "No trusted stage transitions in this period; legacy history stays unknown.",
    "missing_geocode": "Missing or invalid coordinates; these cases remain in the total.",
    "filtered_out": "Authorized baseline minus source selection; not lifecycle exclusion.",
    "lifecycle_exclusions": "Unknown: no authoritative lifecycle exclusion stream is available.",
    "conversion": "Unknown: incomplete entries/exits cannot establish a conversion rate.",
    "period": "Inclusive UTC period; current stage and metric_stage are independent selectors.",
    "overlap": "A case can appear in several stages/metrics. Rows are not an additive conversion.",
    "coverage": "Observed stage evidence is partial, never complete historical coverage.",
}


def _number(query: Mapping[str, str], key: str, default: int, low: int, high: int) -> int:
    raw = query.get(key, str(default))
    try:
        value = int(raw)
    except (ValueError, TypeError):
        raise ValueError(f"{key} must be a whole number from {low} to {high}.") from None
    if not low <= value <= high:
        raise ValueError(f"{key} must be a whole number from {low} to {high}.")
    return value


def _geocoded(case: Record) -> bool:
    home = case["home"]
    lat, lon = home.get("lat"), home.get("lon")
    return (
        type(lat) in (int, float)
        and type(lon) in (int, float)
        and math.isfinite(lat)
        and math.isfinite(lon)
        and -90 <= lat <= 90
        and -180 <= lon <= 180
    )


def _group(case: Record, by: str) -> str:
    value = (
        case.get("building_id")
        if by == "building"
        else case["home"].get("area" if by == "area" else "type")
    )
    if value is not None and not isinstance(value, str):
        raise ValueError("Grouping field is malformed; inspect the manual case record.")
    return value.strip() if value and value.strip() else UNKNOWN


def _bounds(raw: str | None) -> tuple[float, float, float, float] | None:
    if raw is None:
        return None
    try:
        parts = [float(x) for x in raw.split(",")]
    except ValueError:
        raise ValueError("Map bounds require south,west,north,east numbers.") from None
    if (
        len(parts) != 4
        or not all(math.isfinite(x) for x in parts)
        or not -90 <= parts[0] <= parts[2] <= 90
        or not -180 <= parts[1] <= parts[3] <= 180
    ):
        raise ValueError("Map bounds require ordered geographic coordinates.")
    return parts[0], parts[1], parts[2], parts[3]


def read(store: Any, user: Record, query: Mapping[str, str]) -> Record:
    """Read through the existing synchronized Store boundary without adding a writer."""
    if user.get("role") not in projection.STAFF_ROLES:
        raise PermissionError("Only registered staff can read the coordinator view.")
    if set(query) - PARAMETERS or any(
        not isinstance(v, str) or not v.strip() for v in query.values()
    ):
        raise ValueError("Unknown or empty coordinator parameter; clear it and try again.")
    view, by, metric = (
        query.get("view", "mine"),
        query.get("group_by", "area"),
        query.get("metric", "current"),
    )
    if view not in ("mine", "all"):
        raise ValueError("Choose mine or all current open cases.")
    if by not in ("area", "building", "archetype") or metric not in METRICS:
        raise ValueError("Choose a published grouping and count definition.")
    if query.get("flag", "") not in (
        "",
        "hazard",
        "support",
        "long",
        "nodecision",
        "fundingprog",
        "funding",
    ):
        raise ValueError("Choose a published case signal.")
    if query.get("metric_stage") and query["metric_stage"] not in progress.STAGES:
        raise ValueError("Choose a published lifecycle stage for drillthrough.")
    if metric == "filtered_out" and ("group" in query or "metric_stage" in query):
        raise ValueError("Filter exclusions cannot also select a heatmap or stage cell.")
    if metric not in ("current", "entries", "exits", "returns", "reopens", "stopped") and (
        "metric_stage" in query
    ):
        raise ValueError("This count has no lifecycle stage selector.")
    limit = _number(query, "limit", 50, 1, 100)
    offset = _number(query, "offset", 0, 0, 10**9)
    zoom = _number(query, "zoom", 8, 0, 20)
    bounds = _bounds(query.get("bbox"))
    text = query.get("q", "")
    if len(text) > 200:
        raise ValueError("Search must be at most 200 characters.")
    filters = {k: query[k] for k in FILTERS if k in query}
    taskqueues.validate_queue(filters.get("queue", ""))
    with store.lock:
        actor = store.staff.get(user.get("email"))
        if (
            actor is None
            or actor.get("role") not in projection.STAFF_ROLES
            or any(actor.get(k) != user.get(k) for k in ("email", "code", "role"))
        ):
            raise PermissionError("Your staff access has changed; sign in again.")
        baseline = store._filtered(actor, view, "", {})
        selected = store._filtered(actor, view, text, filters)
        cohort = {
            "view": view,
            "filters": filters,
            "q": text,
            "selection_basis": DEFINITIONS["population"],
            "baseline_cases": len(baseline),
            "selected_cases": len(selected),
            "excluded_by_filters": len(baseline) - len(selected),
        }
        try:
            intact = store.verify_ledger()["intact"]
        except (OSError, ValueError, TypeError, KeyError, AttributeError):
            logging.getLogger(__name__).exception("Coordinator audit verification unavailable")
            intact = None
        evidence = progress.report(
            selected,
            as_of=query.get("as_of"),
            start=query.get("start"),
            cohort=cohort,
            scenario=None,
            audit_intact=intact,
        )
        return _assemble(
            store,
            actor,
            query,
            baseline,
            selected,
            cohort,
            evidence,
            by,
            metric,
            limit,
            offset,
            zoom,
            bounds,
        )


def _assemble(
    store: Any,
    actor: Record,
    query: Mapping[str, str],
    baseline: list[Record],
    selected: list[Record],
    cohort: Record,
    evidence: Record,
    by: str,
    metric: str,
    limit: int,
    offset: int,
    zoom: int,
    bounds: tuple[float, float, float, float] | None,
) -> Record:
    ids = {c["id"] for c in selected}
    members: dict[str, set[str]] = {key: set() for key in METRICS}
    members["current"] = ids.copy()
    members["filtered_out"] = {c["id"] for c in baseline} - ids
    stages: dict[str, dict[str, set[str]]] = {}

    def stage_sets(stage: str) -> dict[str, set[str]]:
        return stages.setdefault(
            stage,
            {
                key: set()
                for key in ("current", "entries", "exits", "returns", "reopens", "stopped")
            },
        )

    policy_approved = taskqueues.approved_priority(ranking.CURRENT)
    heat: dict[tuple[str, str], list[Record]] = {}
    groups: set[str] = set()
    for case in selected:
        cid, stage = case["id"], case["stage"]
        stage_sets(stage)["current"].add(cid)
        group = _group(case, by)
        groups.add(group)
        heat.setdefault((group, stage), []).append(case)
        if not _geocoded(case):
            members["missing_geocode"].add(cid)
        context = store.work_context(case, actor)
        if stage in progress.PAUSED or any(b["current_stop"] for b in context["blockers"]):
            members["stopped"].add(cid)
            stage_sets(stage)["stopped"].add(cid)
        if policy_approved and "priority" in context["queues"]:
            members["priority"].add(cid)

    for history in evidence["histories"]:
        cid = history["case_id"]
        # Missing initial entry/final exit does not invalidate an observed transition.
        bad = any(
            e["source"].startswith("returns")
            and e["code"] not in {"unknown_initial_stage_entry", "unknown_stage_exit"}
            for e in history["exceptions"]
        )
        events = (
            [e for e in history["events"] if e["kind"] in ("advance", "return", "reopen")]
            if evidence["audit_integrity"] == "Intact" and not bad
            else []
        )
        if not events:
            members["unknown_history"].add(cid)
        for event in events:
            old, new = event["from_stage"], event["to_stage"]
            members["entries"].add(cid)
            members["exits"].add(cid)
            stage_sets(new)["entries"].add(cid)
            stage_sets(old)["exits"].add(cid)
            key = {"return": "returns", "reopen": "reopens"}.get(event["kind"])
            if key:
                members[key].add(cid)
                stage_sets(new)[key].add(cid)
    if metric == "priority" and not policy_approved:
        raise ValueError("Approved priority is unavailable: the existing policy is not approved.")
    if metric in ("entries", "exits", "returns", "reopens") and (
        evidence["audit_integrity"] != "Intact"
    ):
        raise ValueError("Observed flow is unavailable while audit evidence is untrusted.")
    chosen = members[metric].copy()
    if "metric_stage" in query:
        chosen &= stages.get(query["metric_stage"], {}).get(metric, set())
    if "group" in query:
        chosen &= {c["id"] for c in selected if _group(c, by) == query["group"]}
    drill = [c for c in baseline if c["id"] in chosen]
    mapped = [c for c in drill if _geocoded(c)]
    # Preserve existing closed-field guards and the current marker/cluster policy.
    map_result = insights.map_view(mapped, {}, bounds, zoom, cap=insights.MAP_CAP)
    map_result.update(
        in_view=map_result["total"],
        total=len(drill),
        mapped=len(mapped),
        missing_geocode=len(drill) - len(mapped),
    )
    for point in map_result["items"]:
        if map_result["mode"] == "points":
            point["name"] = point["id"]
            point.pop("address")
    ordered = sorted(drill, key=lambda c: c["id"])
    record_stops = members["stopped"].copy()
    if metric == "filtered_out":
        for case in drill:
            if case["stage"] in progress.PAUSED or any(
                blocker["current_stop"] for blocker in store.work_context(case, actor)["blockers"]
            ):
                record_stops.add(case["id"])
    # Only permitted current fields, never private narratives or historical raw actors.
    records = [
        dict(
            **scalars(c, ("id", "stage")),
            **scalars(c["home"], ("address", "postcode")),
            geocode="Recorded" if _geocoded(c) else "Unknown or invalid",
            stopped=c["id"] in record_stops,
        )
        for c in ordered[offset : offset + limit]
    ]
    order = {stage: i for i, stage in enumerate(insights.STAGE_ORDER + ["Completed"])}
    rows = [
        dict(
            stage=stage,
            **{key: len(value) for key, value in values.items()},
            denominator=len(selected),
            conversion=None,
            lifecycle_exclusions=None,
        )
        for stage, values in sorted(stages.items(), key=lambda x: (order.get(x[0], 999), x[0]))
    ]
    if evidence["audit_integrity"] != "Intact":
        for row in rows:
            for key in ("entries", "exits", "returns", "reopens"):
                row[key] = None
    counts: Record = {key: len(value) for key, value in members.items() if key != "priority"}
    if evidence["audit_integrity"] != "Intact":
        for key in ("entries", "exits", "returns", "reopens"):
            counts[key] = None
    return dict(
        schema="coordinator/v1",
        cohort=cohort,
        as_of=evidence["as_of"],
        period_start=evidence["period_start"],
        current_as_of=store.as_of,
        approval_status=evidence["approval_status"],
        definitions=DEFINITIONS,
        audit_integrity=evidence["audit_integrity"],
        data_limits=progress.LIMITS,
        priority=dict(
            status=ranking.CURRENT["status"],
            version=ranking.CURRENT["version"],
            approved=policy_approved,
            count=len(members["priority"]) if policy_approved else None,
        ),
        counts=counts,
        coverage=dict(
            denominator=len(selected),
            stage_history_partial=len(selected) - len(members["unknown_history"]),
            stage_history_unknown=len(members["unknown_history"]),
            complete_history=0,
            missing_geocode=len(members["missing_geocode"]),
            lifecycle_exclusions=None,
            true_conversion=None,
        ),
        group_by=by,
        groups=sorted(groups),
        heatmap=[
            dict(
                group=group,
                stage=stage,
                count=len(cases),
                denominator=len(selected),
                stopped=sum(c["id"] in members["stopped"] for c in cases),
                missing_geocode=sum(c["id"] in members["missing_geocode"] for c in cases),
                unknown_history=sum(c["id"] in members["unknown_history"] for c in cases),
            )
            for (group, stage), cases in sorted(heat.items())
        ],
        funnel=rows,
        selection=dict(
            metric=metric,
            metric_stage=query.get("metric_stage"),
            group=query.get("group"),
            total=len(drill),
        ),
        records=dict(items=records, total=len(drill), limit=limit, offset=offset),
        map=map_result,
    )
