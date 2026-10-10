"""Evidence-linked grant states, kept apart from provider invoices and payments (FR-019, AC-022).

A grant moves through opportunity, award, claimable, submitted, accepted or
rejected, and cash received. One person proposes each change with its source;
a different person approves it, and both stay in the history. Nothing here
reads or changes invoices or payment status, and nothing is submitted to a
funder by the system.
"""
from . import controls as k

GRANT_FLOW = {"Not recorded": ("Opportunity",), "Opportunity": ("Award",), "Award": ("Claimable",), "Claimable": ("Submitted",),
              "Submitted": ("Accepted", "Rejected"), "Accepted": ("Cash received",), "Rejected": ("Claimable",), "Cash received": ()}
GRANT_STATES = tuple(GRANT_FLOW)
GRANT_ACTIONS = ("grant_open", "grant_propose", "grant_approve", "grant_withdraw")


def grant_summary(c):
    gs = c.get("grants") or []
    return ", ".join(f"{g['scheme']}: {g['state']}" for g in gs) if gs else "No grant record"


class GrantMixin:
    def grant_action(self, user, case_id, body):
        k.refuse_bulk(body)
        action = body.get("action")
        if action not in GRANT_ACTIONS:
            raise ValueError("Unknown step.")
        k.require_role(user, k.FINANCE_ROLES, "the Grants and Evidence Officer or a manager")
        with self.lock:
            c = self._case(case_id)
            if c.get("exercise"):
                raise PermissionError("Use separate version-bound exercise application/award/claim/cash events.")
            grants = c.setdefault("grants", [])
            if action == "grant_open":
                g = dict(id=k.next_id(grants, "GR"), scheme=k.text(body.get("scheme"), "the scheme or funder", 80), state="Not recorded",
                         pending=None, history=[])
                grants.append(g)
                self._grant_set_pending(user, g, "Opportunity", body)
                detail = f"{g['id']} opened"
            else:
                g = k.find(grants, body.get("id"), "grant")
                detail = getattr(self, "_" + action)(user, g, body)
            self.audit(user["email"], f"finance_{action}", case_id, detail)
            self.save()

    def _grant_set_pending(self, user, g, to, body):
        if g["pending"]:
            raise ValueError("A change is already waiting for approval.")
        if to not in GRANT_FLOW[g["state"]]:
            raise ValueError(f"A grant cannot go from '{g['state']}' to '{to}'.")
        amount = k.money(body.get("amount"), "the amount") if (to == "Cash received" or body.get("amount") not in (None, "")) else None
        g["pending"] = dict(to=to, source=k.text(body.get("source"), "the evidence or source for this change", 200), amount=amount,
                            by=user["email"], name=user["name"], at=k.now())

    def _grant_propose(self, user, g, body):
        self._grant_set_pending(user, g, body.get("to"), body)
        return f"{g['id']} proposed {g['pending']['to']}"

    def _grant_approve(self, user, g, body):
        k.require_role(user, k.FINANCE_APPROVERS, "a manager")
        p = g["pending"]
        if not p:
            raise ValueError("There is no change waiting for approval.")
        k.different_person(user, p["by"], "approve this grant change")
        g["history"].append(dict(state=p["to"], source=p["source"], amount=p["amount"], proposed_by=p["name"], proposed_at=p["at"],
                                 approved_by=user["name"], approved_at=k.now()))
        g.update(state=p["to"], pending=None)
        return f"{g['id']} now {g['state']}"

    def _grant_withdraw(self, user, g, body):
        if not g["pending"]:
            raise ValueError("There is no change waiting for approval.")
        g["pending"] = None
        return f"{g['id']} proposed change withdrawn"
