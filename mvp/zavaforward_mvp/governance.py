"""Frozen protocol, benefits register, phase release decisions and guardrail pauses (RULE-019, RULE-020, RULE-024; issue #126).

This records what named people decide. It never decides, signs or releases for
anyone, and an AI assistant has no part in it. Nothing here approves a protocol,
a DPIA, a lawful measurement basis or a release: each is a reference a qualified
person supplies. Fixtures that use it are labelled synthetic demonstration data.

* Protocol: a version is frozen with every required field, then approved by a
  different person with the OD-36 DPIA and lawful measurement-basis references.
  A change is a new version with a reason and needs a new approval.
* Capture gate: Phase 0 pilot or comparison event capture is open only while the
  latest protocol version is approved and the benefits register is approved.
* Benefits register: BG-011 event definitions and the minimum detectable effect
  (MDE). A target is never reported pass or fail when the MDE exceeds it.
* Release decisions: every phase and tranche has a recorded decision with
  requirements, evidence, unresolved issues and named approvers.
* Guardrail breach: pauses its scope until restart is authorised under the OD-35
  authority and a release decision for that scope. Emergency and statutory
  hazard response continues outside the pause.
"""
from . import controls as k

MANAGER_ROLES = ("Retrofit Programme Manager", "Programme Support Officer")
BREACH_ROLES = MANAGER_ROLES + ("Quality Inspector", "Building Safety Liaison")
PROTOCOL_FIELDS = (
    ("event_dictionary", "the event dictionary"), ("accepted_handover_definition", "the accepted-handover definition"),
    ("clock_pause_rules", "the clock and pause rules"), ("cohort_eligibility", "the cohort eligibility"),
    ("entry_cutoff", "the entry cut-off"), ("denominators", "the denominators"),
    ("matching_variables", "the matching variables"), ("primary_measures", "the primary measures"),
    ("mde", "the minimum detectable effect"), ("thresholds", "the thresholds"),
    ("unfinished_case_handling", "the unfinished-case handling"), ("exclusions", "the exclusions"),
    ("analysis_code_version", "the analysis code version"),
)
BG011_FIELDS = (
    ("population_denominator", "the accepted-home population and denominator"), ("start_event", "the start event"),
    ("stop_event", "the stop event"), ("elapsed_statistic", "the elapsed-time statistic"),
    ("comparable_cohort", "the comparable baseline and cohort"), ("measurement_window", "the measurement window"),
    ("pause_rules", "the rules for pauses, incomplete cases, withdrawals and exclusions"),
    ("effort_roles_tasks", "the coordination-hour roles and tasks, including shifted effort and recording cost"),
)
BG011_TARGETS = dict(cycle_time=20.0, coordination_hours=25.0)
PHASES = ("Phase 0 capture", "Shadow testing", "Live pilot")
DECISIONS = ("Release", "Withhold")
SCOPE_KINDS = ("home", "work package", "archetype", "workstream")
EMERGENCY_NOTE = "Emergency and statutory hazard response continues outside any pause."


def target_verdict(target_pct, mde_pct, observed_pct=None):
    """Never a pass or fail when the MDE is missing or larger than the target."""
    if mde_pct is None:
        return dict(verdict="Not assessable", reason="The minimum detectable effect is not recorded.")
    if mde_pct > target_pct:
        return dict(verdict="Interval estimate only",
                    reason=f"The MDE ({mde_pct:g}%) exceeds the target ({target_pct:g}%), so report an interval estimate and caveat, not a pass or fail.")
    if observed_pct is None:
        return dict(verdict="Awaiting result", reason="The pilot can distinguish the target; no result is recorded.")
    return dict(verdict="Pass" if observed_pct >= target_pct else "Fail", reason="The MDE does not exceed the target.")


def _pct(value, label):
    try:
        n = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Enter {label} as a percentage.")
    if not 0 < n <= 100:
        raise ValueError(f"Enter {label} as a percentage above 0 and up to 100.")
    return n


def _need_manager(user, what):
    k.require_role(user, MANAGER_ROLES, f"a manager can {what}")


class GovernanceMixin:
    def _gov(self):
        g = self.data.setdefault("governance", {})
        g.setdefault("protocol_versions", [])
        g.setdefault("benefits", {})
        g.setdefault("releases", [])
        g.setdefault("breaches", [])
        return g

    @staticmethod
    def _next_id(prefix, items):
        return f"{prefix}-{len(items) + 1}"

    # ---- protocol and benefits register
    def protocol_freeze(self, user, body):
        k.refuse_bulk(body)
        _need_manager(user, "freeze a protocol version")
        fields = {key: k.text(body.get(key), label, 600) for key, label in PROTOCOL_FIELDS}
        with self.lock:
            g = self._gov()
            versions = g["protocol_versions"]
            reason = k.text(body.get("reason"), "why this version is needed", 300, required=bool(versions))
            v = dict(version=len(versions) + 1, fields=fields, reason=reason or "First version", frozen_by=user["email"], frozen_at=k.now(),
                     status="Frozen, awaiting approval", approval=None, synthetic=bool(body.get("synthetic")))
            versions.append(v)
            self.audit(user["email"], "protocol_freeze", "-", f"protocol version {v['version']} frozen")
            self.save()
            return v

    def protocol_approve(self, user, body):
        k.refuse_bulk(body)
        _need_manager(user, "approve a protocol version")
        with self.lock:
            versions = self._gov()["protocol_versions"]
            if not versions:
                raise ValueError("Freeze a protocol version first.")
            v = versions[-1]
            if body.get("version") not in (None, v["version"]):
                raise ValueError("Only the latest protocol version can be approved.")
            k.different_person(user, v["frozen_by"], "approve this protocol version")
            if v["approval"]:
                raise ValueError("This protocol version is already approved.")
            v["approval"] = dict(by=user["email"], at=k.now(), dpia_ref=k.text(body.get("dpia_ref"), "the approved OD-36 DPIA reference", 200),
                                 lawful_basis_ref=k.text(body.get("lawful_basis_ref"), "the lawful measurement-basis decision reference", 200))
            v["status"] = "Approved"
            self.audit(user["email"], "protocol_approve", "-", f"protocol version {v['version']} approved")
            self.save()
            return v

    def benefits_record(self, user, body):
        """BG-011 event definitions and the Phase 0 MDE; recording them does not approve them."""
        k.refuse_bulk(body)
        _need_manager(user, "record the benefits register")
        defs = {key: k.text(body.get(key), label, 600) for key, label in BG011_FIELDS}
        mde = dict(cycle_time=_pct(body.get("mde_cycle_time_pct"), "the cycle-time MDE"),
                   coordination_hours=_pct(body.get("mde_coordination_hours_pct"), "the coordination-hours MDE"))
        with self.lock:
            g = self._gov()
            entry = dict(goal="BG-011", definitions=defs, mde_pct=mde, targets_pct=dict(BG011_TARGETS), recorded_by=user["email"],
                         recorded_at=k.now(), status="Recorded, awaiting approval", approved_by=None, synthetic=bool(body.get("synthetic")))
            g["benefits"]["BG-011"] = entry
            self.audit(user["email"], "benefits_record", "-", "BG-011 definitions and MDE recorded")
            self.save()
            return entry

    def benefits_approve(self, user, body):
        k.refuse_bulk(body)
        _need_manager(user, "approve the benefits register")
        with self.lock:
            e = self._gov()["benefits"].get("BG-011")
            if not e:
                raise ValueError("Record the BG-011 definitions and MDE first.")
            k.different_person(user, e["recorded_by"], "approve the benefits register")
            e["approved_by"], e["approved_at"], e["status"] = user["email"], k.now(), "Approved"
            self.audit(user["email"], "benefits_approve", "-", "BG-011 register approved")
            self.save()
            return e

    def benefit_verdicts(self, observed=None):
        e = self._gov()["benefits"].get("BG-011")
        if not e:
            return {name: target_verdict(t, None) for name, t in BG011_TARGETS.items()}
        observed = observed or {}
        return {name: target_verdict(t, e["mde_pct"][name], observed.get(name)) for name, t in BG011_TARGETS.items()}

    def capture_gate(self):
        """Reasons Phase 0 capture is closed; empty only when protocol, DPIA, lawful basis and benefits register are approved."""
        g = self._gov()
        versions = g["protocol_versions"]
        why = []
        if not versions:
            why.append("No pilot protocol is frozen. Owner: programme manager. Next action: freeze version 1.")
        elif not versions[-1]["approval"]:
            why.append(f"Protocol version {versions[-1]['version']} is not approved with the DPIA and lawful measurement basis. Owner: programme manager.")
        e = g["benefits"].get("BG-011")
        if not e or e["status"] != "Approved":
            why.append("The benefits register (BG-011 definitions and MDE) is not approved. Owner: programme manager.")
        return why

    def require_capture_open(self):
        why = self.capture_gate()
        if why:
            raise PermissionError("Phase 0 capture is closed. " + " ".join(why))

    def guard_case_event(self, c):
        """Capture gate for pilot-cohort cases (c["pilot"]) and pause check for every case; hazard response is deliberately not routed here."""
        if c.get("pilot"):
            self.require_capture_open()
        home = c.get("home") or {}
        for kind, scope in (("home", c["id"]), ("home", home.get("address")), ("archetype", home.get("type"))):
            if scope:
                self.require_not_paused(kind, scope)

    # ---- release decisions
    def release_record(self, user, body):
        k.refuse_bulk(body)
        _need_manager(user, "record a release decision")
        scope_kind = body.get("scope_kind")
        if scope_kind not in ("phase", "tranche"):
            raise ValueError("Choose phase or tranche.")
        scope = k.text(body.get("scope"), "the phase or tranche", 120)
        if scope_kind == "phase" and scope not in PHASES:
            raise ValueError("Choose one of the delivery phases.")
        decision = body.get("decision")
        if decision not in DECISIONS:
            raise ValueError("Choose Release or Withhold.")
        approvers = [a.strip() for a in (body.get("approvers") or []) if isinstance(a, str) and a.strip()]
        if not approvers:
            raise ValueError("Name at least one approver.")
        rec = dict(scope_kind=scope_kind, scope=scope, decision=decision, requirements=k.text(body.get("requirements"), "the applicable requirements", 400),
                   evidence=k.text(body.get("evidence"), "the acceptance evidence", 600), unresolved=k.text(body.get("unresolved"), "the unresolved issues (or none)", 400),
                   envelope_ref=k.text(body.get("envelope_ref"), "the approved cost and risk envelope reference", 200), approvers=approvers,
                   recorded_by=user["email"], recorded_at=k.now(), synthetic=bool(body.get("synthetic")))
        if decision == "Release" and scope == "Phase 0 capture":
            self.require_capture_open()
        if decision == "Release" and scope in ("Shadow testing", "Live pilot") and not self.is_released("Phase 0 capture"):
            raise PermissionError(f"{scope} cannot be released until Phase 0 capture is released. Owner: programme manager.")
        if decision == "Release" and scope == "Shadow testing":
            rec["shadow_entry_evidence"] = k.text(body.get("shadow_entry_evidence"), "the shadow-mode entry evidence", 400)
        with self.lock:
            rel = self._gov()["releases"]
            rec["id"] = self._next_id("REL", rel)
            rel.append(rec)
            self.audit(user["email"], "release_record", "-", f"{rec['id']} {decision} {scope}")
            self.save()
            return rec

    def is_released(self, scope):
        """The latest decision for the scope governs."""
        last = next((r for r in reversed(self._gov()["releases"]) if r["scope"] == scope), None)
        return bool(last and last["decision"] == "Release")

    def release_gaps(self):
        g = self._gov()
        recorded = {r["scope"] for r in g["releases"]}
        return [p for p in PHASES if p not in recorded]

    # ---- guardrail breach and restart
    def breach_record(self, user, body):
        k.refuse_bulk(body)
        k.require_role(user, BREACH_ROLES, "a manager, quality inspector or building safety liaison can record a guardrail breach")
        scope_kind = body.get("scope_kind")
        if scope_kind not in SCOPE_KINDS:
            raise ValueError("Choose home, work package, archetype or workstream.")
        rec = dict(scope_kind=scope_kind, scope=k.text(body.get("scope"), "the affected scope", 120),
                   owner=k.text(body.get("owner"), "the owner", 120), evidence=k.text(body.get("evidence"), "the evidence", 600),
                   containment=k.text(body.get("containment"), "the containment", 400),
                   resident_impact=k.text(body.get("resident_impact"), "the resident impact", 400),
                   remediation=k.text(body.get("remediation"), "the remediation", 400),
                   restart_authority=k.text(body.get("restart_authority"), "the restart authority (OD-35)", 200),
                   recorded_by=user["email"], recorded_at=k.now(), status="Paused", restart=None, synthetic=bool(body.get("synthetic")))
        with self.lock:
            br = self._gov()["breaches"]
            rec["id"] = self._next_id("BRE", br)
            br.append(rec)
            self.audit(user["email"], "breach_record", "-", f"{rec['id']} paused {scope_kind} {rec['scope']}")
            self.save()
            return rec

    def breach_restart(self, user, body):
        k.refuse_bulk(body)
        _need_manager(user, "authorise a restart")
        with self.lock:
            g = self._gov()
            b = next((x for x in g["breaches"] if x["id"] == body.get("id")), None)
            if not b:
                raise ValueError("Choose one of the breaches.")
            if b["status"] != "Paused":
                raise ValueError("This breach is not paused.")
            k.different_person(user, b["recorded_by"], "authorise the restart")
            rel = next((r for r in g["releases"] if r["id"] == body.get("release_id")), None)
            if not rel or rel["decision"] != "Release" or rel["recorded_at"] < b["recorded_at"]:
                raise PermissionError("Restart needs a Release decision recorded after the breach. Owner: programme manager.")
            b["restart"] = dict(by=user["email"], at=k.now(), release_id=rel["id"], authority_ref=k.text(body.get("authority_ref"), "the OD-35 authority reference", 200),
                                remediation_evidence=k.text(body.get("remediation_evidence"), "the accepted remediation evidence", 600))
            b["status"] = "Restart authorised"
            self.audit(user["email"], "breach_restart", "-", f"{b['id']} restart authorised")
            self.save()
            return b

    def paused_scopes(self):
        return [dict(id=b["id"], scope_kind=b["scope_kind"], scope=b["scope"]) for b in self._gov()["breaches"] if b["status"] == "Paused"]

    def is_paused(self, scope_kind, scope):
        return any(p["scope_kind"] == scope_kind and p["scope"] == scope for p in self.paused_scopes())

    def require_not_paused(self, scope_kind, scope):
        if self.is_paused(scope_kind, scope):
            raise PermissionError(f"This {scope_kind} is paused after a guardrail breach until restart is authorised. {EMERGENCY_NOTE}")

    def governance_view(self, user):
        _need_manager(user, "see the governance register")
        g = self._gov()
        return dict(protocol=g["protocol_versions"], benefits=g["benefits"], verdicts=self.benefit_verdicts(), releases=g["releases"],
                    release_gaps=self.release_gaps(), breaches=g["breaches"], paused=self.paused_scopes(),
                    capture_open=not self.capture_gate(), capture_blockers=self.capture_gate(), note=EMERGENCY_NOTE)
