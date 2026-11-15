"""Public non-retaliation, non-refusal and zero-hazard-delay guard facade (Issue #220).

Re-exports the canonical store-independent challenge register and fail-closed case-safeguard
primitives from ``zava_forward.core.challenges`` under ``zava_forward.core.no_retaliation_guard``.
"""

from __future__ import annotations

from .challenges import (
    ACCESSIBLE_ROUTE,
    FORBIDDEN_ADVERSE_FIELDS,
    NON_DIGITAL_CHANNELS,
    NOT_INFERRED,
    PROTECTION,
    RESOLVED,
    ROUTES,
    SAFEGUARDS,
    STATUSES,
    SUBJECT_KINDS,
    SUBMITTER_KINDS,
    ChallengeRegister,
    ChallengeSafeguardError,
    Node,
    Record,
    assert_no_adverse_challenge_effects,
    build_non_retaliation_assurance,
    reject_adverse_mapping,
)

__all__ = [
    "ACCESSIBLE_ROUTE",
    "FORBIDDEN_ADVERSE_FIELDS",
    "NON_DIGITAL_CHANNELS",
    "NOT_INFERRED",
    "PROTECTION",
    "RESOLVED",
    "ROUTES",
    "SAFEGUARDS",
    "STATUSES",
    "SUBJECT_KINDS",
    "SUBMITTER_KINDS",
    "ChallengeRegister",
    "ChallengeSafeguardError",
    "Node",
    "Record",
    "assert_no_adverse_challenge_effects",
    "build_non_retaliation_assurance",
    "reject_adverse_mapping",
]
