"""Budgets, commitments, provider invoices, match exceptions, payment holds and Finance disposition (FR-018).

Everything here is a record of what a named person decided. The system compares
lines and lists exceptions, but it never pays anything: "payment status" is a
note of what Finance did elsewhere. Each approval needs a different person from
the one who prepared it, and none of these can be done in bulk (FR-007).
"""
from . import controls as k

INVOICE_KINDS = ("Invoice", "Valuation")
DISPOSITIONS = ("Accept for payment", "Reject and return to provider", "Keep on hold")
PAYMENT_STATUSES = ("Not payable yet", "Awaiting payment run", "Paid outside this system")
FINANCE_ACTIONS = ("budget_propose", "budget_approve", "commit_raise", "commit_approve", "invoice_receive", "invoice_match",
                   "hold_place", "hold_release", "disposition", "payment_status")
PAYMENT_NOTE = "Record only: this system never makes or releases a payment."


def _fin(c):
    return c.setdefault("finance", dict(budget=None, commitments=[], invoices=[]))


def _committed(f):
    return sum(x["amount"] for x in f["commitments"] if x["status"] != "Cancelled")


def _norm(s):
    return (s or "").strip().lower()


def match_invoice(c, inv):
    """Compare each line with the approved commitment, the budget, milestone evidence and earlier invoices."""
    f = _fin(c)
    ex = []
    budget = f["budget"] if f["budget"] and f["budget"]["status"] == "Approved" else None
    coms = [x for x in f["commitments"] if x["status"] == "Approved" and _norm(x["supplier"]) == _norm(inv["supplier"])
            and _norm(x["work_order"]) == _norm(inv["work_order"])]
    com = coms[0] if coms else None
    inv["commitment"] = com["id"] if com else None
    if not com:
        ex.append(dict(line=None, code="no_commitment", message="No approved commitment for this supplier and work order."))
    others = [o for o in f["invoices"] if o["id"] != inv["id"]]
    for o in others:
        if _norm(o["supplier"]) == _norm(inv["supplier"]) and _norm(o["ref"]) == _norm(inv["ref"]) and o["disposition"] != "Reject and return to provider":
            ex.append(dict(line=None, code="duplicate", message=f"Same supplier and reference as {o['id']}."))
    total = sum(ln["amount"] for ln in inv["lines"])
    paid_before = sum(sum(ln["amount"] for ln in o["lines"]) for o in others
                      if com and o.get("commitment") == com["id"] and o["disposition"] == "Accept for payment")
    if com and paid_before + total > com["amount"] + 0.005:
        ex.append(dict(line=None, code="over_commitment",
                       message=f"Total £{paid_before + total:,.2f} with earlier accepted invoices is above the commitment of £{com['amount']:,.2f}."))
    if not budget:
        ex.append(dict(line=None, code="no_budget", message="No approved budget, so the budget check is unknown."))
    else:
        accepted = sum(ln["amount"] for o in others if o["disposition"] == "Accept for payment" for ln in o["lines"])
        if accepted + total > budget["amount"] + 0.005:
            ex.append(dict(line=None, code="over_budget",
                           message=f"Would take accepted invoices to £{accepted + total:,.2f}, above the approved budget of £{budget['amount']:,.2f}."))
    for i, ln in enumerate(inv["lines"]):
        if com and _norm(ln["measure"]) != _norm(com["measure"]):
            ex.append(dict(line=i, code="not_in_scope", message=f"'{ln['measure']}' is not the authorised measure ('{com['measure']}')."))
        if com and ln["quantity"] > com["quantity"] + 1e-9:
            ex.append(dict(line=i, code="quantity", message=f"Quantity {ln['quantity']:g} is above the {com['quantity']:g} authorised."))
        if not ln["milestone_ref"]:
            ex.append(dict(line=i, code="no_milestone", message="Accepted milestone evidence is unknown for this line."))
        elif c.get("exercise"):
            allowed = c["exercise"].get("milestones", {})
            milestone = allowed.get(ln["milestone_ref"])
            if (not milestone or milestone.get("stale") or milestone["work_order"] != inv["work_order"]
                    or abs(milestone["amount"] - ln["amount"]) > 0.005):
                ex.append(dict(line=i, code="unaccepted_milestone", message="Exact accepted same-home milestone/amount evidence is missing."))
    return ex


class FinanceMixin:
    def finance_action(self, user, case_id, body):
        k.refuse_bulk(body)
        action = body.get("action")
        if action not in FINANCE_ACTIONS:
            raise ValueError("Unknown step.")
        k.require_role(user, k.FINANCE_ROLES, "the Grants and Evidence Officer or a manager")
        with self.lock:
            c = self._case(case_id)
            f = _fin(c)
            detail = getattr(self, "_fin_" + action)(user, c, f, body)
            self.audit(user["email"], f"finance_{action}", case_id, detail)
            self.save()

    # ---- budget and commitments
    def _fin_budget_propose(self, user, c, f, body):
        if f["budget"] and f["budget"]["status"] == "Approved":
            raise ValueError("The budget is already approved. Ask a manager to change it.")
        amount = k.money(body.get("amount"), "the budget")
        if c.get("exercise") and amount not in (20000, 22000):
            raise ValueError("Exercise base is GBP 20000, envelope GBP 22000; variations need unavailable Sponsor authority.")
        f["budget"] = dict(amount=amount, status="Proposed", proposed_by=user["email"], proposed_name=user["name"], at=k.now(),
                           note=k.text(body.get("note"), "a note", 200, False), approved_by=None)
        if c.get("exercise"):
            f["budget"].update(base=20000, contingency=2000, envelope=22000,
                               amount_kind="base" if amount == 20000 else "envelope")
        return f"budget {amount:.2f} proposed"

    def _fin_budget_approve(self, user, c, f, body):
        k.require_role(user, k.FINANCE_APPROVERS, "a manager")
        b = f["budget"]
        if not b or b["status"] != "Proposed":
            raise ValueError("There is no proposed budget to approve.")
        k.different_person(user, b["proposed_by"], "approve the budget")
        b.update(status="Approved", approved_by=user["name"], approved_email=user["email"], approved_at=k.now())
        return f"budget {b['amount']:.2f} approved"

    def _fin_commit_raise(self, user, c, f, body):
        b = f["budget"]
        if not b or b["status"] != "Approved":
            raise ValueError("A commitment needs an approved budget first.")
        amount = k.money(body.get("amount"), "the commitment")
        if c.get("exercise") and (amount != 18000 or body.get("contract") != "EX-CALL-OFF-001"):
            raise ValueError("Exercise commitment must match the fictional GBP 18000 call-off; variations are blocked.")
        if _committed(f) + amount > b["amount"] + 0.005:
            raise ValueError(f"That is more than the budget left (£{b['amount'] - _committed(f):,.2f}).")
        com = dict(id=k.next_id(f["commitments"], "COM"), supplier=k.text(body.get("supplier"), "the supplier", 80),
                   contract=k.text(body.get("contract"), "the contract reference", 60),
                   work_order=k.text(body.get("work_order"), "the work order", 60),
                   measure=k.text(body.get("measure"), "the measure", 80), amount=amount, quantity=k.quantity(body.get("quantity")),
                   status="Raised", raised_by=user["email"], raised_name=user["name"], at=k.now(), approved_by=None)
        f["commitments"].append(com)
        return f"{com['id']} {amount:.2f} raised"

    def _fin_commit_approve(self, user, c, f, body):
        k.require_role(user, k.FINANCE_APPROVERS, "a manager")
        com = k.find(f["commitments"], body.get("id"), "commitment")
        if com["status"] != "Raised":
            raise ValueError("Only a raised commitment can be approved.")
        k.different_person(user, com["raised_by"], "approve the commitment")
        com.update(status="Approved", approved_by=user["name"], approved_at=k.now())
        return f"{com['id']} approved"

    # ---- provider invoice or valuation intake and matching
    def _fin_invoice_receive(self, user, c, f, body):
        lines = body.get("lines")
        if not isinstance(lines, list) or not lines or len(lines) > 30 or not all(isinstance(ln, dict) for ln in lines):
            raise ValueError("Add at least one invoice line.")
        clean = [dict(measure=k.text(ln.get("measure"), "the measure on each line", 80), quantity=k.quantity(ln.get("quantity")),
                      amount=k.money(ln.get("amount"), "each line amount"), milestone_ref=k.text(ln.get("milestone_ref"), "", 80, False))
                 for ln in lines]
        inv = dict(id=k.next_id(f["invoices"], "INV"), kind=k.choice(body.get("kind", "Invoice"), INVOICE_KINDS, "the kind"),
                   supplier=k.text(body.get("supplier"), "the supplier", 80), work_order=k.text(body.get("work_order"), "the work order", 60),
                   ref=k.text(body.get("ref"), "the provider's invoice reference", 60), lines=clean, status="Received", exceptions=[],
                   commitment=None, hold=None, disposition=None, disposition_by=None, payment_status="Not payable yet",
                   payment_note=PAYMENT_NOTE, received_by=user["email"], received_name=user["name"], received_at=k.now())
        f["invoices"].append(inv)
        return f"{inv['id']} {inv['kind'].lower()} received"

    def _fin_invoice_match(self, user, c, f, body):
        inv = k.find(f["invoices"], body.get("id"), "invoice")
        if inv["disposition"] and inv["disposition"] != "Keep on hold":
            raise ValueError("Finance has already decided on this one.")
        inv["exceptions"] = match_invoice(c, inv)
        inv["status"] = "Exception, with Finance" if inv["exceptions"] else "Matched"
        return f"{inv['id']} {inv['status']} ({len(inv['exceptions'])} exceptions)"

    # ---- payment holds, Finance disposition and payment status
    def _fin_hold_place(self, user, c, f, body):
        inv = k.find(f["invoices"], body.get("id"), "invoice")
        if inv["hold"]:
            raise ValueError("This is already on hold.")
        inv["hold"] = dict(by=user["email"], name=user["name"], at=k.now(), reason=k.text(body.get("reason"), "why it is on hold"))
        return f"{inv['id']} hold placed"

    def _fin_hold_release(self, user, c, f, body):
        inv = k.find(f["invoices"], body.get("id"), "invoice")
        if not inv["hold"]:
            raise ValueError("This is not on hold.")
        k.different_person(user, inv["hold"]["by"], "release the hold")
        k.text(body.get("note"), "a note on why the hold is released", 200)
        inv["hold"] = None
        return f"{inv['id']} hold released"

    def _fin_disposition(self, user, c, f, body):
        k.require_role(user, k.FINANCE_APPROVERS, "a manager")
        inv = k.find(f["invoices"], body.get("id"), "invoice")
        decision = k.choice(body.get("decision"), DISPOSITIONS, "the decision")
        k.different_person(user, inv["received_by"], "decide on this invoice")
        if inv["disposition"] and inv["disposition"] != "Keep on hold":
            raise ValueError("Finance has already decided on this one.")
        note = k.text(body.get("note"), "a note for the decision", 300)
        if decision == "Accept for payment":
            if c.get("exercise") and match_invoice(c, inv):
                raise ValueError("Current milestone/budget evidence no longer matches; rematch and resolve exceptions.")
            if inv["status"] != "Matched":
                raise ValueError("Run the match first. It can only be accepted when every line matches.")
            if inv["hold"]:
                raise ValueError("Release the hold first.")
        inv.update(disposition=decision, disposition_by=user["name"], disposition_email=user["email"], disposition_note=note,
                   disposition_at=k.now(), payment_status="Not payable yet")
        return f"{inv['id']} {decision}"

    def _fin_payment_status(self, user, c, f, body):
        inv = k.find(f["invoices"], body.get("id"), "invoice")
        status = k.choice(body.get("status"), PAYMENT_STATUSES, "the payment status")
        if status != "Not payable yet":
            if inv["disposition"] != "Accept for payment":
                raise ValueError("Finance must accept the invoice for payment first.")
            if inv["hold"]:
                raise ValueError("Release the hold first.")
            if c.get("exercise") and match_invoice(c, inv):
                raise ValueError("Current milestone/budget evidence no longer matches; obtain independent re-review before recording payment.")
        if status == "Paid outside this system":
            k.different_person(user, inv.get("disposition_email"), "record the payment")
            if c.get("exercise"):
                inv["external_payment_evidence"] = k.text(body.get("evidence"), "fictional external payment evidence reference", 300)
        inv["payment_status"] = status
        return f"{inv['id']} payment noted as {status}"

    def finance_queue(self, user):
        """Human queue of invoices with exceptions or holds, across cases."""
        k.require_role(user, k.FINANCE_ROLES, "the Grants and Evidence Officer or a manager")
        out = []
        with self.lock:
            for c in self.cases.values():
                for inv in (c.get("finance") or {}).get("invoices", []):
                    if inv["disposition"] in (None, "Keep on hold") and (inv["exceptions"] or inv["hold"] or inv["status"] == "Received"):
                        out.append(dict(case_id=c["id"], address=c["home"]["address"], invoice=inv["id"], supplier=inv["supplier"],
                                        ref=inv["ref"], status=inv["status"], exceptions=len(inv["exceptions"]), on_hold=bool(inv["hold"]),
                                        total=round(sum(ln["amount"] for ln in inv["lines"]), 2)))
        return out
