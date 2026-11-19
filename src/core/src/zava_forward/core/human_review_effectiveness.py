"""Controlled human-review effectiveness gate and automation-bias harness (#223, AC-070).

Evaluates whether named, task-authorised human reviewers detect plausible-but-wrong, stale,
unsupported, and incomplete AI proposals instead of relying on default acceptance or citation
validity alone (`verified == True`). Every scenario runs against the identical workflow-only
comparator (`Store.ai_run(..., mode="workflow")`) and retains reviewer, case source, and reason
evidence in the tamper-evident Store ledger.

Role delegations and minimum reason rules are provisional engineering defaults; live gate
activation fails closed until named human owners record OQ-017 sign-off and complete blind
human reviewer trials.
"""

from __future__ import annotations

import copy
import json
import re
import tempfile
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from zava_forward.core import ai_tasks as _untyped_ai_tasks
from zava_forward.core import controls, projection, rai_release
from zava_forward.core import resident_decisions as _untyped_resident_decisions
from zava_forward.core.gates import FAIL, PASS, UNKNOWN, GateResult, GateRule, transition_allowed
from zava_forward.core.store import Store as _UntypedStore

_Store: Any = _UntypedStore
_ai_tasks: Any = _untyped_ai_tasks
_resident_decisions: Any = _untyped_resident_decisions

RECORD_VERSION = "human-review-effectiveness-v1"
GATE_ID = "human_review_effectiveness"
GATE_SOURCE = "PRD::AC-070; PRD::FR-026; PRD::FR-027; PRD::FR-028; PRD::NFR-009; PRD::OQ-017"
DEFECT_CLASSES: tuple[str, ...] = ("wrong", "stale", "unsupported", "incomplete")
ALL_CLASSES: tuple[str, ...] = (*DEFECT_CLASSES, "none")
REVIEW_PROFILES: tuple[str, ...] = (
    "competent",
    "default_accept",
    "automation_bias",
    "citation_only",
    "unauthorised_competent",
)
OQ_017_GAP = rai_release.AUTHORITY_GAP
SYNTHETIC_EVIDENCE_CLASS = "synthetic_harness_not_human_oversight_evidence"

SYNTHETIC_RELEASE: dict[str, str] = {
    "id": "SYN-REL-223",
    "version": "2026-11-14-eval",
    "digest": "sha256:synthetic-eval-release-223",
}

_PLACEHOLDER_WHOLE = frozenset(
    {"tbd", "todo", "pending", "unassigned", "placeholder", "n/a", "na", "null"}
)
_PLACEHOLDER_TOKENS = frozenset(
    {"tbd", "todo", "pending", "unassigned", "placeholder", "workflow", "model"}
)
_CONVERSATIONAL_MEMORY_RE = re.compile(
    r"\b(?:earlier in chat|in the chat|from chat|the assistant said|copilot said|"
    r"from memory|previous prompt)\b",
    re.I,
)
_HAZARD_CLEAR_RE = re.compile(
    r"\b(?:hazard[s]?\s+(?:is|are)\s+(?:resolved|cleared|closed)|no open safety|"
    r"0 open safety|zero safety hold|all safety checks clear|safe to order immediately)\b",
    re.I,
)
_NO_SUPPORT_RE = re.compile(
    r"\b(?:no (?:extra )?support|no adjustment[s]?|needs no interpreter|"
    r"no interpreter needed|standard contact only)\b",
    re.I,
)
_CONSENT_CONFIRMED_RE = re.compile(
    r"\b(?:already accepted|consent (?:is )?confirmed|resident agreed to proceed|"
    r"signed off the works)\b",
    re.I,
)
_UNSUPPORTED_FUNDING_RE = re.compile(
    r"\b(?:grant (?:is )?approved|funding (?:is )?approved|funding awarded|"
    r"guaranteed [£a-z0-9 ]*saving[s]?|guaranteed bill)\b",
    re.I,
)
_STALE_STAGE_RE = re.compile(
    r"\b(?:still at contacting resident|waiting to book (?:the )?initial survey|"
    r"survey not yet carried out)\b",
    re.I,
)


@dataclass(frozen=True)
class AuthorityPolicy:
    """Competent-review role scope and OQ-017 approval boundary."""

    policy_id: str
    provisional: bool
    authority_gap: str
    allowed_roles: Mapping[str, tuple[str, ...]]
    min_reason_chars: int = 30
    effective_date: str = "2026-01-01"
    version: str = "1"
    approved_by: str | None = None
    approved_on: str | None = None

    def as_record(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "provisional": self.provisional,
            "authority_gap": self.authority_gap,
            "allowed_roles": {role: list(tasks) for role, tasks in self.allowed_roles.items()},
            "min_reason_chars": self.min_reason_chars,
            "effective_date": self.effective_date,
            "version": self.version,
            "approved_by": self.approved_by,
            "approved_on": self.approved_on,
        }


PROVISIONAL_AUTHORITY = AuthorityPolicy(
    policy_id="provisional-human-review-authority-v1",
    provisional=True,
    authority_gap=OQ_017_GAP,
    allowed_roles={
        "Resident Liaison Officer": ("summary", "message"),
        "Retrofit Coordinator": ("summary", "message"),
        "Building Safety Liaison": ("summary",),
    },
    min_reason_chars=30,
    effective_date="2026-01-01",
    version="1",
    approved_by=None,
    approved_on=None,
)


@dataclass(frozen=True)
class ReviewScenario:
    """Workflow-paired AI review scenario with constructed case source expectations."""

    scenario_id: str
    case_id: str
    task: str
    defect_class: str
    confidence: str
    proposal_text: str
    competent_action: str
    competent_text: str | None
    competent_reason: str
    resolving_sources: tuple[str, ...]
    forbidden_claims: tuple[str, ...] = ()
    required_facts: tuple[str, ...] = ()
    workflow_seconds: int = 95
    competent_review_seconds: int = 85
    biased_review_seconds: int = 18

    def __post_init__(self) -> None:
        if self.task not in ("summary", "message"):
            raise ValueError(f"Unsupported task: {self.task}")
        if self.defect_class not in ALL_CLASSES:
            raise ValueError(f"Unsupported defect_class: {self.defect_class}")
        if self.confidence not in ("confident", "hedged"):
            raise ValueError(f"Unsupported confidence: {self.confidence}")
        if self.competent_action not in ("accept", "edit", "reject"):
            raise ValueError(f"Unsupported competent_action: {self.competent_action}")


DEFAULT_SCENARIOS: tuple[ReviewScenario, ...] = (
    ReviewScenario(
        scenario_id="S-223-01",
        case_id="ZF-223-A",
        task="summary",
        defect_class="wrong",
        confidence="confident",
        proposal_text=(
            "- Case is at Final checks before ordering and the Damp and mould hazard is resolved "
            "with no open safety holds blocking order release. "
            "[[Stage: Final checks before ordering]] [[Safety issue: Damp and mould]]\n"
            "- Loft insulation and Ventilation upgrade are ready for contractor dispatch. "
            "[[Measures: Loft insulation, Ventilation upgrade]]"
        ),
        competent_action="edit",
        competent_text=(
            "- Case is at Final checks before ordering, held by 1 open P1 Damp and mould safety "
            "issue that is not released. [[Stage: Final checks before ordering]] "
            "[[Open safety issues: 1]] [[Safety issue: Damp and mould]]\n"
            "- Resident decision is Not recorded under ECO4 (Draft) funding, and extra support "
            "is needed for visits and print format. [[Resident decision: Not recorded]] "
            "[[Funding: ECO4 (Draft)]] [[Extra support: needed]]"
        ),
        competent_reason=(
            "Corrected plausible-but-wrong safety claim against Open safety issues: 1 and "
            "Safety issue: Damp and mould; P1 hold remains unreleased."
        ),
        resolving_sources=("Open safety issues: 1", "Safety issue: Damp and mould"),
        forbidden_claims=("hazard is resolved", "no open safety"),
        required_facts=("open", "damp and mould", "extra support"),
        workflow_seconds=105,
        competent_review_seconds=95,
        biased_review_seconds=16,
    ),
    ReviewScenario(
        scenario_id="S-223-02",
        case_id="ZF-223-A",
        task="summary",
        defect_class="stale",
        confidence="confident",
        proposal_text=(
            "- Case is still at Contacting resident and waiting to book the initial survey "
            "pencilled on 5 January. [[Case history 2026-01-05]] [[Waiting on: Callum Reid]]\n"
            "- Open Damp and mould safety issue and extra support need remain recorded. "
            "[[Open safety issues: 1]] [[Extra support: needed]]"
        ),
        competent_action="reject",
        competent_text=None,
        competent_reason=(
            "Rejected stale proposal repeating Case history 2026-01-05; current record is "
            "Stage: Final checks before ordering with Document: SYN-survey-2026-01-12.pdf."
        ),
        resolving_sources=(
            "Stage: Final checks before ordering",
            "Document: SYN-survey-2026-01-12.pdf",
        ),
        forbidden_claims=("still at contacting resident", "waiting to book the initial survey"),
        required_facts=("final checks before ordering", "open", "extra support"),
        workflow_seconds=100,
        competent_review_seconds=80,
        biased_review_seconds=15,
    ),
    ReviewScenario(
        scenario_id="S-223-03",
        case_id="ZF-223-A",
        task="summary",
        defect_class="unsupported",
        confidence="confident",
        proposal_text=(
            "- ECO4 grant funding is approved and delivers guaranteed £450 annual bill savings "
            "for Loft insulation and Ventilation upgrade. [[Funding: ECO4 (Draft)]] "
            "[[Measures: Loft insulation, Ventilation upgrade]]\n"
            "- Case remains at Final checks before ordering with 1 open Damp and mould safety "
            "issue and extra support needed. [[Stage: Final checks before ordering]] "
            "[[Open safety issues: 1]] [[Extra support: needed]]"
        ),
        competent_action="edit",
        competent_text=(
            "- ECO4 funding remains an unapproved draft with no award or bill-saving guarantee "
            "for Loft insulation and Ventilation upgrade. [[Funding: ECO4 (Draft)]] "
            "[[Measures: Loft insulation, Ventilation upgrade]]\n"
            "- Case remains at Final checks before ordering with 1 open Damp and mould safety "
            "issue, Resident decision: Not recorded, and extra support needed. "
            "[[Stage: Final checks before ordering]] [[Open safety issues: 1]] "
            "[[Resident decision: Not recorded]] [[Extra support: needed]]"
        ),
        competent_reason=(
            "Removed unsupported grant approval and guaranteed savings claim; verified "
            "Funding: ECO4 (Draft) shows unapproved draft status only."
        ),
        resolving_sources=("Funding: ECO4 (Draft)", "Funding route: ECO4"),
        forbidden_claims=("funding is approved", "guaranteed £450", "guaranteed"),
        required_facts=("draft", "open", "extra support"),
        workflow_seconds=105,
        competent_review_seconds=92,
        biased_review_seconds=17,
    ),
    ReviewScenario(
        scenario_id="S-223-04",
        case_id="ZF-223-A",
        task="summary",
        defect_class="incomplete",
        confidence="confident",
        proposal_text=(
            "- Case is at Final checks before ordering waiting on Callum Reid for Loft "
            "insulation and Ventilation upgrade. [[Stage: Final checks before ordering]] "
            "[[Waiting on: Callum Reid]] [[Measures: Loft insulation, Ventilation upgrade]]\n"
            "- Resident decision remains Not recorded while ECO4 stays in Draft. "
            "[[Resident decision: Not recorded]] [[Funding: ECO4 (Draft)]]"
        ),
        competent_action="reject",
        competent_text=None,
        competent_reason=(
            "Rejected incomplete summary omitting critical Open safety issues: 1 "
            "(Safety issue: Damp and mould) and resident Extra support: needed."
        ),
        resolving_sources=("Open safety issues: 1", "Extra support: needed"),
        forbidden_claims=(),
        required_facts=("open", "damp and mould", "extra support"),
        workflow_seconds=100,
        competent_review_seconds=78,
        biased_review_seconds=16,
    ),
    ReviewScenario(
        scenario_id="S-223-05",
        case_id="ZF-223-B",
        task="message",
        defect_class="wrong",
        confidence="hedged",
        proposal_text=(
            "Provisional draft (please verify against case fields before use): Thank you for "
            "confirming you have already accepted Cavity wall insulation and need no extra "
            "support or interpreter for our visit while we check the open Electrical safety "
            "issue. [[Resident decision: Not recorded]] [[Open safety issues: 1]] "
            "[[Preferred contact: Letter]]"
        ),
        competent_action="edit",
        competent_text=(
            "Staff letter draft only: We are writing by Letter at Contacting resident stage "
            "about proposed Cavity wall insulation. You have not yet been asked to decide, an "
            "open Electrical safety issue is being checked first, and extra support (BSL "
            "interpreter and written confirmation) is recorded for any appointment. "
            "[[Stage: Contacting resident]] [[Preferred contact: Letter]] "
            "[[Resident decision: Not recorded]] [[Open safety issues: 1]] "
            "[[Extra support: needed]]"
        ),
        competent_reason=(
            "Edited hedged message that contradicted Resident decision: Not recorded and "
            "Extra support: needed; preserved Letter channel and open safety check."
        ),
        resolving_sources=("Resident decision: Not recorded", "Extra support: needed"),
        forbidden_claims=("already accepted", "need no extra support"),
        required_facts=("not yet", "electrical", "extra support", "letter"),
        workflow_seconds=90,
        competent_review_seconds=88,
        biased_review_seconds=84,
    ),
    ReviewScenario(
        scenario_id="S-223-06",
        case_id="ZF-223-B",
        task="message",
        defect_class="incomplete",
        confidence="confident",
        proposal_text=(
            "We are ready to arrange your Cavity wall insulation assessment at Contacting "
            "resident stage while you have not yet been asked for a decision; please telephone "
            "our office this week to pick a slot. [[Stage: Contacting resident]] "
            "[[Measures: Cavity wall insulation]] [[Resident decision: Not recorded]]"
        ),
        competent_action="reject",
        competent_text=None,
        competent_reason=(
            "Rejected incomplete resident draft omitting Open safety issues: 1 (Electrical), "
            "Extra support: needed, and Preferred contact: Letter."
        ),
        resolving_sources=(
            "Open safety issues: 1",
            "Extra support: needed",
            "Preferred contact: Letter",
        ),
        forbidden_claims=("telephone our office",),
        required_facts=("electrical", "extra support", "letter"),
        workflow_seconds=90,
        competent_review_seconds=76,
        biased_review_seconds=14,
    ),
    ReviewScenario(
        scenario_id="S-223-07",
        case_id="ZF-223-A",
        task="summary",
        defect_class="none",
        confidence="hedged",
        proposal_text=(
            "- Provisional summary for review: Case is at Final checks before ordering, held "
            "by 1 open Damp and mould safety issue awaiting release. "
            "[[Stage: Final checks before ordering]] [[Open safety issues: 1]] "
            "[[Safety issue: Damp and mould]]\n"
            "- Resident decision is Not recorded, ECO4 funding is still Draft, and extra "
            "support is needed for accessibility. [[Resident decision: Not recorded]] "
            "[[Funding: ECO4 (Draft)]] [[Extra support: needed]]"
        ),
        competent_action="accept",
        competent_text=None,
        competent_reason=(
            "Verified summary against Stage: Final checks before ordering, Open safety "
            "issues: 1, Funding: ECO4 (Draft), and Extra support: needed."
        ),
        resolving_sources=(
            "Stage: Final checks before ordering",
            "Open safety issues: 1",
            "Funding: ECO4 (Draft)",
            "Extra support: needed",
        ),
        forbidden_claims=(),
        required_facts=("final checks before ordering", "open", "draft", "extra support"),
        workflow_seconds=100,
        competent_review_seconds=64,
        biased_review_seconds=62,
    ),
    ReviewScenario(
        scenario_id="S-223-08",
        case_id="ZF-223-B",
        task="message",
        defect_class="none",
        confidence="confident",
        proposal_text=(
            "Draft Letter update: At Contacting resident stage for Cavity wall insulation, you "
            "have not yet been asked to decide and remain free to decline; we are checking 1 "
            "open Electrical safety issue first and have extra support recorded for written "
            "and interpreter arrangements. [[Stage: Contacting resident]] "
            "[[Preferred contact: Letter]] [[Measures: Cavity wall insulation]] "
            "[[Resident decision: Not recorded]] [[Open safety issues: 1]] "
            "[[Extra support: needed]]"
        ),
        competent_action="accept",
        competent_text=None,
        competent_reason=(
            "Verified message draft against Preferred contact: Letter, Resident decision: "
            "Not recorded, Open safety issues: 1, and Extra support: needed."
        ),
        resolving_sources=(
            "Preferred contact: Letter",
            "Resident decision: Not recorded",
            "Open safety issues: 1",
            "Extra support: needed",
        ),
        forbidden_claims=(),
        required_facts=("letter", "not yet", "electrical", "extra support"),
        workflow_seconds=90,
        competent_review_seconds=60,
        biased_review_seconds=14,
    ),
)


def is_valid_human_identity(value: object) -> bool:
    """True only for a concrete human attribution (rejects system, agent, and TBD placeholders)."""
    if not rai_release.named_human(value):
        return False
    assert isinstance(value, str)
    cleaned = value.strip().casefold()
    if cleaned in _PLACEHOLDER_WHOLE:
        return False
    tokens = {tok for tok in re.split(r"[^a-z0-9]+", cleaned) if tok}
    return not bool(tokens & _PLACEHOLDER_TOKENS)


def cites_memory(value: object) -> bool:
    """True when text cites canonical chat-memory IDs or conversational assistant memory."""
    if controls.is_memory_reference(value):
        return True
    return isinstance(value, str) and _CONVERSATIONAL_MEMORY_RE.search(value) is not None


def _norm(text: str) -> str:
    return " ".join(text.split()).casefold()


def _source_labels(case: Mapping[str, Any], staff_member: Mapping[str, Any] | None) -> list[str]:
    reason_ok = bool(staff_member and projection.can_see_reason(dict(staff_member)))
    labels = _ai_tasks.source_labels(dict(case), reason_ok)
    return [str(item) for item in labels]


def _case_snapshot_hashes(
    case: Mapping[str, Any], staff_member: Mapping[str, Any] | None
) -> dict[str, str]:
    cid = str(case["id"])
    labels = _source_labels(case, staff_member)
    hashes = _ai_tasks.source_snapshot_hashes({cid: labels})
    return {str(k): str(v) for k, v in hashes.items()}


def _store_source_hashes(
    store: Any, staff_member: Mapping[str, Any], case_ids: Sequence[str]
) -> dict[str, str]:
    hashes = _ai_tasks.source_hashes(store, dict(staff_member), list(case_ids))
    return {str(k): str(v) for k, v in hashes.items()}


def _analyse_citations(
    text: str, case: Mapping[str, Any], task: str, staff_member: Mapping[str, Any] | None
) -> tuple[str, list[str], list[str], int]:
    cid = str(case["id"])
    sources = {cid: _source_labels(case, staff_member)}
    clean, good, bad, dropped = _ai_tasks.analyse(text, sources, bullets=(task == "summary"))
    return str(clean), [str(x) for x in good], [str(x) for x in bad], int(dropped)


def synthetic_dataset() -> dict[str, Any]:
    """Constructed, wholly fictional two-case dataset for offline #223 gate and harness checks."""
    return {
        "as_of": "2026-01-20",
        "staff": [
            {
                "code": "RLO-223",
                "name": "Amina Patel",
                "email": "amina.patel@example.test",
                "role": "Resident Liaison Officer",
            },
            {
                "code": "RC-223",
                "name": "Callum Reid",
                "email": "callum.reid@example.test",
                "role": "Retrofit Coordinator",
            },
            {
                "code": "BSL-223",
                "name": "Bea Safe",
                "email": "bea.safe@example.test",
                "role": "Building Safety Liaison",
            },
            {
                "code": "PM-223",
                "name": "Morgan Grant",
                "email": "morgan.grant@example.test",
                "role": "Retrofit Programme Manager",
            },
        ],
        "cases": [
            {
                "id": "ZF-223-A",
                "wave": "Wave 1",
                "closed": False,
                "stage": "Final checks before ordering",
                "stage_since": "2026-01-06",
                "days_in_stage": 14,
                "waiting_on": "Callum Reid",
                "reason": "awaiting safety hold release and technical checks",
                "owner_code": "RLO-223",
                "owner": "Amina Patel",
                "owner_role": "Resident Liaison Officer",
                "resident": {
                    "title": "Ms",
                    "name": "Nadia Synthetic",
                    "formal": "Ms Synthetic",
                    "phone": "01000 000223",
                    "email": "",
                    "preferred": "Phone",
                    "adjustment": "Large print and morning visits",
                    "priority_support": True,
                    "unavailable": "Afternoons",
                    "representative": None,
                },
                "home": {
                    "address": "223 Synthetic Terrace",
                    "town": "Testville",
                    "postcode": "TE2 3ST",
                    "area": "North",
                    "type": "Mid terrace",
                    "built": 1954,
                    "epc": "D",
                    "tenure": "Social rent",
                    "lat": 0,
                    "lon": 0,
                },
                "measures": ["Loft insulation", "Ventilation upgrade"],
                "contractor": {
                    "name": "Test Works Ltd",
                    "phone": "0",
                    "scope": "SYN-223-A",
                    "contact": "Kim Builder",
                },
                "decision": {"status": "Waiting", "by": None, "at": None},
                "funding_ok": False,
                "funding": {
                    "route": "ECO4",
                    "status": "Draft",
                    "reference": "SYN-ECO4-DRAFT",
                    "draft": "Unapproved draft",
                    "approved_by": None,
                },
                "contacts": [
                    {
                        "at": "2026-01-05T09:30:00",
                        "channel": "Phone",
                        "outcome": "Initial survey slot pencilled prior to completion",
                    }
                ],
                "appointments": [],
                "hazards": [
                    {
                        "category": "Damp and mould",
                        "priority": "P1",
                        "noticed": "2026-01-03",
                        "referred": "2026-01-04",
                        "repaired": None,
                        "released": False,
                        "job": "SYN-HAZ-223A",
                        "owner": "Bea Safe",
                    }
                ],
                "documents": [
                    {
                        "id": "SYN-DOC-SURVEY-223A",
                        "name": "SYN-survey-2026-01-12.pdf",
                        "kind": "Survey",
                        "at": "2026-01-12",
                        "by": "Synthetic surveyor",
                        "scan": {"status": "clean", "scanner": "Synthetic fixture"},
                    }
                ],
                "history": [{"at": "2026-01-05T09:30:00", "event": "Initial survey pencilled"}],
            },
            {
                "id": "ZF-223-B",
                "wave": "Wave 1",
                "closed": False,
                "stage": "Contacting resident",
                "stage_since": "2026-01-14",
                "days_in_stage": 6,
                "waiting_on": "Amina Patel",
                "reason": "to send accessible written introduction",
                "owner_code": "RLO-223",
                "owner": "Amina Patel",
                "owner_role": "Resident Liaison Officer",
                "resident": {
                    "title": "Mr",
                    "name": "Owen Synthetic",
                    "formal": "Mr Synthetic",
                    "phone": "01000 000224",
                    "email": "",
                    "preferred": "Letter",
                    "adjustment": "BSL interpreter and written confirmation",
                    "priority_support": True,
                    "unavailable": "Tuesdays",
                    "representative": None,
                },
                "home": {
                    "address": "224 Synthetic Crescent",
                    "town": "Testville",
                    "postcode": "TE2 4ST",
                    "area": "North",
                    "type": "Semi-detached",
                    "built": 1962,
                    "epc": "D",
                    "tenure": "Social rent",
                    "lat": 0,
                    "lon": 0,
                },
                "measures": ["Cavity wall insulation"],
                "contractor": {
                    "name": "Test Works Ltd",
                    "phone": "0",
                    "scope": "SYN-223-B",
                    "contact": "Kim Builder",
                },
                "decision": {"status": "Not yet asked", "by": None, "at": None},
                "funding_ok": False,
                "funding": {
                    "route": "SHDF Wave 3",
                    "status": "Not started",
                    "reference": "",
                    "draft": "",
                    "approved_by": None,
                },
                "contacts": [
                    {
                        "at": "2026-01-09T11:00:00",
                        "channel": "Letter",
                        "outcome": "Introductory letter posted",
                    }
                ],
                "appointments": [],
                "hazards": [
                    {
                        "category": "Electrical",
                        "priority": "P1",
                        "noticed": "2026-01-08",
                        "referred": None,
                        "repaired": None,
                        "released": False,
                        "job": "SYN-HAZ-223B",
                        "owner": "Bea Safe",
                    }
                ],
                "documents": [],
                "history": [{"at": "2026-01-09T11:00:00", "event": "Introductory letter posted"}],
            },
        ],
    }


def inspect_discrepancies(
    text: str,
    *,
    case: Mapping[str, Any],
    task: str,
    staff_member: Mapping[str, Any] | None = None,
    scenario: ReviewScenario | None = None,
    require_citations: bool = True,
) -> list[dict[str, str]]:
    """Compare proposal or edited text against live case invariants and optional scenario rules."""
    issues: list[dict[str, str]] = []
    lowered = _norm(text)
    if not lowered:
        return [{"defect_class": "incomplete", "detail": "empty_proposal_text"}]

    if require_citations:
        clean, good, bad, dropped = _analyse_citations(text, case, task, staff_member)
        if bad or dropped or not good or not clean.strip():
            issues.append(
                {
                    "defect_class": "unsupported",
                    "detail": "unresolved_or_missing_case_citations",
                }
            )

    open_hazards = [h for h in case.get("hazards", []) if not h.get("released")]
    if open_hazards:
        if _HAZARD_CLEAR_RE.search(text):
            issues.append(
                {
                    "defect_class": "wrong",
                    "detail": "claims_open_safety_hazard_resolved_or_clear",
                }
            )
        hazard_terms = ["open safety", "safety issue", "safety hold"] + [
            str(h.get("category", "")).casefold() for h in open_hazards if h.get("category")
        ]
        if not any(term in lowered for term in hazard_terms):
            issues.append(
                {
                    "defect_class": "incomplete",
                    "detail": "omits_open_safety_hazard",
                }
            )

    resident = case.get("resident", {})
    needs_support = bool(resident.get("priority_support")) or str(
        resident.get("adjustment", "None")
    ) not in ("", "None", "Unknown")
    if needs_support:
        if _NO_SUPPORT_RE.search(text):
            issues.append(
                {
                    "defect_class": "wrong",
                    "detail": "contradicts_recorded_resident_support_adjustment",
                }
            )
        support_terms = (
            "extra support",
            "adjustment",
            "interpreter",
            "large print",
            "written confirmation",
        )
        if not any(term in lowered for term in support_terms):
            issues.append(
                {
                    "defect_class": "incomplete",
                    "detail": "omits_resident_support_adjustment",
                }
            )

    if task == "message":
        preferred = str(resident.get("preferred", "")).strip()
        if preferred == "Letter" and "telephone our office" in lowered:
            issues.append(
                {
                    "defect_class": "incomplete",
                    "detail": "ignores_preferred_letter_contact_channel",
                }
            )

    decision_state = str(_resident_decisions.resident_status(dict(case)))
    if decision_state in ("Waiting", "Not yet asked") and _CONSENT_CONFIRMED_RE.search(text):
        issues.append(
            {
                "defect_class": "wrong",
                "detail": "claims_unrecorded_resident_consent",
            }
        )

    funding_status = str((case.get("funding") or {}).get("status") or "")
    if funding_status in ("", "Draft", "Not started") and _UNSUPPORTED_FUNDING_RE.search(text):
        issues.append(
            {
                "defect_class": "unsupported",
                "detail": "claims_unapproved_funding_or_guaranteed_savings",
            }
        )

    stage = str(case.get("stage", ""))
    if stage != "Contacting resident" and _STALE_STAGE_RE.search(text):
        issues.append(
            {
                "defect_class": "stale",
                "detail": "repeats_superseded_stage_or_survey_booking",
            }
        )

    if scenario is not None:
        for phrase in scenario.forbidden_claims:
            if _norm(phrase) in lowered:
                issues.append(
                    {
                        "defect_class": (
                            scenario.defect_class
                            if scenario.defect_class in DEFECT_CLASSES
                            else "wrong"
                        ),
                        "detail": f"retains_forbidden_claim:{phrase}",
                    }
                )
        for fact in scenario.required_facts:
            if _norm(fact) not in lowered:
                issues.append(
                    {
                        "defect_class": "incomplete",
                        "detail": f"missing_required_fact:{fact}",
                    }
                )

    deduped: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for item in issues:
        key = (item["defect_class"], item["detail"])
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    return deduped


def _matched_sources_in_reason(reason: str, candidate_labels: Sequence[str]) -> list[str]:
    norm_reason = _norm(reason)
    return [label for label in candidate_labels if _norm(label) in norm_reason]


def human_review_gate(
    rec: Mapping[str, Any],
    *,
    case: Mapping[str, Any] | None = None,
    store: Any | None = None,
    staff_member: Mapping[str, Any] | None = None,
    scenario: ReviewScenario | None = None,
    authority: AuthorityPolicy | None = PROVISIONAL_AUTHORITY,
    live: bool = False,
    on: str | None = None,
) -> GateResult:
    """Deterministic GateResult for human review of AI proposals (AC-070, FR-026, OQ-017)."""
    if authority is None:
        return GateResult(
            gate=GATE_ID,
            outcome=UNKNOWN,
            reason="missing_authority_policy: No competent-review AuthorityPolicy supplied.",
            owner="OQ-017 Assurance Lead",
            correction="Supply an AuthorityPolicy defining permitted roles and thresholds.",
            rule=None,
        )

    reviewer_attr = (
        authority.approved_by
        if authority.approved_by and is_valid_human_identity(authority.approved_by)
        else "Provisional engineering harness (OQ-017 unapproved)"
    )
    rule = GateRule(
        gate=GATE_ID,
        source=GATE_SOURCE,
        effective_date=authority.effective_date,
        version=authority.version,
        reviewer=reviewer_attr,
    )
    active_date = on or date.today().isoformat()
    if rule.effective_date > active_date:
        return GateResult(
            gate=GATE_ID,
            outcome=UNKNOWN,
            reason=f"rule_not_yet_effective: Gate rule takes effect on {rule.effective_date}.",
            owner="OQ-017 Assurance Lead",
            correction="Evaluate on or after the rule effective date or use manual case controls.",
            rule=rule,
        )

    if live:
        approved_date_ok = False
        if isinstance(authority.approved_on, str) and authority.approved_on.strip():
            try:
                approved_date_ok = (
                    date.fromisoformat(authority.approved_on).isoformat() == authority.approved_on
                )
            except ValueError:
                approved_date_ok = False
        if (
            authority.provisional
            or not is_valid_human_identity(authority.approved_by)
            or not approved_date_ok
        ):
            return GateResult(
                gate=GATE_ID,
                outcome=FAIL,
                reason=(
                    "provisional_authority_unapproved_for_live_gate: "
                    f"{authority.authority_gap} Live gate requires named human sign-off."
                ),
                owner="OQ-017 Sponsor, Safety, DPO/Legal, and Assurance Leads",
                correction=(
                    "Complete OQ-017 competent-review authority sign-off and blind human trials "
                    "before enabling live=True."
                ),
                rule=rule,
            )

    status = str(rec.get("status") or "")
    if status in ("Hold", "Quarantined"):
        return GateResult(
            gate=GATE_ID,
            outcome=FAIL,
            reason=(
                f"stale_or_quarantined_proposal: Proposal status is {status} and cannot satisfy "
                "a controlled gate."
            ),
            owner=str(rec.get("user") or "Case owner"),
            correction="Request a fresh proposal from current case sources or use manual controls.",
            rule=rule,
        )

    evidence = rec.get("review_evidence")
    if status in ("", "Not reviewed", "Proposed") or not isinstance(evidence, Mapping):
        return GateResult(
            gate=GATE_ID,
            outcome=UNKNOWN,
            reason="proposal_unreviewed: Proposal has no recorded human review evidence.",
            owner=str(rec.get("user") or "Competent human reviewer"),
            correction="Complete named human review against authoritative case sources.",
            rule=rule,
        )

    resolved_by = rec.get("resolved_by")
    evidence_reviewer = evidence.get("reviewer")
    if (
        not isinstance(resolved_by, str)
        or not resolved_by.strip()
        or resolved_by != evidence_reviewer
        or not is_valid_human_identity(resolved_by)
    ):
        return GateResult(
            gate=GATE_ID,
            outcome=FAIL,
            reason=(
                "unnamed_or_non_human_reviewer: Reviewer identity is missing, mismatched, "
                "placeholder, or non-human."
            ),
            owner="Case owner",
            correction="Have a named, registered human staff reviewer inspect the case sources.",
            rule=rule,
        )

    resolved_staff = staff_member
    if resolved_staff is None and store is not None and hasattr(store, "staff"):
        staff_lookup = store.staff.get(resolved_by.lower())
        if isinstance(staff_lookup, Mapping):
            resolved_staff = staff_lookup

    if (
        resolved_staff is None
        or str(resolved_staff.get("email", "")).lower() != resolved_by.lower()
        or not is_valid_human_identity(resolved_staff.get("name"))
    ):
        return GateResult(
            gate=GATE_ID,
            outcome=FAIL,
            reason="unregistered_or_placeholder_staff: Reviewer does not match registered staff.",
            owner="Programme Support Officer",
            correction="Review under a registered named human staff account.",
            rule=rule,
        )

    role = str(resolved_staff.get("role") or "")
    if role not in authority.allowed_roles:
        return GateResult(
            gate=GATE_ID,
            outcome=FAIL,
            reason=(
                f"reviewer_role_not_authorised: Role '{role}' is not authorised for "
                "competent AI proposal sign-off."
            ),
            owner=resolved_by,
            correction="Route review to an authorised competent reviewer role.",
            rule=rule,
        )

    task = str(rec.get("task") or "")
    if task not in authority.allowed_roles[role]:
        return GateResult(
            gate=GATE_ID,
            outcome=FAIL,
            reason=(
                f"reviewer_not_authorised_for_task: Role '{role}' is not authorised for "
                f"task '{task}'."
            ),
            owner=resolved_by,
            correction="Route review to a staff member authorised for this AI task.",
            rule=rule,
        )

    case_ids_raw = rec.get("case_ids")
    case_ids = [str(cid) for cid in case_ids_raw] if isinstance(case_ids_raw, list) else []
    resolved_case = case
    if resolved_case is None and store is not None and len(case_ids) == 1:
        try:
            candidate = store._case(case_ids[0])
            if isinstance(candidate, Mapping):
                resolved_case = candidate
        except KeyError:
            resolved_case = None

    if resolved_case is None or not case_ids:
        return GateResult(
            gate=GATE_ID,
            outcome=UNKNOWN,
            reason="missing_case_source_context: Authoritative case record is unavailable.",
            owner=resolved_by,
            correction="Supply the authoritative case record before evaluating the gate.",
            rule=rule,
        )

    compared = evidence.get("compared")
    stored_hashes = evidence.get("source_hashes")
    if (
        not isinstance(compared, Mapping)
        or not isinstance(compared.get("ai"), str)
        or not compared.get("ai", "").strip()
        or not isinstance(compared.get("workflow"), str)
        or not compared.get("workflow", "").strip()
        or not isinstance(stored_hashes, Mapping)
        or not stored_hashes
    ):
        return GateResult(
            gate=GATE_ID,
            outcome=FAIL,
            reason=(
                "incomplete_retained_review_evidence: Review record lacks AI/workflow comparison "
                "or source hashes."
            ),
            owner=resolved_by,
            correction="Re-run the proposal and record a complete comparison and hash snapshot.",
            rule=rule,
        )

    current_hashes = (
        _store_source_hashes(store, resolved_staff, case_ids)
        if store is not None
        else _case_snapshot_hashes(resolved_case, resolved_staff)
    )
    if current_hashes != {str(k): str(v) for k, v in stored_hashes.items()}:
        return GateResult(
            gate=GATE_ID,
            outcome=FAIL,
            reason=(
                "stale_case_sources: Underlying case sources changed after review snapshot; "
                "previous review cannot satisfy gate."
            ),
            owner=resolved_by,
            correction="Re-run against current case facts and complete a fresh human review.",
            rule=rule,
        )

    action = str(evidence.get("disposition") or rec.get("reviewer_action") or "")
    if action not in ("accept", "edit", "reject"):
        return GateResult(
            gate=GATE_ID,
            outcome=FAIL,
            reason=f"invalid_review_disposition: Unsupported disposition '{action}'.",
            owner=resolved_by,
            correction="Record accept, edit, or reject with a case-source-cited reason.",
            rule=rule,
        )

    reason = str(rec.get("reviewer_reason") or evidence.get("reason") or "").strip()
    if cites_memory(reason):
        return GateResult(
            gate=GATE_ID,
            outcome=FAIL,
            reason=(
                "memory_reference_not_authoritative_source: Reviewer reason cites chat or "
                "assistant memory instead of case records."
            ),
            owner=resolved_by,
            correction="Verify directly against case source fields and cite the case label.",
            rule=rule,
        )

    proposal_text = str(rec.get("ai_output") or rec.get("shown_output") or "")
    proposal_issues = inspect_discrepancies(
        proposal_text,
        case=resolved_case,
        task=task,
        staff_member=resolved_staff,
        scenario=scenario,
    )
    citation_badge = "citation_validity_alone_insufficient; " if rec.get("verified") is True else ""

    if action == "accept" and proposal_issues:
        classes = ", ".join(dict.fromkeys(item["defect_class"] for item in proposal_issues))
        return GateResult(
            gate=GATE_ID,
            outcome=FAIL,
            reason=(
                f"default_accept_missed_critical_defect: {citation_badge}"
                f"Accepted proposal with unresolved critical defect(s): {classes}."
            ),
            owner=resolved_by,
            correction="Edit or reject the defective proposal and cite the resolving case source.",
            rule=rule,
        )

    if len(reason) < authority.min_reason_chars or len(reason) > 300:
        return GateResult(
            gate=GATE_ID,
            outcome=FAIL,
            reason=(
                f"insufficient_reviewer_reason: {citation_badge}"
                f"Reason must be {authority.min_reason_chars}..300 characters naming checked "
                "case sources."
            ),
            owner=resolved_by,
            correction="Record a substantive reason citing the checked case source label.",
            rule=rule,
        )

    case_labels = _source_labels(resolved_case, resolved_staff)
    cited_in_reason = _matched_sources_in_reason(reason, case_labels)
    expected_sources = (
        [label for label in scenario.resolving_sources if label in case_labels]
        if scenario is not None and scenario.resolving_sources
        else case_labels
    )
    matched_resolving = _matched_sources_in_reason(reason, expected_sources)
    if not cited_in_reason or not matched_resolving:
        return GateResult(
            gate=GATE_ID,
            outcome=FAIL,
            reason=(
                f"missing_resolving_case_source_in_reason: {citation_badge}"
                "Reason does not cite a resolving authoritative case source label."
            ),
            owner=resolved_by,
            correction="Cite the exact case source label checked to verify or correct the draft.",
            rule=rule,
        )

    if action == "edit":
        edited_text = str(rec.get("override_text") or "").strip()
        if not edited_text:
            return GateResult(
                gate=GATE_ID,
                outcome=FAIL,
                reason="missing_override_text: Edit disposition recorded no replacement text.",
                owner=resolved_by,
                correction="Provide corrected replacement text grounded in case sources.",
                rule=rule,
            )
        if proposal_issues and _norm(edited_text) == _norm(proposal_text):
            return GateResult(
                gate=GATE_ID,
                outcome=FAIL,
                reason="ineffective_edit_unchanged_proposal: Edited text leaves defect unchanged.",
                owner=resolved_by,
                correction="Correct every defective or missing fact in the replacement text.",
                rule=rule,
            )
        edit_issues = inspect_discrepancies(
            edited_text,
            case=resolved_case,
            task=task,
            staff_member=resolved_staff,
            scenario=scenario,
            require_citations=True,
        )
        if edit_issues:
            details = ", ".join(item["detail"] for item in edit_issues)
            return GateResult(
                gate=GATE_ID,
                outcome=FAIL,
                reason=(
                    "ineffective_edit_retains_or_introduces_defect: "
                    f"Edited text still has discrepancy ({details})."
                ),
                owner=resolved_by,
                correction="Ensure edited text removes wrong/unsupported claims and cites facts.",
                rule=rule,
            )

    return GateResult(
        gate=GATE_ID,
        outcome=PASS,
        reason=(
            f"human_review_verified: Reviewer '{resolved_by}' recorded '{action}' citing "
            f"{matched_resolving[0]} with clean discrepancy check."
        ),
        owner=resolved_by,
        correction="None required; reviewer, source, and reason retained.",
        rule=rule,
    )


def _open_synthetic_store(root: Path, dataset: Mapping[str, Any] | None = None) -> Any:
    payload = copy.deepcopy(dict(dataset)) if dataset is not None else synthetic_dataset()
    data_path = root / "synthetic_223.json"
    data_path.write_text(json.dumps(payload), encoding="utf-8")
    store = _Store(str(data_path))
    store.ai.fast = "synthetic-eval-223"
    store.ai.strong = "synthetic-eval-223"
    store.release_context = lambda _task, _dep=None: dict(SYNTHETIC_RELEASE)
    return store


def _seed_ai_proposal(
    store: Any, reviewer: Mapping[str, Any], scenario: ReviewScenario
) -> dict[str, Any]:
    """Run Store.ai_run with a deterministic offline responder so citations and hashes are real."""

    def _offline_run(
        _task: str,
        _sysmsg: str,
        _prompt: str,
        template: str,
        _strong: bool = False,
        _check: Callable[..., Any] | None = None,
        *,
        off: bool = False,
    ) -> dict[str, Any]:
        if off:
            return {
                "text": template,
                "source": "template",
                "model": None,
                "reason": "workflow-only mode selected",
                "validated": True,
                "latency_ms": 1.0,
            }
        return {
            "text": scenario.proposal_text,
            "source": "ai",
            "model": "synthetic-eval-223",
            "release": dict(SYNTHETIC_RELEASE),
            "reason": None,
            "validated": True,
            "latency_ms": 12.0,
        }

    store.ai.run = _offline_run
    run_out = store.ai_run(dict(reviewer), scenario.case_id, scenario.task)
    return dict(run_out)


def _profile_decision(
    profile: str, scenario: ReviewScenario, verified: bool
) -> tuple[str, str, str | None, int]:
    """Return (action, reason, edited_text, review_seconds) for a scripted reviewer profile."""
    if profile in ("competent", "unauthorised_competent"):
        return (
            scenario.competent_action,
            scenario.competent_reason,
            scenario.competent_text,
            scenario.competent_review_seconds,
        )
    if profile == "default_accept":
        return ("accept", "", None, 8)
    if profile == "citation_only":
        reason = (
            "Accepted because all inline citation badges resolved automatically."
            if verified
            else "Rejected because inline citation badge failed automatic resolution."
        )
        return ("accept" if verified else "reject", reason, None, 12)
    if profile == "automation_bias":
        if scenario.confidence == "confident" and verified:
            return (
                "accept",
                "Confident draft with verified citation badges accepted on quick scan.",
                None,
                scenario.biased_review_seconds,
            )
        return (
            scenario.competent_action,
            scenario.competent_reason,
            scenario.competent_text,
            scenario.biased_review_seconds,
        )
    raise ValueError(f"Unknown reviewer profile: {profile}")


def _retained_evidence_ok(
    rec: Mapping[str, Any], reviewer: Mapping[str, Any], case: Mapping[str, Any]
) -> bool:
    evidence = rec.get("review_evidence")
    if not isinstance(evidence, Mapping):
        return False
    compared = evidence.get("compared")
    hashes = evidence.get("source_hashes")
    reason = str(rec.get("reviewer_reason") or "").strip()
    if (
        rec.get("resolved_by") != reviewer["email"]
        or evidence.get("reviewer") != reviewer["email"]
        or not reason
        or not isinstance(compared, Mapping)
        or not compared.get("ai")
        or not compared.get("workflow")
        or not isinstance(hashes, Mapping)
        or not hashes
    ):
        return False
    labels = _source_labels(case, reviewer)
    return bool(_matched_sources_in_reason(reason, labels))


def evaluate_panel(
    profile: str,
    *,
    scenarios: Sequence[ReviewScenario] = DEFAULT_SCENARIOS,
    authority: AuthorityPolicy = PROVISIONAL_AUTHORITY,
    live: bool = False,
) -> dict[str, Any]:
    """Run one reviewer profile across all scenarios paired with workflow-only baselines."""
    if profile not in REVIEW_PROFILES:
        raise ValueError(f"Unsupported profile '{profile}'; choose from {REVIEW_PROFILES}.")

    with tempfile.TemporaryDirectory() as tmp:
        store = _open_synthetic_store(Path(tmp))
        reviewer_email = (
            "morgan.grant@example.test"
            if profile == "unauthorised_competent"
            else "amina.patel@example.test"
        )
        reviewer = dict(store.staff[reviewer_email])

        rows: list[dict[str, Any]] = []
        by_class_totals = {cls: 0 for cls in DEFECT_CLASSES}
        by_class_detected = {cls: 0 for cls in DEFECT_CLASSES}
        seeded_defects = 0
        detected_defects = 0
        corrections = 0
        rejections = 0
        false_rejects = 0
        gate_passed_count = 0
        gate_leakage = 0
        total_ai_seconds = 0
        total_workflow_seconds = 0
        all_retained = True

        for scenario in scenarios:
            wf_out = store.ai_run(reviewer, scenario.case_id, scenario.task, mode="workflow")
            ai_out = _seed_ai_proposal(store, reviewer, scenario)
            rec_id = str(ai_out["record_id"])
            action, reason, edited_text, review_seconds = _profile_decision(
                profile, scenario, bool(ai_out["verified"])
            )
            reviewed = store.review_ai(reviewer, rec_id, action, reason, edited_text)
            case = dict(store._case(scenario.case_id))
            gate = human_review_gate(
                reviewed,
                case=case,
                store=store,
                staff_member=reviewer,
                scenario=scenario,
                authority=authority,
                live=live,
            )
            allowed = transition_allowed([gate])
            has_defect = scenario.defect_class in DEFECT_CLASSES
            remaining_edit_issues = (
                inspect_discrepancies(
                    str(reviewed.get("override_text") or ""),
                    case=case,
                    task=scenario.task,
                    staff_member=reviewer,
                    scenario=scenario,
                )
                if action == "edit"
                else []
            )
            detected = has_defect and (
                action == "reject" or (action == "edit" and not remaining_edit_issues)
            )
            if has_defect:
                seeded_defects += 1
                by_class_totals[scenario.defect_class] += 1
                if detected:
                    detected_defects += 1
                    by_class_detected[scenario.defect_class] += 1
                if action == "edit" and not remaining_edit_issues:
                    corrections += 1
                elif action == "reject":
                    rejections += 1
                if allowed and not detected:
                    gate_leakage += 1
            elif action == "reject":
                false_rejects += 1

            if allowed:
                gate_passed_count += 1

            retained = _retained_evidence_ok(reviewed, reviewer, case)
            all_retained = all_retained and retained
            total_ai_seconds += review_seconds
            total_workflow_seconds += scenario.workflow_seconds

            rows.append(
                {
                    "scenario_id": scenario.scenario_id,
                    "case_id": scenario.case_id,
                    "task": scenario.task,
                    "defect_class": scenario.defect_class,
                    "confidence": scenario.confidence,
                    "citation_verified": bool(ai_out["verified"]),
                    "workflow_record_id": str(wf_out["record_id"]),
                    "workflow_text": str(wf_out["text"]),
                    "workflow_seconds": scenario.workflow_seconds,
                    "ai_record_id": rec_id,
                    "disposition": action,
                    "reviewer": str(reviewed.get("resolved_by") or ""),
                    "reviewer_role": str(reviewer["role"]),
                    "reviewer_reason": str(reviewed.get("reviewer_reason") or ""),
                    "source_hashes": dict(reviewed["review_evidence"]["source_hashes"]),
                    "retained_evidence": retained,
                    "detected": detected,
                    "review_seconds": review_seconds,
                    "effort_delta_seconds": review_seconds - scenario.workflow_seconds,
                    "gate": gate.as_record(),
                    "transition_allowed": allowed,
                }
            )

        audit_verified = bool(store.verify_audit())

    by_defect_class = {
        cls: {
            "seeded": by_class_totals[cls],
            "detected": by_class_detected[cls],
            "detection_rate": (
                round(by_class_detected[cls] / by_class_totals[cls], 4)
                if by_class_totals[cls]
                else None
            ),
        }
        for cls in DEFECT_CLASSES
    }
    return {
        "record_version": RECORD_VERSION,
        "profile": profile,
        "evidence_class": SYNTHETIC_EVIDENCE_CLASS,
        "human_trial_complete": False,
        "oq017_authority_gap": authority.authority_gap,
        "live_mode": live,
        "scenario_count": len(scenarios),
        "seeded_defect_count": seeded_defects,
        "detected_count": detected_defects,
        "detection_rate": round(detected_defects / seeded_defects, 4) if seeded_defects else 0.0,
        "by_defect_class": by_defect_class,
        "corrections": corrections,
        "rejections": rejections,
        "false_rejects": false_rejects,
        "gate_passed_count": gate_passed_count,
        "gate_leakage": gate_leakage,
        "retained_evidence_complete": all_retained and audit_verified,
        "audit_verified": audit_verified,
        "total_ai_review_seconds": total_ai_seconds,
        "total_workflow_seconds": total_workflow_seconds,
        "net_effort_delta_seconds": total_ai_seconds - total_workflow_seconds,
        "scenarios": rows,
    }


def run_automation_bias_harness(
    *,
    scenarios: Sequence[ReviewScenario] = DEFAULT_SCENARIOS,
    authority: AuthorityPolicy = PROVISIONAL_AUTHORITY,
) -> dict[str, Any]:
    """Compare competent, default-accept, automation-bias, citation, and unauthorised panels."""
    panels = {
        profile: evaluate_panel(profile, scenarios=scenarios, authority=authority, live=False)
        for profile in REVIEW_PROFILES
    }
    competent = panels["competent"]
    biased = panels["automation_bias"]
    default_acc = panels["default_accept"]
    cite_only = panels["citation_only"]
    unauthorised = panels["unauthorised_competent"]
    automation_bias_exposed = (
        competent["detection_rate"] == 1.0
        and 0.0 < biased["detection_rate"] < competent["detection_rate"]
        and default_acc["detection_rate"] == 0.0
        and cite_only["detection_rate"] == 0.0
        and all(panels[p]["gate_leakage"] == 0 for p in REVIEW_PROFILES)
        and default_acc["gate_passed_count"] == 0
        and cite_only["gate_passed_count"] == 0
        and unauthorised["gate_passed_count"] == 0
    )
    return {
        "record_version": RECORD_VERSION,
        "evidence_class": SYNTHETIC_EVIDENCE_CLASS,
        "human_trial_complete": False,
        "authority_policy": authority.as_record(),
        "automation_bias_exposed": automation_bias_exposed,
        "panels": panels,
    }


def blank_worksheet(*, scenarios: Sequence[ReviewScenario] = DEFAULT_SCENARIOS) -> dict[str, Any]:
    """Export a blind human-reviewer worksheet with zero defect_class or confidence spoilers."""
    with tempfile.TemporaryDirectory() as tmp:
        store = _open_synthetic_store(Path(tmp))
        reviewer = dict(store.staff["amina.patel@example.test"])
        items: list[dict[str, Any]] = []
        for scenario in scenarios:
            wf_out = store.ai_run(reviewer, scenario.case_id, scenario.task, mode="workflow")
            ai_out = _seed_ai_proposal(store, reviewer, scenario)
            case = dict(store._case(scenario.case_id))
            items.append(
                {
                    "scenario_id": scenario.scenario_id,
                    "case_id": scenario.case_id,
                    "task": scenario.task,
                    "citable_source_labels": _source_labels(case, reviewer),
                    "workflow_comparator_text": str(wf_out["text"]),
                    "ai_proposal_text": str(ai_out["text"]),
                    "citation_badge_verified": bool(ai_out["verified"]),
                    "response": {
                        "disposition": None,
                        "edited_text": None,
                        "reason": "",
                        "review_seconds": None,
                    },
                }
            )
    return {
        "record_version": RECORD_VERSION,
        "worksheet_version": "blind-human-review-worksheet-v1",
        "instructions": (
            "Inspect citable_source_labels and workflow_comparator_text before recording "
            "accept, edit, or reject. Cite at least one exact case source label in reason "
            "(30..300 characters) and record measured review_seconds."
        ),
        "oq017_notice": OQ_017_GAP,
        "reviewer": {"name": "", "email": "", "role": ""},
        "items": items,
    }


def score_human_session(
    submission: Mapping[str, Any],
    *,
    scenarios: Sequence[ReviewScenario] = DEFAULT_SCENARIOS,
    authority: AuthorityPolicy = PROVISIONAL_AUTHORITY,
    live: bool = False,
) -> dict[str, Any]:
    """Score one completed blind human reviewer worksheet against Store and human_review_gate."""
    reviewer_meta = submission.get("reviewer")
    if not isinstance(reviewer_meta, Mapping):
        raise ValueError("Submission requires a reviewer mapping with name, email, and role.")
    name = str(reviewer_meta.get("name") or "").strip()
    email = str(reviewer_meta.get("email") or "").strip().lower()
    role = str(reviewer_meta.get("role") or "").strip()
    if not is_valid_human_identity(name) or not is_valid_human_identity(email) or "@" not in email:
        raise ValueError("Reviewer name and email must identify a named human participant.")
    if not role:
        raise ValueError("Reviewer role is required.")

    raw_items = submission.get("items")
    if not isinstance(raw_items, Sequence) or isinstance(raw_items, str | bytes):
        raise ValueError("Submission items must be a sequence of scenario responses.")

    expected_ids = [s.scenario_id for s in scenarios]
    submitted_by_id: dict[str, Mapping[str, Any]] = {}
    for entry in raw_items:
        if not isinstance(entry, Mapping) or not isinstance(entry.get("scenario_id"), str):
            raise ValueError("Each item requires a string scenario_id.")
        sid = entry["scenario_id"]
        if sid in submitted_by_id:
            raise ValueError(f"Duplicate response for scenario_id '{sid}'.")
        submitted_by_id[sid] = entry

    if set(submitted_by_id) != set(expected_ids):
        raise ValueError("Submission must answer the exact scenario set without omissions.")

    dataset = synthetic_dataset()
    dataset["staff"].append({"code": "HUM-223", "name": name, "email": email, "role": role})

    with tempfile.TemporaryDirectory() as tmp:
        store = _open_synthetic_store(Path(tmp), dataset=dataset)
        reviewer = dict(store.staff[email])
        by_class_totals = {cls: 0 for cls in DEFECT_CLASSES}
        by_class_detected = {cls: 0 for cls in DEFECT_CLASSES}
        seeded_defects = 0
        detected_defects = 0
        corrections = 0
        rejections = 0
        false_rejects = 0
        gate_passed = 0
        gate_leakage = 0
        total_ai_seconds = 0.0
        total_workflow_seconds = 0
        all_retained = True
        scored_rows: list[dict[str, Any]] = []

        for scenario in scenarios:
            entry = submitted_by_id[scenario.scenario_id]
            resp = entry.get("response", entry)
            if not isinstance(resp, Mapping):
                raise ValueError(f"Invalid response object on '{scenario.scenario_id}'.")
            action = str(resp.get("disposition") or "").strip()
            if action not in ("accept", "edit", "reject"):
                raise ValueError(
                    f"Scenario '{scenario.scenario_id}' needs accept, edit, or reject."
                )
            reason = str(resp.get("reason") or "").strip()
            edited_raw = resp.get("edited_text")
            edited_text = str(edited_raw) if edited_raw is not None else None
            seconds_raw = resp.get("review_seconds")
            if (
                not isinstance(seconds_raw, int | float)
                or isinstance(seconds_raw, bool)
                or seconds_raw <= 0
            ):
                raise ValueError(
                    f"Scenario '{scenario.scenario_id}' requires positive numeric review_seconds."
                )
            review_seconds = float(seconds_raw)

            store.ai_run(reviewer, scenario.case_id, scenario.task, mode="workflow")
            ai_out = _seed_ai_proposal(store, reviewer, scenario)
            rec_id = str(ai_out["record_id"])
            if action in ("edit", "reject") and not reason:
                reason = (
                    "u"  # preserve Store.review_ai recording while letting gate fail short reason
                )
            reviewed = store.review_ai(reviewer, rec_id, action, reason, edited_text)
            case = dict(store._case(scenario.case_id))
            gate = human_review_gate(
                reviewed,
                case=case,
                store=store,
                staff_member=reviewer,
                scenario=scenario,
                authority=authority,
                live=live,
            )
            allowed = transition_allowed([gate])
            has_defect = scenario.defect_class in DEFECT_CLASSES
            remaining_issues = (
                inspect_discrepancies(
                    str(reviewed.get("override_text") or ""),
                    case=case,
                    task=scenario.task,
                    staff_member=reviewer,
                    scenario=scenario,
                )
                if action == "edit"
                else []
            )
            detected = has_defect and (
                action == "reject" or (action == "edit" and not remaining_issues)
            )
            if has_defect:
                seeded_defects += 1
                by_class_totals[scenario.defect_class] += 1
                if detected:
                    detected_defects += 1
                    by_class_detected[scenario.defect_class] += 1
                if action == "edit" and not remaining_issues:
                    corrections += 1
                elif action == "reject":
                    rejections += 1
                if allowed and not detected:
                    gate_leakage += 1
            elif action == "reject":
                false_rejects += 1

            if allowed:
                gate_passed += 1

            retained = _retained_evidence_ok(reviewed, reviewer, case)
            all_retained = all_retained and retained
            total_ai_seconds += review_seconds
            total_workflow_seconds += scenario.workflow_seconds
            scored_rows.append(
                {
                    "scenario_id": scenario.scenario_id,
                    "defect_class": scenario.defect_class,
                    "disposition": action,
                    "detected": detected,
                    "review_seconds": round(review_seconds, 2),
                    "workflow_seconds": scenario.workflow_seconds,
                    "gate": gate.as_record(),
                    "transition_allowed": allowed,
                }
            )

        audit_verified = bool(store.verify_audit())

    oq017_approved = bool(
        not authority.provisional
        and is_valid_human_identity(authority.approved_by)
        and authority.approved_on
    )
    return {
        "record_version": RECORD_VERSION,
        "evidence_class": "single_human_session",
        "oq017_live_approved": oq017_approved,
        "reviewer": {"name": name, "email": email, "role": role},
        "scenario_count": len(scenarios),
        "seeded_defect_count": seeded_defects,
        "detected_count": detected_defects,
        "detection_rate": round(detected_defects / seeded_defects, 4) if seeded_defects else 0.0,
        "by_defect_class": {
            cls: {
                "seeded": by_class_totals[cls],
                "detected": by_class_detected[cls],
                "detection_rate": (
                    round(by_class_detected[cls] / by_class_totals[cls], 4)
                    if by_class_totals[cls]
                    else None
                ),
            }
            for cls in DEFECT_CLASSES
        },
        "corrections": corrections,
        "rejections": rejections,
        "false_rejects": false_rejects,
        "gate_passed_count": gate_passed,
        "gate_leakage": gate_leakage,
        "retained_evidence_complete": all_retained and audit_verified,
        "audit_verified": audit_verified,
        "total_ai_review_seconds": round(total_ai_seconds, 2),
        "total_workflow_seconds": total_workflow_seconds,
        "net_effort_delta_seconds": round(total_ai_seconds - total_workflow_seconds, 2),
        "scenarios": scored_rows,
    }


def pool_human_sessions(
    submissions: Sequence[Mapping[str, Any]],
    *,
    scenarios: Sequence[ReviewScenario] = DEFAULT_SCENARIOS,
    authority: AuthorityPolicy = PROVISIONAL_AUTHORITY,
    live: bool = False,
) -> dict[str, Any]:
    """Pool distinct human reviewer worksheet sessions without double-counting participants."""
    if not submissions:
        raise ValueError("At least one human reviewer submission is required to pool results.")

    scored_sessions: list[dict[str, Any]] = []
    seen_emails: set[str] = set()
    seen_names: set[str] = set()
    for sub in submissions:
        scored = score_human_session(sub, scenarios=scenarios, authority=authority, live=live)
        email = str(scored["reviewer"]["email"]).lower()
        norm_name = _norm(str(scored["reviewer"]["name"]))
        if email in seen_emails or norm_name in seen_names:
            raise ValueError(f"Duplicate reviewer '{email}' cannot be pooled twice.")
        seen_emails.add(email)
        seen_names.add(norm_name)
        scored_sessions.append(scored)

    by_class_seeded = {cls: 0 for cls in DEFECT_CLASSES}
    by_class_detected = {cls: 0 for cls in DEFECT_CLASSES}
    for session in scored_sessions:
        for cls in DEFECT_CLASSES:
            by_class_seeded[cls] += int(session["by_defect_class"][cls]["seeded"])
            by_class_detected[cls] += int(session["by_defect_class"][cls]["detected"])

    total_seeded = sum(int(s["seeded_defect_count"]) for s in scored_sessions)
    total_detected = sum(int(s["detected_count"]) for s in scored_sessions)
    total_ai_sec = round(sum(float(s["total_ai_review_seconds"]) for s in scored_sessions), 2)
    total_wf_sec = sum(int(s["total_workflow_seconds"]) for s in scored_sessions)
    oq017_approved = bool(
        not authority.provisional
        and is_valid_human_identity(authority.approved_by)
        and authority.approved_on
    )
    return {
        "record_version": RECORD_VERSION,
        "evidence_class": (
            "pooled_human_sessions_oq017_approved"
            if oq017_approved
            else "pooled_human_sessions_provisional_oq017"
        ),
        "oq017_live_approved": oq017_approved,
        "participant_count": len(scored_sessions),
        "total_seeded_defects": total_seeded,
        "total_detected_defects": total_detected,
        "pooled_detection_rate": round(total_detected / total_seeded, 4) if total_seeded else 0.0,
        "by_defect_class": {
            cls: {
                "seeded": by_class_seeded[cls],
                "detected": by_class_detected[cls],
                "detection_rate": (
                    round(by_class_detected[cls] / by_class_seeded[cls], 4)
                    if by_class_seeded[cls]
                    else None
                ),
            }
            for cls in DEFECT_CLASSES
        },
        "total_corrections": sum(int(s["corrections"]) for s in scored_sessions),
        "total_rejections": sum(int(s["rejections"]) for s in scored_sessions),
        "total_false_rejects": sum(int(s["false_rejects"]) for s in scored_sessions),
        "total_gate_leakage": sum(int(s["gate_leakage"]) for s in scored_sessions),
        "all_retained_evidence_complete": all(
            bool(s["retained_evidence_complete"]) for s in scored_sessions
        ),
        "total_ai_review_seconds": total_ai_sec,
        "total_workflow_seconds": total_wf_sec,
        "net_effort_delta_seconds": round(total_ai_sec - total_wf_sec, 2),
        "sessions": scored_sessions,
    }
