"""Acceptance-criteria status for the optional discovery assistant (issue 125).

Pure and deterministic: no store, network, model or clock access. It adds the missing no-write
attestation (human-supplied pointers to observed read-only access, never inferred) and combines the
readiness, attestation and comparison reports into one status. Every criterion stays unmet until a
human accountable owner judges the pointed-to evidence; this code never connects company data,
grants access or declares the assistant approved.
"""

from collections.abc import Iterable
from dataclasses import dataclass, field

from zava_forward.core import discovery_assistant_boundary as boundary
from zava_forward.core import discovery_assistant_evaluation as evaluation

ACCEPTANCE_VERSION = "discovery-assistant-acceptance-v1"

NO_WRITE_ITEMS: tuple[tuple[str, str], ...] = (
    ("credential-scope", "Credential or role granted to the assistant is read-only"),
    ("write-attempt-denied", "A write attempt against each connected system was observed denied"),
    ("own-evidence-log-only", "The only writable target is the assistant's own evidence log"),
)
NO_WRITE_KEYS = tuple(key for key, _ in NO_WRITE_ITEMS)


@dataclass(frozen=True)
class NoWriteEvidence:
    """A human-supplied pointer to observed evidence for one no-write item."""

    item: str
    evidence_reference: str
    observed_by_role: str


@dataclass(frozen=True)
class NoWriteReport:
    satisfied: tuple[str, ...]
    missing: tuple[str, ...]
    invalid: tuple[str, ...]
    no_write_access_established: bool = False
    next_step: str = ""


def assess_no_write(evidence: Iterable[NoWriteEvidence]) -> NoWriteReport:
    """List which no-write items have named observed evidence; never establishes the criterion."""
    seen: set[str] = set()
    invalid: list[str] = []
    for entry in evidence:
        if entry.item not in NO_WRITE_KEYS:
            invalid.append(f"unknown-item:{str(entry.item)[:40]}")
        elif entry.item in seen:
            invalid.append(f"duplicate:{entry.item}")
        elif not (
            boundary._valid(entry.evidence_reference) and boundary._valid(entry.observed_by_role)
        ):
            invalid.append(f"unusable-evidence:{entry.item}")
        else:
            seen.add(entry.item)
    missing = tuple(k for k in NO_WRITE_KEYS if k not in seen)
    done = not missing and not invalid
    return NoWriteReport(
        satisfied=tuple(k for k in NO_WRITE_KEYS if k in seen),
        missing=missing,
        invalid=tuple(invalid),
        next_step=(
            "Accountable owner reviews the observed evidence and records a human conclusion."
            if done
            else "Supply observed evidence for each missing item; do not connect company data."
        ),
    )


@dataclass(frozen=True)
class AcceptanceStatus:
    acceptance_version: str
    readiness_ready_for_owner_decision: bool
    no_write_evidence_complete: bool
    comparison_complete: bool
    criteria_met: dict[str, bool]
    blockers: tuple[str, ...]
    connection_to_company_data_permitted: bool = False
    approved_solution: bool = False
    manual_path: str = boundary.MANUAL_PATH
    notes: tuple[str, ...] = field(default_factory=tuple)


def assess_acceptance(
    readiness: boundary.ReadinessReport,
    no_write: NoWriteReport,
    comparison: evaluation.ComparisonReport,
) -> AcceptanceStatus:
    """Summarise the three acceptance criteria; all stay False pending human judgement."""
    ready = readiness.status == boundary.READY_FOR_OWNER_DECISION
    write_done = not no_write.missing and not no_write.invalid
    compared = not comparison.incomplete and not comparison.invalid
    blockers = tuple(
        name
        for name, ok in (
            ("readiness-evidence-incomplete", ready),
            ("no-write-evidence-incomplete", write_done),
            ("comparison-incomplete", compared),
        )
        if not ok
    )
    return AcceptanceStatus(
        acceptance_version=ACCEPTANCE_VERSION,
        readiness_ready_for_owner_decision=ready,
        no_write_evidence_complete=write_done,
        comparison_complete=compared,
        criteria_met={
            "readiness-before-connection": False,
            "no-write-access": False,
            "compared-with-manual-and-conventional": False,
        },
        blockers=blockers,
        notes=(
            "Evidence completeness is not acceptance; named humans judge the pointed-to results.",
        ),
    )
