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
from .finance import _identity

GRANT_FLOW = {"Not recorded": ("Opportunity",), "Opportunity": ("Award",), "Award": ("Claimable",), "Claimable": ("Submitted",),
              "Submitted": ("Accepted", "Rejected"), "Accepted": ("Cash received",), "Rejected": ("Claimable",), "Cash received": ()}
GRANT_STATES = tuple(GRANT_FLOW)
ELIGIBILITY_OUTCOMES = ("Eligible", "Not eligible", "Not assessed")
GRANT_ACTIONS = ("grant_open", "grant_propose", "grant_approve", "grant_withdraw")


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


def grant_eligibility_verdict(recorded, on=None):
    """Gate a submission on recorded eligibility; only an explicit Eligible with evidence passes."""
    outcome = recorded.get("outcome") if isinstance(recorded, dict) else None
    source = recorded.get("source") if isinstance(recorded, dict) else None
    evidenced = isinstance(source, str) and bool(source.strip())
    state = None
    if outcome == "Eligible" and evidenced:
        state = True
    elif outcome == "Not eligible" and evidenced:
        state = False
    reason = {True: "Eligibility confirmed: met.", False: "The grant is recorded as not eligible."}.get(
        state, "Eligibility is not assessed, so the grant cannot be submitted.")
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
                         pending=None, history=[], eligibility=dict(outcome="Not assessed", source=None, by=None, at=None))
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
        eligibility = None
        if body.get("eligibility") not in (None, ""):
            outcome = k.choice(body["eligibility"], ELIGIBILITY_OUTCOMES, "the eligibility outcome")
            ref = body.get("eligibility_source")
            if outcome != "Not assessed" and (not isinstance(ref, str) or not ref.strip() or len(ref) > 200):
                raise ValueError("Add the exact eligibility evidence reference, from 1 to 200 characters.")
            eligibility = dict(outcome=outcome, source=ref.strip() if isinstance(ref, str) and ref.strip() else None,
                               by=user["email"], at=k.now())
        g["pending"] = dict(to=to, source=source.strip(), amount=amount, currency="GBP",
                            by=user["email"], name=user["name"], at=k.now(), identity=_identity(user))
        if eligibility is not None:
            g["pending"]["eligibility"] = eligibility

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
        recorded = p["eligibility"] if "eligibility" in p else g.get("eligibility", "legacy")
        if p["to"] == "Submitted" and recorded != "legacy":
            verdict = grant_eligibility_verdict(recorded)
            if not gates.transition_allowed([verdict]):
                raise ValueError(f"{verdict.reason} Owner: {verdict.owner}. Next action: {verdict.correction}")
        authority = self._financial_authority(user, "grant:" + p["to"], case_id, g["scheme"])
        g["history"].append(dict(state=p["to"], source=p["source"], amount=p["amount"], proposed_by=p["name"], proposed_at=p["at"],
                                 approved_by=user["name"], approved_at=k.now(), case_id=case_id, scheme=g["scheme"], currency=p["currency"],
                                 proposed_identity=deepcopy(identity), approved_identity=_identity(user), authority=authority,
                                 source_status="Supplied, unverified",
                                 eligibility="Not assessed (legacy record)" if recorded == "legacy" else deepcopy(recorded)))
        if "eligibility" in p:
            g["eligibility"] = p["eligibility"]
        g.update(state=p["to"], pending=None)
        return f"{g['id']} now {g['state']}"

    def _grant_withdraw(self, user, g, body, case_id):
        if not g["pending"]:
            raise ValueError("There is no change waiting for approval.")
        g["pending"] = None
        return f"{g['id']} proposed change withdrawn"
