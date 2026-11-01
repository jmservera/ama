"""Content-free consumption and financial evidence in the existing assistant ledger."""

from __future__ import annotations

import hashlib
import json
import logging
import re
import uuid
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, localcontext
from typing import Any, Protocol

SCHEMA = "ai-consumption-v1"
PARTITION = "ai-consumption"
MAX_EVENTS = 10000
UNKNOWN = "Unknown"
COMPONENTS = ("hosting", "review", "correction", "assurance", "support")
QUALITY = ("critical_misses", "unsupported_claims", "overrides", "reopened_cases")
EVENT_FIELDS = {
    "price": (
        "id source source_hash retrieved version model currency start end "
        "input_rate output_rate cached_rate synthetic"
    ),
    "authority": (
        "id owner evidence price capability configuration start end budgets max_calls max_depth"
    ),
    "reserved": (
        "id at root attempt capability case_type configuration prompt depth retry "
        "authority owner price model budgets input_bound output_bound liability"
    ),
    "completed": "id at tokens charge outcome held returned_model",
    "alert": "owner root attempt reason route at",
    "output": "root output eligible at",
    "review": "output action at revision intent",
    "review-intent": "id output action at revision",
    "review-orphan": "root output at",
    "review-unresolved": "root output action at reason revision",
    "billing": "id allocation budget start end currency billed tolerance complete synthetic",
}


def reference(value: str) -> str:
    if not isinstance(value, str) or not 1 <= len(value) <= 1000000:
        raise ValueError("A bounded evidence reference is required.")
    return hashlib.sha256(value.encode()).hexdigest()


def opaque(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[a-f0-9]{64}", value):
        raise ValueError("A SHA-256 evidence reference is required.")
    return value


def amount(value: str) -> Decimal:
    if not isinstance(value, str) or not re.fullmatch(r"\d{1,32}(?:\.\d{1,24})?", value):
        raise ValueError("Money must be a finite nonnegative exact decimal string.")
    return Decimal(value)


def charge_amount(value: str) -> Decimal:
    if not isinstance(value, str) or not re.fullmatch(r"\d{1,39}(?:\.\d{1,30})?", value):
        raise ValueError("Computed charge exceeds bounded exact token arithmetic.")
    return Decimal(value)


def timestamp(value: str) -> float:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("Evidence time needs an explicit timezone.")
    return result.timestamp()


def report_period(start: str, end: str, as_of: str) -> tuple[float, float, float]:
    begin, finish, cutoff = timestamp(start), timestamp(end), timestamp(as_of)
    if begin >= finish or cutoff < finish:
        raise ValueError("A complete exclusive period and review as-of time are required.")
    return begin, finish, cutoff


def count(value: int, maximum: int = 10**12) -> int:
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError("A bounded nonnegative integer is required.")
    return value


def money_sum(values: Iterator[Decimal]) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = 80
        return sum(values, Decimal(0))


def usage(value: object) -> dict[str, int | None] | None:
    if not isinstance(value, dict):
        return None
    keys = ("prompt_tokens", "completion_tokens", "total_tokens")
    if not all(type(value.get(k)) is int and 0 <= value[k] <= 10**12 for k in keys):
        return None
    if value["total_tokens"] != value["prompt_tokens"] + value["completion_tokens"]:
        return None
    cached = value.get("cached_tokens")
    if cached is None:
        details = value.get("prompt_tokens_details")
        cached = details.get("cached_tokens") if isinstance(details, dict) else None
    if cached is not None and (
        type(cached) is not int or not 0 <= cached <= value["prompt_tokens"]
    ):
        return None
    return {**{k: value[k] for k in keys}, "cached_tokens": cached}


@dataclass(frozen=True)
class CallContext:
    root: str
    attempt: str
    capability: str
    case_type: str
    configuration: str
    prompt: str
    depth: int = 1
    retry: int = 0

    def metadata(self) -> dict[str, Any]:
        for value in (self.root, self.attempt, self.configuration, self.prompt):
            opaque(value)
        for value in (self.capability, self.case_type):
            if not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", value):
                raise ValueError("Closed capability/case-type identifier required.")
        count(self.depth, 100)
        count(self.retry, 100)
        if self.depth == 0:
            raise ValueError("Agent depth begins at one.")
        return dict(
            root=self.root,
            attempt=self.attempt,
            capability=self.capability,
            case_type=self.case_type,
            configuration=self.configuration,
            prompt=self.prompt,
            depth=self.depth,
            retry=self.retry,
        )


CURRENT: ContextVar[CallContext | None] = ContextVar("ai_consumption_context", default=None)


@contextmanager
def call_context(context: CallContext) -> Iterator[None]:
    context.metadata()
    token = CURRENT.set(context)
    try:
        yield
    finally:
        CURRENT.reset(token)


def batch_spread(totals: list[int], batch: Mapping[str, Any] | None) -> dict[str, Any]:
    """Spread of tokens per proposal, only under a recorded finite spend authority."""
    label = "recorded usage; not an authorised held-out batch"
    unknown: dict[str, Any] = dict(
        median=UNKNOWN, standard_deviation=UNKNOWN, spend_authority=None, evidence_label=label
    )
    if batch is None or not totals:
        return unknown
    maximum = batch.get("max_proposals")
    if (
        set(batch) != {"authority", "evidence", "held_out", "max_proposals"}
        or batch["held_out"] is not True
        or not isinstance(maximum, int)
        or isinstance(maximum, bool)
        or not 0 < maximum <= MAX_EVENTS
        or len(totals) > maximum
    ):
        return unknown
    mean = Decimal(sum(totals)) / len(totals)
    ordered = sorted(totals)
    middle = len(ordered) // 2
    median = (
        Decimal(ordered[middle])
        if len(ordered) % 2
        else Decimal(ordered[middle - 1] + ordered[middle]) / 2
    )
    with localcontext() as ctx:
        ctx.prec = 28
        variance = Decimal(sum((Decimal(t) - mean) ** 2 for t in totals)) / len(totals)
        deviation = variance.sqrt()
    return dict(
        median=str(median),
        standard_deviation=format(deviation, "f"),
        spend_authority=dict(
            authority=reference(str(batch["authority"])),
            evidence=reference(str(batch["evidence"])),
            max_proposals=maximum,
        ),
        evidence_label="owner-authorised held-out batch as supplied; not verified by this software",
    )


class LedgerPort(Protocol):
    mssql: bool
    sql: bool

    def transaction(self) -> Any: ...
    def now(self, db: Any) -> float: ...
    def event(self, db: Any, tid: str, **body: Any) -> None: ...


class DispatchHeld(RuntimeError):
    """Safe code only; never provider content."""


def bounded_model(value: object) -> str | None:
    return value if isinstance(value, str) and len(value) <= 512 else None


class Consumption:
    def __init__(self, port: LedgerPort) -> None:
        self.port = port

    def _read(self, db: Any) -> list[dict[str, Any]]:
        query = "SELECT body FROM assistant_events WHERE task_id=? ORDER BY at,id"
        query += " OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY" if self.port.mssql else " LIMIT ?"
        rows = db.execute(query, (PARTITION, MAX_EVENTS + 1)).fetchall()
        if len(rows) > MAX_EVENTS:
            raise DispatchHeld("meter-capacity-reached")
        records = [json.loads(row[0]) for row in rows]
        if any(
            r.get("schema") != SCHEMA
            or r.get("kind") not in EVENT_FIELDS
            or set(r) != {"schema", "kind", *EVENT_FIELDS.get(r.get("kind"), "").split()}
            for r in records
        ):
            raise DispatchHeld("meter-evidence-invalid")
        return records

    def _event(self, db: Any, kind: str, **fields: Any) -> None:
        if kind == "alert":
            fields["at"] = self.port.now(db)
        self.port.event(db, PARTITION, schema=SCHEMA, kind=kind, **fields)

    @staticmethod
    def _currency_hold(
        records: list[dict[str, Any]], budgets: set[str], pid: str, currency: str | None
    ) -> str | None:
        prices = {r["id"]: r for r in records if r["kind"] == "price"}
        for r in records:
            if (
                r["kind"] == "authority"
                and r["price"] != pid
                and budgets.intersection(b["id"] for b in r["budgets"])
            ):
                other = prices.get(r["price"])
                if currency is None or other is None:
                    return "budget-currency-unknown"
                if currency != other["currency"]:
                    return "budget-currency-mismatch"
        return None

    def price(
        self,
        *,
        source: str,
        source_hash: str,
        retrieved: str,
        version: str,
        model: str,
        currency: str,
        start: str,
        end: str,
        input_rate: str,
        output_rate: str,
        cached_rate: str,
        synthetic: bool,
    ) -> str:
        """Rates per million tokens; retrieval is supplied evidence, never inferred."""
        if not re.fullmatch(r"https://(?:azure\.microsoft\.com|prices\.azure\.com)/\S+", source):
            raise ValueError("An official Azure price source URL is required.")
        if not re.fullmatch(r"[a-z0-9][a-z0-9.-]{0,119}", model):
            raise ValueError("A configured model identifier is required.")
        if currency not in ("USD", "GBP", "EUR") or type(synthetic) is not bool:
            raise ValueError("Explicit currency/evidence class required.")
        begin, finish, fetched = timestamp(start), timestamp(end), timestamp(retrieved)
        if begin >= finish or fetched > finish:
            raise ValueError("Price period is invalid.")
        body = dict(
            source=source,
            source_hash=opaque(source_hash),
            retrieved=fetched,
            version=reference(version),
            model=model,
            currency=currency,
            start=begin,
            end=finish,
            input_rate=format(amount(input_rate), "f"),
            output_rate=format(amount(output_rate), "f"),
            cached_rate=format(amount(cached_rate), "f"),
            synthetic=synthetic,
        )
        if amount(cached_rate) > amount(input_rate):
            raise ValueError("Cached rate must not exceed the conservative input rate.")
        pid = reference(json.dumps(body, sort_keys=True))
        with self.port.transaction() as db:
            records = self._read(db)
            budgets = {
                b["id"]
                for r in records
                if r["kind"] == "authority" and r["price"] == pid
                for b in r["budgets"]
            }
            if self._currency_hold(records, budgets, pid, currency):
                raise ValueError("Shared budget currencies are conflicting or unresolved.")
            if not any(r.get("id") == pid for r in records):
                self._event(db, "price", id=pid, **body)
        return pid

    def authorize(
        self,
        *,
        authority: str,
        owner: str,
        evidence: str,
        price: str,
        capability: str,
        configuration: str,
        start: str,
        end: str,
        budgets: list[Mapping[str, Any]],
        max_calls: int,
        max_depth: int,
    ) -> str:
        """Record operator-supplied authority, not an approval by this software."""
        if not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", capability):
            raise ValueError("A capability identifier is required.")
        begin, finish = timestamp(start), timestamp(end)
        if begin >= finish or not 1 <= count(max_calls, 100) or not 1 <= count(max_depth, 100):
            raise ValueError("Finite request limits and period required.")
        if not 1 <= len(budgets) <= 8:
            raise ValueError("Finite period and task budgets are required.")
        selected: list[dict[str, Any]] = []
        for b in budgets:
            if set(b) != {"id", "calls", "tokens", "amount"}:
                raise ValueError("Unexpected budget fields.")
            selected.append(
                dict(
                    id=opaque(b["id"]),
                    calls=count(b["calls"]),
                    tokens=count(b["tokens"]),
                    amount=format(amount(b["amount"]), "f"),
                )
            )
        if len({b["id"] for b in selected}) != len(selected):
            raise ValueError("Duplicate budget identity.")
        aid = reference(authority)
        body = dict(
            id=aid,
            owner=reference(owner),
            evidence=reference(evidence),
            price=opaque(price),
            capability=capability,
            configuration=opaque(configuration),
            start=begin,
            end=finish,
            budgets=selected,
            max_calls=max_calls,
            max_depth=max_depth,
        )
        with self.port.transaction() as db:
            records = self._read(db)
            previous = next((r for r in records if r.get("id") == aid), None)
            if previous:
                if previous != dict(schema=SCHEMA, kind="authority", **body):
                    raise ValueError("Authority is immutable; budget identities cannot reset.")
                return aid
            prices = {r["id"]: r for r in records if r["kind"] == "price"}
            if self._currency_hold(
                records, {b["id"] for b in selected}, price, prices.get(price, {}).get("currency")
            ):
                raise ValueError("Shared budget currencies are conflicting or unresolved.")
            for b in selected:
                for r in records:
                    if r["kind"] == "authority":
                        old = next((v for v in r["budgets"] if v["id"] == b["id"]), None)
                        if old is not None and old != b:
                            raise ValueError("Existing budget limits are immutable.")
            if any(
                r["kind"] == "authority"
                and r["capability"] == capability
                and r["configuration"] == configuration
                and max(begin, r["start"]) < min(finish, r["end"])
                for r in records
            ):
                raise ValueError("Overlapping authority for one configuration is ambiguous.")
            self._event(db, "authority", **body)
        return aid

    @staticmethod
    def _charge(price: Mapping[str, Any], used: Mapping[str, Any]) -> Decimal | None:
        if used.get("cached_tokens") is None:
            return None
        with localcontext() as ctx:
            ctx.prec = 80
            return (
                Decimal(count(used["prompt_tokens"]) - count(used["cached_tokens"]))
                * amount(price["input_rate"])
                + Decimal(count(used["cached_tokens"])) * amount(price["cached_rate"])
                + Decimal(count(used["completion_tokens"])) * amount(price["output_rate"])
            ) / Decimal(1000000)

    def reserve(
        self,
        context: CallContext,
        model: str,
        input_bound: int | None,
        output: int,
        *,
        live: bool = False,
    ) -> str:
        metadata = context.metadata()
        count(output)
        if input_bound is not None:
            count(input_bound)
        held = None
        with self.port.transaction() as db:
            records, now = self._read(db), self.port.now(db)
            authorities = [
                r
                for r in records
                if r["kind"] == "authority"
                and r["capability"] == context.capability
                and r["configuration"] == context.configuration
            ]
            authority = next(
                (r for r in reversed(authorities) if r["start"] <= now < r["end"]), None
            )
            owner = (
                authority["owner"]
                if authority
                else (
                    authorities[-1]["owner"] if authorities else reference("unassigned-owner-OD-51")
                )
            )
            price = next(
                (
                    r
                    for r in records
                    if r["kind"] == "price"
                    and authority
                    and r["id"] == authority["price"]
                    and r["model"] == model
                    and r["retrieved"] <= now
                    and r["start"] <= now < r["end"]
                ),
                None,
            )
            reservations = [r for r in records if r["kind"] == "reserved"]
            if any(r["attempt"] == context.attempt for r in reservations):
                held = "duplicate-attempt"
            elif not authority:
                held = "authority-expired" if authorities else "authority-unknown"
            elif not price or (live and price["synthetic"]):
                held = "price-unknown"
            elif input_bound is None:
                held = "liability-unknown"
            elif context.depth > authority["max_depth"]:
                held = "request-depth-limit"
            elif sum(r["root"] == context.root for r in reservations) >= authority["max_calls"]:
                held = "request-call-limit"
            cost = (
                self._charge(
                    price,
                    dict(prompt_tokens=input_bound, completion_tokens=output, cached_tokens=0),
                )
                if price and input_bound is not None
                else None
            )
            if authority and price is not None and not held:
                held = self._currency_hold(
                    records, {b["id"] for b in authority["budgets"]}, price["id"], price["currency"]
                )
            if authority and not held:
                completions = {r["id"]: r for r in records if r["kind"] == "completed"}
                for budget in authority["budgets"]:
                    prior = [r for r in reservations if budget["id"] in r["budgets"]]
                    if any(
                        (r["id"] in completions and completions[r["id"]]["held"])
                        or (r["id"] not in completions and now >= r["at"] + 40)
                        for r in prior
                    ):
                        held = "liability-unknown"
                        break
                    tokens = sum(
                        completions[r["id"]]["tokens"]["total_tokens"]
                        if r["id"] in completions
                        else r["input_bound"] + r["output_bound"]
                        for r in prior
                    )
                    money = money_sum(
                        (
                            charge_amount(completions[r["id"]]["charge"])
                            if r["id"] in completions
                            else charge_amount(r["liability"])
                            for r in prior
                        ),
                    )
                    if len(prior) + 1 > budget["calls"]:
                        held = "call-budget-limit"
                    elif tokens + input_bound + output > budget["tokens"]:
                        held = "token-budget-limit"
                    elif cost is None or money_sum(iter((money, cost))) > amount(budget["amount"]):
                        held = "money-budget-limit"
                    if held:
                        break
            if held:
                self._event(
                    db,
                    "alert",
                    owner=owner,
                    root=context.root,
                    attempt=context.attempt,
                    reason=held,
                    route="workflow-only",
                )
            else:
                if authority is None or price is None or cost is None:
                    raise ValueError("Financial admission invariant failed.")
                rid = reference(uuid.uuid4().hex)
                self._event(
                    db,
                    "reserved",
                    id=rid,
                    at=now,
                    **metadata,
                    authority=authority["id"],
                    owner=owner,
                    price=price["id"],
                    model=model,
                    budgets=[b["id"] for b in authority["budgets"]],
                    input_bound=input_bound,
                    output_bound=output,
                    liability=format(cost, "f"),
                )
        if held:
            raise DispatchHeld(held)
        return rid

    def dispatch_check(self, rid: str) -> None:
        """Recheck exclusive expiry after credential acquisition, before the network."""
        with self.port.transaction() as db:
            records, now = self._read(db), self.port.now(db)
            reserved = next(r for r in records if r["kind"] == "reserved" and r["id"] == rid)
            authority = next(
                r for r in records if r["kind"] == "authority" and r["id"] == reserved["authority"]
            )
            price = next(
                r for r in records if r["kind"] == "price" and r["id"] == reserved["price"]
            )
            held = (
                "authority-expired"
                if now >= min(authority["end"], price["end"])
                else "liability-unknown"
                if now >= reserved["at"] + 40
                else None
            )
            completions = {r["id"]: r for r in records if r["kind"] == "completed"}
            if not held and any(
                r["kind"] == "reserved"
                and set(reserved["budgets"]).intersection(r["budgets"])
                and (
                    (r["id"] in completions and completions[r["id"]]["held"])
                    or (r["id"] not in completions and now >= r["at"] + 40)
                )
                for r in records
            ):
                held = "liability-unknown"
            if not held:
                held = self._currency_hold(
                    records, set(reserved["budgets"]), price["id"], price["currency"]
                )
            if not held and rid in completions:
                held = "duplicate-attempt"
            if held:
                self._event(
                    db,
                    "alert",
                    owner=reserved["owner"],
                    root=reserved["root"],
                    attempt=reserved["attempt"],
                    reason=held,
                    route="workflow-only",
                )
        if held:
            raise DispatchHeld(held)

    def complete(self, rid: str, value: object, model: object, outcome: str) -> None:
        if outcome not in ("returned", "timeout", "provider-unavailable"):
            raise ValueError("Closed provider outcome required.")
        opaque(rid)
        with self.port.transaction() as db:
            records = self._read(db)
            reservation = next(
                (r for r in records if r["kind"] == "reserved" and r["id"] == rid), None
            )
            if reservation is None:
                raise ValueError("Unknown financial reservation.")
            if any(r["kind"] == "completed" and r["id"] == rid for r in records):
                return
            price = next(
                r for r in records if r["kind"] == "price" and r["id"] == reservation["price"]
            )
            used = usage(value)
            safe_model = bounded_model(model)
            charge = self._charge(price, used) if used else None
            reason = None
            if (
                model != reservation["model"]
                or used is None
                or charge is None
                or self.port.now(db) >= reservation["at"] + 40
            ):
                reason = "liability-unknown"
            elif (
                used["prompt_tokens"] > reservation["input_bound"]
                or used["completion_tokens"] > reservation["output_bound"]
                or charge > charge_amount(reservation["liability"])
            ):
                reason = "liability-overrun"
            self._event(
                db,
                "completed",
                id=rid,
                at=self.port.now(db),
                tokens=used,
                charge=format(charge, "f") if charge is not None else None,
                outcome=outcome,
                held=reason is not None,
                returned_model=reference(safe_model) if safe_model is not None else None,
            )
            if reason:
                self._event(
                    db,
                    "alert",
                    owner=reservation["owner"],
                    root=reservation["root"],
                    attempt=reservation["attempt"],
                    reason=reason,
                    route="workflow-only",
                )

    def publish_output(
        self, root: str, output: str, *, eligible: bool, db: Any = None
    ) -> dict[str, str] | None:
        """A financial hold cannot invalidate the caller's manual delivery route."""
        try:
            self.output(root, output, eligible=eligible, db=db)
        except DispatchHeld as error:
            logging.getLogger(__name__).warning("AI output attribution held (%s)", error)
            return dict(status="unresolved", reason=str(error), cost=UNKNOWN)
        return None

    def output(self, root: str, output: str, *, eligible: bool, db: Any = None) -> None:
        opaque(root)
        oid = reference(output)

        def write(conn: Any) -> None:
            records = self._read(conn)
            if any(
                r["kind"] == "review-orphan"
                and (r["root"] == root or r["output"] == oid)
                and (r["root"] != root or r["output"] != oid)
                for r in records
            ):
                raise ValueError("Output attribution differs from the original review root.")
            previous = next(
                (
                    r
                    for r in records
                    if r["kind"] == "output" and (r["root"] == root or r["output"] == oid)
                ),
                None,
            )
            if previous and (
                previous["root"] != root
                or previous["output"] != oid
                or previous["eligible"] != eligible
            ):
                raise ValueError("Output attribution is immutable.")
            if previous is None:
                self._event(
                    conn, "output", root=root, output=oid, eligible=eligible, at=self.port.now(conn)
                )

        if type(eligible) is not bool:
            raise ValueError("Explicit proposal eligibility required.")
        if db is not None:
            write(db)
        else:
            with self.port.transaction() as conn:
                write(conn)

    @staticmethod
    def _review_revision(records: list[dict[str, Any]], oid: str) -> int:
        return count(
            max(
                (
                    r["revision"]
                    for r in records
                    if r["kind"] in ("review", "review-intent") and r["output"] == oid
                ),
                default=0,
            )
        )

    @staticmethod
    def _pending_review(records: list[dict[str, Any]], oid: str, action: str) -> str | None:
        intents = [r for r in records if r["kind"] == "review-intent" and r["output"] == oid]
        latest = max(intents, key=lambda r: r["revision"], default=None)
        reviewed = max(
            (r["revision"] for r in records if r["kind"] == "review" and r["output"] == oid),
            default=0,
        )
        return (
            opaque(latest["id"])
            if latest and latest["revision"] > reviewed and latest["action"] == action
            else None
        )

    def pending_review(self, output: str, action: str) -> str | None:
        if action not in ("accept", "edit-accept", "reject"):
            raise ValueError("Closed review disposition required.")
        with self.port.transaction() as db:
            return self._pending_review(self._read(db), reference(output), action)

    def review_intent(self, output: str, action: str, *, root: str | None = None) -> str:
        if action not in ("accept", "edit-accept", "reject"):
            raise ValueError("Closed review disposition required.")
        oid = reference(output)
        if root is not None:
            opaque(root)
        with self.port.transaction() as db:
            records = self._read(db)
            linked = next(
                (r for r in records if r["kind"] == "output" and r["output"] == oid), None
            )
            if linked is not None and root is not None and linked["root"] != root:
                raise ValueError("Output attribution differs from the original review root.")
            if linked is None:
                if action != "reject" or root is None:
                    raise ValueError("Output attribution is missing; economics remains incomplete.")
                associations = [
                    r
                    for r in records
                    if r["kind"] in ("output", "review-orphan")
                    and (r["root"] == root or r["output"] == oid)
                ]
                if any(r["root"] != root or r["output"] != oid for r in associations):
                    raise ValueError("Output attribution differs from the original review root.")
                if not associations:
                    self._event(db, "review-orphan", root=root, output=oid, at=self.port.now(db))
            pending = self._pending_review(records, oid, action)
            if pending:
                return pending
            iid = reference(uuid.uuid4().hex)
            self._event(
                db,
                "review-intent",
                id=iid,
                output=oid,
                action=action,
                at=self.port.now(db),
                revision=count(self._review_revision(records, oid) + 1),
            )
            return iid

    def review(
        self,
        output: str,
        action: str,
        *,
        db: Any = None,
        intent: str | None = None,
        root: str | None = None,
    ) -> None:
        if action not in ("accept", "edit-accept", "reject"):
            raise ValueError("Closed review disposition required.")
        oid = reference(output)
        if root is not None:
            opaque(root)
            if action != "reject":
                raise ValueError("Only rejection can repair an unlinked assistant output.")

        def write(conn: Any) -> None:
            records = self._read(conn)
            linked = next(
                (r for r in records if r["kind"] == "output" and r["output"] == oid), None
            )
            if root is not None and any(
                r["kind"] in ("output", "review-orphan")
                and (r["root"] == root or r["output"] == oid)
                and (r["root"] != root or r["output"] != oid)
                for r in records
            ):
                raise ValueError("Output attribution differs from the original review root.")
            orphan = any(r["kind"] == "review-orphan" and r["output"] == oid for r in records)
            if linked is None and not (action == "reject" and (root is not None or orphan)):
                raise ValueError("Output attribution is missing; economics remains incomplete.")
            if intent is not None:
                opaque(intent)
                pending = self._pending_review(records, oid, action)
                if pending != intent:
                    if any(
                        r["kind"] == "review"
                        and r["intent"] == intent
                        and r["output"] == oid
                        and r["action"] == action
                        for r in records
                    ):
                        return
                    raise ValueError("Review intent does not match the pending attribution.")
            previous = max(
                (r for r in records if r["kind"] == "review" and r["output"] == oid),
                key=lambda r: r["revision"],
                default=None,
            )
            revision = self._review_revision(records, oid)
            if (
                intent is None
                and previous
                and previous["action"] == action
                and previous["revision"] == revision
            ):
                return
            if linked is None and root is not None:
                self._event(
                    conn, "output", root=root, output=oid, eligible=False, at=self.port.now(conn)
                )
            self._event(
                conn,
                "review",
                output=oid,
                action=action,
                at=self.port.now(conn),
                revision=count(revision + 1),
                intent=intent,
            )

        if db is not None:
            write(db)
        else:
            with self.port.transaction() as conn:
                write(conn)

    def review_unresolved(
        self, root: str, output: str, reason: str, *, revision: int, db: Any
    ) -> None:
        """Persist withdrawal without scanning unavailable metering evidence."""
        if reason not in ("meter-capacity-reached", "meter-evidence-invalid"):
            raise ValueError("A closed metering hold reason is required.")
        self._event(
            db,
            "review-unresolved",
            root=opaque(root),
            output=reference(output),
            action="reject",
            at=self.port.now(db),
            reason=reason,
            revision=count(revision),
        )

    def billing(
        self,
        *,
        source: str,
        allocation: str,
        budget: str,
        start: str,
        end: str,
        currency: str,
        billed: str,
        tolerance: str,
        complete: bool,
        synthetic: bool,
    ) -> str:
        begin, finish = timestamp(start), timestamp(end)
        if (
            begin >= finish
            or currency not in ("USD", "GBP", "EUR")
            or type(complete) is not bool
            or type(synthetic) is not bool
            or amount(tolerance) > 1
        ):
            raise ValueError("Billing period, coverage and owner tolerance are required.")
        bid = reference(source)
        body = dict(
            id=bid,
            allocation=reference(allocation),
            budget=opaque(budget),
            start=begin,
            end=finish,
            currency=currency,
            billed=format(amount(billed), "f"),
            tolerance=format(amount(tolerance), "f"),
            complete=complete,
            synthetic=synthetic,
        )
        with self.port.transaction() as db:
            records = self._read(db)
            for r in records:
                if r["kind"] == "billing" and (
                    r["id"] == bid
                    or (r["budget"] == budget and max(begin, r["start"]) < min(finish, r["end"]))
                ):
                    raise ValueError("Duplicate/overlapping billing; preserve original evidence.")
            self._event(db, "billing", **body)
        return bid

    def report(
        self,
        *,
        start: str,
        end: str,
        as_of: str,
        quality: Mapping[str, Any] | None = None,
        components: Mapping[str, str] | None = None,
        capacity_hours: str | None = None,
        batch: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        begin, finish, cutoff = report_period(start, end, as_of)
        with self.port.transaction() as db:
            records = self._read(db)
        calls = [r for r in records if r["kind"] == "reserved" and begin <= r["at"] < finish]
        completions = {
            r["id"]: r for r in records if r["kind"] == "completed" and r["at"] <= cutoff
        }
        outputs = {r["root"]: r for r in records if r["kind"] == "output" and r["at"] <= cutoff}
        reviews: dict[str, Any] = {}
        for r in records:
            if r["kind"] == "review" and r["at"] <= cutoff:
                if r["revision"] > reviews.get(r["output"], {}).get("revision", 0):
                    reviews[r["output"]] = r
        roots = {r["root"] for r in calls}
        unresolved = {
            r["output"]
            for r in records
            if r["kind"] == "review-unresolved" and r["at"] <= cutoff and r["root"] in roots
        }
        accepted = sum(
            root in outputs
            and outputs[root]["eligible"]
            and outputs[root]["output"] not in unresolved
            and reviews.get(outputs[root]["output"], {}).get("action") in ("accept", "edit-accept")
            for root in roots
        )
        unknown = sum(r["id"] not in completions or completions[r["id"]]["held"] for r in calls)
        unjoined = len(roots - outputs.keys())
        cohort_outputs = {o["output"] for o in outputs.values() if o["root"] in roots}
        orphan_outputs = {
            r["output"]
            for r in records
            if r["kind"] == "review-orphan" and r["at"] <= cutoff and r["root"] in roots
        }
        unjoined_reviews = len(
            {
                r["output"]
                for r in records
                if r["kind"] == "review-intent"
                and r["at"] <= cutoff
                and r["output"] in cohort_outputs | orphan_outputs
                and r["revision"] > reviews.get(r["output"], {}).get("revision", 0)
            }
            | (orphan_outputs - cohort_outputs)
            | unresolved
        )
        prices = {r["id"]: r for r in records if r["kind"] == "price"}
        currencies = {prices[r["price"]]["currency"] for r in calls}
        projected = (
            None
            if unknown
            else money_sum(charge_amount(completions[r["id"]]["charge"]) for r in calls)
        )
        bills = [
            r
            for r in records
            if r["kind"] == "billing"
            and r["start"] == begin
            and r["end"] == finish
            and r["complete"]
            and currencies == {r["currency"]}
            and calls
            and all(r["budget"] in c["budgets"] for c in calls)
        ]
        bill = bills[0] if len(bills) == 1 else None
        cost, ratio, variance, status = UNKNOWN, UNKNOWN, UNKNOWN, "unreconciled"
        if bill and projected is not None and not unjoined and not unjoined_reviews:
            billed = amount(bill["billed"])
            cost = format(billed, "f")
            if accepted:
                with localcontext() as ctx:
                    ctx.prec = 80
                    ratio = format(billed / accepted, "f")
            if billed:
                with localcontext() as ctx:
                    ctx.prec = 80
                    delta = abs(billed - projected) / billed
                variance = format(delta, "f")
                status = "variance-alert" if delta > amount(bill["tolerance"]) else "reconciled"
            else:
                variance = "0" if projected == 0 else UNKNOWN
                status = "reconciled" if projected == 0 else "variance-alert"
        measures: dict[str, Any] = {k: UNKNOWN for k in QUALITY}
        quality_status = UNKNOWN
        if quality is not None:
            if (
                set(quality) != {"approved", "cohort", "metrics"}
                or type(quality["approved"]) is not bool
            ):
                raise ValueError("Explicit quality authority and matched cohort required.")
            expected_cohort = reference(json.dumps(sorted(roots)))
            if quality["cohort"] != expected_cohort or set(quality["metrics"]) != set(QUALITY):
                raise ValueError("Quality must match the exact call cohort.")
            quality_status = "Pass" if quality["approved"] else UNKNOWN
            for key in QUALITY:
                metric = quality["metrics"][key]
                if set(metric) != {"count", "denominator", "floor", "baseline"}:
                    raise ValueError("Closed observed quality metric required.")
                observed, denominator = count(metric["count"]), count(metric["denominator"])
                floor, baseline = amount(metric["floor"]), amount(metric["baseline"])
                if observed > denominator or floor > 1 or baseline > 1:
                    raise ValueError("Invalid quality rate.")
                with localcontext() as ctx:
                    ctx.prec = 80
                    rate = Decimal(observed) / denominator if denominator else None
                measures[key] = dict(
                    count=observed,
                    denominator=denominator,
                    rate=str(rate) if rate is not None else UNKNOWN,
                )
                if rate is None:
                    if quality_status != "Failure":
                        quality_status = UNKNOWN
                elif rate > floor or rate > baseline:
                    quality_status = "Failure"
        other = {k: UNKNOWN for k in COMPONENTS}
        if components is not None:
            if set(components) - set(COMPONENTS):
                raise ValueError("Unexpected TCA component.")
            other.update({k: format(amount(v), "f") for k, v in components.items()})
        total = UNKNOWN
        if cost != UNKNOWN and all(v != UNKNOWN for v in other.values()):
            total = format(
                money_sum(iter([amount(cost), *(amount(v) for v in other.values())])), "f"
            )
        totals = []
        for root in roots:
            attempts = [r for r in calls if r["root"] == root]
            if all(r["id"] in completions and completions[r["id"]]["tokens"] for r in attempts):
                totals.append(sum(completions[r["id"]]["tokens"]["total_tokens"] for r in attempts))
        spread = batch_spread(totals, batch)
        alerts = [r for r in records if r["kind"] == "alert" and begin <= r["at"] < finish]
        return dict(
            schema=SCHEMA,
            period=dict(start=start, end=end, as_of=as_of, basis="call-time UTC [start,end)"),
            coverage="incomplete"
            if unknown or unjoined or unjoined_reviews
            else "recorded-ledger-only",
            coverage_gaps=[
                "Historical calls and independent resident accounting are not financially joined.",
                "Supplied price/billing/quality evidence is not verified by this software.",
            ],
            cohort=reference(json.dumps(sorted(roots))),
            calls=len(calls),
            retries=sum(r["retry"] > 0 for r in calls),
            failures=sum(completions.get(r["id"], {}).get("outcome") != "returned" for r in calls),
            unknown_liabilities=unknown,
            owned_alerts=[
                dict(owner=r["owner"], reason=r["reason"], route=r["route"]) for r in alerts
            ],
            tokens_per_proposal=dict(
                measured=len(totals),
                missing=len(roots) - len(totals),
                minimum=min(totals) if totals else UNKNOWN,
                maximum=max(totals) if totals else UNKNOWN,
                mean=str(Decimal(sum(totals)) / len(totals)) if totals else UNKNOWN,
                evidence_label=spread.pop("evidence_label"),
                **spread,
            ),
            unjoined_outputs=unjoined,
            unjoined_reviews=unjoined_reviews,
            accepted_proposals=accepted,
            denominator="human-accepted eligible proposal outputs in call-time cohort",
            token_cost=cost,
            projected_token_charge=format(projected, "f") if projected is not None else UNKNOWN,
            cost_per_accepted_proposal=ratio,
            reconciliation=status,
            variance_fraction=variance,
            currency=next(iter(currencies)) if len(currencies) == 1 else UNKNOWN,
            financial_source=bill["id"] if bill else None,
            evidence_label=(
                "synthetic"
                if (bill and bill["synthetic"])
                or any(prices[r["price"]]["synthetic"] for r in calls)
                else "supplied-unverified"
            ),
            other_tca_components=other,
            total_cost_of_ai=total,
            quality=measures,
            quality_status=quality_status,
            quality_qualified_cost=ratio if quality_status == "Pass" else UNKNOWN,
            capacity_hours=format(amount(capacity_hours), "f")
            if capacity_hours is not None
            else UNKNOWN,
            capacity_classification="capacity, not cash; Finance-booked destination not supplied",
            cash_value=UNKNOWN,
        )
