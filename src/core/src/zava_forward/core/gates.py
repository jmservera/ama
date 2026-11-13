"""Deterministic gate results for controlled transitions (FR-008, RULE-001, RULE-002; issue #82).

A gate returns pass, fail or unknown with a plain-word reason, the responsible owner and
a correction route. Unknown never passes: only an explicit pass lets a transition go ahead.
Each gate is tied to a rule record naming its source, effective date, version and reviewer.
The rule records here are exercise fixtures, not legal or operational approval.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from typing import Any

PASS, FAIL, UNKNOWN = "pass", "fail", "unknown"
OUTCOMES = (PASS, FAIL, UNKNOWN)
GATE_KINDS = (
    "evidence",
    "eligibility",
    "authority",
    "safety",
    "resident",
    "funding",
    "capacity",
    "quality",
    "finance",
)


@dataclass(frozen=True)
class GateRule:
    gate: str
    source: str
    effective_date: str
    version: str
    reviewer: str

    def __post_init__(self) -> None:
        for value in (self.gate, self.source, self.version, self.reviewer):
            if not isinstance(value, str) or not value.strip():
                raise ValueError("A gate rule needs a gate, source, version and reviewer.")
        if date.fromisoformat(self.effective_date).isoformat() != self.effective_date:
            raise ValueError("A gate rule effective date must be ISO YYYY-MM-DD.")

    def as_record(self) -> dict[str, str]:
        return dict(
            gate=self.gate,
            source=self.source,
            effective_date=self.effective_date,
            version=self.version,
            reviewer=self.reviewer,
        )


@dataclass(frozen=True)
class GateResult:
    gate: str
    outcome: str
    reason: str
    owner: str
    correction: str
    rule: GateRule | None = None

    def __post_init__(self) -> None:
        if self.outcome not in OUTCOMES:
            raise ValueError("A gate outcome is pass, fail or unknown.")
        if not self.reason.strip():
            raise ValueError("A gate result needs a reason.")

    @property
    def passed(self) -> bool:
        return self.outcome == PASS

    def as_record(self) -> dict[str, Any]:
        return dict(
            gate=self.gate,
            outcome=self.outcome,
            reason=self.reason,
            owner=self.owner,
            correction=self.correction,
            rule=self.rule.as_record() if self.rule else None,
        )


def _result(rule: GateRule, outcome: str, reason: str, owner: str, correction: str) -> GateResult:
    return GateResult(rule.gate, outcome, reason, owner, correction, rule)


def check(
    rule: GateRule, state: Any, *, owner: str, correction: str, label: str, on: str | None = None
) -> GateResult:
    """Pass only when state is exactly True; missing or non-boolean evidence is unknown."""
    if rule.effective_date > (on or date.today().isoformat()):
        return _result(
            rule, UNKNOWN, f"The rule for {label} is not yet in effect.", owner, correction
        )
    if state is True:
        return _result(rule, PASS, f"{label}: met.", owner, correction)
    if state is False:
        return _result(rule, FAIL, f"{label}: not met.", owner, correction)
    return _result(
        rule, UNKNOWN, f"{label}: no evidence recorded, so this cannot pass.", owner, correction
    )


def transition_allowed(results: Iterable[GateResult]) -> bool:
    """A transition needs at least one gate and every gate an explicit pass."""
    items = list(results)
    return bool(items) and all(r.outcome == PASS for r in items)


def unmet(results: Iterable[GateResult]) -> list[GateResult]:
    return [r for r in results if r.outcome != PASS]


SAFETY_RELEASE_RULE = GateRule(
    gate="safety",
    source="docs/brds/agentic-retrofit-programme-brd.md RULE-001; PRD FR-008 (exercise fixture)",
    effective_date="2026-11-03",
    version="1",
    reviewer="Unreviewed exercise rule: named reviewer required before live use",
)


def _norm(value: Any) -> str:
    return value.strip().casefold() if isinstance(value, str) else ""


def _reason(value: Any, fallback: str) -> str:
    """A caller reason only when it is a non-blank string, so a gate result is never blank."""
    return value if isinstance(value, str) and value.strip() else fallback


def _recorders(items: Iterable[Any] | None) -> list[Any] | None:
    """Recorder identities: strings or None (unknown) from a non-string iterable, else None."""
    if items is None or isinstance(items, (str, bytes, dict)):
        return None
    try:
        listed = list(items)
    except TypeError:
        return None
    return listed if all(item is None or isinstance(item, str) for item in listed) else None


def _text_items(items: Iterable[Any] | None) -> list[str] | None:
    """Non-blank strings from a non-string iterable; anything else is unreadable (None)."""
    if items is None or isinstance(items, (str, bytes, dict)):
        return None
    try:
        listed = list(items)
    except TypeError:
        return None
    if not all(isinstance(item, str) and item.strip() for item in listed):
        return None
    return listed


def safety_release_gate(
    hold: dict[str, Any] | None,
    actor: dict[str, Any],
    recorders: Iterable[Any],
    on: str | None = None,
) -> GateResult:
    """Release needs the hold's named accountable role and a person other than the recorders.

    recorders are identities of whoever raised the issue or recorded the repair.
    """
    role = hold.get("accountable_role") if isinstance(hold, dict) else None
    owner = role if isinstance(role, str) and role.strip() else "Building Safety Liaison"
    fix = f"Ask the {owner} to record the release decision."
    rule = SAFETY_RELEASE_RULE
    if not isinstance(hold, dict) or not _norm(role):
        return _result(
            rule,
            UNKNOWN,
            "No accountable safety role is recorded for this stop, so work cannot restart.",
            owner,
            "Record the accountable role by referring the issue to the safety service.",
        )
    if _norm(actor.get("role")) != _norm(role):
        return _result(rule, FAIL, f"Only the {role} can restart this stopped work.", owner, fix)
    identity = [actor.get(k) for k in ("email", "code", "oid")]
    others = _recorders(recorders)
    if others is None or any(v is not None and not isinstance(v, str) for v in identity):
        return _result(
            rule,
            UNKNOWN,
            "The releasing or recording identity is malformed, so independence is unverified.",
            owner,
            fix,
        )
    me = {_norm(v) for v in identity} - {""}
    if not me:
        return _result(
            rule, UNKNOWN, "The releasing person's identity is not recorded.", owner, fix
        )
    if any(_norm(r) in me for r in others):
        return _result(
            rule,
            FAIL,
            "A different person must restart this stopped work. "
            "You raised it or recorded the repair.",
            owner,
            fix,
        )
    return check(
        rule,
        True,
        owner=owner,
        correction=fix,
        label="Accountable role and independent person",
        on=on,
    )


_UNREVIEWED = "Unreviewed exercise rule: named reviewer required before live use"
_BRD = "docs/brds/agentic-retrofit-programme-brd.md"


def _booking_rule(gate: str, source: str) -> GateRule:
    return GateRule(gate, source, "2026-11-04", "1", _UNREVIEWED)


BOOKING_RULES = {
    "funding": _booking_rule("funding", f"{_BRD} RULE-001; PRD FR-008 (exercise fixture)"),
    "safety": _booking_rule("safety", f"{_BRD} RULE-001; PRD FR-008 (exercise fixture)"),
    "resident": _booking_rule("resident", f"{_BRD} RULE-002; PRD FR-008 (exercise fixture)"),
    "evidence": _booking_rule("evidence", f"{_BRD} RULE-001; PRD FR-008 (exercise fixture)"),
}


def booking_gates(
    case: dict[str, Any], resident_reasons: Iterable[str] | None, on: str | None = None
) -> list[GateResult]:
    """Funding, safety and resident gates for 'Ready to book'; missing evidence is unknown.

    resident_reasons is the resident gate's list of unmet conditions, or None when it could
    not be worked out.
    """
    funding = case.get("funding_ok")
    results = [
        check(
            BOOKING_RULES["funding"],
            funding if isinstance(funding, bool) else None,
            owner=str(case.get("owner") or "Case owner"),
            correction="Check the funding and record it.",
            label="Funding confirmed",
            on=on,
        )
    ]
    hazards = case.get("hazards")
    safe: bool | None = None
    if isinstance(hazards, list):
        safe = all(isinstance(h, dict) and h.get("released") is True for h in hazards)
    results.append(
        check(
            BOOKING_RULES["safety"],
            safe,
            owner="Building Safety Liaison",
            correction="Obtain the independent safety decision to restart retrofit work.",
            label="No open safety issue",
            on=on,
        )
    )
    reasons = _text_items(resident_reasons)
    results.append(
        check(
            BOOKING_RULES["resident"],
            None if reasons is None else not reasons,
            owner="Resident Liaison Officer",
            correction="Review the resident's current decision and authority.",
            label="Resident decision current",
            on=on,
        )
    )
    return results


def evidence_gate(missing: Iterable[str] | None, owner: str, on: str | None = None) -> GateResult:
    """Pass only when the required evidence kinds are all on file; None means not worked out."""
    kinds = _text_items(missing)
    result = check(
        BOOKING_RULES["evidence"],
        None if kinds is None else not kinds,
        owner=owner,
        correction="Upload or request the missing evidence and record it.",
        label="Required evidence on file",
        on=on,
    )
    if result.outcome == FAIL and kinds:
        reason = f"Required evidence missing: {', '.join(kinds)}."
        return GateResult(result.gate, FAIL, reason, owner, result.correction, result.rule)
    return result


QUALITY_RULE = GateRule(
    gate="quality",
    source=(
        "docs/prds/zava-forward-retrofit-programme-demonstrator.md FR-008 (governing) and FR-017; "
        "versioned quality checklist in quality.CHECKLISTS (exercise fixture)"
    ),
    effective_date="2026-11-05",
    version="1",
    reviewer=_UNREVIEWED,
)


def quality_gate(gaps: Iterable[str] | None, owner: str, on: str | None = None) -> GateResult:
    """Pass only when every checklist item has evidence; None means the record is unreadable."""
    items = _text_items(gaps)
    result = check(
        QUALITY_RULE,
        None if items is None else not items,
        owner=owner,
        correction="Ask the quality owner to record evidence for every check before this step.",
        label="Quality evidence on file",
        on=on,
    )
    if result.outcome == FAIL and items:
        reason = f"Checks without evidence: {'; '.join(items)}."
        return GateResult(result.gate, FAIL, reason, owner, result.correction, result.rule)
    return result


CAPACITY_RULE = GateRule(
    gate="capacity",
    source=(
        "docs/prds/zava-forward-retrofit-programme-demonstrator.md FR-008 (governing) and FR-016; "
        "evidenced committed capacity in procurement (exercise fixture)"
    ),
    effective_date="2026-11-06",
    version="1",
    reviewer=_UNREVIEWED,
)


def capacity_gate(state: bool | None, reason: str, on: str | None = None) -> GateResult:
    """True passes, False is a known violation, None is missing or unreadable evidence."""
    owner = "Contract Manager"
    correction = "Ask the contract manager to record current evidenced capacity."
    if state is True:
        return check(
            CAPACITY_RULE,
            True,
            owner=owner,
            correction=correction,
            label="Evidenced capacity",
            on=on,
        )
    return _result(
        CAPACITY_RULE,
        FAIL if state is False else UNKNOWN,
        _reason(reason, "Evidenced capacity is not confirmed."),
        owner,
        correction,
    )


class CapacityGateError(ValueError):
    """A capacity refusal that keeps its ValueError text and carries the gate result."""

    def __init__(self, message: str, state: bool | None) -> None:
        super().__init__(message)
        self.state = state
        self.result = capacity_gate(state, message)


def _controlled_rule(gate: str, requirement: str) -> GateRule:
    return GateRule(
        gate,
        f"docs/prds/zava-forward-retrofit-programme-demonstrator.md FR-008 (governing) and "
        f"{requirement} (exercise fixture)",
        "2026-11-13",
        "1",
        _UNREVIEWED,
    )


ELIGIBILITY_RULE = _controlled_rule("eligibility", "FR-019 grant and funder eligibility")
AUTHORITY_RULE = _controlled_rule("authority", "FR-019 scoped financial designation")
FINANCE_RULE = _controlled_rule("finance", "FR-019 approved budget and commitment limit")


def _outcome_gate(
    rule: GateRule,
    state: bool | None,
    reason: str,
    owner: str,
    correction: str,
    label: str,
    on: str | None,
) -> GateResult:
    """True passes only through the rule's effective-date check; False fails, None is unknown."""
    if state is True:
        return check(rule, True, owner=owner, correction=correction, label=label, on=on)
    return _result(
        rule,
        FAIL if state is False else UNKNOWN,
        _reason(reason, f"{label}: not confirmed, so this cannot pass."),
        owner,
        correction,
    )


def eligibility_gate(
    state: bool | None, reason: str, owner: str, on: str | None = None
) -> GateResult:
    """Only an explicit recorded eligibility pass lets a transition go ahead."""
    return _outcome_gate(
        ELIGIBILITY_RULE,
        state,
        reason,
        owner,
        "Ask the Grants Officer to record the eligibility check.",
        "Eligibility confirmed",
        on,
    )


def authority_gate(state: bool | None, reason: str, on: str | None = None) -> GateResult:
    owner = "Finance authority owner"
    return _outcome_gate(
        AUTHORITY_RULE,
        state,
        reason,
        owner,
        "Ask the Finance authority owner to record a current scoped designation.",
        "Current scoped financial designation",
        on,
    )


def finance_gate(state: bool | None, reason: str, on: str | None = None) -> GateResult:
    return _outcome_gate(
        FINANCE_RULE,
        state,
        reason,
        "Finance approver",
        "Ask Finance to approve a budget that covers this commitment.",
        "Approved budget covers the commitment",
        on,
    )


class AuthorityGateError(PermissionError):
    """An authority refusal that keeps its PermissionError text and carries the gate result."""

    def __init__(self, message: str, state: bool | None, on: str | None = None) -> None:
        super().__init__(message)
        self.state = state
        self.result = authority_gate(state, message, on)


class FinanceGateError(ValueError):
    """A finance refusal that keeps its ValueError text and carries the gate result."""

    def __init__(self, message: str, state: bool | None, on: str | None = None) -> None:
        super().__init__(message)
        self.state = state
        self.result = finance_gate(state, message, on)


CONTROLLED_RULES: tuple[GateRule, ...] = (
    SAFETY_RELEASE_RULE,
    *BOOKING_RULES.values(),
    QUALITY_RULE,
    CAPACITY_RULE,
    ELIGIBILITY_RULE,
    AUTHORITY_RULE,
    FINANCE_RULE,
)


def unreviewed_rules() -> list[GateRule]:
    """Rules still carrying the explicit unreviewed marker; a named reviewer clears an entry."""
    return [r for r in CONTROLLED_RULES if r.reviewer == _UNREVIEWED]
