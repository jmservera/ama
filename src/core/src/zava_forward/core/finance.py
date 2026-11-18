"""Budgets, commitments, provider invoices, match exceptions, payment holds and Finance disposition (FR-018).

Everything here is a record of what a named person decided. The system compares
lines and lists exceptions, but it never pays anything: "payment status" is a
note of what Finance did elsewhere. Each approval needs a different person from
the one who prepared it, and none of these can be done in bulk (FR-007).
"""
import ast
import json
import logging
import os
import tempfile
from collections.abc import Mapping
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import Any

from . import controls as k
from . import gates
from .gates import FinanceGateError, finance_gate
from .change_provenance import _actor

INVOICE_KINDS = ("Invoice", "Valuation")
DISPOSITIONS = ("Accept for payment", "Reject and return to provider", "Keep on hold")
PAYMENT_STATUSES = ("Not payable yet", "Awaiting payment run", "Paid outside this system")
FINANCE_ACTIONS = ("budget_propose", "budget_approve", "commit_raise", "commit_approve", "invoice_receive", "invoice_match",
                   "hold_place", "hold_release", "disposition", "payment_status")
PAYMENT_NOTE = "Record only: this system never makes or releases a payment."


PROTECTED_FINANCE_OPERATIONS: tuple[str, str, str, str] = (
    "submit_bid",
    "approve_match_funding",
    "certify_claim",
    "record_cash",
)

_AUTOMATED_ACTOR_KINDS: frozenset[str] = frozenset(
    {
        "ai",
        "ai_proposal",
        "agent",
        "anonymous",
        "assistant",
        "automated",
        "automation",
        "background_worker",
        "bot",
        "cron",
        "daemon",
        "job",
        "llm",
        "managed-identity",
        "managed_identity",
        "model",
        "orchestrator",
        "pipeline",
        "scheduler",
        "service",
        "service-principal",
        "service_principal",
        "system",
        "unauthenticated",
        "webhook",
        "worker",
    }
)
_AUTOMATED_BOOL_FLAGS: tuple[tuple[str, str], ...] = (
    ("automated", "automated"),
    ("is_automated", "automated"),
    ("is_agent", "agent"),
    ("is_system", "system"),
    ("is_worker", "worker"),
    ("worker", "worker"),
    ("service_principal", "service_principal"),
    ("managed_identity", "managed_identity"),
    ("ai_generated", "ai"),
    ("auto_apply", "ai_proposal_apply"),
)
_AUTOMATED_ACTOR_KEYS: tuple[str, ...] = (
    "actor_type",
    "kind",
    "principal_type",
    "identity_source",
    "auth_provider",
    "caller_type",
    "source",
)
_AUTOMATED_EMAIL_PREFIXES: tuple[str, ...] = (
    "system@",
    "agent@",
    "worker@",
    "orchestrator@",
    "bot@",
    "noreply@",
    "automation@",
    "assistant@",
    "service-principal@",
    "managed-identity@",
)
_AUTOMATED_CODE_PREFIXES: tuple[str, ...] = (
    "auto-",
    "bot-",
    "sys-",
    "agent-",
    "worker-",
    "orch-",
    "sp-",
    "mi-",
)
_PROPOSAL_APPLY_KEYS: tuple[str, ...] = (
    "proposal_id",
    "recommendation_id",
    "assistant_task_id",
    "ai_proposal",
    "from_proposal",
    "apply_proposal",
    "auto_apply",
    "ai_apply",
    "envelope",
)
_DIRECT_AUTOMATED_ACTIONS: dict[str, str] = {
    "submit_bid": "submit_bid",
    "auto_submit": "submit_bid",
    "approve_match_funding": "approve_match_funding",
    "match_funding_approve": "approve_match_funding",
    "auto_approve": "approve_match_funding",
    "certify_claim": "certify_claim",
    "auto_certify": "certify_claim",
    "record_cash": "record_cash",
    "cash_receipt": "record_cash",
    "auto_record_cash": "record_cash",
}
_AUTOMATED_CORE_MODULES: tuple[str, ...] = (
    "ai.py",
    "ai_consumption.py",
    "ai_prompts.py",
    "ai_registry.py",
    "ai_tasks.py",
    "assistants.py",
    "chat_case_answers.py",
    "chat_isolation.py",
    "chat_panel.py",
    "coordinator.py",
    "resident_assistant.py",
    "workflows.py",
)
_GATED_AUTHORITY_SYMBOLS: frozenset[str] = frozenset(
    {"finance_action", "grant_action", "funding_step", "_financial_authority"}
)


class AutomatedFinanceAuthorityRefusedError(ValueError):
    """Structured RULE-010 refusal when an automated, non-human, or proposal path touches finance or grants."""

    def __init__(
        self,
        reason: str,
        *,
        operation: str = "finance_authority",
        actor_kind: str = "automated",
        rule: str = "RULE-010",
        code: str = "automated_finance_authority_refused",
    ) -> None:
        self.operation: str = operation
        self.actor_kind: str = actor_kind
        self.reason: str = reason
        self.rule: str = rule
        self.code: str = code
        super().__init__(f"{rule} ({code}) [{operation}/{actor_kind}]: {reason}")

    def as_record(self) -> dict[str, str]:
        return {
            "code": self.code,
            "rule": self.rule,
            "operation": self.operation,
            "actor_kind": self.actor_kind,
            "reason": self.reason,
        }


def classify_finance_operation(
    surface: str,
    action: object = None,
    body: object = None,
    *,
    pending_to: object = None,
) -> str:
    """Map a finance, grant, funding-application, or form-pack call to its protected RULE-010 operation."""
    act = _norm(action)
    if not act and isinstance(body, Mapping):
        act = _norm(body.get("action"))
    if act in _DIRECT_AUTOMATED_ACTIONS:
        return _DIRECT_AUTOMATED_ACTIONS[act]
    if surface == "funding_step":
        if act == "submit":
            return "submit_bid"
        if act == "approve":
            return "approve_match_funding"
        if act == "confirm":
            return "record_cash"
        if act == "certify":
            return "certify_claim"
        return "submit_bid"
    if surface == "finance_action":
        if act in ("payment_status", "disposition"):
            return "record_cash"
        return "approve_match_funding"
    if surface == "grant_action":
        raw_to = body.get("to") if isinstance(body, Mapping) else None
        target = (
            raw_to.strip()
            if isinstance(raw_to, str) and raw_to.strip()
            else (pending_to.strip() if isinstance(pending_to, str) else "")
        )
        if target == "Cash received":
            return "record_cash"
        if act == "grant_open" or target == "Opportunity":
            return "submit_bid"
        if target == "Award":
            return "approve_match_funding"
        if act == "grant_eligibility" or target in (
            "Claimable",
            "Submitted",
            "Accepted",
            "Rejected",
        ):
            return "certify_claim"
        return "certify_claim"
    if surface == "form_review":
        if act == "submit":
            return "submit_bid"
        if act == "approve":
            return "approve_match_funding"
        return "certify_claim"
    return "finance_authority"


def _stored_staff_record(store: Any, email: str) -> dict[str, Any] | None:
    if not email:
        return None
    if hasattr(store, "db") and hasattr(store, "dblock"):
        with store.dblock:
            row = store.db.execute("SELECT body FROM staff WHERE email=?", (email,)).fetchone()
        if row and isinstance(row[0], str):
            loaded = json.loads(row[0])
            return loaded if isinstance(loaded, dict) else None
        return None
    staff = getattr(store, "staff", None)
    if isinstance(staff, Mapping):
        person = staff.get(email)
        return person if isinstance(person, dict) else None
    return None


def guard_no_automated_finance_authority(
    user: object,
    *,
    operation: str = "finance_authority",
    body: object = None,
    store: Any = None,
    check_stored_human: bool = False,
) -> None:
    """Deterministically refuse non-human, unauthenticated, automated, or AI proposal-apply callers."""
    if user is None:
        raise AutomatedFinanceAuthorityRefusedError(
            "Unauthenticated caller cannot submit bids, approve match funding, certify claims, or record cash.",
            operation=operation,
            actor_kind="unauthenticated",
        )
    if not isinstance(user, dict):
        raise AutomatedFinanceAuthorityRefusedError(
            "Non-staff caller object cannot exercise human financial or grant authority.",
            operation=operation,
            actor_kind="non_dict_caller",
        )
    email = _norm(user.get("email"))
    code = _norm(user.get("code"))
    if not email and not code:
        raise AutomatedFinanceAuthorityRefusedError(
            "Unauthenticated caller without named staff identity cannot exercise financial or grant authority.",
            operation=operation,
            actor_kind="unauthenticated",
        )
    if user.get("human") is False:
        raise AutomatedFinanceAuthorityRefusedError(
            "Caller is marked human=False; named human authority is required.",
            operation=operation,
            actor_kind="non_human",
        )
    caller_auth = user.get("financial_authority")
    if isinstance(caller_auth, Mapping) and caller_auth.get("human") is False:
        raise AutomatedFinanceAuthorityRefusedError(
            "Caller financial_authority has human=False; automated delegation is forbidden.",
            operation=operation,
            actor_kind="non_human",
        )
    for flag_key, kind in _AUTOMATED_BOOL_FLAGS:
        if bool(user.get(flag_key)):
            raise AutomatedFinanceAuthorityRefusedError(
                f"Automated caller flag '{flag_key}' is forbidden on financial and grant operations.",
                operation=operation,
                actor_kind=kind,
            )
    for meta_key in _AUTOMATED_ACTOR_KEYS:
        meta_val = _norm(user.get(meta_key))
        if meta_val in _AUTOMATED_ACTOR_KINDS:
            raise AutomatedFinanceAuthorityRefusedError(
                f"Automated or non-human principal ({meta_key}={meta_val!r}) cannot exercise financial authority.",
                operation=operation,
                actor_kind=meta_val,
            )
    role_val = _norm(user.get("role"))
    if role_val in _AUTOMATED_ACTOR_KINDS:
        raise AutomatedFinanceAuthorityRefusedError(
            f"Automated role {role_val!r} cannot exercise human financial or grant authority.",
            operation=operation,
            actor_kind=role_val,
        )
    if email in _AUTOMATED_ACTOR_KINDS or email.startswith(_AUTOMATED_EMAIL_PREFIXES):
        raise AutomatedFinanceAuthorityRefusedError(
            f"Automated principal email {email!r} cannot exercise human financial or grant authority.",
            operation=operation,
            actor_kind="automated_principal",
        )
    if code in _AUTOMATED_ACTOR_KINDS or code.startswith(_AUTOMATED_CODE_PREFIXES):
        raise AutomatedFinanceAuthorityRefusedError(
            f"Automated principal code {code!r} cannot exercise human financial or grant authority.",
            operation=operation,
            actor_kind="automated_principal",
        )
    for prop_key in _PROPOSAL_APPLY_KEYS:
        if user.get(prop_key) is not None:
            raise AutomatedFinanceAuthorityRefusedError(
                f"AI proposal context '{prop_key}' on caller cannot auto-apply financial or grant changes.",
                operation=operation,
                actor_kind="ai_proposal_apply",
            )
    if isinstance(body, Mapping):
        act = _norm(body.get("action"))
        if act in _DIRECT_AUTOMATED_ACTIONS:
            raise AutomatedFinanceAuthorityRefusedError(
                f"Automated shortcut action {act!r} is forbidden; each step requires named human review.",
                operation=_DIRECT_AUTOMATED_ACTIONS[act],
                actor_kind="automated_action",
            )
        if body.get("automated") is True or body.get("approved") is True:
            raise AutomatedFinanceAuthorityRefusedError(
                "Pre-approved or automated execution flags in request payloads are forbidden.",
                operation=operation,
                actor_kind="ai_proposal_apply",
            )
        body_actor_type = _norm(body.get("actor_type"))
        if body_actor_type in _AUTOMATED_ACTOR_KINDS:
            raise AutomatedFinanceAuthorityRefusedError(
                f"Automated payload actor_type={body_actor_type!r} is forbidden.",
                operation=operation,
                actor_kind=body_actor_type,
            )
        body_source = _norm(body.get("source"))
        if body_source in {"ai", "ai_proposal", "assistant", "agent", "automated"}:
            raise AutomatedFinanceAuthorityRefusedError(
                f"Automated proposal source {body_source!r} cannot execute financial or grant actions.",
                operation=operation,
                actor_kind="ai_proposal_apply",
            )
        for prop_key in _PROPOSAL_APPLY_KEYS:
            if body.get(prop_key) is not None:
                raise AutomatedFinanceAuthorityRefusedError(
                    f"AI proposal payload field '{prop_key}' cannot be applied to financial or grant state.",
                    operation=operation,
                    actor_kind="ai_proposal_apply",
                )
    if check_stored_human and store is not None:
        stored = _stored_staff_record(store, email)
        if isinstance(stored, Mapping):
            if stored.get("human") is False:
                raise AutomatedFinanceAuthorityRefusedError(
                    "Stored staff record is marked non-human and cannot exercise financial authority.",
                    operation=operation,
                    actor_kind="non_human_staff",
                )
            for flag_key, kind in _AUTOMATED_BOOL_FLAGS:
                if bool(stored.get(flag_key)):
                    raise AutomatedFinanceAuthorityRefusedError(
                        f"Stored staff record carries automated flag '{flag_key}'.",
                        operation=operation,
                        actor_kind=kind,
                    )
            stored_auth = stored.get("financial_authority")
            if isinstance(stored_auth, Mapping) and stored_auth.get("human") is False:
                raise AutomatedFinanceAuthorityRefusedError(
                    "Stored staff financial_authority has human=False; automated delegation is forbidden.",
                    operation=operation,
                    actor_kind="non_human_staff",
                )




def _fin(c):
    return c.setdefault("finance", dict(budget=None, commitments=[], invoices=[]))


def _committed(f):
    return sum(x["amount"] for x in f["commitments"] if x["status"] != "Cancelled")


def _norm(s):
    return s.strip().lower() if isinstance(s, str) else ""


def _same(a, b):
    """Equal only when both are non-blank strings; malformed values never pair."""
    return isinstance(a, str) and isinstance(b, str) and bool(_norm(a)) and _norm(a) == _norm(b)


def identity_well_formed(identity):
    """Email and code are non-blank strings; oid is absent, None or a string."""
    return (isinstance(identity, dict)
            and all(isinstance(identity.get(key), str) and identity[key].strip() for key in ("email", "code"))
            and (identity.get("oid") is None or isinstance(identity["oid"], str)))


def _identity(user):
    return {key: user.get(key) for key in ("email", "code", "oid")}


def _independent(store, user, other, identity, what):
    if identity is None or identity == {}:
        if hasattr(store, "db"):
            with store.dblock:
                row = store.db.execute("SELECT body FROM staff WHERE email=?", (_norm(other),)).fetchone()
            identity = _identity(json.loads(row[0])) if row else None
        else:
            person = store.staff.get(_norm(other))
            identity = _identity(person) if person else None
    if not identity_well_formed(identity):
        raise PermissionError("The preparer's identity is unknown or malformed. Resolve it before approval.")
    if any(not isinstance(user.get(key), (str, type(None))) for key in ("email", "code", "oid")):
        raise PermissionError("Your identity is malformed. Ask an administrator to correct it before approval.")
    if any(_norm(user.get(key)) and _norm(user.get(key)) == _norm(identity.get(key))
           for key in ("email", "code", "oid")):
        raise PermissionError(f"A different person must {what}. You prepared this one.")
    return identity


def validate_sql(store):
    """Repeat staff and independence checks inside the existing writer transaction."""
    context = getattr(store.local, "finance_validation", None)
    if context is not None:
        guard_no_automated_finance_authority(
            context["actor"],
            operation=context.get("operation", "finance_authority"),
            store=store,
            check_stored_human=bool(context.get("check_stored_human")),
        )
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
    coms = [x for x in f["commitments"] if x["status"] == "Approved" and _same(x["supplier"], inv["supplier"])
            and _same(x["work_order"], inv["work_order"])]
    com = coms[0] if len(coms) == 1 else None
    inv["commitment"] = com["id"] if com else None
    if len(coms) > 1:
        ex.append(dict(line=None, code="ambiguous_commitment", message="More than one approved commitment matches. Finance must resolve the reference."))
    elif not com:
        ex.append(dict(line=None, code="no_commitment", message="No approved commitment for this supplier and work order."))
    others = [o for o in f["invoices"] if o["id"] != inv["id"]]
    for o in others:
        if _same(o["supplier"], inv["supplier"]) and _same(o["ref"], inv["ref"]) and o["disposition"] != "Reject and return to provider":
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
        if com and not _same(ln["measure"], com["measure"]):
            ex.append(dict(line=i, code="not_in_scope", message=f"'{ln['measure']}' is not the authorised measure ('{com['measure']}')."))
        if com and ln["quantity"] > com["quantity"] + 1e-9:
            ex.append(dict(line=i, code="quantity", message=f"Quantity {ln['quantity']:g} is above the {com['quantity']:g} authorised."))
        if not ln["milestone_ref"]:
            ex.append(dict(line=i, code="no_milestone", message="Accepted milestone evidence is unknown for this line."))
    return [dict(error, line=i) for error in ex
            for i in (range(len(inv["lines"])) if error["line"] is None else [error["line"]])]


class FinanceMixin:
    def finance_action(self, user, case_id, body):
        action = body.get("action") if isinstance(body, Mapping) else None
        op = classify_finance_operation("finance_action", action, body)
        guard_no_automated_finance_authority(user, operation=op)
        k.refuse_bulk(body)
        guard_no_automated_finance_authority(
            user, operation=op, body=body, store=self, check_stored_human=True
        )
        if action not in FINANCE_ACTIONS:
            raise ValueError("Unknown step.")
        with self._finance_operation(user, case_id, operation=op, check_stored_human=True) as (actor, c):
            detail = getattr(self, "_fin_" + action)(actor, c, _fin(c), body)
            self.audit(actor["email"], f"finance_{action}", case_id, detail)

    @contextmanager
    def _finance_operation(self, user, case_id, *, operation: str = "finance_authority", check_stored_human: bool = False):
        with self.lock:
            guard_no_automated_finance_authority(
                user, operation=operation, store=self, check_stored_human=check_stored_human
            )
            actor = _actor(self, user)
            k.require_role(actor, k.FINANCE_ROLES, "the Grants and Evidence Officer or a manager")
            c = self._case(case_id)
            before = deepcopy(c)
            sql = hasattr(self, "db")
            prior_pending = list(self.local.pending) if sql else None
            audit_size = None if sql else (os.path.getsize(self.audit_path) if os.path.exists(self.audit_path) else 0)
            audit_head = None if sql else self.last_hash
            saving = False
            context = dict(
                actor=actor,
                independent=[],
                authorities=[],
                operation=operation,
                check_stored_human=check_stored_human,
            )
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
        if not b:
            raise FinanceGateError("A commitment needs an approved budget first.", False)
        if not isinstance(b, dict) or not isinstance(b.get("status"), str):
            raise FinanceGateError("The budget record cannot be read. Ask Finance to restore it.", None)
        if b["status"] != "Approved":
            raise FinanceGateError("A commitment needs an approved budget first.", False)
        amount = k.money(body.get("amount"), "the commitment")
        try:
            left = b["amount"] - _committed(f)
            over = amount > left + 0.005
        except (KeyError, TypeError, ValueError):
            raise FinanceGateError("The budget or commitment amounts cannot be read. Ask Finance to restore them.", None) from None
        if over:
            raise FinanceGateError(f"That is more than the budget left (£{left:,.2f}).", False)
        verdict = finance_gate(True, "Approved budget covers the commitment: met.")
        if not gates.transition_allowed([verdict]):
            raise FinanceGateError(verdict.reason, None)
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
            raise ValueError("Payment is already paused for this invoice. Ask Finance if it needs to be restarted.")
        inv["hold"] = dict(by=user["email"], name=user["name"], at=k.now(), reason=k.text(body.get("reason"), "why payment is paused"), identity=_identity(user))
        return f"{inv['id']} hold placed"

    def _fin_hold_release(self, user, c, f, body):
        inv = k.find(f["invoices"], body.get("id"), "invoice")
        if not inv["hold"]:
            raise ValueError("Payment is not paused for this invoice, so there is nothing to restart.")
        self._fin_independent(user, inv["hold"]["by"], inv["hold"].get("identity"), "restart payment")
        k.text(body.get("note"), "a note on why payment is restarted", 200)
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
                raise ValueError("Payment is paused. A different Finance user must restart payment first, then try again.")
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
                raise ValueError("Payment is paused. A different Finance user must restart payment first, then try again.")
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

    def exposure_signal(self, user, limits_path=None):
        """Read-only pause signal comparing recorded commitments with person-approved limits.

        Limits come only from a person-supplied file; none recorded means Held. This never
        approves, resumes or contains activity.
        """
        from . import exposure_limits as el
        from .data_paths import data_file
        k.require_role(user, k.FINANCE_ROLES, "the Grants and Evidence Officer or a manager")
        path = limits_path or os.environ.get("ZF_APPROVED_LIMITS") or data_file().parent / "approved-limits.json"
        try:
            limits = el.load_limits(Path(path))
        except el.LimitsError as exc:
            return el.held(str(exc))
        try:
            with self.lock:
                exposure = el.committed_exposure(deepcopy(list(self.cases.values())))
            return el.assess(limits, exposure)
        except (el.LimitsError, ArithmeticError, AttributeError, TypeError, ValueError) as exc:
            reason = str(exc) if isinstance(exc, el.LimitsError) else "Recorded commitments cannot be read."
            return el.held(reason)


def _scan_python_files_for_authority_calls(paths: list[Path]) -> list[str]:
    violations: list[str] = []
    for path in paths:
        if not path.is_file():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and node.attr in _GATED_AUTHORITY_SYMBOLS:
                violations.append(f"{path.name}:{node.lineno}:{node.attr}")
            elif isinstance(node, ast.Name) and node.id in _GATED_AUTHORITY_SYMBOLS:
                violations.append(f"{path.name}:{node.lineno}:{node.id}")
    return violations


def _build_disposable_probe_store(tmp_dir: str) -> tuple[Any, dict[str, Any], dict[str, str]]:
    from .grants import GRANT_STATES
    from .store import Store

    case_id = "ZF-VERIFY-93"
    route = "SYN-93"

    def _syn_staff(code: str, role: str, oid: str) -> dict[str, Any]:
        email = f"{code.lower()}@example.test"
        return {
            "code": code,
            "name": f"{role} {code}",
            "email": email,
            "role": role,
            "oid": oid,
            "financial_authority": {
                "kind": "Synthetic exercise",
                "status": "Active",
                "human": True,
                "subject": {"email": email, "code": code, "oid": oid},
                "evidence_ref": "SYN-93 invariant probe, not real authority",
                "effective_from": "2026-01-01T00:00:00+00:00",
                "expires_at": "2099-01-01T00:00:00+00:00",
                "permissions": [
                    {"action": act, "case_id": case_id, "route": route}
                    for act in (
                        *("grant:" + state for state in GRANT_STATES),
                        "application:approve",
                        "application:submit",
                        "application:confirm",
                    )
                ],
            },
        }

    geo = _syn_staff("GEO-93", "Grants and Evidence Officer", "synthetic-93-geo")
    pm1 = _syn_staff("PM-93-A", "Retrofit Programme Manager", "synthetic-93-a")
    pm2 = _syn_staff("PM-93-B", "Retrofit Programme Manager", "synthetic-93-b")
    seed_data: dict[str, Any] = {
        "staff": [geo, pm1, pm2],
        "cases": [
            {
                "id": case_id,
                "wave": "Wave 1",
                "closed": False,
                "stage": "Final checks before ordering",
                "stage_since": "2026-01-01",
                "days_in_stage": 5,
                "waiting_on": pm1["name"],
                "reason": "synthetic invariant check",
                "owner_code": pm1["code"],
                "owner": pm1["name"],
                "owner_role": pm1["role"],
                "resident": {
                    "title": "Ms",
                    "name": "Pat Synthetic",
                    "formal": "Ms Synthetic",
                    "phone": "01000 000000",
                    "email": "",
                    "preferred": "Phone",
                    "adjustment": "None",
                    "priority_support": False,
                    "unavailable": "",
                    "representative": None,
                },
                "home": {
                    "address": "93 Synthetic Lane",
                    "town": "Testville",
                    "postcode": "TE1 1ST",
                    "area": "Test",
                    "type": "Mid terrace",
                    "built": 1950,
                    "epc": "D",
                    "tenure": "Social rent",
                    "lat": 0,
                    "lon": 0,
                },
                "measures": "Loft insulation",
                "contractor": {
                    "name": "Test Ltd",
                    "phone": "0",
                    "scope": "x",
                    "contact": "Kim Builder",
                },
                "decision": {"status": "Accepted", "by": "Pat Synthetic", "at": "2026-01-01"},
                "funding_ok": False,
                "funding_route": route,
                "contacts": [],
                "appointments": [],
                "hazards": [],
                "history": [],
            }
        ],
    }
    seed_path = Path(tmp_dir) / "probe-93.json"
    seed_path.write_text(json.dumps(seed_data), encoding="utf-8")
    probe = Store(str(seed_path))

    # Arm funding draft (Approved -> ready for 'submit'; second case for 'approve'/'confirm')
    with probe.lock:
        probe._case(case_id)["funding"]["route"] = route
        missing_kinds = [
            str(x["kind"]) for x in probe.checklist(probe.cases[case_id]) if not x["present"]
        ]
        probe.save()
    for doc_kind in missing_kinds:
        probe.add_document(
            pm1,
            case_id,
            f"{doc_kind.lower().replace(' ', '-')}-probe-93.txt",
            doc_kind,
            f"Synthetic {doc_kind} probe evidence".encode(),
            metadata={
                "source": "SYN-93",
                "source_version": "1",
                "reason": "Synthetic invariant probe",
            },
        )
    probe.funding_draft(pm1, case_id)
    probe.funding_step(pm1, case_id, "approve", "SYN-93 human review")

    # Arm budget + commitment ready for match-funding approval, plus an accepted invoice ready for cash recording
    probe.finance_action(
        geo, case_id, {"action": "budget_propose", "amount": 10000, "note": "SYN-93 budget"}
    )
    probe.finance_action(pm1, case_id, {"action": "budget_approve"})
    probe.finance_action(
        geo,
        case_id,
        {
            "action": "commit_raise",
            "supplier": "Test Ltd",
            "contract": "C-1",
            "work_order": "WO-1",
            "measure": "Loft insulation",
            "amount": 5000,
            "quantity": 10,
        },
    )
    cmt_id = str(probe.detail(case_id)["finance"]["commitments"][0]["id"])
    probe.finance_action(pm1, case_id, {"action": "commit_approve", "id": cmt_id})
    probe.finance_action(
        geo,
        case_id,
        {
            "action": "invoice_receive",
            "kind": "Invoice",
            "supplier": "Test Ltd",
            "work_order": "WO-1",
            "ref": "INV-REF-93",
            "lines": [
                {
                    "measure": "Loft insulation",
                    "quantity": 10,
                    "amount": 1000,
                    "milestone_ref": "MS-1",
                }
            ],
        },
    )
    inv_id = str(probe.detail(case_id)["finance"]["invoices"][0]["id"])
    probe.finance_action(geo, case_id, {"action": "invoice_match", "id": inv_id})
    probe.finance_action(
        pm1,
        case_id,
        {
            "action": "disposition",
            "id": inv_id,
            "decision": "Accept for payment",
            "note": "SYN-93 accepted",
        },
    )
    # Raise a second commitment COM-2 so commit_approve (approve_match_funding) is armed right now
    probe.finance_action(
        geo,
        case_id,
        {
            "action": "commit_raise",
            "supplier": "Test Ltd",
            "contract": "C-2",
            "work_order": "WO-1",
            "measure": "Loft insulation",
            "amount": 1000,
            "quantity": 2,
        },
    )
    pending_cmt_id = str(probe.detail(case_id)["finance"]["commitments"][-1]["id"])

    # Arm GR-1 with pending Submitted (certify_claim) and GR-2 with pending Cash received (record_cash)
    probe.grant_action(
        geo, case_id, {"action": "grant_open", "scheme": route, "source": "SYN-93 notice 1"}
    )
    probe.grant_action(pm1, case_id, {"action": "grant_approve", "id": "GR-1"})
    for next_to in ("Award", "Claimable"):
        probe.grant_action(
            geo,
            case_id,
            {"action": "grant_propose", "id": "GR-1", "to": next_to, "source": f"SYN-93 {next_to}"},
        )
        probe.grant_action(pm2, case_id, {"action": "grant_approve", "id": "GR-1"})
    probe.grant_action(
        geo,
        case_id,
        {
            "action": "grant_eligibility",
            "id": "GR-1",
            "eligibility": "Eligible",
            "eligibility_source": "SYN-93 elig",
        },
    )
    probe.grant_action(
        pm1,
        case_id,
        {"action": "grant_propose", "id": "GR-1", "to": "Submitted", "source": "SYN-93 claim"},
    )

    probe.grant_action(
        geo, case_id, {"action": "grant_open", "scheme": route, "source": "SYN-93 notice 2"}
    )
    probe.grant_action(pm1, case_id, {"action": "grant_approve", "id": "GR-2"})
    for next_to in ("Award", "Claimable", "Submitted", "Accepted"):
        if next_to == "Submitted":
            probe.grant_action(
                geo,
                case_id,
                {
                    "action": "grant_eligibility",
                    "id": "GR-2",
                    "eligibility": "Eligible",
                    "eligibility_source": "SYN-93 elig 2",
                },
            )
        proposer = pm1 if next_to == "Submitted" else geo
        probe.grant_action(
            proposer,
            case_id,
            {"action": "grant_propose", "id": "GR-2", "to": next_to, "source": f"SYN-93 {next_to}"},
        )
        probe.grant_action(pm2, case_id, {"action": "grant_approve", "id": "GR-2"})
    probe.grant_action(
        geo,
        case_id,
        {
            "action": "grant_propose",
            "id": "GR-2",
            "to": "Cash received",
            "source": "SYN-93 remittance",
            "amount": 1000,
        },
    )

    refs = {
        "case_id": case_id,
        "route": route,
        "inv_id": inv_id,
        "pending_cmt_id": pending_cmt_id,
        "claim_grant_id": "GR-1",
        "cash_grant_id": "GR-2",
    }
    return probe, pm2, refs


def verify_no_automated_finance_authority(store: Any = None) -> dict[str, Any]:
    """Deterministically verify RULE-010 / AC-035 across registry, module boundaries, and all four operations.

    Raises AutomatedFinanceAuthorityRefusedError if any automated, non-human, unauthenticated, or
    AI proposal-apply path can submit a bid, approve match funding, certify a claim, or record cash,
    or if caller store state is mutated during verification.
    """
    from . import ai_registry, bounded_ai, form_review

    caller_before_cases: dict[str, Any] | None = None
    caller_before_audit: int | None = None
    if store is not None:
        with store.lock:
            if hasattr(store, "_sync"):
                store._sync()
            caller_before_cases = deepcopy(store.cases)
            caller_before_audit = len(list(store.audit_entries()))

    # 1. Verify bounded-AI capability registry keeps funding tasks strictly propose-only
    cap_audit = bounded_ai.audit_registered_capabilities({})
    if not cap_audit.get("ok"):
        raise AutomatedFinanceAuthorityRefusedError(
            f"Bounded-AI capability registry failed propose-only audit: {cap_audit.get('violations')}",
            operation="finance_authority",
            actor_kind="capability_registry",
        )
    reg_tasks = ai_registry.tasks()
    for cap_id in ("funding-evidence", "funding_draft"):
        cap_entry = (cap_audit.get("capabilities") or {}).get(cap_id)
        raw_spec = reg_tasks.get(cap_id)
        if not isinstance(cap_entry, Mapping) or cap_entry.get("propose_only") is not True:
            raise AutomatedFinanceAuthorityRefusedError(
                f"Funding capability {cap_id!r} is missing or not propose-only in bounded_ai audit.",
                operation="finance_authority",
                actor_kind="capability_registry",
            )
        if not isinstance(raw_spec, Mapping) or "no write" not in str(
            raw_spec.get("permitted_capability", "")
        ):
            raise AutomatedFinanceAuthorityRefusedError(
                f"Funding task {cap_id!r} permits writes or lacks propose-only boundary in ai_registry.",
                operation="finance_authority",
                actor_kind="capability_registry",
            )

    # 2. Verify AST boundaries of core automation modules and sibling agents/orchestrator packages
    core_dir = Path(__file__).resolve().parent
    scan_paths: list[Path] = [core_dir / name for name in _AUTOMATED_CORE_MODULES]
    repo_src_dir = core_dir.parents[3]
    for sibling_pkg in ("agents", "orchestrator"):
        sibling_src = repo_src_dir / sibling_pkg / "src"
        if sibling_src.is_dir():
            scan_paths.extend(sorted(sibling_src.rglob("*.py")))
    ast_violations = _scan_python_files_for_authority_calls(scan_paths)
    if ast_violations:
        raise AutomatedFinanceAuthorityRefusedError(
            f"Automation modules reference gated financial authority symbols: {', '.join(ast_violations)}",
            operation="finance_authority",
            actor_kind="module_boundary",
        )

    # 3. Execute live refusal probes across all four protected operations on a disposable synthetic store
    checked_actors: tuple[tuple[str, object], ...] = (
        ("unauthenticated_none", None),
        ("non_dict_caller", "orchestrator-worker"),
        ("unauthenticated_empty", {}),
        (
            "agent",
            {
                "code": "AGENT-93",
                "name": "Funding Agent",
                "email": "agent@example.test",
                "role": "Retrofit Programme Manager",
                "actor_type": "agent",
            },
        ),
        (
            "orchestrator",
            {
                "code": "ORCH-93",
                "name": "Workflow Orchestrator",
                "email": "orchestrator@example.test",
                "role": "Retrofit Programme Manager",
                "actor_type": "orchestrator",
            },
        ),
        (
            "service_principal",
            {
                "code": "PM-SP-93",
                "name": "Batch Service Principal",
                "email": "batch.sp@example.test",
                "role": "Retrofit Programme Manager",
                "service_principal": True,
            },
        ),
        (
            "non_human",
            {
                "code": "PM-NH-93",
                "name": "Synthetic Automated Approver",
                "email": "nonhuman@example.test",
                "role": "Retrofit Programme Manager",
                "human": False,
            },
        ),
    )

    refusal_counts: dict[str, int] = {op: 0 for op in PROTECTED_FINANCE_OPERATIONS}
    with tempfile.TemporaryDirectory() as tmp_dir:
        probe, designated_human, refs = _build_disposable_probe_store(tmp_dir)
        cid = refs["case_id"]
        before_probe_cases = deepcopy(probe.cases)
        before_probe_audit = len(list(probe.audit_entries()))

        for _label, actor in checked_actors:
            probes: tuple[tuple[str, Any], ...] = (
                (
                    "submit_bid",
                    lambda a=actor: probe.funding_step(a, cid, "submit", "SYN-93 auto bid"),
                ),
                (
                    "submit_bid",
                    lambda a=actor: probe.grant_action(
                        a,
                        cid,
                        {"action": "grant_open", "scheme": refs["route"], "source": "SYN-93"},
                    ),
                ),
                (
                    "submit_bid",
                    lambda a=actor: form_review.action(probe, a, cid, {"action": "submit_bid"}),
                ),
                (
                    "approve_match_funding",
                    lambda a=actor: probe.finance_action(
                        a, cid, {"action": "commit_approve", "id": refs["pending_cmt_id"]}
                    ),
                ),
                (
                    "approve_match_funding",
                    lambda a=actor: probe.funding_step(a, cid, "approve", "SYN-93 auto approve"),
                ),
                (
                    "certify_claim",
                    lambda a=actor: probe.grant_action(
                        a, cid, {"action": "grant_approve", "id": refs["claim_grant_id"]}
                    ),
                ),
                (
                    "certify_claim",
                    lambda a=actor: form_review.action(probe, a, cid, {"action": "certify_claim"}),
                ),
                (
                    "record_cash",
                    lambda a=actor: probe.grant_action(
                        a, cid, {"action": "grant_approve", "id": refs["cash_grant_id"]}
                    ),
                ),
                (
                    "record_cash",
                    lambda a=actor: probe.finance_action(
                        a,
                        cid,
                        {
                            "action": "payment_status",
                            "id": refs["inv_id"],
                            "status": "Paid outside this system",
                        },
                    ),
                ),
                (
                    "record_cash",
                    lambda a=actor: probe.funding_step(a, cid, "confirm", "SYN-93 auto cash"),
                ),
            )
            for expected_op, call in probes:
                try:
                    call()
                except AutomatedFinanceAuthorityRefusedError as err:
                    if err.operation != expected_op:
                        raise AutomatedFinanceAuthorityRefusedError(
                            f"Expected refusal operation {expected_op!r}, got {err.operation!r}.",
                            operation=expected_op,
                            actor_kind="invariant_mismatch",
                        ) from err
                    refusal_counts[expected_op] += 1
                else:
                    raise AutomatedFinanceAuthorityRefusedError(
                        f"Automated actor succeeded on protected operation {expected_op!r}.",
                        operation=expected_op,
                        actor_kind="invariant_breach",
                    )

        # Also verify AI proposal-apply payloads are deterministically refused even when passed by a designated human
        proposal_probes: tuple[tuple[str, Any], ...] = (
            (
                "submit_bid",
                lambda: probe.funding_step(
                    designated_human,
                    cid,
                    "submit",
                    "SYN-93 bid",
                    body={"proposal_id": "PROP-93", "auto_apply": True},
                ),
            ),
            (
                "approve_match_funding",
                lambda: probe.finance_action(
                    designated_human,
                    cid,
                    {
                        "action": "commit_approve",
                        "id": refs["pending_cmt_id"],
                        "proposal_id": "PROP-93",
                    },
                ),
            ),
            (
                "certify_claim",
                lambda: probe.grant_action(
                    designated_human,
                    cid,
                    {
                        "action": "grant_approve",
                        "id": refs["claim_grant_id"],
                        "recommendation_id": "REC-93",
                    },
                ),
            ),
            (
                "record_cash",
                lambda: probe.grant_action(
                    designated_human,
                    cid,
                    {
                        "action": "grant_approve",
                        "id": refs["cash_grant_id"],
                        "ai_proposal": {"to": "Cash received"},
                    },
                ),
            ),
        )
        for expected_op, call in proposal_probes:
            try:
                call()
            except AutomatedFinanceAuthorityRefusedError as err:
                if err.operation != expected_op:
                    raise AutomatedFinanceAuthorityRefusedError(
                        f"Proposal-apply probe expected {expected_op!r}, got {err.operation!r}.",
                        operation=expected_op,
                        actor_kind="invariant_mismatch",
                    ) from err
                refusal_counts[expected_op] += 1
            else:
                raise AutomatedFinanceAuthorityRefusedError(
                    f"AI proposal-apply payload succeeded on protected operation {expected_op!r}.",
                    operation=expected_op,
                    actor_kind="invariant_breach",
                )

        if (
            probe.cases != before_probe_cases
            or len(list(probe.audit_entries())) != before_probe_audit
        ):
            raise AutomatedFinanceAuthorityRefusedError(
                "Refused automated probes mutated case state or appended audit entries.",
                operation="finance_authority",
                actor_kind="state_mutation",
            )
        if not probe.verify_audit():
            raise AutomatedFinanceAuthorityRefusedError(
                "Audit hash chain invalid after automated refusal probes.",
                operation="finance_authority",
                actor_kind="audit_integrity",
            )

    if store is not None:
        with store.lock:
            if hasattr(store, "_sync"):
                store._sync()
            after_cases = deepcopy(store.cases)
            after_audit = len(list(store.audit_entries()))
        if after_cases != caller_before_cases or after_audit != caller_before_audit:
            raise AutomatedFinanceAuthorityRefusedError(
                "Caller store was mutated during verify_no_automated_finance_authority.",
                operation="finance_authority",
                actor_kind="state_mutation",
            )

    total_probes = sum(refusal_counts.values())
    actor_labels = tuple(label for label, _actor in checked_actors) + ("ai_proposal_apply",)
    return {
        "ok": True,
        "rule": "RULE-010",
        "operations": PROTECTED_FINANCE_OPERATIONS,
        "operations_verified": PROTECTED_FINANCE_OPERATIONS,
        "actors_checked": actor_labels,
        "ai_capabilities_checked": ("funding-evidence", "funding_draft"),
        "capabilities_verified": ("funding-evidence", "funding_draft"),
        "module_boundaries_checked": tuple(p.name for p in scan_paths),
        "scanned_module_count": len(scan_paths),
        "probes_executed": total_probes,
        "refusal_counts": refusal_counts,
    }
