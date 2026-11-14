"""Affected-person challenge and correction route (FR-052, AC-071, FR-043).

A store-independent register plus deterministic case-safeguard verification. It records, updates,
escalates and resolves constructed challenges against a source, policy, proposal or human_decision
version, and marks only transitive dependents stale on correction. It never reads or writes consent,
refusal, retaliation, sanction, closure or hazard-clock state, and fails closed on any adverse
mutation.
"""

from collections.abc import Iterable, Mapping
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import date
from typing import Any

from . import controls

Record = dict[str, Any]
Node = tuple[str, str, str]

ROUTES = ("digital", "staff_recorded")
NON_DIGITAL_CHANNELS = ("phone", "in_person", "paper", "assisted_visit")
SUBJECT_KINDS = ("source", "policy", "proposal", "human_decision")
STATUSES = ("received", "under_review", "escalated", "corrected", "upheld", "withdrawn")
RESOLVED = ("corrected", "upheld", "withdrawn")
ACCESSIBLE_ROUTE = (
    "You can also challenge this by phone, in person or on paper, and a member of staff will "
    "record it for you. No digital access is needed."
)
PROTECTION = (
    "Challenging this will not change your tenancy, repairs, services or any other decision about "
    "you. If you have a safety concern, tell us and a named person will pick it up straight away."
)
NOT_INFERRED = (
    "consent",
    "refusal",
    "sanction",
    "retaliation",
    "unrelated_closure",
    "hazard_clock",
    "delayed_hazard_response",
)
FORBIDDEN_ADVERSE_FIELDS = frozenset(
    {
        "retaliation",
        "retaliation_flag",
        "penalty",
        "priority_penalty",
        "sanction",
        "adverse_action",
        "service_restriction",
        "tenancy_warning",
        "refusal",
        "inferred_refusal",
        "consent",
        "unrelated_closure",
        "hazard_clock",
        "hazard_delay",
        "hazard_pause",
        "emergency_hold_delay",
    }
)
SAFEGUARDS: dict[str, bool] = {
    "no_retaliation": True,
    "no_inferred_refusal": True,
    "no_delayed_hazard_response": True,
}
_RETALIATION_OR_PRIORITY_KEYS = (
    "resident",
    "funding",
    "wave",
    "stage",
    "days_in_stage",
    "closed",
    "service_requests",
    "appointments",
)
_REFUSAL_OR_CONSENT_KEYS = ("decision", "measure_decisions", "resident_reviews")


class ChallengeSafeguardError(ValueError):
    """Raised when a challenge operation attempts retaliation, inferred refusal or hazard delay."""


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} is required.")
    return value.strip()


def reject_adverse_mapping(payload: Mapping[str, Any], context: str = "Challenge payload") -> None:
    """Fail closed if any forbidden retaliation, refusal or hazard-delay key is supplied."""
    found = sorted(k for k in payload if k in FORBIDDEN_ADVERSE_FIELDS)
    if found:
        joined = ", ".join(found)
        raise ChallengeSafeguardError(
            f"{context} includes forbidden adverse or inferred field(s): {joined}."
        )


def _scan_nested_forbidden_keys(value: Any, context: str) -> None:
    if isinstance(value, Mapping):
        reject_adverse_mapping(value, context)
        for sub_val in value.values():
            _scan_nested_forbidden_keys(sub_val, context)
    elif isinstance(value, list | tuple):
        for item in value:
            _scan_nested_forbidden_keys(item, context)


def _parse_explanations(explanations: Iterable[Mapping[str, Any]]) -> list[Record]:
    out: list[Record] = []
    for item in explanations:
        if not isinstance(item, Mapping):
            raise ValueError("Each explanation must be a mapping.")
        reject_adverse_mapping(item, "Challenge explanation")
        extra_keys = set(item) - {"kind", "text", "permitted"}
        if extra_keys:
            raise ValueError("Explanation keys must be kind, text and permitted only.")
        out.append(
            {
                "kind": _text(item.get("kind"), "Explanation kind"),
                "text": _text(item.get("text"), "Explanation text"),
                "permitted": item.get("permitted") is True,
            }
        )
    return out


def assert_no_adverse_challenge_effects(
    before_case: Mapping[str, Any], after_case: Mapping[str, Any]
) -> None:
    """Verify that a challenge mutation caused no retaliation, inferred refusal or hazard delay."""
    new_top_keys = set(after_case) - set(before_case)
    forbidden_top = sorted(k for k in new_top_keys if k in FORBIDDEN_ADVERSE_FIELDS)
    if forbidden_top:
        raise ChallengeSafeguardError(
            f"Challenge mutation added forbidden adverse case field(s): {', '.join(forbidden_top)}."
        )
    for key in sorted(k for k in after_case if k in FORBIDDEN_ADVERSE_FIELDS):
        if key not in before_case or after_case.get(key) != before_case.get(key):
            raise ChallengeSafeguardError(
                f"Challenge mutation introduced or altered forbidden adverse case field '{key}'."
            )
    _scan_nested_forbidden_keys(
        after_case.get("affected_challenges", ()), "Case affected_challenges"
    )
    if before_case.get("hazards") != after_case.get("hazards"):
        raise ChallengeSafeguardError(
            "Challenge mutation altered or delayed statutory/safety hazard state or clocks."
        )
    for key in _REFUSAL_OR_CONSENT_KEYS:
        if before_case.get(key) != after_case.get(key):
            raise ChallengeSafeguardError(
                f"Challenge mutation altered resident consent or refusal state ('{key}')."
            )
    for key in _RETALIATION_OR_PRIORITY_KEYS:
        if before_case.get(key) != after_case.get(key):
            raise ChallengeSafeguardError(
                "Challenge mutation caused retaliatory, priority or unrelated "
                f"closure change ('{key}')."
            )
    for key in sorted((set(before_case) | set(after_case)) - {"affected_challenges"}):
        if (key in before_case) != (key in after_case) or before_case.get(key) != after_case.get(
            key
        ):
            raise ChallengeSafeguardError(
                f"Challenge mutation modified non-challenge case field '{key}'."
            )


@dataclass
class ChallengeRegister:
    """Challenges plus an injected `{node: [upstream nodes]}` graph; node = (kind, id, version)."""

    dependencies: Mapping[Node, Iterable[Node]] = field(default_factory=dict)
    challenges: dict[str, Record] = field(default_factory=dict)
    stale: dict[Node, Record] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.dependencies = {k: tuple(v) for k, v in self.dependencies.items()}

    def dependents(self, item: Node) -> list[Node]:
        out: set[Node] = set()
        frontier = [item]
        while frontier:
            current = frontier.pop()
            for child, parents in self.dependencies.items():
                if current in parents and child not in out and child != item:
                    out.add(child)
                    frontier.append(child)
        return sorted(out)

    def _record(
        self,
        route: str,
        subject: Mapping[str, str],
        decision_ref: str,
        statement: str,
        owner: str,
        next_update: str,
        explanations: Iterable[Mapping[str, Any]],
        extra: Mapping[str, Any],
        hazard_concern: bool = False,
        received_on: str | None = None,
    ) -> Record:
        reject_adverse_mapping(subject, "Challenge subject")
        extra_subject_keys = set(subject) - {"kind", "id", "version"}
        if extra_subject_keys:
            raise ValueError("Subject keys must be kind, id and version only.")
        kind = subject.get("kind")
        if kind not in SUBJECT_KINDS:
            raise ValueError("Subject kind must be source, policy, proposal or human_decision.")
        due = date.fromisoformat(next_update).isoformat()
        parsed_received = date.fromisoformat(received_on).isoformat() if received_on else None
        parsed_explanations = _parse_explanations(explanations)
        seq = len(self.challenges) + 1
        while f"CH-{seq:03d}" in self.challenges:
            seq += 1
        cid = f"CH-{seq:03d}"
        rec: Record = {
            "id": cid,
            "route": route,
            "subject": {
                "kind": kind,
                "id": _text(subject.get("id"), "Subject id"),
                "version": _text(subject.get("version"), "Subject version"),
            },
            "decision_ref": _text(decision_ref, "Human decision reference"),
            "statement": _text(statement, "Challenge statement"),
            "owner": _text(owner, "Human owner"),
            "next_update": due,
            "accessible_route": ACCESSIBLE_ROUTE,
            "status": "received",
            "resolution": None,
            "explanations": parsed_explanations,
            "history": [{"status": "received", "note": "Challenge recorded."}],
            **extra,
        }
        if hazard_concern:
            # Immediate human referral; the existing hazard process and its clock stay untouched.
            rec["hazard_referral"] = {
                "to": rec["owner"],
                "status": "referred_on_receipt",
                "received_on": parsed_received,
            }
        self.challenges[cid] = rec
        return deepcopy(rec)

    def record_digital(
        self,
        subject: Mapping[str, str],
        decision_ref: str,
        statement: str,
        owner: str,
        next_update: str,
        explanations: Iterable[Mapping[str, Any]] = (),
        hazard_concern: bool = False,
        received_on: str | None = None,
    ) -> Record:
        return self._record(
            "digital",
            subject,
            decision_ref,
            statement,
            owner,
            next_update,
            explanations,
            {},
            hazard_concern,
            received_on,
        )

    def record_staff(
        self,
        recorded_by: str,
        channel: str,
        subject: Mapping[str, str],
        decision_ref: str,
        statement: str,
        owner: str,
        next_update: str,
        explanations: Iterable[Mapping[str, Any]] = (),
        hazard_concern: bool = False,
        received_on: str | None = None,
    ) -> Record:
        if channel not in NON_DIGITAL_CHANNELS:
            raise ValueError("Channel must be phone, in_person, paper or assisted_visit.")
        extra = {"recorded_by": _text(recorded_by, "Recording staff member"), "channel": channel}
        return self._record(
            "staff_recorded",
            subject,
            decision_ref,
            statement,
            owner,
            next_update,
            explanations,
            extra,
            hazard_concern,
            received_on,
        )

    def _get(self, cid: str) -> Record:
        if cid not in self.challenges:
            raise KeyError(cid)
        return self.challenges[cid]

    def update(
        self,
        cid: str,
        statement: str,
        next_update: str | None = None,
        *,
        route: str = "digital",
        recorded_by: str | None = None,
        channel: str | None = None,
        explanations: Iterable[Mapping[str, Any]] = (),
        hazard_concern: bool = False,
        received_on: str | None = None,
    ) -> Record:
        """Append an affected-person update without retaliation, refusal or hazard delay."""
        rec = self._get(cid)
        if rec["status"] in RESOLVED:
            raise ValueError("A resolved challenge cannot be updated here.")
        if route not in ROUTES:
            raise ValueError("Route must be digital or staff_recorded.")
        staff_fields: Record = {}
        if route == "digital":
            if recorded_by is not None or channel is not None:
                raise ValueError("Digital updates cannot set recorded_by or channel.")
        else:
            if channel not in NON_DIGITAL_CHANNELS:
                raise ValueError("Channel must be phone, in_person, paper or assisted_visit.")
            staff_fields = {
                "recorded_by": _text(recorded_by, "Recording staff member"),
                "channel": channel,
            }
        note_text = _text(statement, "Challenge update statement")
        due = date.fromisoformat(next_update).isoformat() if next_update is not None else None
        parsed_received = (
            date.fromisoformat(received_on).isoformat() if received_on is not None else None
        )
        parsed_explanations = _parse_explanations(explanations)
        updates: list[Record] = rec.setdefault("updates", [])
        entry: Record = {
            "sequence": len(updates) + 1,
            "route": route,
            "statement": note_text,
            "explanations": deepcopy(parsed_explanations),
            **staff_fields,
        }
        if due is not None:
            entry["next_update"] = due
            rec["next_update"] = due
        updates.append(entry)
        rec["explanations"].extend(parsed_explanations)
        rec["history"].append({"status": rec["status"], "note": "Challenge updated."})
        if hazard_concern:
            existing = rec.get("hazard_referral")
            if existing is None:
                rec["hazard_referral"] = {
                    "to": rec["owner"],
                    "status": "referred_on_receipt",
                    "received_on": parsed_received,
                }
            elif existing.get("status") == "referred_on_receipt":
                # Unconditionally keep original received_on (including None) so ageing never resets.
                existing["to"] = rec["owner"]
            else:
                prior: list[Record] = rec.setdefault("previous_hazard_handoffs", [])
                prior.append(deepcopy(existing))
                rec["hazard_referral"] = {
                    "to": rec["owner"],
                    "status": "referred_on_receipt",
                    "received_on": parsed_received,
                }
        return deepcopy(rec)

    def review(self, cid: str, owner: str, next_update: str) -> Record:
        rec = self._get(cid)
        if rec["status"] in RESOLVED:
            raise ValueError("A resolved challenge cannot be reopened here.")
        if _text(owner, "Reviewing owner") != rec["owner"]:
            raise PermissionError("Only the named human owner can review this challenge.")
        due = date.fromisoformat(next_update).isoformat()
        rec["status"] = "under_review"
        rec["next_update"] = due
        rec["history"].append({"status": "under_review", "note": "Owner review started."})
        return deepcopy(rec)

    def escalate(
        self,
        cid: str,
        escalated_to: str,
        reason: str,
        next_update: str,
        *,
        escalated_by: str | None = None,
    ) -> Record:
        """Escalate an unresolved challenge to a distinct named human owner without hazard delay."""
        rec = self._get(cid)
        if rec["status"] in RESOLVED:
            raise ValueError("A resolved challenge cannot be escalated.")
        new_owner = _text(escalated_to, "Escalation owner")
        if new_owner == rec["owner"]:
            raise ValueError("Escalation requires a different named human owner.")
        why = _text(reason, "Escalation reason")
        if controls.is_memory_reference(why):
            raise ValueError(controls.MEMORY_REFUSAL)
        due = date.fromisoformat(next_update).isoformat()
        actor = (
            _text(escalated_by, "Escalating actor") if escalated_by is not None else rec["owner"]
        )
        previous_owner = rec["owner"]
        rec["owner"] = new_owner
        rec["status"] = "escalated"
        rec["next_update"] = due
        rec.setdefault("escalations", []).append(
            {
                "from": previous_owner,
                "to": new_owner,
                "by": actor,
                "reason": why,
                "next_update": due,
            }
        )
        rec["history"].append({"status": "escalated", "note": f"Escalated to {new_owner}."})
        referral = rec.get("hazard_referral")
        if referral is not None and referral.get("status") == "referred_on_receipt":
            referral.setdefault("originally_referred_to", previous_owner)
            referral["to"] = new_owner
        return deepcopy(rec)

    def resolve(self, cid: str, owner: str, outcome: str, evidence: str) -> Record:
        """Resolve a challenge; only a correction marks dependents stale for re-review."""
        rec = self._get(cid)
        if outcome not in RESOLVED:
            raise ValueError("Outcome must be corrected, upheld or withdrawn.")
        if rec["status"] in RESOLVED:
            raise ValueError("This challenge is already resolved.")
        if _text(owner, "Resolving owner") != rec["owner"]:
            raise PermissionError("Only the named human owner can resolve this challenge.")
        proof = _text(evidence, "Resolution evidence")
        if controls.is_memory_reference(proof):
            raise ValueError(controls.MEMORY_REFUSAL)
        rec["status"] = outcome
        rec["resolution"] = {"outcome": outcome, "evidence": proof}
        rec["history"].append({"status": outcome, "note": "Resolved with evidence."})
        if outcome == "corrected":
            subject = rec["subject"]
            node = (subject["kind"], subject["id"], subject["version"])
            for item in self.dependents(node):
                self.stale[item] = {
                    "reason": f"Upstream {subject['id']}/{subject['version']} corrected via {cid}.",
                    "prior_version_preserved": True,
                }
        return deepcopy(rec)

    def confirm_hazard_handoff(self, cid: str, owner: str, evidence: str) -> Record:
        """Record the named owner's evidenced human handoff of a hazard concern."""
        rec = self._get(cid)
        referral = rec.get("hazard_referral")
        if referral is None:
            raise ValueError("This challenge has no hazard referral.")
        if referral["status"] == "handed_off":
            raise ValueError("This hazard concern is already handed off.")
        if _text(owner, "Handing-off owner") != rec["owner"]:
            raise PermissionError("Only the named human owner can confirm a hazard handoff.")
        proof = _text(evidence, "Hazard handoff evidence")
        if controls.is_memory_reference(proof):
            raise ValueError(controls.MEMORY_REFUSAL)
        referral["status"] = "handed_off"
        referral["handoff_evidence"] = proof
        rec["history"].append({"status": rec["status"], "note": "Hazard handoff evidenced."})
        return deepcopy(rec)

    def hazard_referrals(self) -> list[Record]:
        """Hazard concerns awaiting an evidenced human handoff, whatever the challenge status."""
        return [
            deepcopy(r)
            for r in self.challenges.values()
            if r.get("hazard_referral", {}).get("status") == "referred_on_receipt"
        ]

    def hazard_referrals_overdue(self, today: str, max_days: int) -> list[Record]:
        """Unhanded hazard referrals older than `max_days`, or of unknown age, for the owner.

        `max_days` is required: no limit has been approved by the owner, so the caller must
        state it. A `received_on` after `today` is flagged with `data_quality`.

        Read-only: it flags a possible delay for human follow-up and never starts, stops or
        changes any hazard clock or record.
        """
        now = date.fromisoformat(today)
        out: list[Record] = []
        for rec in self.hazard_referrals():
            received = rec["hazard_referral"].get("received_on")
            age = (now - date.fromisoformat(received)).days if received else None
            future = age is not None and age < 0
            if age is None or age > max_days or future:
                flagged: Record = {**rec, "referral_age_days": age}
                if future:
                    flagged["data_quality"] = "received_on is in the future"
                out.append(flagged)
        return out

    def overdue(self, today: str) -> list[Record]:
        """Unresolved challenges past their promised next update, for the human owner."""
        cutoff = date.fromisoformat(today).isoformat()
        return [
            deepcopy(r)
            for r in self.challenges.values()
            if r["status"] not in RESOLVED and r["next_update"] < cutoff
        ]

    def view(self, cid: str) -> Record:
        """Person-facing view: only permitted explanations, plus owner, next update, resolution."""
        rec = deepcopy(self._get(cid))
        rec["explanations"] = [e for e in rec["explanations"] if e["permitted"]]
        if "updates" in rec:
            for item in rec["updates"]:
                item["explanations"] = [e for e in item.get("explanations", []) if e["permitted"]]
        rec["not_inferred"] = list(NOT_INFERRED)
        rec["protection"] = PROTECTION
        rec["safeguards"] = dict(SAFEGUARDS)
        return rec
