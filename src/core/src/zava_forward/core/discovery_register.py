"""Phase 0 retrofit-flow discovery records (BG-011; issue #124).

Pure, in-memory rules for the discovery brief. It records what named owners
validate and never validates, ranks or infers a cause for them. Nothing here
reads company data, calls a model or writes a source system, so discovery stays
fully manual and works when AI is unavailable. Fixtures that use it are
synthetic demonstration data.

* Owner: the accountable discovery owner is nominated by the sponsor and the
  accepted-handover endpoint is agreed by a named person before the owner is
  complete.
* Dictionary: the ten separate lifecycle events must each be defined and
  validated by the operational owner of that event.
* Constraint register: a candidate constraint is a hypothesis. It becomes a
  company finding only after a named operational owner validates it, and only
  with supporting and contradicting evidence recorded. A dispute stays visible.
"""

from dataclasses import dataclass, field, replace
from datetime import date

ENDPOINT = "accepted handover"
REQUIRED_EVENTS = (
    "candidate selection",
    "work release",
    "appointment",
    "installation",
    "practical completion",
    "invoice",
    "documentary completion",
    "physical acceptance",
    "evidence acceptance",
    "resident handover",
)
PROPOSED, VALIDATED, DISPUTED = "PROPOSED", "VALIDATED", "DISPUTED"
SUPPORTS, CONTRADICTS = "supports", "contradicts"
NOT_FINDING = "Candidate only. Not a company finding until the named owner validates it."


@dataclass(frozen=True)
class DiscoveryOwner:
    nominated_by: str = ""
    owner: str = ""
    endpoint: str = ""
    endpoint_agreed_by: str = ""

    def status(self) -> str:
        if not (self.nominated_by.strip() and self.owner.strip()):
            return "NOT_NOMINATED"
        if self.endpoint.strip().lower() != ENDPOINT or not self.endpoint_agreed_by.strip():
            return "ENDPOINT_NOT_AGREED"
        return "ENDPOINT_AGREED"


@dataclass(frozen=True)
class EventDefinition:
    event: str
    meaning: str
    owner_role: str
    validated_by: str = ""
    validated_on: date | None = None

    @property
    def validated(self) -> bool:
        return bool(self.validated_by.strip()) and self.validated_on is not None


def validate_event(
    definition: EventDefinition, validator: str, role: str, on: date
) -> EventDefinition:
    """Record owner validation; only the role that owns the event may validate it."""
    if role != definition.owner_role:
        raise ValueError(
            f"{definition.event} is validated by the {definition.owner_role}, not the {role}"
        )
    if not validator.strip():
        raise ValueError("A named validator is required")
    return replace(definition, validated_by=validator.strip(), validated_on=on)


def dictionary_gaps(definitions: list[EventDefinition]) -> list[str]:
    """Plain-language gaps; an empty list means the dictionary is validated."""
    by_event = {d.event: d for d in definitions}
    gaps = []
    for event in REQUIRED_EVENTS:
        found = by_event.get(event)
        if found is None:
            gaps.append(f"Define the {event} event as a separate event")
        elif not found.meaning.strip():
            gaps.append(f"Add a meaning for the {event} event")
        elif not found.validated:
            gaps.append(f"The {found.owner_role} has not validated the {event} event")
    return gaps


@dataclass(frozen=True)
class Evidence:
    statement: str
    source_ref: str
    direction: str


@dataclass(frozen=True)
class Constraint:
    code: str
    summary: str
    owner_roles: tuple[str, ...]
    evidence: tuple[Evidence, ...] = ()
    no_contradiction_note: str = ""
    status: str = PROPOSED
    validated_by: str = ""
    decision_note: str = ""
    proposed_by: str = field(default="", compare=False)

    def of(self, direction: str) -> tuple[Evidence, ...]:
        return tuple(e for e in self.evidence if e.direction == direction)

    @property
    def is_company_finding(self) -> bool:
        return self.status == VALIDATED and bool(self.validated_by)


def add_evidence(constraint: Constraint, item: Evidence) -> Constraint:
    if item.direction not in (SUPPORTS, CONTRADICTS):
        raise ValueError("Evidence must support or contradict the constraint")
    if not (item.statement.strip() and item.source_ref.strip()):
        raise ValueError("Evidence needs a statement and a traceable source reference")
    if constraint.status != PROPOSED:
        raise ValueError(
            "Evidence cannot change a constraint after an owner decision; propose a new version"
        )
    return replace(constraint, evidence=constraint.evidence + (item,))


def evidence_gaps(constraint: Constraint) -> list[str]:
    gaps = []
    if not constraint.of(SUPPORTS):
        gaps.append("Record supporting evidence")
    if not constraint.of(CONTRADICTS) and not constraint.no_contradiction_note.strip():
        gaps.append("Record contradicting evidence, or note what was searched and not found")
    return gaps


def decide(
    constraint: Constraint, validator: str, role: str, accept: bool, note: str
) -> Constraint:
    """Record an owner decision. The proposer cannot decide; evidence gaps block acceptance."""
    if role not in constraint.owner_roles:
        raise ValueError(
            f"{constraint.code} is decided by {' or '.join(constraint.owner_roles)}, not the {role}"
        )
    if not validator.strip() or validator.strip() == constraint.proposed_by.strip():
        raise ValueError("A named owner other than the proposing analyst must decide")
    if not note.strip():
        raise ValueError("A decision note is required")
    if accept:
        gaps = evidence_gaps(constraint)
        if gaps:
            raise ValueError("; ".join(gaps))
    return replace(
        constraint,
        status=VALIDATED if accept else DISPUTED,
        validated_by=validator.strip(),
        decision_note=note.strip(),
    )


def register_rows(constraints: list[Constraint]) -> list[dict[str, object]]:
    """Rows in the order given, which is the proposed test order, not a ranking of fact."""
    return [
        dict(
            rank=i,
            code=c.code,
            summary=c.summary,
            status=c.status,
            supporting=len(c.of(SUPPORTS)),
            contradicting=len(c.of(CONTRADICTS)),
            gaps=evidence_gaps(c),
            notice="" if c.is_company_finding else NOT_FINDING,
        )
        for i, c in enumerate(constraints, start=1)
    ]


CANDIDATE_CONSTRAINTS = (
    Constraint("CAP", "Supplier or professional capacity", ("Procurement and Contracts",)),
    Constraint(
        "HANDOFF", "Unaccepted handoffs and approval queues", ("Retrofit Programme Manager",)
    ),
    Constraint(
        "RESIDENT",
        "Resident access, adjustment and decision readiness",
        ("Resident Engagement and Housing",),
    ),
    Constraint(
        "DEPEND",
        "Property, building-safety or maintenance dependencies",
        ("Building Safety, Repairs and Assets",),
    ),
    Constraint(
        "QUALITY",
        "Physical or documentary quality failure",
        ("Programme and independent quality owner",),
    ),
)
