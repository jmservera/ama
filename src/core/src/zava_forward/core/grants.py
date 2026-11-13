"""Evidence-linked grant states, kept apart from provider invoices and payments (FR-019, AC-022).

A grant moves through opportunity, award, claimable, submitted, accepted or
rejected, and cash received. One person proposes each change with its source;
a different person approves it, and both stay in the history. Nothing here
reads or changes invoices or payment status, and nothing is submitted to a
funder by the system.
"""
import os
from copy import deepcopy
from datetime import UTC, datetime

from . import controls as k
from . import gates
from .change_provenance import _actor
from .finance import _identity, _norm

GRANT_FLOW = {"Not recorded": ("Opportunity",), "Opportunity": ("Award",), "Award": ("Claimable",), "Claimable": ("Submitted",),
              "Submitted": ("Accepted", "Rejected"), "Accepted": ("Cash received",), "Rejected": ("Claimable",), "Cash received": ()}
GRANT_STATES = tuple(GRANT_FLOW)
ELIGIBILITY_OUTCOMES = ("Eligible", "Not eligible", "Not assessed")
GRANT_ACTIONS = ("grant_open", "grant_propose", "grant_approve", "grant_withdraw", "grant_eligibility")
ELIGIBILITY_VERIFIER = "Grants and Evidence Officer"


def authority_now():
    return datetime.now(UTC)


def require_authority(store, user, action, case_id, route):
    """Validate explicit fixture designation; never infer real financial delegation."""
    actor = _actor(store, user)
    authority = actor.get("financial_authority")
    denied = "Current scoped human financial designation is required. Ask the Finance authority owner."

    def refuse(state):
        raise gates.AuthorityGateError(denied, state)

    readable = (isinstance(authority, dict)
                and set(authority) == {"kind", "status", "human", "subject", "evidence_ref",
                                       "effective_from", "expires_at", "permissions"})
    if os.environ.get("ZF_ENV", "").lower() == "production":
        refuse(False)
    if not readable:
        refuse(None)
    if (authority["kind"] != "Synthetic exercise" or authority["status"] != "Active"
            or authority["human"] is not True or authority["subject"] != _identity(actor)
            or any(not isinstance(actor.get(key), str) or not actor[key].strip()
                   for key in ("email", "code"))
            or not isinstance(authority["evidence_ref"], str) or not authority["evidence_ref"].strip()
            or not isinstance(route, str) or not route.strip()
            or route in ("Not decided", "Unknown")):
        refuse(False)
    try:
        start = datetime.fromisoformat(authority["effective_from"])
        end = datetime.fromisoformat(authority["expires_at"])
        if start.utcoffset() is None or end.utcoffset() is None:
            refuse(None)
        if not start <= authority_now() < end:
            refuse(False)
    except (ValueError, TypeError):
        refuse(None)
    permissions = authority["permissions"]
    if (not isinstance(permissions, list) or not permissions
            or any(not isinstance(p, dict) or set(p) != {"action", "case_id", "route"}
                   or any(not isinstance(v, str) or not v.strip() or v == "*" for v in p.values())
                   for p in permissions)):
        refuse(None)
    if dict(action=action, case_id=case_id, route=route) not in permissions:
        refuse(False)
    verdict = gates.authority_gate(True, "Current scoped financial designation: met.")
    if not gates.transition_allowed([verdict]):
        refuse(None)
    return deepcopy(authority)


def _same_person(a, b):
    return any(_norm(a.get(key)) and _norm(a.get(key)) == _norm(b.get(key)) for key in ("email", "code", "oid"))


def _complete(identity):
    return isinstance(identity, dict) and all(_norm(identity.get(key)) for key in ("email", "code"))


def grant_eligibility_verdict(recorded, proposer=None, approver=None, on=None):
    """Only an evidenced Eligible outcome from the Grants Officer, distinct from proposer and approver, passes."""
    rec = recorded if isinstance(recorded, dict) else {}
    outcome, source = rec.get("outcome"), rec.get("source")
    evidenced = isinstance(source, str) and bool(source.strip())
    identity = rec.get("identity")
    state = None
    reason = "Eligibility is not assessed, so the grant cannot be submitted."
    if outcome == "Not eligible" and evidenced:
        state, reason = False, "The grant is recorded as not eligible."
    elif outcome == "Eligible" and evidenced:
        if rec.get("role") != ELIGIBILITY_VERIFIER:
            reason = "Eligibility was not recorded by the Grants Officer, so it is unverified."
        elif not (_complete(identity) and _complete(proposer) and _complete(approver)):
            reason = "Eligibility recorder or approver identity is unknown, so independence is unverified."
        elif _same_person(identity, proposer) or _same_person(identity, approver):
            reason = "The eligibility check must be recorded by someone other than the proposer and approver."
        else:
            state, reason = True, "Eligibility confirmed: met."
    return gates.eligibility_gate(state, reason, "Grants Officer", on)


def grant_summary(c):
    gs = c.get("grants") or []
    return ", ".join(f"{g['scheme']}: {g['state']}" for g in gs) if gs else "No grant record"


class GrantMixin:
    def grant_action(self, user, case_id, body):
        k.refuse_bulk(body)
        action = body.get("action")
        if action not in GRANT_ACTIONS:
            raise ValueError("Unknown step.")
        with self._finance_operation(user, case_id) as (user, c):
            grants = c.setdefault("grants", [])
            if action == "grant_open":
                g = dict(id=k.next_id(grants, "GR"), scheme=k.text(body.get("scheme"), "the scheme or funder", 80), state="Not recorded",
                         pending=None, history=[], eligibility=None)
                grants.append(g)
                self._grant_set_pending(user, g, "Opportunity", body)
                detail = f"{g['id']} opened"
            else:
                g = k.find(grants, body.get("id"), "grant")
                detail = getattr(self, "_" + action)(user, g, body, case_id)
            self.audit(user["email"], f"finance_{action}", case_id, detail)

    def _grant_set_pending(self, user, g, to, body):
        if g["pending"]:
            raise ValueError("A change is already waiting for approval.")
        if to not in GRANT_FLOW[g["state"]]:
            raise ValueError(f"A grant cannot go from '{g['state']}' to '{to}'.")
        if body.get("currency", "GBP") != "GBP":
            raise ValueError("Grant records use GBP only. Supply a separate evidenced GBP amount.")
        source = body.get("source")
        if not isinstance(source, str) or not source.strip() or len(source) > 200:
            raise ValueError("Add the exact evidence reference, from 1 to 200 characters.")
        amount = k.money(body.get("amount"), "the amount") if (to == "Cash received" or body.get("amount") not in (None, "")) else None
        g["pending"] = dict(to=to, source=source.strip(), amount=amount, currency="GBP",
                            by=user["email"], name=user["name"], at=k.now(), identity=_identity(user))

    def _grant_eligibility(self, user, g, body, case_id):
        k.require_role(user, (ELIGIBILITY_VERIFIER,), "the Grants and Evidence Officer")
        if g["state"] != "Claimable":
            raise ValueError("Eligibility is checked while the grant is Claimable, just before submission.")
        outcome = k.choice(body.get("eligibility"), ELIGIBILITY_OUTCOMES, "the eligibility outcome")
        ref = body.get("eligibility_source")
        if outcome != "Not assessed" and (not isinstance(ref, str) or not ref.strip() or len(ref) > 200):
            raise ValueError("Add the exact eligibility evidence reference, from 1 to 200 characters.")
        g["eligibility"] = dict(outcome=outcome, source=ref.strip() if isinstance(ref, str) and ref.strip() else None,
                                by=user["email"], role=user["role"], identity=_identity(user), at=k.now())
        return f"{g['id']} eligibility recorded: {outcome}"

    def _grant_propose(self, user, g, body, case_id):
        self._grant_set_pending(user, g, body.get("to"), body)
        return f"{g['id']} proposed {g['pending']['to']}"

    def _grant_approve(self, user, g, body, case_id):
        k.require_role(user, k.FINANCE_APPROVERS, "a manager")
        p = g["pending"]
        if not p:
            raise ValueError("There is no change waiting for approval.")
        identity = self._fin_independent(user, p["by"], p.get("identity"), "approve this grant change")
        if p.get("currency") != "GBP":
            raise ValueError("Legacy proposal currency is unknown. Withdraw and re-propose with GBP evidence.")
        recorded = g.get("eligibility")
        if p["to"] == "Submitted":
            verdict = grant_eligibility_verdict(recorded, p.get("identity"), _identity(user))
            if not gates.transition_allowed([verdict]):
                raise ValueError(f"{verdict.reason} Owner: {verdict.owner}. Next action: {verdict.correction}")
        authority = self._financial_authority(user, "grant:" + p["to"], case_id, g["scheme"])
        g["history"].append(dict(state=p["to"], source=p["source"], amount=p["amount"], proposed_by=p["name"], proposed_at=p["at"],
                                 approved_by=user["name"], approved_at=k.now(), case_id=case_id, scheme=g["scheme"], currency=p["currency"],
                                 proposed_identity=deepcopy(identity), approved_identity=_identity(user), authority=authority,
                                 source_status="Supplied, unverified",
                                 eligibility=deepcopy(recorded) if p["to"] == "Submitted" else None))
        if p["to"] == "Rejected":
            g["eligibility"] = None
        g.update(state=p["to"], pending=None)
        return f"{g['id']} now {g['state']}"

    def _grant_withdraw(self, user, g, body, case_id):
        if not g["pending"]:
            raise ValueError("There is no change waiting for approval.")
        g["pending"] = None
        return f"{g['id']} proposed change withdrawn"
