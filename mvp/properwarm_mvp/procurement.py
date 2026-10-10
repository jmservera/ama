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
from datetime import date

from . import projection
from .workflows import MANAGER_ROLES, _now, _today

OUTCOMES = ("Booked", "Declined by provider", "Resident not available", "No access", "Rebooking needed")
ISSUED, APPOINTED, COMPLETED, WITHDRAWN = "Issued", "Appointed", "Completed", "Withdrawn"
ACTIVE = (ISSUED, APPOINTED, COMPLETED)
TRANSITIONS = {ISSUED: (APPOINTED, WITHDRAWN), APPOINTED: (COMPLETED, WITHDRAWN, ISSUED), COMPLETED: (ISSUED,), WITHDRAWN: ()}


def _clean(text, n=300):
    return (text or "").strip()[:n]


def _iso(value, what):
    try:
        return date.fromisoformat(str(value)).isoformat()
    except ValueError:
        raise ValueError(f"Enter {what} as a date such as 2026-04-01.")


def _count(value, what):
    try:
        n = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{what} must be a whole number.")
    if n < 0 or n > 100000:
        raise ValueError(f"{what} must be between 0 and 100000.")
    return n


class ProcurementMixin:
    def _proc(self):
        return self.data.setdefault("procurement", dict(packages=[], work_orders=[]))

    def _need_manager(self, user, what):
        if user["role"] not in MANAGER_ROLES:
            raise PermissionError(f"Only a manager can {what}.")

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

    def _invalidate_work_order_evidence(self, w, user, reason):
        c = self._case(w["case_id"])
        if not c.get("exercise"):
            return
        for rec in c.get("quality", []):
            if rec.get("work_order") == w["id"] and not rec.get("stale"):
                rec.update(stale=True, reassessment_reason=reason)
                rec["history"].append(dict(at=_now(), by=user["name"], from_state=rec["state"],
                                          to_state=rec["state"], note=f"Work-order evidence requires fresh review: {reason}"))
        state = c["exercise"]
        for ref, milestone in state.get("milestones", {}).items():
            if milestone["work_order"] == w["id"] and ref in (f"{w['id']}:installation", f"{w['id']}:handover"):
                state.setdefault("milestone_history", []).append(dict(reference=ref, **milestone))
                milestone.update(stale=True, reassessment_reason=reason)

    # ---- packages and capacity
    def create_package(self, user, name, period_from, period_to, scope, contract_ref):
        self._need_manager(user, "create a package")
        name, scope, contract_ref = _clean(name, 80), _clean(scope, 400), _clean(contract_ref, 60)
        if not name or not scope or not contract_ref:
            raise ValueError("Enter a package name, what it covers and the contract or call-off reference.")
        start, end = _iso(period_from, "the start"), _iso(period_to, "the end")
        if end < start:
            raise ValueError("The package cannot end before it starts.")
        with self.lock:
            proc = self._proc()
            p = dict(id=f"PKG-{len(proc['packages']) + 1:03d}", name=name, period_from=start, period_to=end, contract_ref=contract_ref,
                     scope=scope, scope_version=1, scope_history=[dict(version=1, scope=scope, by=user["name"], at=_now(), reason="First version")],
                     capacity={}, created_by=user["name"], created_at=_now())
            proc["packages"].append(p)
            self.audit(user["email"], "package_created", "-", f"{p['id']} {name} {start} to {end} ref {contract_ref}")
            self.save()
            return p["id"]

    def rescope_package(self, user, pid, scope, reason):
        self._need_manager(user, "change a package scope")
        scope, reason = _clean(scope, 400), _clean(reason)
        if not scope or not reason:
            raise ValueError("Enter the new scope and why it changed.")
        with self.lock:
            p = self._package(pid)
            p["scope_version"] += 1
            p["scope"] = scope
            p["scope_history"].append(dict(version=p["scope_version"], scope=scope, by=user["name"], at=_now(), reason=reason))
            for w in self._proc()["work_orders"]:
                if w["package"] == pid:
                    self._invalidate_work_order_evidence(w, user, f"Package scope changed: {reason}")
            self.audit(user["email"], "package_rescoped", "-", f"{pid} scope version {p['scope_version']}: {reason}")
            self.save()

    def set_capacity(self, user, pid, contractor, offered, committed, evidence=""):
        self._need_manager(user, "record capacity")
        contractor, evidence = _clean(contractor, 80), _clean(evidence, 300)
        offered, committed = _count(offered, "Offered capacity"), _count(committed, "Committed capacity")
        if contractor not in {c["contractor"]["name"] for c in self.cases.values()}:
            raise ValueError("Choose a contractor already working on a case.")
        if committed > offered:
            raise ValueError("Committed capacity cannot be more than was offered.")
        if committed and not evidence:
            raise ValueError("Committed capacity needs evidence, such as a signed commitment or a resource plan reference.")
        with self.lock:
            p = self._package(pid)
            if committed < self._committed_used(p, contractor):
                raise ValueError("Committed capacity cannot drop below the work orders already issued.")
            row = p["capacity"].setdefault(contractor, dict(history=[]))
            row.update(offered=offered, committed=committed, evidence=evidence, by=user["name"], at=_now())
            row["history"].append(dict(offered=offered, committed=committed, evidence=evidence, by=user["name"], at=row["at"]))
            self.audit(user["email"], "capacity_recorded", "-", f"{pid} {contractor}: offered {offered}, committed with evidence {committed}")
            self.save()

    # ---- work orders
    def issue_work_order(self, user, pid, case_id, scope=""):
        self._need_manager(user, "issue a work order")
        with self.lock:
            p = self._package(pid)
            c = self._case(case_id)
            if c.get("exercise"):
                from .store import GateError
                why = self.exercise_readiness(c)
                if c["exercise"]["lifecycle"] != "Ready":
                    why.append("Record the Ready lifecycle step before work release.")
                if why:
                    raise GateError(why)
            contractor = c["contractor"]["name"]
            if c["closed"]:
                raise ValueError("This case is closed.")
            if p["period_to"] < _today():
                raise ValueError("This package period has ended.")
            cap = p["capacity"].get(contractor)
            if not cap or not cap["committed"]:
                raise ValueError(f"{contractor} has no evidenced committed capacity in this package.")
            if c.get("exercise") and not self.exercise_current(cap.get("at"), 7):
                raise ValueError("Committed capacity needs a fresh human evidence review (7 day internal trigger).")
            if self._committed_used(p, contractor) >= cap["committed"]:
                raise ValueError(f"{contractor} is at its evidenced committed capacity. Record more evidenced capacity first.")
            if any(w["case_id"] == case_id and w["package"] == pid and w["state"] in ACTIVE for w in self._proc()["work_orders"]):
                raise ValueError("This case already has a work order in this package.")
            wos = self._proc()["work_orders"]
            text = _clean(scope, 400) or p["scope"]
            w = dict(id=f"WO-{len(wos) + 1:04d}", package=pid, case_id=case_id, contractor=contractor, state=ISSUED,
                     versions=[dict(version=1, scope=text, scope_version=p["scope_version"], issued_by=user["name"], issued_at=_now(), reason="First issue")],
                     appointments=[], history=[dict(at=_now(), by=user["name"], from_state=None, to_state=ISSUED, note="")], corrections=[])
            wos.append(w)
            self.audit(user["email"], "workorder_issued", case_id, f"{w['id']} to {contractor} in {pid}, version 1")
            self.save()
            return w["id"]

    def _new_version(self, w, user, scope, reason):
        p = self._package(w["package"])
        w["versions"].append(dict(version=len(w["versions"]) + 1, scope=_clean(scope, 400) or w["versions"][-1]["scope"],
                                  scope_version=p["scope_version"], issued_by=user["name"], issued_at=_now(), reason=reason))

    def reissue_work_order(self, user, wid, scope, reason):
        self._need_manager(user, "change a work order")
        reason = _clean(reason)
        if not reason:
            raise ValueError("Say why the work order is changing.")
        with self.lock:
            w = self._work_order(wid)
            if w["state"] not in (ISSUED, APPOINTED):
                raise ValueError(f"This work order is '{w['state']}' and cannot be changed.")
            if self._case(w["case_id"]).get("exercise"):
                raise PermissionError("Exercise scope changes require new design and resident choice; withdraw and reissue after review.")
            self._new_version(w, user, scope, reason)
            self.audit(user["email"], "workorder_reissued", w["case_id"], f"{wid} version {len(w['versions'])}: {reason}")
            self.save()

    def record_wo_appointment(self, user, wid, outcome, when=""):
        self._need_manager(user, "record an appointment outcome")
        if outcome not in OUTCOMES:
            raise ValueError("Choose an outcome from the list.")
        when = _iso(when, "the appointment date") if outcome == "Booked" else _clean(when, 40)
        with self.lock:
            w = self._work_order(wid)
            if w["state"] not in (ISSUED, APPOINTED):
                raise ValueError(f"This work order is '{w['state']}'. Appointments can only be recorded while it is open.")
            if outcome == "Booked":
                if w["state"] == ISSUED:
                    self._wo_move(w, APPOINTED, user, f"Booked {when}")
            elif w["state"] == APPOINTED:
                self._wo_move(w, ISSUED, user, outcome)
            w["appointments"].append(dict(outcome=outcome, date=when, by=user["name"], at=_now()))
            self.audit(user["email"], "workorder_appointment", w["case_id"], f"{wid}: {outcome} {when}".strip())
            self.save()

    def complete_work_order(self, user, wid, note=""):
        self._need_manager(user, "record completion")
        with self.lock:
            w = self._work_order(wid)
            if self._case(w["case_id"]).get("exercise"):
                from .store import GateError
                why = self.exercise_readiness(self._case(w["case_id"]))
                if w["versions"][-1]["scope_version"] != self._package(w["package"])["scope_version"]:
                    why.append("Package scope changed; obtain new design and resident review before release.")
                if why:
                    raise GateError(why)
            self._wo_move(w, COMPLETED, user, _clean(note))
            w.update(completed_by=user["name"], completed_at=_now())
            self.audit(user["email"], "workorder_completed", w["case_id"], f"{wid} {_clean(note)}".strip())
            self.save()

    def correct_work_order(self, user, wid, reason, scope=""):
        self._need_manager(user, "record a correction")
        reason = _clean(reason)
        if not reason:
            raise ValueError("Say what needs correcting.")
        with self.lock:
            w = self._work_order(wid)
            c = self._case(w["case_id"])
            if c.get("exercise"):
                if c["closed"]:
                    raise ValueError("Return the closed case to its owned review workflow before correcting the work order.")
                if ((scope and scope != w["versions"][-1]["scope"])
                        or w["versions"][-1]["scope_version"] != self._package(w["package"])["scope_version"]):
                    raise PermissionError("A changed exercise scope requires new independent design and resident choice.")
            self._wo_move(w, ISSUED, user, f"Correction: {reason}")
            self._new_version(w, user, scope, f"Correction: {reason}")
            w["corrections"].append(dict(reason=reason, by=user["name"], at=_now()))
            self._invalidate_work_order_evidence(w, user, reason)
            self.audit(user["email"], "workorder_corrected", w["case_id"], f"{wid} version {len(w['versions'])}: {reason}")
            self.save()

    def withdraw_work_order(self, user, wid, reason):
        self._need_manager(user, "withdraw a work order")
        reason = _clean(reason)
        if not reason:
            raise ValueError("Say why the work order is withdrawn.")
        with self.lock:
            w = self._work_order(wid)
            self._wo_move(w, WITHDRAWN, user, reason)
            self.audit(user["email"], "workorder_withdrawn", w["case_id"], f"{wid}: {reason}")
            self.save()

    # ---- views
    def _wo_view(self, w, c, contractor_view):
        cur = w["versions"][-1]
        out = dict(id=w["id"], package=w["package"], case_id=w["case_id"], address=c["home"]["address"], postcode=c["home"]["postcode"],
                   measures=c["measures"], needs_notice=projection.needs_notice(c), named_contact=c["owner"], state=w["state"],
                   version=cur["version"], scope=cur["scope"],
                   appointments=[{k: a[k] for k in ("outcome", "date")} for a in w["appointments"]])
        if not contractor_view:
            out.update(contractor=w["contractor"], issued_by=cur["issued_by"], issued_at=cur["issued_at"], versions=w["versions"],
                       corrections=w["corrections"], history=w["history"])
        return out

    def list_work_orders(self, user, case_id=None):
        with self.lock:
            contractor_view = projection.is_contractor(user)
            out = []
            for w in self._proc()["work_orders"]:
                if contractor_view and w["contractor"] != user.get("contractor"):
                    continue
                if case_id and w["case_id"] != case_id:
                    continue
                c = self.cases.get(w["case_id"])
                if c:
                    out.append(self._wo_view(w, c, contractor_view))
            return out

    def list_packages(self, user):
        with self.lock:
            out = []
            for p in self._proc()["packages"]:
                cap = [dict(contractor=k, offered=v["offered"], committed=v["committed"], evidence=v["evidence"], recorded_by=v["by"], recorded_at=v["at"],
                            in_use=self._committed_used(p, k), headroom=v["committed"] - self._committed_used(p, k),
                            unevidenced=v["offered"] - v["committed"]) for k, v in sorted(p["capacity"].items())]
                out.append(dict(id=p["id"], name=p["name"], period_from=p["period_from"], period_to=p["period_to"], contract_ref=p["contract_ref"],
                                scope=p["scope"], scope_version=p["scope_version"], scope_history=p["scope_history"], capacity=cap))
            return out
