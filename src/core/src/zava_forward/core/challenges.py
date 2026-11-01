"""Affected-person challenge and correction route (FR-052, AC-071, FR-043).

A store-independent register. It records a constructed challenge against a source, policy or
proposal version and the human decision, and marks only transitive dependents stale. It never reads
or writes consent, refusal, sanction, closure or hazard-clock state.
"""

from collections.abc import Iterable, Mapping
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import date
from typing import Any

Record = dict[str, Any]
Node = tuple[str, str, str]

ROUTES = ("digital", "staff_recorded")
NON_DIGITAL_CHANNELS = ("phone", "in_person", "paper", "assisted_visit")
SUBJECT_KINDS = ("source", "policy", "proposal")
STATUSES = ("received", "under_review", "corrected", "upheld", "withdrawn")
RESOLVED = ("corrected", "upheld", "withdrawn")
ACCESSIBLE_ROUTE = (
    "You can also challenge this by phone, in person or on paper, and a member of staff will "
    "record it for you. No digital access is needed."
)
NOT_INFERRED = ("consent", "refusal", "sanction", "unrelated_closure", "hazard_clock")


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} is required.")
    return value.strip()


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
    ) -> Record:
        kind = subject.get("kind")
        if kind not in SUBJECT_KINDS:
            raise ValueError("Subject kind must be source, policy or proposal.")
        due = date.fromisoformat(next_update).isoformat()
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
            "explanations": [
                {
                    "kind": _text(e.get("kind"), "Explanation kind"),
                    "text": _text(e.get("text"), "Explanation text"),
                    "permitted": e.get("permitted") is True,
                }
                for e in explanations
            ],
            "history": [{"status": "received", "note": "Challenge recorded."}],
            **extra,
        }
        if hazard_concern:
            # Immediate human referral; the existing hazard process and its clock stay untouched.
            rec["hazard_referral"] = {"to": rec["owner"], "status": "referred_on_receipt"}
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
        )

    def _get(self, cid: str) -> Record:
        if cid not in self.challenges:
            raise KeyError(cid)
        return self.challenges[cid]

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

    def view(self, cid: str) -> Record:
        """Person-facing view: only permitted explanations, plus owner, next update, resolution."""
        rec = deepcopy(self._get(cid))
        rec["explanations"] = [e for e in rec["explanations"] if e["permitted"]]
        rec["not_inferred"] = list(NOT_INFERRED)
        return rec
