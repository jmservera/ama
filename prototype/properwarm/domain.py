"""Deterministic domain rules. Constructed, non-identifying exercise data only."""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field

STAGES = ["new", "assessment", "design_ready", "installation", "quality_review", "closed"]
TRANSITIONS = {s: STAGES[i + 1] for i, s in enumerate(STAGES[:-1])}
# Stages that need a named human approval; an agent or orchestrator can never supply it.
GATED = {"design_ready", "quality_review", "closed"}
HUMAN_ROLES = {"coordinator", "assessor", "quality", "finance"}
SERVICE_ROLES = {"agent", "orchestrator", "importer"}
PROPOSAL_TASKS = {"extract", "reconcile", "summarise", "draft", "raise_review"}
FORBIDDEN_PROPOSAL_FIELDS = {"transition", "to_stage", "approve", "write", "sql"}


class Rejected(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


@dataclass
class Case:
    case_id: str
    stage: str = "new"
    version: int = 1


@dataclass
class Proposal:
    proposal_id: str
    case_id: str
    task: str
    summary: str
    citations: list
    model_tier: str
    status: str = "pending"


@dataclass
class Store:
    cases: dict = field(default_factory=dict)
    proposals: dict = field(default_factory=dict)
    audit: list = field(default_factory=list)
    idempotency: dict = field(default_factory=dict)

    def add_case(self, case_id: str) -> Case:
        self.cases[case_id] = Case(case_id)
        self._audit("system", "case.created", case_id, {"stage": "new"})
        return self.cases[case_id]

    def _audit(self, actor: str, event: str, case_id: str, detail: dict) -> dict:
        prev = self.audit[-1]["hash"] if self.audit else "0" * 64
        body = {"seq": len(self.audit) + 1, "ts": time.time(), "actor": actor, "event": event,
                "case_id": case_id, "detail": detail, "prev": prev}
        body["hash"] = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
        self.audit.append(body)
        return body

    def verify_audit(self) -> bool:
        prev = "0" * 64
        for row in self.audit:
            check = {k: v for k, v in row.items() if k != "hash"}
            if row["prev"] != prev or hashlib.sha256(json.dumps(check, sort_keys=True).encode()).hexdigest() != row["hash"]:
                return False
            prev = row["hash"]
        return True

    def transition(self, actor: str, role: str, case_id: str, to_stage: str,
                   expected_version: int, key: str, approver: str | None = None) -> Case:
        if key in self.idempotency:
            return self.idempotency[key]
        if role in SERVICE_ROLES:
            raise Rejected("forbidden_role", f"{role} cannot change case state")
        if role not in HUMAN_ROLES:
            raise Rejected("unknown_role", "role is not recognised")
        case = self.cases.get(case_id)
        if case is None:
            raise Rejected("not_found", "case does not exist")
        if case.version != expected_version:
            raise Rejected("version_conflict", "case changed; reload and retry")
        if TRANSITIONS.get(case.stage) != to_stage:
            raise Rejected("invalid_transition", f"{case.stage} cannot move to {to_stage}")
        if to_stage in GATED and (not approver or approver == actor):
            raise Rejected("approval_required", "a different named human must approve this stage")
        case.stage, case.version = to_stage, case.version + 1
        self._audit(actor, "case.transitioned", case_id, {"to": to_stage, "approver": approver, "key": key})
        self.idempotency[key] = case
        return case

    def submit_proposal(self, actor: str, role: str, payload: dict) -> Proposal:
        if role != "agent":
            raise Rejected("forbidden_role", "only the agent identity submits proposals")
        bad = FORBIDDEN_PROPOSAL_FIELDS & set(payload)
        if bad:
            raise Rejected("forbidden_field", f"proposal may not carry {sorted(bad)}")
        task, case_id = payload.get("task"), payload.get("case_id")
        if task not in PROPOSAL_TASKS:
            raise Rejected("invalid_task", "task is not an allowed bounded task")
        if case_id not in self.cases:
            raise Rejected("not_found", "case does not exist")
        citations = payload.get("citations")
        if not isinstance(citations, list) or not citations or not all(isinstance(c, str) and c for c in citations):
            raise Rejected("missing_citation", "every proposal needs source citations")
        if not isinstance(payload.get("summary"), str) or not payload["summary"].strip():
            raise Rejected("invalid_schema", "summary is required")
        pid = f"P{len(self.proposals) + 1}"
        prop = Proposal(pid, case_id, task, payload["summary"], citations, payload.get("model_tier", "standard"))
        self.proposals[pid] = prop
        self._audit(actor, "proposal.submitted", case_id, {"proposal": pid, "task": task, "tier": prop.model_tier})
        return prop

    def decide_proposal(self, actor: str, role: str, proposal_id: str, accept: bool) -> Proposal:
        if role not in HUMAN_ROLES:
            raise Rejected("forbidden_role", "only a human reviewer decides a proposal")
        prop = self.proposals.get(proposal_id)
        if prop is None:
            raise Rejected("not_found", "proposal does not exist")
        prop.status = "accepted" if accept else "rejected"
        # Acceptance records a decision about the suggestion. It never advances the case.
        self._audit(actor, f"proposal.{prop.status}", prop.case_id, {"proposal": proposal_id})
        return prop
