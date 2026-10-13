"""SYNTHETIC DATA ONLY. Flow handlers, part B: resident decision, funding,
release gates, block synchronisation, installation, QA, evidence, handover,
aftercare and grant claims."""
from datetime import date, timedelta

from zf_model import (P, SNAP, RULE_V2_FROM, RLO03_LEFT, add_wd, closure_sweep_on_or_after,
                      last_wd_of_month, lognorm, make_household, pick, quarter_end)


class FlowB:
    def start_decision(self, c, d):
        if "void_done" not in c.flags and self.rng.random() < P["void_rate"]:
            return self.go_void(c, d)
        if "pause_done" not in c.flags and self.rng.random() < P["resident_pause_rate"]:
            c.flags.add("pause_done")
            self.ev(c, d, "RESIDENT_PAUSE_REQUESTED", "CRM", self.rlo(c, d),
                    reason=self.rng.choice(["Family circumstances", "Health", "Christmas and new year period"]))
            self.set_state(c, d, "Resident pause", "RESIDENT_PAUSE")
            return self.at(add_wd(d, lognorm(self.rng, 35, 0.4, 10)), c, "h_resume_decision")
        self.start_contact(c, d, "decision")

    def h_resume_decision(self, c, d):
        self.ev(c, d, "RESIDENT_PAUSE_ENDED", "CRM", self.rlo(c, d))
        self.start_contact(c, d, "decision")

    def go_void(self, c, d):
        c.flags.update({"void_done", "void_window_missed"})
        c.token += 1
        c.dates.pop("decision", None)
        c.dates.pop("funding", None)
        self.ev(c, d, "PROPERTY_VOID", "HOUSING_MGMT", "Housing management")
        self.set_state(c, d, "Void", "VOID_RELET")
        self.at(add_wd(d, lognorm(self.rng, 28, 0.3, 12)), c, "h_relet")

    def h_relet(self, c, d):
        self.hh_seq += 1
        c.hh = make_household(self.rng, self.hh_seq)
        c.gate = {k: v for k, v in c.gate.items() if not isinstance(k, tuple)}
        self.ev(c, d, "PROPERTY_RELET", "HOUSING_MGMT", "Housing management", notes="New tenancy")
        self.start_contact(c, d, "decision")

    def h_decision(self, c, d):
        r = self.rng.random()
        if r < 0.06:
            c.flags.add("genuine_decline")
            return self.exit(c, d, "Withdrawn", "Resident declined works")
        if r < 0.11 and "variation" not in c.flags:
            c.flags.add("variation")
            self.ev(c, d, "DESIGN_VARIATION_REQUESTED", "CRM", self.rlo(c, d),
                    reason=self.rng.choice(["Ventilation fan location", "Heat pump unit position",
                                            "Loss of kitchen space for cylinder", "Render colour"]))
            self.set_state(c, d, "Design rework", "DESIGN_RETURN")
            return self.at(add_wd(d, lognorm(self.rng, 8, 0.4, 3)), c, "h_design_submit")
        self.ev(c, d, "RESIDENT_WORKS_DECISION", "CRM", self.rlo(c, d), outcome="Accepted",
                notes="Measure-specific decision recorded", evidence_version="WD-v1")
        c.dates["decision"] = d
        self.set_state(c, d, "Funding check", "FUNDING_CHECK")
        self.at(add_wd(d, lognorm(self.rng, 4, 0.4, 1)), c, "h_funding")

    def h_funding(self, c, d):
        if not c.funding_route:
            ok = c.prop.tenure != "Shared ownership" and self.rng.random() < 0.88
            c.funding_route = "WH:SHF Wave 3" if ok else "Internal capital"
        if d.month in (3, 6, 9, 12) and self.rng.random() < 0.12:
            c.flags.add("budget_profile_hold")
            self.ev(c, d, "FUNDING_HELD", "GRANT_TRACKER", "GEO-01", reason="Quarterly budget profile fully committed")
            self.set_state(c, d, "Funding decision", "FUNDING_DECISION")
            nq = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
            return self.at(add_wd(nq, self.rng.randint(3, 12)), c, "h_funding_confirm")
        self.h_funding_confirm(c, d)

    def h_funding_confirm(self, c, d):
        self.ev(c, d, "FUNDING_CONFIRMED", "GRANT_TRACKER", "GEO-01", outcome=c.funding_route)
        c.dates["funding"] = d
        self.check_release(c, d)

    # release gate ------------------------------------------------------------------
    def hold_active(self, c, d):
        h = c.hold
        return bool(h and h["placed"] <= d and (h["released"] is None or h["released"] > d))

    def check_release(self, c, d):
        if "funding" not in c.dates:
            return
        if self.hold_active(c, d):
            cat = "SAFETY_HOLD_STALE" if c.hold["repair"] <= d else "SAFETY_HOLD_ACTIVE"
            return self.set_state(c, d, "Awaiting release gate", cat)
        if c.prop.archetype == "ARC-03":
            c.flags.add("block_ready")
            b = c.prop.building
            b.first_ready = b.first_ready or d
            self.set_state(c, d, "Awaiting release gate", "LEASE_BLOCK_SYNC")
            return self.check_block(b, d)
        if "void_done" not in c.flags and self.rng.random() < P["void_rate"] / 2:
            return self.go_void(c, d)
        self.release(c, d)

    def check_block(self, b, d, force=False):
        if b.released:
            return
        flats = [self.by_prop[f.property_id] for f in b.flats if f.property_id in self.by_prop]
        live = [c for c in flats if not c.closed and "block_left_behind" not in c.flags and c.identified <= d]
        ready = [c for c in live if "block_ready" in c.flags]
        pending = [c for c in live if "block_ready" not in c.flags]
        not_yet = [c for c in flats if c.identified > d]
        if not ready or (b.lease_done and b.lease_done > d) or not_yet:
            return
        if pending and not force:
            return
        for c in pending:
            c.flags.add("block_left_behind")
            c.token += 1
            self.ev(c, d, "BLOCK_PROCEEDED_WITHOUT", "TRACKER", "PM-01",
                    notes=f"{b.building_id} released without this flat")
            self.set_state(c, d, "On hold - missed block programme", "LEASE_BLOCK_SYNC")
        b.released = True
        for c in ready:
            self.ev(c, d, "WORK_ORDER_ISSUED", "TRACKER", "PM-01", "Retrofit programme", c.supplier,
                    notes=f"Block job {b.building_id}")
            c.dates["work_order"] = d
            self.work_orders.append((d, c.cid, c.supplier))
            self.set_state(c, d, "Supplier queue", "SUPPLIER_CAPACITY")
        lead = ready[0]
        self.servers[lead.supplier].request(d, lead, "h_install_served", 1, 0.5 * len(ready),
                                            members=[c.cid for c in ready])

    def daily(self, d):
        if d == RULE_V2_FROM:
            self.resequence(d)
        for b in self.block_list:
            if b.released or b.first_ready is None:
                continue
            if b.lease_done and b.lease_done > d:
                continue
            self.check_block(b, d, force=(d - b.first_ready).days > 150)
        if d == quarter_end(d):
            self.make_claim(d)

    def release(self, c, d):
        self.ev(c, d, "WORK_ORDER_ISSUED", "TRACKER", "PM-01", "Retrofit programme", c.supplier)
        c.dates["work_order"] = d
        self.work_orders.append((d, c.cid, c.supplier))
        self.set_state(c, d, "Supplier queue", "SUPPLIER_CAPACITY")
        self.servers[c.supplier].request(d, c, "h_install_served", 1)

    # installation --------------------------------------------------------------------
    def install_days(self, c, block=False):
        m = c.measures.lower()
        if block:
            dur = lognorm(self.rng, 35, 0.25, 20)
        elif "external wall" in m:
            dur = lognorm(self.rng, 15, 0.3, 8)
        elif "internal wall" in m:
            dur = lognorm(self.rng, 7, 0.3, 4)
        elif "heat pump" in m:
            dur = lognorm(self.rng, 4, 0.3, 2)
        elif "boiler" in m:
            dur = self.rng.randint(2, 3)
        else:
            dur = self.rng.randint(1, 3)
        return dur

    def h_install_served(self, c, d, members=None):
        adate = add_wd(d, self.rng.randint(5, 12))
        if members:
            dur = self.install_days(c, block=True)
            if adate.month in (11, 12, 1, 2):
                dur += self.rng.randint(5, 20)
            for cid in members:
                mc = self.by_cid[cid]
                if mc.closed:
                    continue
                self.set_state(mc, d, "Install booked", "SUPPLIER_CAPACITY")
                self.at(adate, mc, "h_install_start", dur=dur)
            return
        ai = self.appt_row(c, c.supplier, "Installation", d, adate,
                           "All day" if "wall" in c.measures.lower() else self.rng.choice(["AM", "PM", "All day"]))
        self.set_state(c, d, "Install booked", "SUPPLIER_CAPACITY")
        self.at(adate, c, "h_install_visit", ai=ai)

    def h_install_visit(self, c, d, ai):
        a = c.appts[ai]
        if self.rng.random() < 0.015:
            a["outcome"], a["note"] = "REF", "Resident refused entry - does not want works now"
            c.n["ref"] += 1
            c.flags.add("genuine_refusal_at_install")
            return self.exit(c, d, "Withdrawn", "Resident refused works at installation visit")
        if self.rng.random() < self.na_prob(c, install=True):
            c.n["na"] += 1
            note = self.rng.choice(["No answer, card left", "Nobody home at 08:15", "No access, card through door"])
            if a["slot"] != "AM" and note.startswith("Nobody home"):
                note = "Nobody home at 13:30"
            if self.rng.random() < P["ref_misuse_install"][c.supplier]:
                a["outcome"], a["note"] = "REF", note
                c.n["ref"] += 1
                c.flags.add("misrecorded_refusal")
                # Jobs returned by the contractor as refused are closed unless the liaison officer challenges.
                if c.n["ref"] >= 1:
                    if self.rng.random() < P["reinstate_after_ref"]:
                        self.ev(c, d, "WITHDRAWAL_CHALLENGED", "CRM", self.rlo(c, d),
                                notes="Resident says nobody called ahead")
                        self.set_state(c, d, "Contact paused", "RES_ACCESS")
                        return self.at(d + timedelta(days=self.rng.randint(15, 40)), c, "h_rebook_install")
                    c.flags.add("withdrawn_on_misrecorded_refusal")
                    return self.exit(c, d, "Withdrawn", "Resident refused access - job returned by contractor")
            else:
                a["outcome"], a["note"] = "NA", note
            return self.start_contact(c, d, "rebook_install")
        a["outcome"], a["note"] = "ATT", "Operatives on site"
        self.h_install_start(c, d)

    def h_rebook_install(self, c, d):
        self.start_contact(c, d, "rebook_install")

    def h_install_start(self, c, d, dur=None):
        m = c.measures.lower()
        if c.pm_undetected and dur is None and ("loft" in m or "external wall" in m) and self.rng.random() < 0.7:
            c.pm_undetected = False
            c.flags.add("pm_found_on_site")
            self.ev(c, d, "INSTALL_ABORTED", "CONTRACTOR_PORTAL", c.supplier,
                    reason="Roof condition requires renewal before loft works" if "loft" in m
                    else "Windows due for renewal before external wall insulation")
            self.set_state(c, d, "PM dependency hold", "PM_DEPENDENCY")
            c.dates.pop("work_order", None)
            c.dates.pop("decision", None)
            c.dates.pop("funding", None)
            return self.at(d + timedelta(days=lognorm(self.rng, 110, 0.4, 40)), c, "h_pm_cleared")
        c.dates["install_start"] = d
        self.install_starts.append((d, c.cid, c.supplier))
        self.ev(c, d, "INSTALL_STARTED", "CONTRACTOR_PORTAL", c.supplier)
        self.set_state(c, d, "On site", "INSTALL_WORK")
        if dur is None:
            dur = self.install_days(c)
            if "external wall" in m and d.month in (11, 12, 1, 2):
                dur += self.rng.randint(5, 20)
                c.flags.add("weather_delay")
        self.at(add_wd(d, dur), c, "h_install_complete")

    def h_install_complete(self, c, d):
        c.dates["install_complete"] = d
        self.install_completes.append((d, c.cid, c.supplier))
        self.ev(c, d, "INSTALL_COMPLETE", "CONTRACTOR_PORTAL", c.supplier, outcome="Practical completion claimed")
        self.set_state(c, d, "Awaiting QA and evidence", "QA_QUEUE")
        self.servers["QA"].request(d, c, "h_qa_served", 1)
        self.at(self.evidence_date(c, d), c, "h_evidence_submit")

    def evidence_date(self, c, d):
        if c.supplier == "SUP-F2":
            me = last_wd_of_month(d)
            if (me - d).days < 4:
                me = last_wd_of_month(me + timedelta(days=7))
            return add_wd(me, self.rng.randint(0, 3))
        return add_wd(d, self.rng.randint(3, 10))

    def refresh_post(self, c, d):
        if c.state not in ("Awaiting QA and evidence",):
            return
        if "qa_pass" not in c.dates:
            cat = "QA_DEFECT" if c.gate.get("remediating") else "QA_QUEUE"
        elif "evidence_accepted" not in c.dates:
            cat = "EVIDENCE_REJECTION" if c.n["ev_reject"] else "EVIDENCE_SUBMISSION"
        else:
            return
        if cat != c.cat:
            self.set_state(c, d, c.state, cat)

    def h_qa_served(self, c, d):
        self.at(add_wd(d, self.rng.randint(1, 5)), c, "h_qa_inspect")

    def h_qa_inspect(self, c, d):
        first = c.n["qa_fail"] == 0 and not c.gate.get("qa_seen")
        c.gate["qa_seen"] = True
        pf = {"SUP-F2": 0.22, "SUP-HP": 0.16}.get(c.supplier, 0.10) if first else 0.10
        r = self.rng.random()
        attempt = sum(1 for q in c.quality if q["type"] == "QA inspection") + 1
        if r < pf:
            c.n["qa_fail"] += 1
            n = self.rng.randint(1, 5)
            sev = pick(self.rng, [("Minor", 0.35), ("Major", 0.55), ("Safety-critical", 0.10)])
            reason = self.rng.choice(["Air-sealing incomplete at junctions", "Ventilation undercut missing",
                                      "Render bead detail not to design", "Heat pump controls not commissioned",
                                      "Loft hatch not insulated", "Trickle vents not fitted"])
            c.quality.append(dict(type="QA inspection", date=d, attempt=attempt, result="Fail", defects=n,
                                  severity=sev, reason=reason, reviewer="QA-01"))
            self.ev(c, d, "QA_FAILED", "QA_LOG", "QA-01", reason=reason, outcome=sev)
            c.gate["remediating"] = True
            self.refresh_post(c, d)
            return self.at(add_wd(d, lognorm(self.rng, 14, 0.4, 5)), c, "h_remediation_done")
        res = "Pass with snags" if r < pf + 0.18 else "Pass"
        c.quality.append(dict(type="QA inspection", date=d, attempt=attempt, result=res,
                              defects=self.rng.randint(1, 3) if res != "Pass" else 0,
                              severity="Minor" if res != "Pass" else "", reason="", reviewer="QA-01"))
        self.ev(c, d, "QA_PASSED", "QA_LOG", "QA-01", outcome=res)
        c.dates["qa_pass"] = d
        c.gate.pop("remediating", None)
        self.check_accept(c, d)

    def h_remediation_done(self, c, d):
        self.ev(c, d, "REMEDIATION_COMPLETE", "CONTRACTOR_PORTAL", c.supplier)
        self.servers["QA"].request(d, c, "h_qa_served", 0)

    def h_evidence_submit(self, c, d):
        c.n["ev_version"] += 1
        v = f"EP-v{c.n['ev_version']}"
        c.quality.append(dict(type="Evidence submission", date=d, attempt=c.n["ev_version"], result="Submitted",
                              defects="", severity="", reason="", reviewer=c.supplier))
        self.ev(c, d, "EVIDENCE_SUBMITTED", "EVIDENCE_LOG", c.supplier, c.supplier, "Grants and evidence",
                evidence_version=v)
        self.servers["GEO"].request(d, c, "h_evidence_review", 1)

    def h_evidence_review(self, c, d):
        f2 = c.supplier == "SUP-F2"
        first = c.n["ev_version"] == 1
        p = (P["f2_evidence_reject_first"] if first else P["f2_evidence_reject_later"]) if f2 else \
            (P["other_evidence_reject_first"] if first else P["other_evidence_reject_later"])
        v = f"EP-v{c.n['ev_version']}"
        if self.rng.random() < p:
            c.n["ev_reject"] += 1
            reason = pick(self.rng, [("Missing pre-installation photographs", 0.28),
                                     ("Product certificate missing", 0.18),
                                     ("Ventilation commissioning sheet missing", 0.20),
                                     ("Address on certificate does not match", 0.12),
                                     ("Installer signature missing", 0.10),
                                     ("TrustMark lodgement not found", 0.12)])
            c.quality.append(dict(type="Evidence review", date=d, attempt=c.n["ev_version"], result="Rejected",
                                  defects="", severity="", reason=reason, reviewer="GEO-01"))
            self.ev(c, d, "EVIDENCE_REJECTED", "EVIDENCE_LOG", "GEO-01", "Grants and evidence", c.supplier,
                    reason=reason, evidence_version=v)
            self.refresh_post(c, d)
            nd = self.evidence_date(c, d) if f2 else add_wd(d, lognorm(self.rng, 8, 0.4, 3))
            return self.at(nd, c, "h_evidence_submit")
        c.quality.append(dict(type="Evidence review", date=d, attempt=c.n["ev_version"], result="Accepted",
                              defects="", severity="", reason="", reviewer="GEO-01"))
        self.ev(c, d, "EVIDENCE_ACCEPTED", "EVIDENCE_LOG", "GEO-01", outcome="Documentary acceptance",
                evidence_version=v)
        c.dates["evidence_accepted"] = d
        self.check_accept(c, d)

    def check_accept(self, c, d):
        if "qa_pass" in c.dates and "evidence_accepted" in c.dates:
            self.start_contact(c, d, "handover")
            self.set_state(c, d, "Awaiting resident handover", "HANDOVER_LAG")
        else:
            self.refresh_post(c, d)

    def h_resident_handover(self, c, d):
        self.contact_row(c, d, "handover", c.hh.channel, "Handover visit completed")
        self.ev(c, d, "RESIDENT_HANDOVER", "CRM", self.rlo(c, d), outcome="Handover pack issued and acknowledged")
        c.dates["handover"] = d
        self.set_state(c, d, "Awaiting closure", "ADMIN_CLOSURE")
        self.at(closure_sweep_on_or_after(d), c, "h_close")

    def h_close(self, c, d):
        c.dates["accepted"] = d
        self.exit(c, d, "Accepted handover", "All gates complete")
        if self.rng.random() < 0.07:
            self.at(d + timedelta(days=self.rng.randint(10, 120)), c, "h_aftercare")

    def h_aftercare(self, c, d):
        kind = pick(self.rng, [("Ventilation fan noise", 0.5), ("Heating controls not understood", 0.35),
                               ("Render crack", 0.15)])
        note = ""
        if kind == "Ventilation fan noise" and self.rng.random() < 0.3:
            c.flags.add("aftercare_hazard_signal")
            note = "Resident switched fan off; mentions condensation on bedroom window"
        c.flags.add("aftercare_reopen")
        c.closed = False
        c.token += 1
        self.contact_row(c, d, "aftercare", "Phone", "Inbound report", note=note or kind, direction="Inbound")
        self.ev(c, d, "AFTERCARE_REPORTED", "CRM", self.rlo(c, d), reason=kind, notes=note)
        self.ev(c, d, "CASE_REOPENED", "TRACKER", "PM-01", reason=kind)
        self.set_state(c, d, "Reopened - aftercare", "AFTERCARE")
        self.at(add_wd(d, lognorm(self.rng, 18, 0.5, 5)), c, "h_aftercare_fixed")

    def h_aftercare_fixed(self, c, d):
        self.ev(c, d, "REMEDIATION_COMPLETE", "CONTRACTOR_PORTAL", c.supplier, notes="Aftercare")
        self.set_state(c, d, "Awaiting closure", "ADMIN_CLOSURE")
        self.at(closure_sweep_on_or_after(d), c, "h_reclose")

    def h_reclose(self, c, d):
        self.ev(c, d, "CASE_RECLOSED", "TRACKER", "PM-01")
        self.set_state(c, d, "Accepted handover", "EXIT")
        c.segments.append(("EXIT", d, d, "Accepted handover", "closed"))
        c.closed = True
        c.token += 1

    # grant claims -----------------------------------------------------------------------
    def make_claim(self, qe):
        sub = add_wd(qe, 10)
        q = f"{qe.year}-Q{(qe.month - 1) // 3 + 1}"
        for c in self.cands:
            if c.funding_route != "WH:SHF Wave 3" or c.gate.get("claimed"):
                continue
            ea = c.dates.get("evidence_accepted")
            if not ea or ea > qe:
                continue
            rejected = self.rng.random() < 0.04 and not c.gate.get("claim_rejected")
            received = sub + timedelta(days=self.rng.randint(30, 60))
            self.claims.append(dict(cid=c.cid, quarter=q, submitted=sub,
                                    received=None if rejected else received,
                                    status="Rejected by funder" if rejected else "Received",
                                    reason="Address on certificate does not match funder record" if rejected else ""))
            if rejected:
                c.gate["claim_rejected"] = True
            else:
                c.gate["claimed"] = True
                c.dates["claim_submitted"] = sub
                c.dates["claim_received"] = received
