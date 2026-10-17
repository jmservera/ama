"""Budgets, commitments, provider invoices, match exceptions, payment holds and Finance disposition (FR-018).

Everything here is a record of what a named person decided. The system compares
lines and lists exceptions, but it never pays anything: "payment status" is a
note of what Finance did elsewhere. Each approval needs a different person from
the one who prepared it, and none of these can be done in bulk (FR-007).
"""
import json
import logging
import os
from copy import deepcopy
from contextlib import contextmanager

from . import controls as k
from .change_provenance import _actor

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


def _identity(user):
    return {key: user.get(key) for key in ("email", "code", "oid")}


def _independent(store, user, other, identity, what):
    if not identity:
        if hasattr(store, "db"):
            with store.dblock:
                row = store.db.execute("SELECT body FROM staff WHERE email=?", (_norm(other),)).fetchone()
            identity = _identity(json.loads(row[0])) if row else None
        else:
            person = store.staff.get(_norm(other))
            identity = _identity(person) if person else None
    if not identity or not identity.get("email") or not identity.get("code"):
        raise PermissionError("The preparer's identity is unknown. Resolve it before approval.")
    if any(_norm(user.get(key)) and _norm(user.get(key)) == _norm(identity.get(key))
           for key in ("email", "code", "oid")):
        raise PermissionError(f"A different person must {what}. You prepared this one.")
    return identity


def validate_sql(store):
    """Repeat staff and independence checks inside the existing writer transaction."""
    context = getattr(store.local, "finance_validation", None)
    if context is not None:
        actor = _actor(store, context["actor"])
        k.require_role(actor, k.FINANCE_ROLES, "current Finance staff")
        for other, identity, what in context["independent"]:
            _independent(store, actor, other, identity, what)
        for action, case_id, route, authority in context["authorities"]:
            from .grants import require_authority
            if require_authority(store, actor, action, case_id, route) != authority:
                raise PermissionError("Financial designation changed. Reload before recording this change.")


def match_invoice(c, inv):
    """Compare each line with the approved commitment, the budget, milestone evidence and earlier invoices."""
    f = _fin(c)
    ex = []
    budget = f["budget"] if f["budget"] and f["budget"]["status"] == "Approved" else None
    coms = [x for x in f["commitments"] if x["status"] == "Approved" and _norm(x["supplier"]) == _norm(inv["supplier"])
            and _norm(x["work_order"]) == _norm(inv["work_order"])]
    com = coms[0] if len(coms) == 1 else None
    inv["commitment"] = com["id"] if com else None
    if len(coms) > 1:
        ex.append(dict(line=None, code="ambiguous_commitment", message="More than one approved commitment matches. Finance must resolve the reference."))
    elif not com:
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
    return [dict(error, line=i) for error in ex
            for i in (range(len(inv["lines"])) if error["line"] is None else [error["line"]])]


class FinanceMixin:
    def finance_action(self, user, case_id, body):
        k.refuse_bulk(body)
        action = body.get("action")
        if action not in FINANCE_ACTIONS:
            raise ValueError("Unknown step.")
        with self._finance_operation(user, case_id) as (actor, c):
            detail = getattr(self, "_fin_" + action)(actor, c, _fin(c), body)
            self.audit(actor["email"], f"finance_{action}", case_id, detail)

    @contextmanager
    def _finance_operation(self, user, case_id):
        with self.lock:
            actor = _actor(self, user)
            k.require_role(actor, k.FINANCE_ROLES, "the Grants and Evidence Officer or a manager")
            c = self._case(case_id)
            before = deepcopy(c)
            sql = hasattr(self, "db")
            prior_pending = list(self.local.pending) if sql else None
            audit_size = None if sql else (os.path.getsize(self.audit_path) if os.path.exists(self.audit_path) else 0)
            audit_head = None if sql else self.last_hash
            saving = False
            context = dict(actor=actor, independent=[], authorities=[])
            self._finance_context = context
            if sql:
                self.local.finance_validation = context
            try:
                yield actor, c
                saving = True
                self.save()
            except Exception as error:
                if sql:
                    with self.dblock:
                        try:
                            self._discard(pending=prior_pending)
                        except Exception as recovery_error:
                            error.add_note(
                                f"Finance SQL recovery failed ({type(recovery_error).__name__}); "
                                "original operation failure retained. "
                                "Reload persisted records before retrying."
                            )
                            logging.getLogger(__name__).exception(
                                "Finance SQL recovery failed; original operation failure retained"
                            )
                else:
                    c.clear()
                    c.update(before)
                    # Ledger rollback must not depend on a second successful state write.
                    try:
                        if os.path.exists(self.audit_path):
                            with open(self.audit_path, "r+b") as audit:
                                audit.truncate(audit_size)
                        self.last_hash = audit_head
                    finally:
                        if saving:
                            from .store import Store
                            try:
                                Store.save(self)
                            except Exception as error:
                                raise RuntimeError("Finance state restoration failed; the durable outcome may be unknown. Reload persisted records before retrying.") from error
                raise
            finally:
                self._finance_context = None
                if sql:
                    self.local.finance_validation = None

    def _fin_independent(self, user, other, identity, what):
        resolved = _independent(self, user, other, identity, what)
        # Preserve missing legacy identity so SQL repeats its current registry lookup.
        self._finance_context["independent"].append((other, deepcopy(identity), what))
        return resolved

    def _financial_authority(self, user, action, case_id, route):
        from .grants import require_authority
        authority = require_authority(self, user, action, case_id, route)
        self._finance_context["authorities"].append((action, case_id, route, authority))
        return authority

    # ---- budget and commitments
    def _fin_budget_propose(self, user, c, f, body):
        if f["budget"] and f["budget"]["status"] == "Approved":
            raise ValueError("The budget is already approved. Ask a manager to change it.")
        amount = k.money(body.get("amount"), "the budget")
        f["budget"] = dict(amount=amount, status="Proposed", proposed_by=user["email"], proposed_name=user["name"], at=k.now(),
                           note=k.text(body.get("note"), "a note", 200, False), approved_by=None, proposed_identity=_identity(user))
        return f"budget {amount:.2f} proposed"

    def _fin_budget_approve(self, user, c, f, body):
        k.require_role(user, k.FINANCE_APPROVERS, "a manager")
        b = f["budget"]
        if not b or b["status"] != "Proposed":
            raise ValueError("There is no proposed budget to approve.")
        self._fin_independent(user, b["proposed_by"], b.get("proposed_identity"), "approve the budget")
        b.update(status="Approved", approved_by=user["name"], approved_email=user["email"], approved_at=k.now())
        return f"budget {b['amount']:.2f} approved"

    def _fin_commit_raise(self, user, c, f, body):
        b = f["budget"]
        if not b or b["status"] != "Approved":
            raise ValueError("A commitment needs an approved budget first.")
        amount = k.money(body.get("amount"), "the commitment")
        if _committed(f) + amount > b["amount"] + 0.005:
            raise ValueError(f"That is more than the budget left (£{b['amount'] - _committed(f):,.2f}).")
        com = dict(id=k.next_id(f["commitments"], "COM"), supplier=k.text(body.get("supplier"), "the supplier", 80),
                   contract=k.text(body.get("contract"), "the contract reference", 60),
                   work_order=k.text(body.get("work_order"), "the work order", 60),
                   measure=k.text(body.get("measure"), "the measure", 80), amount=amount, quantity=k.quantity(body.get("quantity")),
                   status="Raised", raised_by=user["email"], raised_name=user["name"], at=k.now(), approved_by=None, raised_identity=_identity(user))
        f["commitments"].append(com)
        return f"{com['id']} {amount:.2f} raised"

    def _fin_commit_approve(self, user, c, f, body):
        k.require_role(user, k.FINANCE_APPROVERS, "a manager")
        com = k.find(f["commitments"], body.get("id"), "commitment")
        if com["status"] != "Raised":
            raise ValueError("Only a raised commitment can be approved.")
        self._fin_independent(user, com["raised_by"], com.get("raised_identity"), "approve the commitment")
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
                   payment_note=PAYMENT_NOTE, received_by=user["email"], received_name=user["name"], received_at=k.now(), received_identity=_identity(user))
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
        inv["hold"] = dict(by=user["email"], name=user["name"], at=k.now(), reason=k.text(body.get("reason"), "why it is on hold"), identity=_identity(user))
        return f"{inv['id']} hold placed"

    def _fin_hold_release(self, user, c, f, body):
        inv = k.find(f["invoices"], body.get("id"), "invoice")
        if not inv["hold"]:
            raise ValueError("This is not on hold.")
        self._fin_independent(user, inv["hold"]["by"], inv["hold"].get("identity"), "release the hold")
        k.text(body.get("note"), "a note on why the hold is released", 200)
        inv["hold"] = None
        return f"{inv['id']} hold released"

    def _fin_disposition(self, user, c, f, body):
        k.require_role(user, k.FINANCE_APPROVERS, "a manager")
        inv = k.find(f["invoices"], body.get("id"), "invoice")
        decision = k.choice(body.get("decision"), DISPOSITIONS, "the decision")
        self._fin_independent(user, inv["received_by"], inv.get("received_identity"), "decide on this invoice")
        if inv["disposition"] and inv["disposition"] != "Keep on hold":
            raise ValueError("Finance has already decided on this one.")
        note = k.text(body.get("note"), "a note for the decision", 300)
        if decision == "Accept for payment":
            if inv["status"] != "Matched":
                raise ValueError("Run the match first. It can only be accepted when every line matches.")
            if inv["hold"]:
                raise ValueError("Release the hold first.")
            if match_invoice(c, inv):
                raise ValueError("The match inputs changed or are unknown. Run the match again and resolve every line exception.")
        inv.update(disposition=decision, disposition_by=user["name"], disposition_email=user["email"], disposition_note=note,
                   disposition_at=k.now(), payment_status="Not payable yet", disposition_identity=_identity(user))
        return f"{inv['id']} {decision}"

    def _fin_payment_status(self, user, c, f, body):
        inv = k.find(f["invoices"], body.get("id"), "invoice")
        status = k.choice(body.get("status"), PAYMENT_STATUSES, "the payment status")
        if status != "Not payable yet":
            if inv["disposition"] != "Accept for payment":
                raise ValueError("Finance must accept the invoice for payment first.")
            if inv["hold"]:
                raise ValueError("Release the hold first.")
        if status == "Paid outside this system":
            self._fin_independent(user, inv.get("disposition_email"), inv.get("disposition_identity"), "record the payment")
        inv["payment_status"] = status
        event = dict(status=status, owner={key: user.get(key) for key in ("email", "code", "name", "role", "oid")}, at=k.now())
        inv.update(payment_status_owner=event["owner"], payment_status_at=event["at"])
        inv.setdefault("payment_status_history", []).append(event)
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
