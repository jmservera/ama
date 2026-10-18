"""Procurement and capacity (FR-016, AC-020, AC-042).

A package has a period, a scope that is versioned, and a contract or call-off
reference. For each contractor it records the capacity offered and, separately,
the capacity committed with evidence. Work orders are controlled: each change
is a new version with its issuer, and no work order can be issued beyond the
evidenced committed capacity. Contractors see only their own work orders, and
those carry no vulnerability reason (PR-002). Managers record appointment
outcomes and completion on a provider's behalf: a provider's word is evidence,
not a decision.
"""
import hashlib
import json
import logging
import os
import re
from contextlib import contextmanager
from copy import deepcopy
from datetime import UTC, date, datetime

from . import controls, projection
from .appointments import AppointmentCommittedError, AppointmentMixin
from .change_provenance import _actor
from .documents import DocumentStoreError
from .workflows import MANAGER_ROLES, _now, _today

OUTCOMES = ("Booked", "Declined by provider", "Resident not available", "No access", "Rebooking needed")
ISSUED, APPOINTED, COMPLETED, WITHDRAWN = "Issued", "Appointed", "Completed", "Withdrawn"
ACTIVE = (ISSUED, APPOINTED, COMPLETED)
TRANSITIONS = {ISSUED: (APPOINTED, WITHDRAWN), APPOINTED: (COMPLETED, WITHDRAWN, ISSUED), COMPLETED: (ISSUED,), WITHDRAWN: ()}
CONSULTATION_STATUSES = ("applies", "complete", "not_applicable", "unknown")


def _clean(text, n=300):
    if text is not None and not isinstance(text, str):
        raise ValueError("Enter text for this procurement field.")
    return (text or "").strip()[:n]


def _iso(value, what):
    try:
        return date.fromisoformat(str(value)).isoformat()
    except ValueError:
        raise ValueError(f"Enter {what} as a date such as 2026-04-01.")


def _count(value, what):
    if type(value) is not int and not (isinstance(value, str) and re.fullmatch(r"[0-9]+", value)):
        raise ValueError(f"{what} must be a whole number.")
    n = int(value)
    if n < 0 or n > 100000:
        raise ValueError(f"{what} must be between 0 and 100000.")
    return n


def validate_sql(store):
    """Repeat authority and read dependencies under the existing writer transaction."""
    from .store import ConflictError
    context = getattr(store.local, "procurement_validation", None)
    if context is None:
        return
    if _actor(store, context["user"]) != context["actor"]:
        raise PermissionError("Contract authority changed. Reload and ask the contract manager.")
    row = store.db.execute("SELECT value FROM meta WHERE key='procurement'").fetchone()
    if (row[0] if row else None) != context["snapshot"]:
        raise ConflictError("Procurement changed. Reload before confirming work.")
    for cid, version in context["cases"].items():
        row = store.db.execute("SELECT rowversion FROM cases WHERE id=?", (cid,)).fetchone()
        if not row or row[0] != version:
            raise ConflictError("Capacity source or covered home changed. Reload before confirming work.")
    for actor, package, action, contractor, authority in context.get("authorities", []):
        if _actor(store, actor) != actor or store._contract_authority(actor, package, action, contractor) != authority:
            raise PermissionError("Contract delegation changed before confirmation. Ask the contract manager to review it again.")


class ProcurementMixin(AppointmentMixin):
    def _proc(self):
        return self.data.setdefault("procurement", dict(packages=[], work_orders=[]))

    def _need_manager(self, user, what):
        actor = _actor(self, user)
        if actor["role"] not in MANAGER_ROLES:
            raise PermissionError(f"Only a manager can {what}.")
        return actor

    def _contract_authority(self, actor, p, action, contractor=None):
        entries = actor.get("contract_authorities")
        for entry in entries if isinstance(entries, list) else []:
            if not isinstance(entry, dict):
                continue
            if (entry.get("contract_ref") == p["contract_ref"]
                    and entry.get("contract_version") == p.get("contract_version")
                    and isinstance(entry.get("reference"), str) and entry["reference"].strip()
                    and isinstance(entry.get("version"), str) and entry["version"].strip()
                    and entry.get("revoked") is False
                    and isinstance(entry.get("actions"), list) and action in entry["actions"]
                    and isinstance(entry.get("suppliers"), list) and entry["suppliers"]
                    and all(isinstance(s, str) and s.strip() and s != "*" for s in entry["suppliers"])
                    and (contractor is None or contractor in entry["suppliers"])
                    and all(k in entry["suppliers"] for k in p["capacity"] if action == "rescope")
                    and isinstance(entry.get("scope_versions"), list)
                    and all(type(v) is int and v > 0 for v in entry["scope_versions"])
                    and p["scope_version"] in entry["scope_versions"]
                    and (action != "rescope" or p["scope_version"] + 1 in entry["scope_versions"])
                    and ("package_ids" not in entry or
                         isinstance(entry["package_ids"], list) and p["id"] in entry["package_ids"])):
                try:
                    start = _iso(entry.get("valid_from"), "the delegation start")
                    end = _iso(entry.get("valid_to"), "the delegation end")
                except ValueError:
                    continue
                if start <= _today() <= end and p.get("contract_version"):
                    return deepcopy(entry)
        raise PermissionError("A named contract manager needs current authority for this contract version, supplier, scope and action. Ask the contract authority owner.")

    @contextmanager
    def _proc_operation(self, user, action, pid=None, wid=None):
        with self.lock:
            if hasattr(self, "db"):
                self._touched()
            before = deepcopy(self.data.get("procurement"))
            case_before = None
            pending = list(self.local.pending) if hasattr(self, "db") else []
            audit_size = os.path.getsize(self.audit_path) if not hasattr(self, "db") and os.path.exists(self.audit_path) else 0
            audit_head = getattr(self, "last_hash", None)
            context = None
            try:
                actor = self._need_manager(user, action)
                w = self._work_order(wid) if wid else None
                if w:
                    case_before = (w["case_id"], deepcopy(self._case(w["case_id"])))
                p = self._package(w["package"] if w else pid) if pid or w else None
                authority = self._contract_authority(actor, p, action, w["contractor"] if w else None) if p and action not in ("capacity", "consultation") else None
                context = dict(user=deepcopy(user), actor=actor, authority=authority, cases={},
                               snapshot=self._proc_snap.get("procurement") if hasattr(self, "db") else None,
                               authorities=[], persisted=False)
                if authority:
                    context["authorities"].append((actor, deepcopy(p), action, w["contractor"] if w else None, authority))
                if hasattr(self, "local"):
                    self.local.procurement_validation = context
                self._proc_context = context
                yield actor
            except BaseException as error:
                if hasattr(self, "db"):
                    try:
                        with self.dblock:
                            self._discard(() if context and context.get("persisted") else pending)
                    except Exception:
                        error.add_note("Procurement recovery failed; reload to establish the outcome.")
                        logging.getLogger(__name__).exception("Procurement SQL recovery failed")
                elif context and context.get("persisted"):
                    pass
                elif before is None:
                    self.data.pop("procurement", None)
                else:
                    self.data["procurement"] = before
                if not hasattr(self, "db") and context is not None and not context.get("persisted"):
                    if case_before is not None:
                        case = self.cases[case_before[0]]
                        case.clear()
                        case.update(case_before[1])
                    if os.path.exists(self.audit_path):
                        with open(self.audit_path, "r+b") as audit:
                            audit.truncate(audit_size)
                    self.last_hash = audit_head
                    from .store import Store
                    Store.save(self)
                if context and context.get("persisted"):
                    raise AppointmentCommittedError("The procurement change committed, but acknowledgement failed. Reload its history before another action.") from error
                raise
            finally:
                self._proc_context = None
                if hasattr(self, "local"):
                    self.local.procurement_validation = None

    def _proc_save(self, user, action, cid, detail):
        if hasattr(self, "db"):
            self.audit(user["email"], action, cid, detail)
            self.save()
        else:
            self.audit(user["email"], action, cid, detail)
            self.save()
        if getattr(self, "_proc_context", None) is not None:
            self._proc_context["persisted"] = True

    def _capacity_source(self, details):
        cid, doc_id = details.get("source_case_id"), details.get("document_id")
        c = self.cases.get(cid)
        doc = next((d for d in c.get("documents", []) if d["id"] == doc_id), None) if c else None
        if (not doc or doc.get("generated") or doc.get("scan", {}).get("status") != "clean"
                or str(doc.get("version")) != details.get("source_version") or not doc.get("content_sha256")):
            raise ValueError("Capacity source/version is missing, changed or unverified. Upload and check the original commitment document.")
        try:
            content = self.docstore.get(cid, doc_id)
        except KeyError:
            raise ValueError("Capacity source bytes are missing. Restore the original commitment document.") from None
        if hashlib.sha256(content).hexdigest() != doc["content_sha256"]:
            raise ValueError("Capacity source bytes changed. Ask the contract manager to review the source again.")
        context = getattr(self, "_proc_context", None)
        if context is not None and hasattr(self, "db"):
            context["cases"][cid] = self._rv[cid]
        return doc

    def _capacity_details(self, p, contractor, details):
        required = {"source_case_id", "document_id", "source_version", "source_date", "reviewed_on",
                    "valid_from", "valid_to", "unit", "case_ids", "status"}
        if not isinstance(details, dict) or set(details) != required:
            raise ValueError("Record the commitment source/version, dates, covered cases and home-work-order unit. Unknown capacity cannot confirm work.")
        if details["status"] != "Committed" or details["unit"] != "home-work-order":
            raise ValueError("Only an accepted committed home-work-order quota can confirm work, not offered capacity or crew estimates.")
        for key in ("source_case_id", "document_id", "source_version"):
            if not isinstance(details[key], str) or not details[key].strip():
                raise ValueError("Enter the capacity source case, document and exact version.")
        if (not isinstance(details["case_ids"], list) or not details["case_ids"]
                or any(not isinstance(cid, str) or cid not in self.cases
                       or self.cases[cid]["contractor"]["name"] != contractor for cid in details["case_ids"])
                or len(set(details["case_ids"])) != len(details["case_ids"])):
            raise ValueError("List the distinct covered case references for this supplier.")
        values = {k: _iso(details[k], k) for k in ("source_date", "reviewed_on", "valid_from", "valid_to")}
        today = date.fromisoformat(_today())
        if (not values["source_date"] <= values["reviewed_on"] <= _today()
                or (today - date.fromisoformat(values["reviewed_on"])).days > 7):
            raise ValueError("Capacity needs a non-future source date and a manager review within 7 days. Ask the contract manager to check it.")
        if not p["period_from"] <= values["valid_from"] <= values["valid_to"] <= p["period_to"]:
            raise ValueError("Capacity delivery dates must be within the package period.")
        doc = self._capacity_source(details)
        return dict(deepcopy(details), **{"content_sha256": doc["content_sha256"]})

    def _evidenced_capacity(self, p, contractor, cid, when=None):
        cap = p["capacity"].get(contractor)
        if (not cap or type(cap.get("committed")) is not int or cap["committed"] <= 0
                or not isinstance(cap.get("evidence"), str) or not cap["evidence"].strip()):
            raise ValueError("No evidenced committed capacity. Ask the contract manager to record current evidence.")
        details = cap.get("details")
        if not isinstance(details, dict):
            raise ValueError("Legacy capacity is unverified. Ask the contract manager to record current evidence.")
        supplied = {k: details.get(k) for k in ("source_case_id", "document_id", "source_version", "source_date", "reviewed_on",
                                               "valid_from", "valid_to", "unit", "case_ids", "status")}
        checked = self._capacity_details(p, contractor, supplied)
        if (checked["content_sha256"] != details.get("content_sha256") or cap.get("scope_version") != p["scope_version"]
                or cap.get("contract_version") != p.get("contract_version") or cid not in details["case_ids"]):
            raise ValueError("Capacity source, scope, contract or covered home changed. Ask the contract manager to record a new commitment version.")
        accepting = self.staff.get(cap.get("accepted_by", ""))
        if hasattr(self, "db"):
            row = self.db.execute("SELECT body FROM staff WHERE email=?", (cap.get("accepted_by"),)).fetchone()
            accepting = json.loads(row[0]) if row else None
        if not accepting or accepting.get("role") not in MANAGER_ROLES:
            raise ValueError("Capacity acceptance no longer has a named authorized manager.")
        authority = self._contract_authority(accepting, p, "capacity", contractor)
        if authority != cap.get("authority"):
            raise ValueError("Capacity acceptance authority changed. Ask the contract manager to review it again.")
        context = getattr(self, "_proc_context", None)
        if context is not None:
            context["authorities"].append((deepcopy(accepting), deepcopy(p), "capacity", contractor, authority))
        when = when or _today()
        if not details["valid_from"] <= when <= details["valid_to"]:
            raise ValueError("The work date is outside the evidenced capacity period. Ask the contract manager to confirm covered dates.")
        if self._committed_used(p, contractor) > cap["committed"]:
            raise ValueError("Committed capacity is below existing orders. The contract manager must resolve the deficit before more work is confirmed.")
        return cap

    def _package(self, pid):
        p = next((p for p in self._proc()["packages"] if p["id"] == pid), None)
        if not p:
            raise ValueError("Choose one of the packages.")
        return p

    def _work_order(self, wid):
        w = next((w for w in self._proc()["work_orders"] if w["id"] == wid), None)
        if not w:
            raise ValueError("Choose one of the work orders.")
        return w

    def _wo_move(self, w, to, user, note):
        if to not in TRANSITIONS[w["state"]]:
            raise ValueError(f"This work order is '{w['state']}'. It cannot go to '{to}' from there.")
        w.setdefault("history", []).append(dict(at=_now(), by=user["name"], from_state=w["state"], to_state=to, note=note))
        w["state"] = to

    def _committed_used(self, pkg, contractor):
        return sum(1 for w in self._proc()["work_orders"] if w["package"] == pkg["id"] and w["contractor"] == contractor and w["state"] in ACTIVE)

    # ---- packages and capacity
    def create_package(self, user, name, period_from, period_to, scope, contract_ref, contract_version=""):
        self._need_manager(user, "create a package")
        name, scope, contract_ref = _clean(name, 80), _clean(scope, 400), _clean(contract_ref, 60)
        if not name or not scope or not contract_ref:
            raise ValueError("Enter a package name, what it covers and the contract or call-off reference.")
        contract_version = _clean(contract_version, 80)
        if not contract_version:
            raise ValueError("Enter the contract or call-off version before creating the package.")
        start, end = _iso(period_from, "the start"), _iso(period_to, "the end")
        if end < start:
            raise ValueError("The package cannot end before it starts.")
        with self._proc_operation(user, "create"):
            proc = self._proc()
            p = dict(id=f"PKG-{len(proc['packages']) + 1:03d}", name=name, period_from=start, period_to=end, contract_ref=contract_ref, contract_version=contract_version,
                     scope=scope, scope_version=1, scope_history=[dict(version=1, scope=scope, by=user["name"], at=_now(), reason="First version")],
                     capacity={}, consultation_status="unknown", consultation_history=[],
                     created_by=user["name"], created_at=_now())
            proc["packages"].append(p)
            self._proc_save(user, "package_created", "-", f"{p['id']} {name} {start} to {end} ref {contract_ref}; draft, not an instruction")
            return p["id"]

    def record_consultation(self, user, pid, details):
        """Record a supplied human decision, never certify Legal authority or compliance."""
        from .store import ConflictError
        fields = {"status", "decided_by", "reason", "source_case_id", "document_id",
                  "source_version", "expected_version"}
        if not isinstance(details, dict) or set(details) != fields:
            raise ValueError("Supply the consultation status, named human decision maker, reason, source/version and current record version.")
        if details["status"] not in CONSULTATION_STATUSES:
            raise ValueError("Choose applies, complete, not_applicable or unknown.")
        if type(details["expected_version"]) is not int or details["expected_version"] < 0:
            raise ValueError("Supply the current consultation record version.")
        for key in fields - {"status", "expected_version"}:
            limit = 300 if key == "reason" else 100
            if not isinstance(details[key], str) or len(details[key]) > limit:
                raise ValueError(f"Supply {key} as text, at most {limit} characters.")
        values = {key: controls.text(details[key], key, 300 if key == "reason" else 100)
                  for key in fields - {"status", "expected_version"}}
        with self._proc_operation(user, "consultation", pid=pid) as actor:
            p = self._package(pid)
            history = p.setdefault("consultation_history", [])
            if details["expected_version"] != len(history):
                raise ConflictError("Consultation record changed. Reload before recording a decision.")
            doc = self._capacity_source(values)
            record = dict(values, status=details["status"], version=len(history) + 1,
                          contract_ref=p["contract_ref"], contract_version=p.get("contract_version"),
                          scope_version=p["scope_version"], content_sha256=doc["content_sha256"],
                          recorded_by={k: actor.get(k) for k in ("email", "code", "name", "role", "oid")},
                          recorded_at=datetime.now(UTC).isoformat(),
                          authority_status="Unverified", source_status="Supplied human decision; not Legal approval")
            history.append(record)
            p["consultation_status"] = "unknown"
            self._proc_save(actor, "consultation_recorded", "-", f"{pid} supplied {record['status']}; record {record['version']}; Legal authority unverified; consultation-dependent actions held")

    def require_consultation_clear(self, p):
        # No verified contract-consultation Legal capability exists in the current registry.
        raise ValueError(f"Consultation status is unknown for {p['id']}. A named authorized Legal adviser must verify the decision before a consultation-dependent action can proceed. Legal consultation authority and contract letting or renewal are not configured; supplied records cannot release this hold.")

    def rescope_package(self, user, pid, scope, reason):
        self._need_manager(user, "change a package scope")
        scope, reason = _clean(scope, 400), _clean(reason)
        if not scope or not reason:
            raise ValueError("Enter the new scope and why it changed.")
        with self._proc_operation(user, "rescope", pid=pid):
            p = self._package(pid)
            p["scope_version"] += 1
            p["scope"] = scope
            p["scope_history"].append(dict(version=p["scope_version"], scope=scope, by=user["name"], at=_now(), reason=reason))
            self._proc_save(user, "package_rescoped", "-", f"{pid} scope version {p['scope_version']}: {reason}")

    def set_capacity(self, user, pid, contractor, offered, committed, evidence="", details=None):
        self._need_manager(user, "record capacity")
        contractor, evidence = _clean(contractor, 80), _clean(evidence, 300)
        offered, committed = _count(offered, "Offered capacity"), _count(committed, "Committed capacity")
        if contractor not in {c["contractor"]["name"] for c in self.cases.values()}:
            raise ValueError("Choose a contractor already working on a case.")
        if committed > offered:
            raise ValueError("Committed capacity cannot be more than was offered.")
        if committed and not evidence:
            raise ValueError("Committed capacity needs evidence, such as a signed commitment or a resource plan reference.")
        with self._proc_operation(user, "capacity", pid=pid) as actor:
            p = self._package(pid)
            authority = self._contract_authority(actor, p, "capacity", contractor)
            self._proc_context["authorities"].append((actor, deepcopy(p), "capacity", contractor, authority))
            accepted = self._capacity_details(p, contractor, details) if committed else None
            row = p["capacity"].setdefault(contractor, dict(history=[]))
            row.update(offered=offered, committed=committed, evidence=evidence, by=user["name"], at=_now(),
                       version=len(row["history"]) + 1, details=accepted, scope_version=p["scope_version"],
                       contract_version=p.get("contract_version"), accepted_by=actor["email"].lower(), authority=authority)
            row["history"].append(deepcopy({k: v for k, v in row.items() if k != "history"}))
            self._proc_save(user, "capacity_recorded", "-", f"{pid} {contractor}: offered {offered}, committed with evidence {committed}; version {row['version']}")

    # ---- work orders
    def issue_work_order(self, user, pid, case_id, scope="", resident_bindings=None):
        self._need_manager(user, "issue a work order")
        with self._proc_operation(user, "issue", pid=pid) as actor:
            p = self._package(pid)
            c = self._case(case_id)
            contractor = c["contractor"]["name"]
            authority = self._contract_authority(actor, p, "issue", contractor)
            self._proc_context["authorities"].append((actor, deepcopy(p), "issue", contractor, authority))
            self.require_safety_clear(c)
            self.require_resident_clear(c, resident_bindings if resident_bindings is not None else [])
            self.require_building_clear(c, pid)
            if c["closed"]:
                raise ValueError("This case is closed.")
            if p["period_to"] < _today():
                raise ValueError("This package period has ended.")
            cap = self._evidenced_capacity(p, contractor, case_id)
            if self._committed_used(p, contractor) >= cap["committed"]:
                raise ValueError(f"{contractor} is at its evidenced committed capacity. Record more evidenced capacity first.")
            if any(w["case_id"] == case_id and w["package"] == pid and w["state"] in ACTIVE for w in self._proc()["work_orders"]):
                raise ValueError("This case already has a work order in this package.")
            wos = self._proc()["work_orders"]
            text = _clean(scope, 400) or p["scope"]
            w = dict(id=f"WO-{len(wos) + 1:04d}", package=pid, case_id=case_id, contractor=contractor, state=ISSUED,
                     versions=[],
                     appointments=[], history=[dict(at=_now(), by=user["name"], from_state=None, to_state=ISSUED, note="")], corrections=[])
            wos.append(w)
            self._new_version(w, user, text, "First issue", resident_bindings, authority)
            self._proc_save(user, "workorder_issued", case_id, f"{w['id']} to {contractor} in {pid}, version 1")
            return w["id"]

    def _new_version(self, w, user, scope, reason, resident_bindings, authority=None):
        p = self._package(w["package"])
        authority = authority or self._proc_context["authority"]
        cap = p["capacity"].get(w["contractor"], {})
        w["versions"].append(dict(version=len(w["versions"]) + 1, scope=_clean(scope, 400) or w["versions"][-1]["scope"],
                                  scope_version=p["scope_version"], resident_bindings=deepcopy(resident_bindings), issued_by=user["name"],
                                  issuer_email=user["email"], authority=deepcopy(authority), contract_ref=p["contract_ref"],
                                  contract_version=p.get("contract_version"), capacity_version=cap.get("version"),
                                  state=w["state"], appointments=deepcopy(w["appointments"]), issued_at=_now(), reason=reason))

    def _existing_capacity(self, w, when=None):
        p = self._package(w["package"])
        return self._evidenced_capacity(p, w["contractor"], w["case_id"], when)

    def reissue_work_order(self, user, wid, scope, reason, resident_bindings=None):
        self._need_manager(user, "change a work order")
        reason = _clean(reason)
        if not reason:
            raise ValueError("Say why the work order is changing.")
        with self._proc_operation(user, "reissue", wid=wid):
            w = self._work_order(wid)
            if w["state"] not in (ISSUED, APPOINTED):
                raise ValueError(f"This work order is '{w['state']}' and cannot be changed.")
            self.require_safety_clear(self.cases[w["case_id"]])
            self.require_resident_clear(self.cases[w["case_id"]], resident_bindings if resident_bindings is not None else [])
            self.require_building_clear(self.cases[w["case_id"]], w["package"])
            self._existing_capacity(w)
            self._new_version(w, user, scope, reason, resident_bindings)
            self._proc_save(user, "workorder_reissued", w["case_id"], f"{wid} version {len(w['versions'])}: {reason}")

    def record_wo_appointment(self, user, wid, outcome, when=""):
        self._need_manager(user, "record an appointment outcome")
        if outcome not in OUTCOMES:
            raise ValueError("Choose an outcome from the list.")
        when = _iso(when, "the appointment date") if outcome == "Booked" else _clean(when, 40)
        with self._proc_operation(user, "appointment", wid=wid):
            w = self._work_order(wid)
            if w["state"] not in (ISSUED, APPOINTED):
                raise ValueError(f"This work order is '{w['state']}'. Appointments can only be recorded while it is open.")
            if outcome == "Booked":
                self.require_appointment_commitment(w)
                if when != w["appointment_offer"]["date"]:
                    raise ValueError("Booked date must match the confirmed appointment offer.")
                self._existing_capacity(w, when)
                self.require_safety_clear(self.cases[w["case_id"]])
                self._resident_work_order_clear(w)
                self.require_building_clear(self.cases[w["case_id"]], w["package"])
                if w["state"] == ISSUED:
                    self._wo_move(w, APPOINTED, user, f"Booked {when}")
            elif w["state"] == APPOINTED:
                self._wo_move(w, ISSUED, user, outcome)
            if outcome != "Booked" and w.get("appointment_offer"):
                w["appointment_offer"]["ended"] = True
            w["appointments"].append(dict(outcome=outcome, date=when, by=user["name"], at=_now()))
            cur = w["versions"][-1]
            self._new_version(w, user, cur["scope"], f"Appointment: {outcome}", cur.get("resident_bindings"))
            self._proc_save(user, "workorder_appointment", w["case_id"], f"{wid}: {outcome} {when}".strip())

    def complete_work_order(self, user, wid, note=""):
        self._need_manager(user, "record completion")
        with self._proc_operation(user, "complete", wid=wid):
            w = self._work_order(wid)
            self.require_appointment_commitment(w)
            self._existing_capacity(w)
            self.require_safety_clear(self.cases[w["case_id"]])
            self._resident_work_order_clear(w)
            self._wo_move(w, COMPLETED, user, _clean(note))
            w.update(completed_by=user["name"], completed_at=_now())
            cur = w["versions"][-1]
            self._new_version(w, user, cur["scope"], f"Completion: {_clean(note)}", cur.get("resident_bindings"))
            self._proc_save(user, "workorder_completed", w["case_id"], f"{wid} {_clean(note)}".strip())

    def correct_work_order(self, user, wid, reason, scope="", resident_bindings=None):
        self._need_manager(user, "record a correction")
        reason = _clean(reason)
        if not reason:
            raise ValueError("Say what needs correcting.")
        with self._proc_operation(user, "correct", wid=wid):
            w = self._work_order(wid)
            self._existing_capacity(w)
            self.require_safety_clear(self.cases[w["case_id"]])
            self.require_resident_clear(self.cases[w["case_id"]], resident_bindings if resident_bindings is not None else [])
            self.require_building_clear(self.cases[w["case_id"]], w["package"])
            self._wo_move(w, ISSUED, user, f"Correction: {reason}")
            self._new_version(w, user, scope, f"Correction: {reason}", resident_bindings)
            w["corrections"].append(dict(reason=reason, by=user["name"], at=_now()))
            self._proc_save(user, "workorder_corrected", w["case_id"], f"{wid} version {len(w['versions'])}: {reason}")

    def withdraw_work_order(self, user, wid, reason):
        self._need_manager(user, "withdraw a work order")
        reason = _clean(reason)
        if not reason:
            raise ValueError("Say why the work order is withdrawn.")
        with self._proc_operation(user, "withdraw", wid=wid):
            w = self._work_order(wid)
            self._wo_move(w, WITHDRAWN, user, reason)
            cur = w["versions"][-1]
            self._new_version(w, user, cur["scope"], f"Withdraw and release allocation: {reason}", cur.get("resident_bindings"))
            self._proc_save(user, "workorder_withdrawn", w["case_id"], f"{wid}: {reason}")

    # ---- views
    def _resident_work_order_clear(self, w):
        p = self._package(w["package"])
        if w["versions"][-1]["scope_version"] != p["scope_version"]:
            raise ValueError("The package scope changed. Reissue with current resident scope bindings.")
        self.require_resident_clear(self.cases[w["case_id"]], w["versions"][-1].get("resident_bindings", []))

    def _wo_view(self, w, c, user):
        contractor_view = projection.is_contractor(user)
        cur = w["versions"][-1]
        bindings = cur.get("resident_bindings") or []
        out = dict(id=w["id"], package=w["package"], case_id=w["case_id"], address=c["home"]["address"], postcode=c["home"]["postcode"],
                   measures=", ".join(b["measure"] for b in bindings) if bindings else "Unknown (resident scope confirmation needed)",
                   needs_notice=projection.needs_notice(c), named_contact=c["owner"], state=w["state"],
                   version=cur["version"], scope=cur["scope"],
                   appointment_control=self.appointment_summary(w, user),
                   appointments=[{k: a[k] for k in ("outcome", "date")} for a in w["appointments"]])
        if not contractor_view:
            out.update(contractor=w["contractor"], issued_by=cur["issued_by"], issued_at=cur["issued_at"], versions=w["versions"],
                       corrections=w["corrections"], history=w["history"])
        return deepcopy(out)

    def _work_order_reader(self, user):
        if projection.is_contractor(user):
            actor = self.staff.get(user.get("email", "").lower())
            if hasattr(self, "db"):
                row = self.db.execute("SELECT body FROM staff WHERE email=?", (user.get("email", "").lower(),)).fetchone()
                actor = json.loads(row[0]) if row else None
            if not actor or any(actor.get(k) != user.get(k) for k in ("email", "code", "name", "role", "contractor", "oid")):
                raise PermissionError("Current registered contractor identity is required to read assigned orders.")
        else:
            _actor(self, user)

    def list_work_orders(self, user, case_id=None):
        with self.lock:
            contractor_view = projection.is_contractor(user)
            self._work_order_reader(user)
            out = []
            for w in self._proc()["work_orders"]:
                if contractor_view and w["contractor"] != user.get("contractor"):
                    continue
                if case_id and w["case_id"] != case_id:
                    continue
                c = self.cases.get(w["case_id"])
                if c:
                    out.append(self._wo_view(w, c, user))
            return out

    def list_packages(self, user):
        with self.lock:
            _actor(self, user)
            out = []
            for p in self._proc()["packages"]:
                cap = [dict(contractor=k, offered=v["offered"], committed=v["committed"], evidence=v["evidence"], recorded_by=v["by"], recorded_at=v["at"],
                            in_use=self._committed_used(p, k), headroom=v["committed"] - self._committed_used(p, k),
                            unevidenced=v["offered"] - v["committed"]) for k, v in sorted(p["capacity"].items())]
                for item in cap:
                    source = p["capacity"][item["contractor"]]
                    item.update(version=source.get("version"), details=deepcopy(source.get("details")),
                                scope_version=source.get("scope_version"), accepted_by=source.get("accepted_by"))
                    try:
                        covered = (source.get("details") or {}).get("case_ids") or [None]
                        self._evidenced_capacity(p, item["contractor"], covered[0])
                        item.update(evidence_status="Evidenced commitment; rechecked before confirmation", usable_committed=source["committed"])
                    except (ValueError, PermissionError, DocumentStoreError) as error:
                        item.update(evidence_status=f"Unknown - not confirmed: {error}", usable_committed=0)
                out.append(dict(id=p["id"], name=p["name"], period_from=p["period_from"], period_to=p["period_to"], contract_ref=p["contract_ref"], contract_version=p.get("contract_version"),
                                scope=p["scope"], scope_version=p["scope_version"], scope_history=p["scope_history"], capacity=cap,
                                consultation_status="unknown", consultation_authority="Unverified",
                                consultation_history=p.get("consultation_history", [])))
            return deepcopy(out)

    def require_booked_capacity(self, c):
        orders = [w for w in self._proc()["work_orders"] if w["case_id"] == c["id"] and w["state"] in ACTIVE]
        if len(orders) != 1 or orders[0]["state"] != APPOINTED:
            raise ValueError("A single evidenced work order with a confirmed appointment is required. Ask the contract manager to issue and book it.")
        w = orders[0]
        self.require_appointment_commitment(w)
        when = w["appointment_offer"]["date"]
        cur = w["versions"][-1]
        actor = self.staff.get(cur.get("issuer_email", ""))
        if hasattr(self, "db"):
            row = self.db.execute("SELECT body FROM staff WHERE email=?", (cur.get("issuer_email"),)).fetchone()
            actor = json.loads(row[0]) if row else None
        if not actor or actor.get("role") not in MANAGER_ROLES:
            raise PermissionError("The booked order needs a current named contract issuer.")
        staff_confirmation = w["appointment_offer"]["confirmations"]["staff"]
        actor = staff_confirmation["actor"]
        if self._contract_authority(actor, self._package(w["package"]), "appointment", w["contractor"]) != staff_confirmation["authority"]:
            raise PermissionError("Booked order authority changed. Ask the contract manager to confirm again.")
        if hasattr(self, "local"):
            context = dict(user=deepcopy(actor), actor=deepcopy(actor), cases={},
                           snapshot=self._proc_snap.get("procurement"),
                           authorities=[(deepcopy(actor), deepcopy(self._package(w["package"])), "appointment", w["contractor"], staff_confirmation["authority"])])
            self.local.procurement_validation = context
            self._proc_context = context
        try:
            self.require_appointment_commitment(w)
            self._existing_capacity(w, when)
            self._resident_work_order_clear(w)
        finally:
            self._proc_context = None
