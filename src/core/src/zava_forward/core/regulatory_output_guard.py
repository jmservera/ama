"""Deterministic output-validation guard for regulatory summaries, assistants, and views.

Inspects generated or rendered regulatory prose and metadata without calling any
model. Blocks or rewrites any claim that:
  1. states a legal or statutory duty is satisfied (`duty_satisfied`),
  2. gives legal advice or binding legal counsel (`legal_advice`), or
  3. applies future, consultative, uncommenced, or non-human-activated rules as
     active operational rules (`future_law_applied_as_active`).
"""

from __future__ import annotations

import re
import threading
import unicodedata
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Literal

GUARD_VERSION = "regulatory-non-advice-guard-v1"
ViolationCategory = Literal[
    "duty_satisfied",
    "legal_advice",
    "future_law_applied_as_active",
]
GuardAction = Literal["passed", "rewritten", "rejected"]
ViolationMode = Literal["rewrite", "reject"]

CATEGORIES: tuple[ViolationCategory, ...] = (
    "duty_satisfied",
    "legal_advice",
    "future_law_applied_as_active",
)
NON_ACTIVE_STATUSES: frozenset[str] = frozenset(
    {"consultation", "future_phase", "historical", "draft", "not_reviewed"}
)
ELIGIBLE_ACTIVE_STATUSES: frozenset[str] = frozenset(
    {"in_force", "guidance", "recorded-synthetic-demo"}
)

ADVISORY_REVIEW_TEXT = (
    "Advisory review item only: dated regulatory reference pending named human "
    "Compliance or Legal review. Legal applicability and satisfaction of any duty "
    "are not assessed; this is not legal advice, and unactivated, consultation, or "
    "future-phase material is not an active operational rule."
)

_CONFUSABLES = str.maketrans(
    {
        "\u0430": "a",
        "\u0410": "A",
        "\u0435": "e",
        "\u0415": "E",
        "\u0456": "i",
        "\u0406": "I",
        "\u043e": "o",
        "\u041e": "O",
        "\u0440": "p",
        "\u0420": "P",
        "\u0441": "c",
        "\u0421": "C",
        "\u0443": "y",
        "\u0423": "Y",
        "\u0445": "x",
        "\u0425": "X",
        "\u04bb": "h",
        "\u04ba": "H",
        "\u0455": "s",
        "\u0405": "S",
        "\u0458": "j",
        "\u0408": "J",
        "\u04cf": "l",
        "\u04c0": "I",
        "\u03b1": "a",
        "\u03b5": "e",
        "\u03b9": "i",
        "\u03bf": "o",
        "\u03c1": "p",
        "\u03ba": "k",
        "\u03bd": "v",
        "\u03c4": "t",
    }
)

_SENTENCE_SPLIT_RE = re.compile(r"[.;!?\n|]+")
_LOCAL_BOUNDARY_RE = re.compile(
    r"(?:,|—|--|\b(?:but|yet|however|whereas|although|though|so|therefore|thus|and)\b)",
    re.I,
)
_SPAN_NEGATION_RE = re.compile(
    r"\b(?:not|no|never|neither|nor|cannot|can't|can\s+not|"
    r"does\s+not|do\s+not|did\s+not|is\s+not|are\s+not|was\s+not|were\s+not|"
    r"will\s+not|must\s+not|may\s+not|should\s+not|"
    r"unassessed|non-binding|inactive)\b",
    re.I,
)
_PRE_NEGATION_RE = re.compile(
    r"\b(?:not|no|never|neither|nor|cannot|can't|can\s+not|"
    r"does\s+not|do\s+not|did\s+not|is\s+not|are\s+not|was\s+not|were\s+not|"
    r"will\s+not|must\s+not|may\s+not|should\s+not|without|whether|if|"
    r"unassessed|non-binding|inactive)\b",
    re.I,
)
_GOVERNING_NEGATION_RE = re.compile(
    r"\b(?:cannot|can't|can\s+not|does\s+not|do\s+not|must\s+not|never)\s+"
    r"(?:decide|confirm|determine|assess|establish|state|mean|imply|"
    r"constitute|give|provide|apply|treat|certify|approve)\b",
    re.I,
)
_GOVERNING_PIVOT_RE = re.compile(
    r"\b(?:but|yet|however|therefore|thus|still|instead|nevertheless)\b",
    re.I,
)
_POST_NEGATION_RE = re.compile(
    r"^\s*(?:is|are|was|were|remains?)?\s*(?:not|never|unassessed|inactive)\b",
    re.I,
)

_DUTY_SATISFIED_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "duty_or_obligation_satisfied",
        re.compile(
            r"\b(?:(?:legal|statutory|regulatory|landlord|provider|housing|safety|"
            r"damp(?:\s+and\s+mould)?|hazard|awaab'?s?\s+law|section\s+[0-9a-z]+)\s+)?"
            r"(?:duty|duties|obligation|obligations)\s+"
            r"(?:under\s+[^.,;]{1,50}\s+)?"
            r"(?:is|are|has\s+been|have\s+been|was|were|stands?|remains?)\s+"
            r"(?:fully\s+|now\s+|already\s+|completely\s+)?"
            r"(?:satisfied|met|fulfilled|discharged)\b",
            re.I,
        ),
    ),
    (
        "satisfies_statutory_duty",
        re.compile(
            r"\b(?:satisf(?:y|ies|ied)|fulfil(?:s|led)?|fulfill(?:s|ed)?|discharg(?:e|es|ed)|"
            r"meet(?:s)?)\s+(?:the\s+|all\s+|its\s+|our\s+|your\s+|their\s+)?"
            r"(?:legal|statutory|regulatory|awaab'?s?\s+law|section\s+[0-9a-z]+)\s+"
            r"(?:duty|duties|obligation|obligations|requirements?)\b",
            re.I,
        ),
    ),
    (
        "complies_with_legislation",
        re.compile(
            r"\b(?:compl(?:y|ies|ied)|in\s+(?:full\s+)?compliance)\s+with\s+"
            r"(?:the\s+)?(?:act|statute|legislation|regulations?|regulatory\s+standard|"
            r"awaab'?s?\s+law|social\s+housing\s+\(regulation\)\s+act|"
            r"landlord\s+and\s+tenant\s+act|building\s+safety\s+act|housing\s+act|"
            r"decent\s+homes\s+standard|section\s+[0-9a-z]+)\b",
            re.I,
        ),
    ),
    (
        "legally_compliant_assertion",
        re.compile(
            r"\b(?:is|are|remains?|stands?|deemed|certified|confirmed(?:\s+to\s+be)?|"
            r"treated\s+as)\s+(?:fully\s+|now\s+)?"
            r"(?:legally|statutorily|regulatorily)\s+compliant\b",
            re.I,
        ),
    ),
    (
        "entity_has_complied",
        re.compile(
            r"\b(?:provider|landlord|home|property|case|organisation|organization|"
            r"zava(?:\s+north\s+homes)?)\s+(?:has|have)\s+(?:fully\s+)?complied\b",
            re.I,
        ),
    ),
)

_LEGAL_ADVICE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "explicit_legal_advice",
        re.compile(
            r"\b(?:legal\s+advice|legal\s+counsel|formal\s+legal\s+opinion|"
            r"binding\s+legal\s+(?:opinion|determination|ruling|interpretation))\b",
            re.I,
        ),
    ),
    (
        "directed_legal_requirement_or_exemption",
        re.compile(
            r"\b(?:you\s+are|the\s+landlord\s+is|the\s+provider\s+is|zava\s+is|"
            r"your\s+organisation\s+is|the\s+tenant\s+is|the\s+resident\s+is)\s+"
            r"(?:now\s+|hereby\s+|strictly\s+)?"
            r"legally\s+(?:required|obliged|obligated|bound|exempt|exempted|"
            r"entitled|permitted|protected|liable|immune)\b",
            re.I,
        ),
    ),
    (
        "verb_legally_obligates_or_exempts",
        re.compile(
            r"\blegally\s+(?:obligates|exempts|immunises|immunizes|binds|absolves)\s+"
            r"(?:you|the\s+landlord|the\s+provider|zava)\b",
            re.I,
        ),
    ),
    (
        "assistant_advises_legally",
        re.compile(
            r"\b(?:we|i|this\s+assistant|this\s+system)\s+"
            r"(?:legally\s+advise|advise\s+you\s+legally|confirm\s+legal\s+liability)\b",
            re.I,
        ),
    ),
)

_FUTURE_LAW_LEXICAL_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "applies_future_or_uncommenced_as_active",
        re.compile(
            r"\b(?:appl(?:y|ies|ied|ying)|treat(?:s|ed|ing)?|enforc(?:e|es|ed|ing))\s+"
            r"(?:the\s+|this\s+|any\s+)?(?:future(?:\s+law|\s+phase|\s+provision)?|"
            r"uncommenced(?:\s+law|\s+phase|\s+provision)?|"
            r"consultation(?:\s+paper|\s+draft|\s+material|\s+proposal)?|"
            r"proposed\s+(?:law|rule|standard|phase))\s+"
            r"(?:now\s+)?(?:as\s+)?(?:an\s+)?(?:active|in\s+force|binding|live|"
            r"operational\s+rule)\b",
            re.I,
        ),
    ),
    (
        "future_or_consultation_is_active_now",
        re.compile(
            r"\b(?:future\s+(?:law|phase(?:\s+\d+)?|provision|rule|standard)|"
            r"uncommenced\s+(?:law|phase(?:\s+\d+)?|provision|rule|standard)|"
            r"consultation(?:\s+(?:draft|material|proposal|paper|rule|phase(?:\s+\d+)?|"
            r"provision|standard))?)\s+"
            r"(?:is|are|applies|operates|takes\s+effect)\s+"
            r"(?:now\s+|currently\s+|already\s+|immediately\s+)?"
            r"(?:as\s+)?"
            r"(?:active|in\s+force|binding|an\s+active\s+(?:operational\s+)?rule|"
            r"a\s+live\s+(?:operational\s+)?(?:rule|control))\b",
            re.I,
        ),
    ),
    (
        "active_without_human_activation",
        re.compile(
            r"\b(?:active\s+operational\s+rule|applies\s+as\s+an\s+active\s+rule)\s+"
            r"without\s+(?:named\s+)?(?:human|owner|compliance)\s+"
            r"(?:rule\s+)?(?:activation|approval|review)\b",
            re.I,
        ),
    ),
)

_CONTEXTUAL_ACTIVE_ASSERTION_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "contextual_active_operational_rule",
        re.compile(
            r"\b(?:active\s+operational\s+rule|active\s+live\s+control|"
            r"currently\s+active\s+rule|applies\s+(?:now\s+)?as\s+an\s+active\s+rule|"
            r"currently\s+in\s+force\s+and\s+active|enforced\s+now\s+as\s+an\s+active\s+rule)\b",
            re.I,
        ),
    ),
)


def normalize_guard_text(text: str) -> str:
    """Fold NFKC, strip Unicode format/invisible characters, and map homoglyphs."""
    normalized = unicodedata.normalize("NFKC", text)
    cleaned = "".join(ch for ch in normalized if unicodedata.category(ch) != "Cf")
    folded = cleaned.translate(_CONFUSABLES)
    return re.sub(r"\s+", " ", folded).strip()


def _day_prefix(value: str | None) -> str | None:
    if not value:
        return None
    stripped = value.strip()
    return stripped[:10] if len(stripped) >= 10 else stripped


def _mask_verbatim_quotes(text: str, verbatim_quotes: Iterable[str] | None) -> str:
    if not verbatim_quotes:
        return text
    masked = text
    for quote in verbatim_quotes:
        norm_quote = normalize_guard_text(quote)
        if norm_quote:
            masked = masked.replace(f'"{norm_quote}"', '"[VERBATIM_EXCERPT]"')
            masked = masked.replace(norm_quote, "[VERBATIM_EXCERPT]")
    return masked


def _is_match_negated(sentence: str, start: int, end: int) -> bool:
    span = sentence[start:end]
    if _SPAN_NEGATION_RE.search(span):
        return True
    after = sentence[end : end + 32]
    local_after = _LOCAL_BOUNDARY_RE.split(after, maxsplit=1)[0]
    if _POST_NEGATION_RE.search(local_after):
        return True
    before = sentence[max(0, start - 64) : start]
    local_before = _LOCAL_BOUNDARY_RE.split(before)[-1]
    if _PRE_NEGATION_RE.search(local_before):
        return True
    wider_before = sentence[max(0, start - 140) : start]
    gov = _GOVERNING_NEGATION_RE.search(wider_before)
    if gov and not _GOVERNING_PIVOT_RE.search(wider_before[gov.end() :]):
        return True
    return False


def advisory_review_summary(
    *,
    source_id: str | None = None,
    provision_id: str | None = None,
    source_date: str | None = None,
    retrieved_date: str | None = None,
    status: str | None = None,
    human_rule_activated: bool | None = None,
) -> str:
    """Build deterministic advisory review-item replacement preserving provenance."""
    parts: list[str] = []
    if provision_id:
        parts.append(f"provision {provision_id}")
    elif source_id:
        parts.append(f"source {source_id}")
    if status:
        parts.append(f"status {status}")
    if source_date:
        parts.append(f"source date {source_date}")
    if retrieved_date:
        parts.append(f"retrieved {retrieved_date}")
    if human_rule_activated is not None:
        act_state = "human-activated" if human_rule_activated else "not human-activated"
        parts.append(act_state)
    prefix = f" ({'; '.join(parts)})" if parts else ""
    return (
        f"Advisory review item only{prefix}: dated regulatory reference pending named "
        "human Compliance or Legal review. Legal applicability and satisfaction of any "
        "duty are not assessed; this is not legal advice, and unactivated, consultation, "
        "or future-phase material is not an active operational rule."
    )


@dataclass(frozen=True)
class GuardDecision:
    checked: bool
    passed: bool
    action: GuardAction
    violations: tuple[ViolationCategory, ...]
    reasons: tuple[str, ...]
    rewritten_text: str | None
    guard_version: str = GUARD_VERSION

    def to_status_dict(self) -> dict[str, Any]:
        """Compact per-payload status block without duplicating full rewritten text."""
        return {
            "checked": self.checked,
            "passed": self.passed,
            "action": self.action,
            "violations": list(self.violations),
            "reasons": list(self.reasons),
            "guard_version": self.guard_version,
        }


class GuardTelemetry:
    """Thread-safe deterministic counter registry for regulatory output guard checks."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._checked_total = 0
        self._passed_total = 0
        self._flagged_total = 0
        self._rewritten_total = 0
        self._rejected_total = 0
        self._by_category: dict[str, int] = {cat: 0 for cat in CATEGORIES}
        self._last_decision: dict[str, Any] | None = None

    def record_decision(self, decision: GuardDecision) -> GuardDecision:
        with self._lock:
            self._checked_total += 1
            if decision.passed:
                self._passed_total += 1
            else:
                self._flagged_total += 1
                if decision.action == "rewritten":
                    self._rewritten_total += 1
                elif decision.action == "rejected":
                    self._rejected_total += 1
                for cat in decision.violations:
                    self._by_category[cat] = self._by_category.get(cat, 0) + 1
            self._last_decision = decision.to_status_dict()
        return decision

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                "guard_version": GUARD_VERSION,
                "deterministic": True,
                "model_calls": 0,
                "checked_total": self._checked_total,
                "passed_total": self._passed_total,
                "flagged_total": self._flagged_total,
                "rewritten_total": self._rewritten_total,
                "rejected_total": self._rejected_total,
                "by_category": dict(self._by_category),
                "last_decision": dict(self._last_decision) if self._last_decision else None,
            }

    def reset(self) -> None:
        with self._lock:
            self._checked_total = 0
            self._passed_total = 0
            self._flagged_total = 0
            self._rewritten_total = 0
            self._rejected_total = 0
            self._by_category = {cat: 0 for cat in CATEGORIES}
            self._last_decision = None


DEFAULT_GUARD_TELEMETRY = GuardTelemetry()


def _unactivated_reason(
    *,
    status: str | None,
    effective: str | None,
    as_of: str | None,
    review_status: str | None,
    human_rule_activated: bool | None,
) -> str | None:
    eff_day = _day_prefix(effective)
    as_of_day = _day_prefix(as_of)
    if status in ("consultation", "future_phase", "historical", "draft"):
        return f"source_status={status}"
    if status is not None and status not in ELIGIBLE_ACTIVE_STATUSES:
        return f"source_status={status}"
    if review_status is not None and review_status in ("not_reviewed", "historical"):
        return f"review_status={review_status}"
    if eff_day and as_of_day and eff_day > as_of_day:
        return f"future_effective={eff_day}>{as_of_day}"
    if human_rule_activated is False:
        return "human_rule_activated=False"
    return None


def inspect_regulatory_output(
    text: str,
    *,
    status: str | None = None,
    effective: str | None = None,
    retrieved: str | None = None,
    as_of: str | None = None,
    review_status: str | None = None,
    human_rule_activated: bool | None = None,
    active_operational_rule: bool | None = None,
    active_control: bool | None = None,
    source_id: str | None = None,
    provision_id: str | None = None,
    verbatim_quotes: Iterable[str] | None = None,
    on_violation: ViolationMode = "rewrite",
    telemetry: GuardTelemetry | None = None,
) -> GuardDecision:
    """Deterministically validate rendered regulatory text and activation context."""
    violations: list[ViolationCategory] = []
    reasons: list[str] = []

    def add_violation(cat: ViolationCategory, reason: str) -> None:
        if cat not in violations:
            violations.append(cat)
        if reason not in reasons:
            reasons.append(reason)

    unactivated = _unactivated_reason(
        status=status,
        effective=effective,
        as_of=as_of,
        review_status=review_status,
        human_rule_activated=human_rule_activated,
    )
    if unactivated is not None and (active_operational_rule is True or active_control is True):
        add_violation(
            "future_law_applied_as_active",
            f"active_flag_with_{unactivated}",
        )

    normalized = normalize_guard_text(text)
    allow_quote_mask = unactivated is None
    inspectable = (
        _mask_verbatim_quotes(normalized, verbatim_quotes) if allow_quote_mask else normalized
    )

    for sentence in _SENTENCE_SPLIT_RE.split(inspectable):
        clause = sentence.strip()
        if not clause:
            continue
        for rule_name, pattern in _DUTY_SATISFIED_PATTERNS:
            for match in pattern.finditer(clause):
                if not _is_match_negated(clause, match.start(), match.end()):
                    add_violation("duty_satisfied", rule_name)
        for rule_name, pattern in _LEGAL_ADVICE_PATTERNS:
            for match in pattern.finditer(clause):
                if not _is_match_negated(clause, match.start(), match.end()):
                    add_violation("legal_advice", rule_name)
        for rule_name, pattern in _FUTURE_LAW_LEXICAL_PATTERNS:
            for match in pattern.finditer(clause):
                if not _is_match_negated(clause, match.start(), match.end()):
                    add_violation("future_law_applied_as_active", rule_name)
        if unactivated is not None:
            for rule_name, pattern in _CONTEXTUAL_ACTIVE_ASSERTION_PATTERNS:
                for match in pattern.finditer(clause):
                    if not _is_match_negated(clause, match.start(), match.end()):
                        add_violation(
                            "future_law_applied_as_active",
                            f"{rule_name}:{unactivated}",
                        )

    if not violations:
        decision = GuardDecision(
            checked=True,
            passed=True,
            action="passed",
            violations=(),
            reasons=(),
            rewritten_text=None,
        )
    else:
        replacement = (
            advisory_review_summary(
                source_id=source_id,
                provision_id=provision_id,
                source_date=_day_prefix(effective),
                retrieved_date=_day_prefix(retrieved),
                status=status,
                human_rule_activated=human_rule_activated,
            )
            if any(
                v is not None
                for v in (
                    source_id,
                    provision_id,
                    effective,
                    retrieved,
                    status,
                    human_rule_activated,
                )
            )
            else ADVISORY_REVIEW_TEXT
        )
        action: GuardAction = "rewritten" if on_violation == "rewrite" else "rejected"
        decision = GuardDecision(
            checked=True,
            passed=False,
            action=action,
            violations=tuple(violations),
            reasons=tuple(reasons),
            rewritten_text=replacement if on_violation == "rewrite" else None,
        )

    if telemetry is not None:
        telemetry.record_decision(decision)
    return decision


def guard_regulatory_text(
    text: str,
    *,
    status: str | None = None,
    effective: str | None = None,
    retrieved: str | None = None,
    as_of: str | None = None,
    review_status: str | None = None,
    human_rule_activated: bool | None = None,
    active_operational_rule: bool | None = None,
    active_control: bool | None = None,
    source_id: str | None = None,
    provision_id: str | None = None,
    verbatim_quotes: Iterable[str] | None = None,
    telemetry: GuardTelemetry | None = None,
) -> tuple[str, GuardDecision]:
    """Validate text and return `(safe_text, decision)` with deterministic advisory rewrite."""
    decision = inspect_regulatory_output(
        text,
        status=status,
        effective=effective,
        retrieved=retrieved,
        as_of=as_of,
        review_status=review_status,
        human_rule_activated=human_rule_activated,
        active_operational_rule=active_operational_rule,
        active_control=active_control,
        source_id=source_id,
        provision_id=provision_id,
        verbatim_quotes=verbatim_quotes,
        on_violation="rewrite",
        telemetry=telemetry,
    )
    if decision.passed:
        return text, decision
    return decision.rewritten_text or ADVISORY_REVIEW_TEXT, decision


def merge_guard_statuses(
    statuses: Iterable[Mapping[str, Any]],
    *,
    telemetry: GuardTelemetry | None = None,
) -> dict[str, Any]:
    """Combine per-item `to_status_dict()` blocks into one aggregate payload check status."""
    items = list(statuses)
    violations: list[str] = []
    reasons: list[str] = []
    rewritten_count = 0
    rejected_count = 0
    for item in items:
        if not item.get("passed", True):
            if item.get("action") == "rewritten":
                rewritten_count += 1
            elif item.get("action") == "rejected":
                rejected_count += 1
            for cat in item.get("violations", ()):
                if cat not in violations:
                    violations.append(str(cat))
            for reason in item.get("reasons", ()):
                if reason not in reasons:
                    reasons.append(str(reason))
    passed = rewritten_count == 0 and rejected_count == 0 and not violations
    action: GuardAction = (
        "passed"
        if passed
        else "rejected"
        if rejected_count > 0 and rewritten_count == 0
        else "rewritten"
    )
    merged: dict[str, Any] = {
        "checked": True,
        "items_checked": len(items),
        "passed": passed,
        "action": action,
        "rewritten_count": rewritten_count,
        "rejected_count": rejected_count,
        "violations": violations,
        "reasons": reasons,
        "guard_version": GUARD_VERSION,
    }
    if telemetry is not None:
        merged["telemetry"] = telemetry.snapshot()
    return merged
