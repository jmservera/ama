"""Management-view AI consumption economics synthesis and invariants (Issue #100).

Produces the BRD Required Management Views `ai_consumption_economics` summary (BRD FR-052,
NFR-012, OD-51; PRD FR-061, NFR-017) with explicit integer denominators (`proposal_count`,
`accepted_outcome_count`, `metered_call_count`, `unmetered_call_count`) and strict fail-closed
`"Unknown"` semantics whenever a dated price source / approved governance (`OD-51`) / reconciled
billing basis or an accepted-outcome count is absent. Numeric or string zero is never substituted
for an unpriced cost or zero-denominator unit-cost ratio.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping, Sequence
from datetime import UTC, date, datetime
from decimal import Decimal, localcontext
from typing import Any

from . import ai_consumption

SCHEMA = "ai-consumption-economics/v1"
UNKNOWN = ai_consumption.UNKNOWN
DENOMINATOR_KEYS = (
    "proposal_count",
    "accepted_outcome_count",
    "metered_call_count",
    "unmetered_call_count",
)
DENOMINATOR_BASIS = (
    "Human-accepted eligible AI proposals only; workflow/template fallbacks, unreviewed drafts, "
    "held/quarantined outputs, and rejected or withdrawn proposals are excluded from "
    "accepted_outcome_count. Unpriced or zero-denominator costs are Unknown, never zero."
)
NON_BENEFIT_NOTICE = (
    "Token count or token cost alone is not Total Cost of AI and is never evidence of efficiency "
    "or cash benefit; released staff time is capacity unless booked cash value is "
    "Finance-confirmed."
)

_HEX64 = re.compile(r"[0-9a-f]{64}")
_CAPABILITY_ID = re.compile(r"[a-z][a-z0-9_-]{0,63}")
_SAFE_TOKEN = re.compile(r"[A-Za-z0-9_.:/-]{1,64}")
_ZERO_COST_STRINGS = frozenset({"0", "0.0", "0.00", "0.000", "0.0000", "-0", "-0.0"})


def _is_hex64(value: object) -> bool:
    return isinstance(value, str) and bool(_HEX64.fullmatch(value))


def _capability_name(raw: object, *, default: str = "unspecified") -> str:
    if isinstance(raw, str):
        cleaned = raw.strip().lower().replace(" ", "-")
        if _CAPABILITY_ID.fullmatch(cleaned):
            return cleaned
    return default


def _sanitize_owner(raw: object) -> str:
    if not isinstance(raw, str) or not raw.strip():
        return "unassigned"
    text = raw.strip()
    if "@" in text or any(ch.isspace() for ch in text) or not _SAFE_TOKEN.fullmatch(text):
        return "configured-owner"
    return text


def _sanitize_code(raw: object, fallback: str) -> str:
    if isinstance(raw, str):
        text = raw.strip()
        if text and "@" not in text and _SAFE_TOKEN.fullmatch(text):
            return text
    return fallback


def parse_record_timestamp(value: object) -> float | None:
    """Deterministically normalize stored ISO/date strings or epoch numbers to UTC epoch seconds."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        return float(value) if value >= 0 else None
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text:
        return None
    if len(text) == 10 and text[4:5] == "-" and text[7:8] == "-":
        try:
            parsed_day = date.fromisoformat(text)
            return datetime(
                parsed_day.year, parsed_day.month, parsed_day.day, tzinfo=UTC
            ).timestamp()
        except (ValueError, OverflowError, OSError):
            return None
    normalized = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        parsed_dt = datetime.fromisoformat(normalized)
        if parsed_dt.tzinfo is None:
            parsed_dt = parsed_dt.replace(tzinfo=UTC)
        return parsed_dt.astimezone(UTC).timestamp()
    except (ValueError, OverflowError, OSError):
        return None


def _extract_meter_root(rec: Mapping[str, Any]) -> str | None:
    direct = rec.get("meter_root")
    if _is_hex64(direct):
        return str(direct)
    envelope = rec.get("envelope")
    if isinstance(envelope, Mapping):
        nested = envelope.get("meter_root")
        if _is_hex64(nested):
            return str(nested)
    return None


def _rec_capability(rec: Mapping[str, Any]) -> str:
    if rec.get("kind") != "ai_task" and not rec.get("task") and not rec.get("capability"):
        return "priority"
    return _capability_name(rec.get("capability") or rec.get("task"), default="priority")


def _positive_money_str(value: Decimal) -> str:
    if value <= 0:
        return UNKNOWN
    return format(value, "f")


def _call_charge(used: Mapping[str, Any], price: Mapping[str, Any]) -> Decimal:
    prompt_toks = int(used["prompt_tokens"])
    cached_toks = int(used.get("cached_tokens", 0) or 0)
    completion_toks = int(used["completion_tokens"])
    with localcontext() as ctx:
        ctx.prec = 80
        return (
            Decimal(prompt_toks - cached_toks) * ai_consumption.amount(str(price["input_rate"]))
            + Decimal(cached_toks) * ai_consumption.amount(str(price["cached_rate"]))
            + Decimal(completion_toks) * ai_consumption.amount(str(price["output_rate"]))
        ) / Decimal(1000000)


def _bound_timestamp(value: object, label: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, int | float) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        parsed = parse_record_timestamp(value)
        if parsed is not None:
            return parsed
        return ai_consumption.timestamp(value)
    raise ValueError(f"Invalid {label} timestamp: {value!r}")


def _ratio_str(numerator: Decimal, denominator: int) -> str:
    if denominator <= 0 or numerator <= 0:
        return UNKNOWN
    with localcontext() as ctx:
        ctx.prec = 80
        return format(numerator / denominator, "f")


def _read_port_events(ledger: Any) -> tuple[list[dict[str, Any]] | None, str | None]:
    """Read durable ledger events without acquiring a write lock; fail closed on hold."""
    port = getattr(ledger, "port", None)
    if port is None:
        return None, None
    if not bool(getattr(port, "sql", False)) or getattr(port, "schema_error", None) is not None:
        return None, "unavailable"
    store_obj = getattr(port, "store", None)
    conn_factory = getattr(store_obj, "assistant_connection", None)
    try:
        if callable(conn_factory):
            db = conn_factory()
            try:
                query = "SELECT body FROM assistant_events WHERE task_id=? ORDER BY at,id"
                query += (
                    " OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY"
                    if getattr(port, "mssql", False)
                    else " LIMIT ?"
                )
                rows = db.execute(
                    query, (ai_consumption.PARTITION, ai_consumption.MAX_EVENTS + 1)
                ).fetchall()
                if len(rows) > ai_consumption.MAX_EVENTS:
                    raise ai_consumption.DispatchHeld("meter-capacity-reached")
                events: list[dict[str, Any]] = []
                for (raw,) in rows:
                    body = json.loads(raw)
                    if not isinstance(body, dict) or not isinstance(body.get("kind"), str):
                        raise ai_consumption.DispatchHeld("meter-evidence-invalid")
                    events.append(body)
                return events, None
            finally:
                db.close()
        read_fn = getattr(ledger, "_read", None)
        tx_fn = getattr(port, "transaction", None)
        if callable(read_fn) and callable(tx_fn):
            with tx_fn() as db:
                loaded = read_fn(db)
            return list(loaded), None
    except (
        ai_consumption.DispatchHeld,
        ValueError,
        KeyError,
        TypeError,
        OSError,
        RuntimeError,
    ):
        return None, "ledger-hold"
    return None, None


def _reconcile_ledger(
    records: Sequence[Mapping[str, Any]],
    *,
    begin: float | None,
    finish: float | None,
    cutoff: float | None,
) -> dict[str, Any]:
    valid_records = [dict(r) for r in records if isinstance(r, Mapping)]
    scoped = [
        r
        for r in valid_records
        if isinstance(r.get("at"), int | float)
        and not isinstance(r.get("at"), bool)
        and (cutoff is None or float(r["at"]) <= cutoff)
    ]
    prices: dict[str, dict[str, Any]] = {
        str(r["id"]): r
        for r in valid_records
        if r.get("kind") == "price" and isinstance(r.get("id"), str)
    }
    calls = [
        r
        for r in scoped
        if r.get("kind") == "reserved"
        and (begin is None or float(r["at"]) >= begin)
        and (finish is None or float(r["at"]) < finish)
    ]
    completions: dict[str, dict[str, Any]] = {
        str(r["id"]): r
        for r in scoped
        if r.get("kind") == "completed" and isinstance(r.get("id"), str)
    }
    roots = {str(r["root"]) for r in calls if isinstance(r.get("root"), str)}
    outputs: dict[str, dict[str, Any]] = {
        str(r["root"]): r
        for r in scoped
        if r.get("kind") == "output" and str(r.get("root")) in roots
    }
    output_ids = {str(v["output"]) for v in outputs.values() if isinstance(v.get("output"), str)}
    unjoined_outputs = len(roots - outputs.keys())
    reviews: dict[str, dict[str, Any]] = {}
    for r in scoped:
        if r.get("kind") == "review" and isinstance(r.get("output"), str):
            out_id = str(r["output"])
            if int(r.get("revision", 0)) > int(reviews.get(out_id, {}).get("revision", 0)):
                reviews[out_id] = r
    unresolved = {
        str(r["output"])
        for r in scoped
        if r.get("kind") == "review-unresolved"
        and str(r.get("root")) in roots
        and isinstance(r.get("output"), str)
    }
    orphan_outputs = {
        str(r["output"])
        for r in scoped
        if r.get("kind") == "review-orphan"
        and str(r.get("root")) in roots
        and isinstance(r.get("output"), str)
    }
    pending_intents = {
        str(r["output"])
        for r in scoped
        if r.get("kind") == "review-intent"
        and isinstance(r.get("output"), str)
        and str(r["output"]) in (output_ids | orphan_outputs)
        and int(r.get("revision", 0)) > int(reviews.get(str(r["output"]), {}).get("revision", 0))
    }
    unjoined_reviews = len(pending_intents | (orphan_outputs - output_ids) | unresolved)
    accepted_roots: set[str] = set()
    if not unjoined_reviews:
        for root in roots:
            out = outputs.get(root)
            if (
                out is not None
                and bool(out.get("eligible"))
                and str(out.get("output", "")) not in unresolved
                and reviews.get(str(out.get("output", "")), {}).get("action")
                in ("accept", "edit-accept")
            ):
                accepted_roots.add(root)

    unknown_liabilities = 0
    retries = 0
    failures = 0
    token_sum = 0
    tokens_complete = True
    projected: Decimal | None = Decimal(0)
    per_cap_projected: dict[str, Decimal | None] = {}
    currencies: set[str] = set()
    retrieved_dates: list[float] = []
    synthetic_flags: set[bool] = set()

    for call in calls:
        cid = str(call.get("id", ""))
        cap = _capability_name(call.get("capability"))
        per_cap_projected.setdefault(cap, Decimal(0))
        if int(call.get("retry", 0)) > 0:
            retries += 1
        done = completions.get(cid)
        if not done or done.get("outcome") != "returned":
            failures += 1
        price = prices.get(str(call.get("price", "")))
        if price is not None:
            if isinstance(price.get("currency"), str):
                currencies.add(price["currency"])
            if isinstance(price.get("synthetic"), bool):
                synthetic_flags.add(price["synthetic"])
            retrieved = price.get("retrieved")
            if (
                isinstance(retrieved, int | float)
                and not isinstance(retrieved, bool)
                and retrieved > 0
            ):
                retrieved_dates.append(float(retrieved))
        if not done or bool(done.get("held")) or done.get("tokens") is None or price is None:
            tokens_complete = False
            unknown_liabilities += 1
            projected = None
            per_cap_projected[cap] = None
        else:
            tok = done["tokens"]
            token_sum += int(tok["total_tokens"])
            raw_charge = done.get("charge")
            call_charge = (
                ai_consumption.charge_amount(str(raw_charge))
                if isinstance(raw_charge, str) and raw_charge
                else _call_charge(tok, price)
            )
            if projected is not None:
                projected += call_charge
            if per_cap_projected[cap] is not None:
                per_cap_projected[cap] = (per_cap_projected[cap] or Decimal(0)) + call_charge

    # Reconcile complete single-currency billing records:
    # - Exact [begin, finish) match when both bounds are supplied;
    # - Complete non-overlapping billing records covering every in-scope call otherwise (PC-002).
    reconciliation = "unreconciled"
    billed_total: Decimal | None = None
    financial_sources: list[str] = []
    all_bills = [
        r
        for r in valid_records
        if r.get("kind") == "billing"
        and bool(r.get("complete"))
        and isinstance(r.get("start"), int | float)
        and isinstance(r.get("end"), int | float)
    ]
    selected_bills: list[dict[str, Any]] = []
    if (
        calls
        and len(currencies) == 1
        and projected is not None
        and not unjoined_outputs
        and not unjoined_reviews
    ):
        target_currency = next(iter(currencies))
        currency_bills = [b for b in all_bills if b.get("currency") == target_currency]
        if begin is not None and finish is not None:
            exact = [
                b
                for b in currency_bills
                if float(b["start"]) == begin
                and float(b["end"]) == finish
                and all(b.get("budget") in c.get("budgets", ()) for c in calls)
            ]
            if len(exact) == 1:
                selected_bills = exact
        else:
            covering: list[dict[str, Any]] = []
            used_ids: set[str] = set()
            all_covered = True
            for call in calls:
                cat = float(call["at"])
                matches = [
                    b
                    for b in currency_bills
                    if float(b["start"]) <= cat < float(b["end"])
                    and b.get("budget") in call.get("budgets", ())
                ]
                if len(matches) != 1:
                    all_covered = False
                    break
                chosen = matches[0]
                bid = str(chosen.get("id", ""))
                if bid not in used_ids:
                    used_ids.add(bid)
                    covering.append(chosen)
            if all_covered and covering:
                ordered = sorted(covering, key=lambda b: (float(b["start"]), float(b["end"])))
                non_overlapping = all(
                    float(ordered[i]["end"]) <= float(ordered[i + 1]["start"])
                    for i in range(len(ordered) - 1)
                )
                if non_overlapping:
                    selected_bills = ordered

    zero_variance = False
    if selected_bills and projected is not None:
        billed_sum = sum((ai_consumption.amount(b["billed"]) for b in selected_bills), Decimal(0))
        max_tol = min(ai_consumption.amount(b["tolerance"]) for b in selected_bills)
        if billed_sum > 0:
            with localcontext() as ctx:
                ctx.prec = 80
                delta = abs(billed_sum - projected) / billed_sum
            if delta <= max_tol:
                reconciliation = "reconciled"
                billed_total = billed_sum
                zero_variance = billed_sum == projected
                financial_sources = [
                    str(b["id"]) for b in selected_bills if isinstance(b.get("id"), str)
                ]
        elif billed_sum == 0 and projected == 0:
            reconciliation = "reconciled"
            billed_total = Decimal(0)
            zero_variance = True
            financial_sources = [
                str(b["id"]) for b in selected_bills if isinstance(b.get("id"), str)
            ]

    alerts = [
        dict(
            owner=_sanitize_owner(r.get("owner")),
            reason=_sanitize_code(r.get("reason"), "threshold-alert"),
            route=_sanitize_code(r.get("route"), "audit-log"),
        )
        for r in scoped
        if r.get("kind") == "alert"
        and (begin is None or float(r["at"]) >= begin)
        and (finish is None or float(r["at"]) < finish)
    ]

    # Per-capability ledger structures
    cap_groups: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for call in calls:
        cap = _capability_name(call.get("capability"))
        root = str(call.get("root", ""))
        cap_groups.setdefault(cap, {}).setdefault(root, []).append(call)

    return dict(
        calls=calls,
        completions=completions,
        roots=roots,
        outputs=outputs,
        output_ids=output_ids,
        reviews=reviews,
        unresolved=unresolved,
        accepted_roots=accepted_roots,
        unjoined_outputs=unjoined_outputs,
        unjoined_reviews=unjoined_reviews,
        unknown_liabilities=unknown_liabilities,
        retries=retries,
        failures=failures,
        total_tokens=token_sum if (calls and tokens_complete) else (0 if not calls else UNKNOWN),
        currencies=currencies,
        retrieved_dates=retrieved_dates,
        tariff_basis=ai_consumption.tariff_basis(synthetic_flags),
        reconciliation=reconciliation,
        billed_total=billed_total,
        zero_variance=zero_variance,
        per_cap_projected=per_cap_projected,
        financial_sources=financial_sources,
        alerts=alerts,
        cap_groups=cap_groups,
    )


def summarize_ai_consumption_economics(
    *,
    recommendations: Iterable[Mapping[str, Any]] | None = None,
    consumption_report: Mapping[str, Any] | None = None,
    ledger_records: Sequence[Mapping[str, Any]] | None = None,
    start: object = None,
    end: object = None,
    as_of: object = None,
    od_51_status: str = "open",
    price_source: str | None = None,
    components: Mapping[str, object] | None = None,
    quality_floor_status: str | None = None,
    booked_value: object = None,
    limit_configured: bool = False,
    ledger_coverage: str | None = None,
    home_count: int | None = None,
) -> dict[str, Any]:
    """Synthesize BRD Required Management Views `ai_consumption_economics` deterministically."""
    if od_51_status not in ("open", "approved"):
        raise ValueError("od_51_status must be 'open' or 'approved'.")
    if home_count is not None and (not isinstance(home_count, int) or isinstance(home_count, bool)):
        raise ValueError("home_count must be an int or None.")

    begin = _bound_timestamp(start, "start")
    finish = _bound_timestamp(end, "end")
    cutoff = _bound_timestamp(as_of, "as_of") if as_of is not None else finish
    if begin is not None and finish is not None and begin > finish:
        raise ValueError("start must not be after end.")
    if finish is not None and cutoff is not None and cutoff < finish:
        raise ValueError("as_of must not precede end.")

    recs = [dict(r) for r in (recommendations or ()) if isinstance(r, Mapping)]

    # Step 1: Extract ledger-side state from raw ledger_records or precomputed consumption_report.
    ledger_state: dict[str, Any] | None = None
    if ledger_records is not None:
        ledger_state = _reconcile_ledger(ledger_records, begin=begin, finish=finish, cutoff=cutoff)

    metered_call_count = 0
    unmetered_call_count = 0
    proposal_count = 0
    accepted_outcome_count = 0
    rejected_or_withdrawn_count = 0
    unreviewed_proposal_count = 0
    workflow_only_excluded_count = 0
    retries = 0
    failures = 0
    total_tokens: int | str = 0
    unknown_liabilities = 0
    unjoined_outputs = 0
    unjoined_reviews = 0
    owned_alerts: list[dict[str, str]] = []
    reconciliation = "unreconciled"
    billed_decimal: Decimal | None = None
    currency_val = UNKNOWN
    tariff_basis = UNKNOWN
    dated_price_present = False
    financial_source_id: str | None = None
    zero_variance = False
    per_cap_projected: dict[str, Decimal | None] = {}

    cap_stats: dict[str, dict[str, Any]] = {}

    def ensure_cap(cap: str) -> dict[str, Any]:
        return cap_stats.setdefault(
            cap,
            dict(
                proposal_count=0,
                accepted_outcome_count=0,
                metered_call_count=0,
                unmetered_call_count=0,
                total_tokens=0,
                tokens_unknown=False,
            ),
        )

    covered_roots: set[str] = set()
    covered_output_digests: set[str] = set()

    if ledger_state is not None:
        calls = ledger_state["calls"]
        outputs = ledger_state["outputs"]
        reviews = ledger_state["reviews"]
        unresolved = ledger_state["unresolved"]
        accepted_roots = ledger_state["accepted_roots"]
        completions = ledger_state["completions"]

        metered_call_count += len(calls)
        retries += int(ledger_state["retries"])
        failures += int(ledger_state["failures"])
        total_tokens = ledger_state["total_tokens"]
        unknown_liabilities = int(ledger_state["unknown_liabilities"])
        unjoined_outputs = int(ledger_state["unjoined_outputs"])
        unjoined_reviews = int(ledger_state["unjoined_reviews"])
        owned_alerts = list(ledger_state["alerts"])
        reconciliation = str(ledger_state["reconciliation"])
        billed_decimal = ledger_state["billed_total"]
        zero_variance = bool(ledger_state["zero_variance"])
        per_cap_projected = dict(ledger_state["per_cap_projected"])
        if len(ledger_state["currencies"]) == 1:
            currency_val = next(iter(ledger_state["currencies"]))
        tariff_basis = str(ledger_state["tariff_basis"])
        dated_price_present = bool(calls) and len(ledger_state["retrieved_dates"]) == len(calls)
        if ledger_state["financial_sources"]:
            financial_source_id = ",".join(ledger_state["financial_sources"])

        covered_roots = set(ledger_state["roots"])
        covered_output_digests = set(ledger_state["output_ids"])

        # Count proposal-eligible roots per capability from ledger
        for cap, root_map in ledger_state["cap_groups"].items():
            entry = ensure_cap(cap)
            entry["metered_call_count"] += sum(len(v) for v in root_map.values())
            for root, attempts in root_map.items():
                if all(
                    str(a.get("id", "")) in completions
                    and completions[str(a.get("id", ""))].get("tokens") is not None
                    for a in attempts
                ):
                    entry["total_tokens"] += sum(
                        int(completions[str(a["id"])]["tokens"]["total_tokens"]) for a in attempts
                    )
                else:
                    entry["tokens_unknown"] = True
                out = outputs.get(root)
                # Non-proposal chat turns record output.eligible == False without a rec row
                is_proposal_root = out is None or bool(out.get("eligible"))
                if is_proposal_root:
                    proposal_count += 1
                    entry["proposal_count"] += 1
                    if root in accepted_roots:
                        accepted_outcome_count += 1
                        entry["accepted_outcome_count"] += 1
                    elif out is not None:
                        out_id = str(out.get("output", ""))
                        rev_action = reviews.get(out_id, {}).get("action")
                        if out_id in unresolved or rev_action in ("reject", "withdraw"):
                            rejected_or_withdrawn_count += 1
                        else:
                            unreviewed_proposal_count += 1
                    else:
                        unreviewed_proposal_count += 1

    elif consumption_report is not None:
        if consumption_report.get("coverage") == "unavailable":
            ledger_coverage = ledger_coverage or "unavailable"
        else:
            metered_call_count += int(consumption_report.get("calls", 0) or 0)
            retries += int(consumption_report.get("retries", 0) or 0)
            failures += int(consumption_report.get("failures", 0) or 0)
            unknown_liabilities = int(consumption_report.get("unknown_liabilities", 0) or 0)
            unjoined_outputs = int(consumption_report.get("unjoined_outputs", 0) or 0)
            unjoined_reviews = int(consumption_report.get("unjoined_reviews", 0) or 0)
            reconciliation = str(consumption_report.get("reconciliation", "unreconciled"))
            tariff_basis = str(consumption_report.get("tariff_basis", UNKNOWN))
            raw_curr = consumption_report.get("currency", UNKNOWN)
            currency_val = str(raw_curr) if isinstance(raw_curr, str) and raw_curr else UNKNOWN
            fin_src = consumption_report.get("financial_source")
            financial_source_id = str(fin_src) if isinstance(fin_src, str) and fin_src else None
            cpo = consumption_report.get("cost_per_accepted_outcome")
            if isinstance(cpo, Mapping) and cpo.get("price_retrieved"):
                dated_price_present = True
            elif tariff_basis not in (UNKNOWN, ""):
                dated_price_present = True
            raw_tok_cost = consumption_report.get("token_cost", UNKNOWN)
            if isinstance(raw_tok_cost, str) and raw_tok_cost != UNKNOWN:
                billed_decimal = ai_consumption.amount(raw_tok_cost)
            raw_var = consumption_report.get("variance_fraction")
            zero_variance = raw_var in ("0", "0.0")
            for alert in consumption_report.get("owned_alerts", ()) or ():
                if isinstance(alert, Mapping):
                    owned_alerts.append(
                        dict(
                            owner=_sanitize_owner(alert.get("owner")),
                            reason=_sanitize_code(alert.get("reason"), "threshold-alert"),
                            route=_sanitize_code(alert.get("route"), "audit-log"),
                        )
                    )
            by_cap_in = consumption_report.get("by_capability")
            tok_sum = 0
            tok_any_unknown = False
            if isinstance(by_cap_in, Mapping):
                for cap_key, cap_val in by_cap_in.items():
                    if not isinstance(cap_val, Mapping):
                        continue
                    cname = _capability_name(cap_key)
                    entry = ensure_cap(cname)
                    c_props = int(cap_val.get("proposals", 0) or 0)
                    c_acc = int(cap_val.get("accepted_proposals", 0) or 0)
                    c_calls = int(cap_val.get("calls", 0) or 0)
                    proposal_count += c_props
                    accepted_outcome_count += c_acc
                    entry["proposal_count"] += c_props
                    entry["accepted_outcome_count"] += c_acc
                    entry["metered_call_count"] += c_calls
                    ctok = cap_val.get("total_tokens", UNKNOWN)
                    if isinstance(ctok, int) and not isinstance(ctok, bool):
                        entry["total_tokens"] += ctok
                        tok_sum += ctok
                    else:
                        entry["tokens_unknown"] = True
                        tok_any_unknown = True
            total_tokens = (
                0 if metered_call_count == 0 else (UNKNOWN if tok_any_unknown else tok_sum)
            )
            if quality_floor_status is None:
                rep_q = consumption_report.get("quality_status")
                if rep_q in ("Pass", "Failure", UNKNOWN):
                    quality_floor_status = str(rep_q)
            if components is None and isinstance(
                consumption_report.get("other_tca_components"), Mapping
            ):
                known_comps = {
                    k: v
                    for k, v in consumption_report["other_tca_components"].items()
                    if isinstance(v, str) and v != UNKNOWN
                }
                if known_comps:
                    components = known_comps

    # Step 2: Reconcile store recommendations without double-counting metered roots (PC-003).
    for rec in recs:
        rec_ts = parse_record_timestamp(rec.get("created"))
        if rec_ts is None:
            rec_ts = parse_record_timestamp(rec.get("resolved_at"))
        if rec_ts is not None:
            if begin is not None and rec_ts < begin:
                resolved_ts = parse_record_timestamp(rec.get("resolved_at"))
                if (
                    resolved_ts is None
                    or resolved_ts < begin
                    or (finish is not None and resolved_ts >= finish)
                ):
                    continue
            if (finish is not None and rec_ts >= finish) or (
                cutoff is not None and rec_ts > cutoff
            ):
                continue
        elif begin is not None:
            continue

        mroot = _extract_meter_root(rec)
        rec_id = rec.get("id")
        hashed_id = (
            ai_consumption.reference(rec_id) if isinstance(rec_id, str) and rec_id.strip() else None
        )
        source = str(rec.get("source") or "")
        status = str(rec.get("status") or "")
        cap_name = _rec_capability(rec)

        # Already covered in ledger_records or consumption_report
        if ledger_state is not None:
            if (mroot and mroot in covered_roots) or (
                hashed_id and hashed_id in covered_output_digests
            ):
                # If a publish-held fallback had output.eligible == False in ledger, ensure its
                # rejected/held status is still reflected in non-accepted proposal denominators
                if mroot and mroot in ledger_state["outputs"]:
                    out_row = ledger_state["outputs"][mroot]
                    if not bool(out_row.get("eligible")):
                        proposal_count += 1
                        ensure_cap(cap_name)["proposal_count"] += 1
                        if status == "Rejected":
                            rejected_or_withdrawn_count += 1
                        else:
                            unreviewed_proposal_count += 1
                continue
        elif consumption_report is not None and mroot is not None:
            continue

        # Pure workflow/template recommendation with no meter root (zero model calls)
        if source != "ai" and mroot is None:
            workflow_only_excluded_count += 1
            continue

        entry = ensure_cap(cap_name)
        proposal_count += 1
        entry["proposal_count"] += 1

        if mroot is not None:
            # Metered envelope present on JSON/standalone recommendation without ledger dump
            metered_call_count += 1
            entry["metered_call_count"] += 1
            env_usage = (
                rec.get("envelope", {}).get("usage")
                if isinstance(rec.get("envelope"), Mapping)
                else None
            )
            tok_total = env_usage.get("total_tokens") if isinstance(env_usage, Mapping) else None
            if isinstance(tok_total, int) and not isinstance(tok_total, bool):
                entry["total_tokens"] += tok_total
                if isinstance(total_tokens, int):
                    total_tokens += tok_total
            else:
                entry["tokens_unknown"] = True
                total_tokens = UNKNOWN
        else:
            # AI-source output lacking durable meter attribution -> explicit unmetered call!
            unmetered_call_count += 1
            entry["unmetered_call_count"] += 1
            entry["tokens_unknown"] = True
            total_tokens = UNKNOWN

        # Accepted outcome eligibility excludes Hold, Quarantined, unverified, fallback & Rejected
        verified_ok = bool(rec.get("verified", rec.get("validated", True)))
        if source == "ai" and status in ("Accepted", "Edited") and verified_ok:
            if unjoined_reviews == 0:
                accepted_outcome_count += 1
                entry["accepted_outcome_count"] += 1
        elif status == "Rejected":
            rejected_or_withdrawn_count += 1
        else:
            unreviewed_proposal_count += 1

    if metered_call_count == 0 and unmetered_call_count == 0:
        total_tokens = 0

    # Step 3: Evaluate Other TCA Components and Quality Floor Status.
    other_components: dict[str, str] = {k: UNKNOWN for k in ai_consumption.COMPONENTS}
    if components is not None:
        unknown_keys = set(components) - set(ai_consumption.COMPONENTS)
        if unknown_keys:
            raise ValueError(f"Unexpected TCA component: {sorted(unknown_keys)!r}")
        for comp_key, comp_val in components.items():
            if comp_val is None or comp_val == UNKNOWN:
                other_components[comp_key] = UNKNOWN
            else:
                other_components[comp_key] = format(ai_consumption.amount(str(comp_val)), "f")

    resolved_quality = (
        quality_floor_status if quality_floor_status in ("Pass", "Failure", UNKNOWN) else UNKNOWN
    )

    # Step 4: Evaluate price_source_configured and fail-closed Unknown cost invariants (FR-3).
    effective_coverage = ledger_coverage or (
        "incomplete"
        if (
            unmetered_call_count > 0
            or unknown_liabilities > 0
            or unjoined_outputs > 0
            or unjoined_reviews > 0
        )
        else ("recorded-ledger-only" if metered_call_count > 0 else "no-metered-calls")
    )
    resolved_price_label = (
        _sanitize_code(price_source, tariff_basis)
        if price_source is not None
        else (tariff_basis if tariff_basis != UNKNOWN else UNKNOWN)
    )
    price_source_configured = bool(
        od_51_status == "approved"
        and effective_coverage not in ("ledger-hold", "unavailable", "incomplete")
        and resolved_price_label != UNKNOWN
        and dated_price_present
        and reconciliation == "reconciled"
        and billed_decimal is not None
        and currency_val != UNKNOWN
        and financial_source_id is not None
        and unmetered_call_count == 0
        and unknown_liabilities == 0
        and unjoined_outputs == 0
        and unjoined_reviews == 0
    )

    token_cost = UNKNOWN
    total_cost_of_ai = UNKNOWN
    token_cost_per_accepted_outcome = UNKNOWN
    cost_per_accepted_outcome = UNKNOWN
    quality_qualified_cost_per_accepted_outcome = UNKNOWN
    resolved_booked_value = UNKNOWN

    if price_source_configured and billed_decimal is not None:
        # Guard zero-billed zero-accepted state: never emit "0" when accepted_outcome_count == 0
        if billed_decimal > 0:
            token_cost = _positive_money_str(billed_decimal)
            if all(v != UNKNOWN for v in other_components.values()):
                tca_decimal = sum(
                    (ai_consumption.amount(v) for v in other_components.values()),
                    billed_decimal,
                )
                total_cost_of_ai = _positive_money_str(tca_decimal)
                if accepted_outcome_count > 0 and resolved_quality == "Pass":
                    cost_per_accepted_outcome = _ratio_str(tca_decimal, accepted_outcome_count)
            if accepted_outcome_count > 0:
                token_cost_per_accepted_outcome = _ratio_str(billed_decimal, accepted_outcome_count)
                if resolved_quality == "Pass":
                    quality_qualified_cost_per_accepted_outcome = token_cost_per_accepted_outcome
        if booked_value is not None and booked_value != UNKNOWN:
            booked_dec = ai_consumption.amount(str(booked_value))
            if booked_dec > 0:
                resolved_booked_value = format(booked_dec, "f")

    if not price_source_configured:
        resolved_price_label = UNKNOWN
        currency_val = UNKNOWN

    # Step 5: Per-capability attribution with fail-closed Unknown rules (PC-005).
    active_caps = sorted(cap_stats)
    single_capability = len(active_caps) == 1
    by_capability: dict[str, dict[str, Any]] = {}
    for cap in active_caps:
        raw_cap = cap_stats[cap]
        c_props = int(raw_cap["proposal_count"])
        c_acc = int(raw_cap["accepted_outcome_count"])
        c_mcalls = int(raw_cap["metered_call_count"])
        c_ucalls = int(raw_cap["unmetered_call_count"])
        c_tokens: int | str = (
            0
            if (c_mcalls == 0 and c_ucalls == 0)
            else (UNKNOWN if raw_cap["tokens_unknown"] else int(raw_cap["total_tokens"]))
        )

        cap_token_cost = UNKNOWN
        cap_total_cost = UNKNOWN
        cap_token_cpo = UNKNOWN
        cap_cpo = UNKNOWN

        if price_source_configured and c_ucalls == 0:
            cap_billed: Decimal | None = None
            if single_capability and billed_decimal is not None and billed_decimal > 0:
                cap_billed = billed_decimal
            elif zero_variance and per_cap_projected.get(cap) is not None:
                proj_cap = per_cap_projected[cap]
                if proj_cap is not None and proj_cap > 0:
                    cap_billed = proj_cap

            if cap_billed is not None and cap_billed > 0:
                cap_token_cost = _positive_money_str(cap_billed)
                if c_acc > 0:
                    cap_token_cpo = _ratio_str(cap_billed, c_acc)
                if single_capability and total_cost_of_ai != UNKNOWN:
                    cap_total_cost = total_cost_of_ai
                    if c_acc > 0 and resolved_quality == "Pass":
                        cap_cpo = _ratio_str(ai_consumption.amount(total_cost_of_ai), c_acc)

        by_capability[cap] = dict(
            proposal_count=c_props,
            accepted_outcome_count=c_acc,
            metered_call_count=c_mcalls,
            unmetered_call_count=c_ucalls,
            total_tokens=c_tokens,
            quality_floor_status=resolved_quality,
            token_cost=cap_token_cost,
            total_cost_of_ai=cap_total_cost,
            token_cost_per_accepted_outcome=cap_token_cpo,
            cost_per_accepted_outcome=cap_cpo,
            booked_value=resolved_booked_value if single_capability else UNKNOWN,
        )

    # Step 6: Metered usage against limits and owned breach alerts (BRD FR-052).
    limit_breaches = sum(
        1
        for a in owned_alerts
        if any(
            tok in a["reason"].lower()
            for tok in ("limit", "cap", "exceeded", "exhausted", "budget")
        )
    )
    alert_breaches = len(owned_alerts)
    if od_51_status != "approved" or not limit_configured:
        limit_status = UNKNOWN
    elif limit_breaches > 0 or alert_breaches > 0:
        limit_status = "breach-recorded"
    else:
        limit_status = "within-configured-limits"

    denominators = dict(
        proposal_count=proposal_count,
        accepted_outcome_count=accepted_outcome_count,
        metered_call_count=metered_call_count,
        unmetered_call_count=unmetered_call_count,
        unreviewed_proposal_count=unreviewed_proposal_count,
        rejected_or_withdrawn_count=rejected_or_withdrawn_count,
        workflow_only_excluded_count=workflow_only_excluded_count,
        basis=DENOMINATOR_BASIS,
    )

    summary: dict[str, Any] = dict(
        schema=SCHEMA,
        od_51_status=od_51_status,
        price_source_configured=price_source_configured,
        price_source=resolved_price_label,
        currency=currency_val,
        coverage=effective_coverage,
        reconciliation=reconciliation,
        proposal_count=proposal_count,
        accepted_outcome_count=accepted_outcome_count,
        metered_call_count=metered_call_count,
        unmetered_call_count=unmetered_call_count,
        denominators=denominators,
        metered_usage=dict(
            metered_call_count=metered_call_count,
            unmetered_call_count=unmetered_call_count,
            retry_count=retries,
            failure_count=failures,
            total_tokens=total_tokens,
            limit_configured=bool(limit_configured and od_51_status == "approved"),
            limit_status=limit_status,
            limit_breach_count=limit_breaches,
            alert_breach_count=alert_breaches,
            owned_alerts=owned_alerts,
        ),
        token_cost=token_cost,
        other_tca_components=other_components,
        total_cost_of_ai=total_cost_of_ai,
        token_cost_per_accepted_outcome=token_cost_per_accepted_outcome,
        cost_per_accepted_outcome=cost_per_accepted_outcome,
        quality_floor_status=resolved_quality,
        quality_qualified_cost_per_accepted_outcome=quality_qualified_cost_per_accepted_outcome,
        booked_value=resolved_booked_value,
        by_capability=by_capability,
        non_benefit_notice=NON_BENEFIT_NOTICE,
    )
    if home_count is not None:
        homes_ok = home_count > 0
        summary["home_count"] = home_count
        summary["tokens_per_home"] = (
            _ratio_str(Decimal(total_tokens), home_count)
            if homes_ok and isinstance(total_tokens, int)
            else UNKNOWN
        )
        summary["token_cost_per_home"] = (
            _ratio_str(ai_consumption.amount(token_cost), home_count)
            if homes_ok and token_cost != UNKNOWN
            else UNKNOWN
        )
    assert_tokenomics_invariants(summary)
    return summary


def store_ai_consumption_economics(
    store: Any,
    *,
    start: object = None,
    end: object = None,
    as_of: object = None,
    recommendations: Iterable[Mapping[str, Any]] | None = None,
    consumption_report: Mapping[str, Any] | None = None,
    od_51_status: str | None = None,
    price_source: str | None = None,
    components: Mapping[str, object] | None = None,
    quality_floor_status: str | None = None,
    booked_value: object = None,
    limit_configured: bool | None = None,
    home_count: int | None = None,
) -> dict[str, Any]:
    """Build deterministic, read-only `ai_consumption_economics` from a Store or SqlStore."""
    with store.lock:
        recs = (
            [dict(r) for r in recommendations]
            if recommendations is not None
            else [dict(r) for r in store.data.get("recommendations", []) if isinstance(r, Mapping)]
        )
        raw_gov = getattr(store, "tokenomics_governance", None)
        if not isinstance(raw_gov, Mapping):
            data_gov = store.data.get("tokenomics_governance")
            raw_gov = data_gov if isinstance(data_gov, Mapping) else {}
        gov = dict(raw_gov)
        ai_client = getattr(store, "ai", None)
        ledger = getattr(ai_client, "consumption", None)

    resolved_od51 = str(
        od_51_status if od_51_status is not None else gov.get("od_51_status", "open")
    )
    resolved_price_source = (
        price_source
        if price_source is not None
        else (str(gov["price_source"]) if isinstance(gov.get("price_source"), str) else None)
    )
    resolved_components = (
        components
        if components is not None
        else (gov["components"] if isinstance(gov.get("components"), Mapping) else None)
    )
    resolved_quality = (
        quality_floor_status
        if quality_floor_status is not None
        else (
            str(gov["quality_floor_status"])
            if isinstance(gov.get("quality_floor_status"), str)
            else None
        )
    )
    resolved_booked = booked_value if booked_value is not None else gov.get("booked_value")
    resolved_limits = (
        limit_configured
        if limit_configured is not None
        else bool(gov.get("limit_configured", False))
    )

    ledger_records: list[dict[str, Any]] | None = None
    ledger_coverage: str | None = None
    if consumption_report is None and ledger is not None:
        ledger_records, ledger_coverage = _read_port_events(ledger)

    return summarize_ai_consumption_economics(
        recommendations=recs,
        consumption_report=consumption_report,
        ledger_records=ledger_records,
        start=start,
        end=end,
        as_of=as_of,
        od_51_status=resolved_od51,
        price_source=resolved_price_source,
        components=resolved_components,
        quality_floor_status=resolved_quality,
        booked_value=resolved_booked,
        limit_configured=resolved_limits,
        ledger_coverage=ledger_coverage,
        home_count=home_count,
    )


def _assert_not_zero_or_none_cost(field_name: str, value: object) -> None:
    if value is None or isinstance(value, bool | int | float):
        raise AssertionError(
            f"{field_name} must be Unknown or a positive Decimal string, got {value!r}"
        )
    if not isinstance(value, str) or value.strip() in _ZERO_COST_STRINGS or not value.strip():
        raise AssertionError(f"{field_name} must never report zero or empty cost, got {value!r}")


def assert_tokenomics_invariants(summary: Mapping[str, Any]) -> None:
    """Verify explicit denominators and strict fail-closed Unknown cost invariants."""
    denoms = summary.get("denominators")
    if not isinstance(denoms, Mapping):
        raise AssertionError("ai_consumption_economics.denominators must be a mapping.")
    for key in DENOMINATOR_KEYS:
        top_val = summary.get(key)
        sub_val = denoms.get(key)
        if not isinstance(top_val, int) or isinstance(top_val, bool) or top_val < 0:
            raise AssertionError(f"Explicit denominator {key} must be a non-negative int.")
        if top_val != sub_val:
            raise AssertionError(
                f"Top-level {key}={top_val!r} must match denominators[{key!r}]={sub_val!r}."
            )

    price_ok = summary.get("price_source_configured")
    if not isinstance(price_ok, bool):
        raise AssertionError("price_source_configured must be a bool.")
    accepted = int(summary["accepted_outcome_count"])
    unmetered = int(summary["unmetered_call_count"])
    if summary.get("od_51_status") != "approved" or unmetered > 0:
        if price_ok:
            raise AssertionError(
                "price_source_configured must be False when OD-51 is open or unmetered calls exist."
            )

    cost_fields = (
        "token_cost",
        "total_cost_of_ai",
        "token_cost_per_accepted_outcome",
        "cost_per_accepted_outcome",
        "quality_qualified_cost_per_accepted_outcome",
        "booked_value",
    )
    for field in cost_fields:
        _assert_not_zero_or_none_cost(field, summary.get(field))

    other_tca = summary.get("other_tca_components")
    if not isinstance(other_tca, Mapping):
        raise AssertionError("other_tca_components must be a mapping.")
    for comp_key, comp_val in other_tca.items():
        if comp_val is None or isinstance(comp_val, bool | int | float):
            raise AssertionError(
                f"other_tca_components[{comp_key!r}] must be str or Unknown, got {comp_val!r}"
            )

    if not price_ok:
        for field in cost_fields:
            if summary.get(field) != UNKNOWN:
                raise AssertionError(
                    f"{field} must be {UNKNOWN!r} when price_source_configured=False, "
                    f"got {summary.get(field)!r}"
                )

    if accepted == 0:
        for unit_field in (
            "token_cost_per_accepted_outcome",
            "cost_per_accepted_outcome",
            "quality_qualified_cost_per_accepted_outcome",
        ):
            if summary.get(unit_field) != UNKNOWN:
                raise AssertionError(
                    f"{unit_field} must be {UNKNOWN!r} when accepted_outcome_count == 0, "
                    f"got {summary.get(unit_field)!r}"
                )

    if "home_count" in summary:
        homes = summary["home_count"]
        if not isinstance(homes, int) or isinstance(homes, bool):
            raise AssertionError("home_count must be an int.")
        for field in ("tokens_per_home", "token_cost_per_home"):
            _assert_not_zero_or_none_cost(field, summary.get(field))
            if homes <= 0 and summary.get(field) != UNKNOWN:
                raise AssertionError(f"{field} must be {UNKNOWN!r} when home_count <= 0.")
        if not price_ok and summary.get("token_cost_per_home") != UNKNOWN:
            raise AssertionError("token_cost_per_home must be Unknown when unpriced.")

    by_cap = summary.get("by_capability")
    if not isinstance(by_cap, Mapping):
        raise AssertionError("by_capability must be a mapping.")
    for cap_name, cap_row in by_cap.items():
        if not isinstance(cap_row, Mapping):
            raise AssertionError(f"by_capability[{cap_name!r}] must be a mapping.")
        for key in DENOMINATOR_KEYS:
            cval = cap_row.get(key)
            if not isinstance(cval, int) or isinstance(cval, bool) or cval < 0:
                raise AssertionError(
                    f"by_capability[{cap_name!r}][{key!r}] must be a non-negative int."
                )
        for cfield in (
            "token_cost",
            "total_cost_of_ai",
            "token_cost_per_accepted_outcome",
            "cost_per_accepted_outcome",
            "booked_value",
        ):
            _assert_not_zero_or_none_cost(
                f"by_capability[{cap_name}].{cfield}", cap_row.get(cfield)
            )
            if not price_ok and cap_row.get(cfield) != UNKNOWN:
                raise AssertionError(
                    f"by_capability[{cap_name}].{cfield} must be {UNKNOWN!r} when unpriced."
                )
        if int(cap_row["accepted_outcome_count"]) == 0:
            for ucfield in ("token_cost_per_accepted_outcome", "cost_per_accepted_outcome"):
                if cap_row.get(ucfield) != UNKNOWN:
                    raise AssertionError(
                        f"by_capability[{cap_name}].{ucfield} must be {UNKNOWN!r} when "
                        "capability accepted_outcome_count == 0."
                    )
