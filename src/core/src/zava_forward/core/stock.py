"""Owned stock comparisons and explicit support uncertainty, never source authority."""

import logging
from collections.abc import Iterable, Iterator, Mapping
from contextlib import contextmanager
from copy import deepcopy
from datetime import UTC, date, datetime
from typing import Any, Literal

type SupportState = Literal["Yes", "No", "Unknown"]
STOCK_FIELDS = ("epc", "type", "built")
SUPPORT_ENCODING = "1"


@contextmanager
def decision_scope(
    store: Any, user: dict[str, Any], case_id: str
) -> Iterator[tuple[dict[str, Any], dict[str, Any]]]:
    """Bind stock/technical writes to current staff and discard failed SQL decisions."""
    from .change_provenance import _actor

    with store.lock:
        actor = _actor(store, user)
        case = store._case(case_id)
        if not hasattr(store, "db"):
            yield case, actor
            return
        previous = getattr(store.local, "stock_decision", None)
        store.local.stock_decision = dict(user=deepcopy(user), actor=actor)
        try:
            yield case, actor
        except BaseException as error:
            try:
                store._discard()
            except Exception:
                error.add_note("Stock/technical recovery failed; reload to establish the outcome.")
                logging.getLogger(__name__).exception("Stock/technical SQL recovery failed")
            raise
        finally:
            store.local.stock_decision = previous


def validate_sql(store: Any) -> None:
    """Repeat identity validation after acquiring the existing SQL writer lock."""
    from .change_provenance import _actor

    context = getattr(store.local, "stock_decision", None)
    if context is not None and _actor(store, context["user"]) != context["actor"]:
        raise PermissionError("Staff authority changed. Reload before recording this decision.")


def support_status(resident: Mapping[str, object]) -> SupportState:
    """Return observed support, keeping missing evidence distinct from a negative."""
    adjustment = resident.get("adjustment")
    positive = (
        isinstance(adjustment, str)
        and bool(adjustment.strip())
        and adjustment not in ("None", "Unknown")
    )
    if resident.get("priority_support") is True or positive:
        return "Yes"
    if resident.get("priority_support") is False and adjustment == "None":
        return "No"
    return "Unknown"


def support_coverage(resident: Mapping[str, object]) -> str:
    """Report incomplete inputs even when another input records a positive need."""
    adjustment = resident.get("adjustment")
    complete = (
        type(resident.get("priority_support")) is bool
        and isinstance(adjustment, str)
        and bool(adjustment.strip())
        and adjustment != "Unknown"
    )
    return "Recorded" if complete else "Unknown"


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 160:
        raise ValueError(f"Add {label}, at most 160 characters.")
    return value.strip()


def _assertion(value: object, field: str) -> dict[str, object]:
    fields = {"value", "source_id", "date", "version", "validation_state"}
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError(
            "Each stock assertion needs value, source_id, date, version and validation_state."
        )
    result: dict[str, object] = {key: _text(value[key], key) for key in fields if key != "value"}
    try:
        observed = date.fromisoformat(str(result["date"]))
    except ValueError:
        raise ValueError("Stock source date must be an ISO date.") from None
    if observed > datetime.now(UTC).date():
        raise ValueError("Stock source date cannot be in the future.")
    if result["validation_state"] not in ("Unvalidated", "Validated", "Disputed", "Unknown"):
        raise ValueError("Choose a recorded stock validation state.")
    raw = value["value"]
    if field == "built":
        if type(raw) is not int or not 1000 <= raw <= datetime.now(UTC).year:
            raise ValueError("Build year must be a recorded integer year.")
    elif field == "epc":
        if not isinstance(raw, str) or raw not in tuple("ABCDEFG"):
            raise ValueError("EPC value must be a recorded band A to G.")
    else:
        raw = _text(raw, "the recorded home type")
    result["value"] = raw
    return result


def comparison(body: Mapping[str, object]) -> dict[str, object]:
    """Validate two competing stock assertions without selecting either as true."""
    if set(body) != {"field", "left", "right", "query_owner"}:
        raise ValueError("A comparison needs exactly field, left, right and query_owner.")
    field = body["field"]
    if not isinstance(field, str) or field not in STOCK_FIELDS:
        raise ValueError("Compare EPC, home type or build year, not resident data.")
    left, right = _assertion(body["left"], field), _assertion(body["right"], field)
    if left["value"] == right["value"]:
        raise ValueError("A conflict needs two different compared values.")
    if (left["source_id"], left["version"]) == (right["source_id"], right["version"]):
        raise ValueError("Use distinct source identifiers or versions.")
    return dict(
        field=field,
        left=left,
        right=right,
        query_owner=_text(body["query_owner"], "a query owner"),
        authority="Unknown",
        resolution="Unknown",
        eligibility="Unknown",
        status="Unresolved",
    )


def query_status(case: Mapping[str, object], query_id: str) -> str:
    """Derive terminal state without rewriting the original comparison."""
    events = case.get("stock_reconciliation_events", [])
    if not isinstance(events, list):
        raise ValueError("Stock reconciliation events must be a list.")
    for event in reversed(events):
        if event["query_id"] == query_id:
            if event["status"] not in ("Withdrawn", "Reconciled"):
                raise ValueError("Unknown stock query event status.")
            return str(event["status"])
    return "Unresolved"


def query_event(body: Mapping[str, object]) -> dict[str, object]:
    """Validate a terminal human disposition, not a winning-source decision."""
    required = {"query_id", "action", "reason"}
    if not required <= set(body) or set(body) - required - {"evidence"}:
        raise ValueError("A query event needs query_id, action, reason and optional evidence.")
    action = body["action"]
    if action not in ("withdraw", "resolve"):
        raise ValueError("Choose withdraw or resolve for the stock query.")
    result: dict[str, object] = dict(
        query_id=_text(body["query_id"], "the query identifier"),
        action=action,
        reason=_text(body["reason"], "the reason"),
        status="Withdrawn" if action == "withdraw" else "Reconciled",
    )
    if action == "resolve" or "evidence" in body:
        result["evidence"] = _text(body.get("evidence"), "the human review evidence reference")
    return result


def blockers(case: Mapping[str, object]) -> list[str]:
    """Expose owned unresolved queries independently of any design record."""
    rows = case.get("stock_reconciliation", [])
    if not isinstance(rows, list):
        raise ValueError("Stock reconciliation must be a list.")
    return [
        f"Stock conflict {row['id']} ({row['field']}) is unresolved. "
        f"Owner: {row['query_owner']['name']}. Next action: obtain source-authority review."
        for row in rows
        if query_status(case, row["id"]) == "Unresolved"
    ]


def queue_rows(cases: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Summarise open stock conflicts per open home, oldest source first. Picks no source."""
    rows: list[dict[str, Any]] = []
    for case in cases:
        if case.get("closed"):
            continue
        open_queries = [
            q
            for q in case.get("stock_reconciliation", [])
            if query_status(case, q["id"]) == "Unresolved"
        ]
        if not open_queries:
            continue
        dates = sorted(
            date.fromisoformat(str(side["date"]))
            for q in open_queries
            for side in (q["left"], q["right"])
        )
        owners = sorted(
            {str(q["query_owner"]["name"]) for q in open_queries if q.get("query_owner")}
        )
        rows.append(
            dict(
                id=case["id"],
                address=case["home"]["address"],
                town=case["home"]["town"],
                open_queries=len(open_queries),
                fields=sorted({str(q["field"]) for q in open_queries}),
                oldest_source_date=dates[0].isoformat(),
                owners=owners,
            )
        )
    rows.sort(key=lambda r: (r["oldest_source_date"], r["id"]))
    return rows
