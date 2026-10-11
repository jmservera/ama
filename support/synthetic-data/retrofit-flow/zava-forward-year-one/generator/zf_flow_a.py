"""SYNTHETIC DATA ONLY. Flow handlers, part A: identification, data checks,
resident contact, survey, assessment, hazards and design approval."""
from datetime import date, datetime, time, timedelta

from zf_model import (P, SNAP, RULE_V2_FROM, RLO03_LEFT, RC02_LEAVE, RC03_START,
                      add_wd, lognorm, pick)

FORMAT_ADJ = ("Large print", "Interpreter", "BSL", "Communication support")
RLO_BY_LOC = {"LA": "RLO-01", "LB": "RLO-02", "LC": "RLO-03"}


class FlowA:
    # helpers ---------------------------------------------------------------
    def rlo(self, c, d):
        base = RLO_BY_LOC[c.prop.locality]
        if base == "RLO-03" and d >= RLO03_LEFT:
            return "RLO-02"
        return base

    def contact_row(self, c, d, purpose, channel, outcome, note="", direction="Outbound"):
        hh = c.hh
        adj_met = ""
        if hh.adjustment_recorded:
            adj_met = "Y" if (purpose, "fmt") in c.gate else "N"
        c.contacts.append(dict(
            dt=datetime.combine(d, time(self.rng.randint(8, 17), self.rng.choice([0, 10, 20, 30, 40, 50]))),
            purpose=purpose, channel=channel, direction=direction, outcome=outcome,
            staff=self.rlo(c, d), note=note, adj_recorded=hh.adjustment if hh.adjustment_recorded else "",
            adj_met=adj_met))

    def appt_row(self, c, supplier, atype, booked, adate, slot):
        c.appts.append(dict(supplier=supplier, type=atype, booked=booked, date=adate, slot=slot,
                            outcome="", note=""))
        return len(c.appts) - 1

    # identification ----------------------------------------------------------
    def h_identified(self, c, d):
        self.set_state(c, d, "Identified", "DATA_CHECK")
        self.ev(c, d, "CANDIDATE_IDENTIFIED", "ASSET_EXTRACT", "PS-01", reason=c.rule,
                notes=f"{c.wave}; priority score {c.score}")
        lag = lognorm(self.rng, 9 if c.wave.startswith("Wave") else 4, 0.5, 1, 40)
        self.at(add_wd(d, lag), c, "h_data_check")

    def h_data_check(self, c, d):
        self.ev(c, d, "DATA_CHECK_COMPLETE", "TRACKER", "PS-01")
        if c.prop.sold and self.rng.random() < 0.7:
            c.flags.add("sold_found_at_data_check")
            return self.exit(c, d, "Excluded", "Sold under right to buy - found at data check")
        if c.prop.tenure == "Shared ownership":
            self.set_state(c, d, "Lease review", "LEASE_REVIEW")
            self.ev(c, d, "LEASE_REVIEW_REQUESTED", "TRACKER", "PM-01", "Retrofit programme", "Legal")
            return self.at(add_wd(d, lognorm(self.rng, 35, 0.4, 10)), c, "h_lease_review_done")
        self.start_contact(c, d, "survey")

    def h_lease_review_done(self, c, d):
        self.ev(c, d, "LEASE_REVIEW_COMPLETE", "MAILBOX", "Legal", "Legal", "Retrofit programme")
        if self.rng.random() < 0.25:
            return self.exit(c, d, "Excluded", "Lease places walls and heating with the shared owner")
        self.start_contact(c, d, "survey")

    def resequence(self, d):
        early = {"Identified", "Contacting (survey)", "Contact paused", "Survey queue"}
        for c in self.cands:
            if c.closed or c.identified > d or c.state not in early:
                continue
            if c.rule == "SEL-2025.1" and c.score < 28:
                c.token += 1
                c.flags.add("deferred_by_rule_change")
                self.set_state(c, d, "Deferred (resequenced)", "RESEQUENCED")
                self.ev(c, d, "RESEQUENCED", "TRACKER", "PM-01", reason="SEL-2026.1",
                        notes="Deferred to Wave 4 after damp-weighted rescoring")
                self.at(date(2026, 4, 13) + timedelta(days=self.rng.randint(0, 25)), c, "h_resume_deferred")

    def h_resume_deferred(self, c, d):
        self.ev(c, d, "RESEQUENCED", "TRACKER", "PM-01", reason="SEL-2026.1", notes="Released into Wave 4")
        self.start_contact(c, d, "survey")

    # resident contact ----------------------------------------------------------
    def start_contact(self, c, d, purpose):
        hh = c.hh
        lag = lognorm(self.rng, 3, 0.5, 1, 20)
        cat = "RES_ACCESS"
        if c.prop.locality == "LC" and RLO03_LEFT <= d <= date(2026, 6, 30):
            lag += self.rng.randint(4, 9)
        if hh.adjustment_recorded and hh.adjustment in FORMAT_ADJ and purpose in ("survey", "decision", "handover") \
                and (purpose, "fmt") not in c.gate:
            lag += lognorm(self.rng, 10, 0.4, 4)
            c.gate[(purpose, "fmt")] = True
            cat = "RES_ADJUST"
        self.set_state(c, d, f"Contacting ({purpose})", cat)
        c.owner_rlo = c.owner_rlo or RLO_BY_LOC[c.prop.locality]
        self.at(add_wd(d, lag), c, "h_contact_attempt", purpose=purpose, k=0)

    def h_contact_attempt(self, c, d, purpose, k):
        hh = c.hh
        if c.cat == "RES_ADJUST":
            self.set_state(c, d, c.state, "RES_ACCESS")
        ch = hh.channel
        p = {"Phone": 0.5, "Text message": 0.45, "Letter": 0.3, "Email": 0.4}[ch]
        if hh.working_hours_unavailable and ch == "Phone":
            p *= 0.6
        if hh.adjustment != "None" and not hh.adjustment_recorded:
            p *= 0.5
        if purpose in ("rebook_install", "handover", "decision"):
            p = min(0.9, p * 1.4)
        if hh.hard_to_reach:
            p = P["hard_to_reach_contact_p"]
        ok = self.rng.random() < p
        if ok:
            self.contact_row(c, d, purpose, ch, "Contacted")
            if c.prop.sold and purpose == "survey":
                c.flags.add("sold_found_at_contact")
                return self.exit(c, d, "Excluded", "Property sold - found at first contact")
            return self.on_contacted(c, d, purpose)
        fail = {"Phone": self.rng.choice(["No answer", "Voicemail left"]),
                "Text message": "Text sent - no reply", "Letter": "Letter sent - no reply",
                "Email": "Email sent - no reply"}[ch]
        self.contact_row(c, d, purpose, ch, fail)
        if k + 1 < 6:
            return self.at(add_wd(d, self.rng.randint(3, 8)), c, "h_contact_attempt", purpose=purpose, k=k + 1)
        c.n["contact_cycles"] += 1
        self.ev(c, d, "CONTACT_PAUSED", "CRM", self.rlo(c, d), reason="No contact after 6 attempts")
        if c.n["contact_cycles"] >= 3:
            c.flags.add("withdrawn_no_contact")
            if self.rng.random() < 0.5:
                c.flags.add("tracker_says_declined")
            return self.exit(c, d, "Withdrawn", "No contact after repeated attempts")
        self.set_state(c, d, "Contact paused", "RES_ACCESS")
        self.at(d + timedelta(days=lognorm(self.rng, 30, 0.3, 14)), c, "h_contact_attempt", purpose=purpose, k=0)

    def on_contacted(self, c, d, purpose):
        self.ev(c, d, "RESIDENT_CONTACTED", "CRM", self.rlo(c, d), outcome=purpose)
        r = self.rng.random()
        if purpose == "survey":
            if r < 0.055:
                c.flags.add("genuine_decline")
                return self.exit(c, d, "Withdrawn", "Resident declined survey")
            if r < 0.09:
                self.contact_row(c, d, purpose, c.hh.channel, "Resident undecided - call back",
                                 note="Resident wants to talk to family first")
                return self.at(d + timedelta(days=self.rng.randint(10, 30)), c, "h_contact_attempt",
                               purpose=purpose, k=0)
        if purpose in ("survey", "rebook_survey"):
            self.set_state(c, d, "Survey queue", "SURVEY_CAPACITY")
            prio = 0 if c.score >= 80 else 1
            return self.servers["SURVEY"].request(d, c, "h_survey_served", prio)
        if purpose == "decision":
            self.set_state(c, d, "Awaiting resident decision", "RES_DECISION")
            return self.at(add_wd(d, lognorm(self.rng, 4, 0.6, 0, 25)), c, "h_decision")
        if purpose == "rebook_install":
            self.set_state(c, d, "Supplier queue", "SUPPLIER_CAPACITY")
            return self.servers[c.supplier].request(d, c, "h_install_served", 0)
        if purpose == "handover":
            return self.at(add_wd(d, self.rng.randint(2, 8)), c, "h_resident_handover")

    # survey and assessment -----------------------------------------------------------
    def h_survey_served(self, c, d):
        adate = add_wd(d, self.rng.randint(4, 12))
        ai = self.appt_row(c, "SUP-RA", "Retrofit assessment", d, adate, self.rng.choice(["AM", "PM"]))
        self.set_state(c, d, "Survey booked", "SURVEY_CAPACITY")
        self.at(adate, c, "h_survey_visit", ai=ai)

    def na_prob(self, c, install=False):
        hh = c.hh
        p = (P["na_working_hours"] if hh.working_hours_unavailable else P["na_default"])
        if install and not hh.working_hours_unavailable:
            p *= 0.5
        if hh.adjustment != "None" and not hh.adjustment_recorded:
            p += P["na_unmet_adjust_bonus"]
        return p

    def h_survey_visit(self, c, d, ai):
        a = c.appts[ai]
        if self.rng.random() < self.na_prob(c):
            c.n["na"] += 1
            note = self.rng.choice(["No answer, card left", "No access - resident not home",
                                    "No reply at door, calling card posted"])
            if self.rng.random() < P["ref_misuse_survey"]:
                a["outcome"], a["note"] = "REF", note
                c.n["ref"] += 1
                c.flags.add("misrecorded_refusal")
                if c.n["ref"] >= 2 and self.rng.random() > P["reinstate_after_ref"]:
                    c.flags.add("withdrawn_on_misrecorded_refusal")
                    return self.exit(c, d, "Withdrawn", "Resident refused access (two recorded refusals)")
            else:
                a["outcome"], a["note"] = "NA", note
            return self.start_contact(c, d, "rebook_survey")
        a["outcome"], a["note"] = "ATT", "Assessment completed on site"
        c.dates["survey"] = d
        self.ev(c, d, "SURVEY_ATTENDED", "ASSESSOR_PORTAL", "SUP-RA")
        self.set_state(c, d, "Assessment write-up", "ASSESSMENT_WORK")
        self.at(add_wd(d, lognorm(self.rng, 4, 0.4, 1, 15)), c, "h_assessment")

    def h_assessment(self, c, d):
        pr = c.prop
        self.ev(c, d, "ASSESSMENT_COMPLETED", "ASSESSOR_PORTAL", "SUP-RA", evidence_version="RA-v1")
        ph = P["hazard_base"] + P["hazard_per_damp_report"] * min(pr.damp_reports, 2)
        ph += P["hazard_arc01_bonus"] if pr.archetype == "ARC-01" else 0
        if self.rng.random() < ph:
            self.raise_hazard(c, c.dates["survey"], d)
        if pr.true_sap >= 69:
            c.flags.add("post_survey_band_c")
            if pr.epc_lodged < date(2015, 10, 1):
                c.flags.add("stale_epc")
            self.ev(c, d, "ASSESSMENT_OUTCOME", "ASSESSOR_PORTAL", "SUP-RA",
                    outcome="Post-survey SAP indicates band C")
            self.set_state(c, d, "Funding decision", "FUNDING_DECISION")
            return self.at(add_wd(d, lognorm(self.rng, 18, 0.5, 3)), c, "h_already_c_decision")
        self.handoff_to_design(c, d)

    def h_already_c_decision(self, c, d):
        if self.rng.random() < 0.7:
            return self.exit(c, d, "Excluded", "Already EPC band C after survey - not eligible for grant")
        c.funding_route = "Internal capital"
        self.ev(c, d, "FUNDING_ROUTE_CHANGED", "TRACKER", "PM-01", outcome="Internal capital",
                reason="Post-survey band C; fabric first improvement retained")
        self.handoff_to_design(c, d)

    def handoff_to_design(self, c, d):
        self.ev(c, d, "HANDOFF_SENT", "MAILBOX", "SUP-RA", "Retrofit assessor", "Design consultancy")
        self.set_state(c, d, "Awaiting designer pickup", "HANDOFF_LAG")
        med = 9 if d.month in (12, 1, 2, 3) else 4
        self.at(add_wd(d, lognorm(self.rng, med, 0.6, 1, 40)), c, "h_design_start")

    def raise_hazard(self, c, aware, written):
        r = self.rng.random()
        if r < 0.75:
            referral = add_wd(aware, self.rng.randint(0, 2))
        elif r < 0.93:
            referral = add_wd(written, self.rng.randint(0, 1))
        else:
            referral = add_wd(written, self.rng.randint(2, 6))
        cat = pick(self.rng, [("Damp and mould", 0.80), ("Electrical", 0.07), ("Structural", 0.08), ("Other", 0.05)])
        prio = pick(self.rng, [("Emergency", 0.05), ("Significant", 0.60), ("Routine", 0.35)])
        inv = add_wd(referral, 1 if prio == "Emergency" else self.rng.randint(3, 9) if prio == "Significant"
                     else self.rng.randint(10, 25))
        rep = inv + timedelta(days=self.rng.randint(5, 15) if prio == "Emergency"
                              else lognorm(self.rng, 32, 0.5, 7))
        placed = referral + timedelta(days=self.rng.randint(0, 3))
        stale = self.rng.random() < P["zombie_share"]
        if stale and self.rng.random() < P["zombie_never_released"]:
            released = None
        elif stale:
            released = rep + timedelta(days=lognorm(self.rng, 24, 0.5, 8))
        else:
            released = rep + timedelta(days=self.rng.randint(0, 5))
        if released and released > SNAP:
            released = None
        h = dict(cid=c.cid, aware=aware, written=written, referral=referral, category=cat, priority=prio,
                 investigation=inv, repair=rep, placed=placed, released=released, stale=stale,
                 job=f"RJ-{700000 + len(self.hazards) * 7 + self.rng.randint(0, 6)}")
        c.hold = h
        c.flags.add("safety_hold")
        if stale:
            c.flags.add("stale_safety_hold")
        self.hazards.append(h)
        self.ev(c, aware, "HAZARD_OBSERVED", "ASSESSOR_PORTAL", "SUP-RA", reason=cat)
        self.at(referral, c, "h_hold_referral")
        self.at(placed, c, "h_hold_placed")
        self.at(rep, c, "h_repair_complete")
        if released:
            self.at(released, c, "h_hold_release")

    def h_hold_referral(self, c, d):
        self.ev(c, d, "HAZARD_REFERRED", "REPAIRS", "SUP-RA", "Retrofit programme", "Repairs and hazard service",
                reason=c.hold["category"])

    def h_hold_placed(self, c, d):
        self.ev(c, d, "SAFETY_HOLD_PLACED", "TRACKER", "BSL-01", reason=c.hold["category"])

    def h_repair_complete(self, c, d):
        self.ev(c, d, "REPAIR_COMPLETED", "REPAIRS", "Repairs service", reason=c.hold["job"])
        if not c.closed and c.state == "Awaiting release gate" and c.cat == "SAFETY_HOLD_ACTIVE":
            self.set_state(c, d, c.state, "SAFETY_HOLD_STALE")

    def h_hold_release(self, c, d):
        self.ev(c, d, "SAFETY_HOLD_RELEASED", "TRACKER", "BSL-01", evidence_version=c.hold["job"])
        if not c.closed and c.state == "Awaiting release gate":
            self.check_release(c, d)

    # design -------------------------------------------------------------------------
    def h_design_start(self, c, d):
        pr, b = c.prop, c.prop.building
        self.ev(c, d, "HANDOFF_ACCEPTED", "MAILBOX", "DES-1", "Retrofit assessor", "Design consultancy")
        self.set_state(c, d, "In design", "DESIGN_WORK")
        if pr.archetype == "ARC-06":
            dur = lognorm(self.rng, 32, 0.3, 15)
        elif pr.archetype == "ARC-03":
            if getattr(b, "design_started", False):
                dur = lognorm(self.rng, 4, 0.4, 1)
                c.flags.add("block_follow")
            else:
                b.design_started = True
                dur = lognorm(self.rng, 18, 0.3, 8)
        else:
            dur = lognorm(self.rng, 11, 0.3, 4)
        m = c.measures.lower()
        need = (pr.roof_due <= 2027 and "loft" in m) or ("external wall" in m and pr.windows_due <= 2027)
        if need and "pm_checked" not in c.flags:
            c.flags.add("pm_checked")
            c.flags.add("pm_dependency")
            if self.rng.random() < P["pm_detect_at_design"]:
                return self.at(add_wd(d, max(1, int(dur * 0.6))), c, "h_pm_identified")
            c.pm_undetected = True
            c.flags.add("pm_missed_at_design")
        self.at(add_wd(d, dur), c, "h_design_submit")

    def h_pm_identified(self, c, d):
        pr = c.prop
        why = f"Roof renewal due {pr.roof_due}" if pr.roof_due <= 2027 else f"Window renewal due {pr.windows_due}"
        self.ev(c, d, "PM_DEPENDENCY_IDENTIFIED", "MAILBOX", "DES-1", reason=why)
        self.set_state(c, d, "PM dependency hold", "PM_DEPENDENCY")
        self.at(add_wd(d, lognorm(self.rng, 8, 0.4, 2)), c, "h_pm_decision")

    def h_pm_decision(self, c, d):
        if self.rng.random() < 0.45 and "loft" in c.measures.lower():
            self.ev(c, d, "DESIGN_RESCOPED", "TRACKER", "PM-01", reason="Loft measure removed pending roof renewal")
            c.measures = c.measures.replace("; loft insulation", "").replace("; loft top-up", "")
            self.set_state(c, d, "In design", "DESIGN_RETURN")
            return self.at(add_wd(d, self.rng.randint(5, 10)), c, "h_design_submit")
        self.ev(c, d, "PM_WORKS_AWAITED", "TRACKER", "PM-01", to_team="Planned maintenance")
        self.at(d + timedelta(days=lognorm(self.rng, 110, 0.4, 40)), c, "h_pm_cleared")

    def h_pm_cleared(self, c, d):
        self.ev(c, d, "PM_DEPENDENCY_CLEARED", "PLANNED_MAINTENANCE", "Planned maintenance")
        self.set_state(c, d, "In design", "DESIGN_RETURN")
        self.at(add_wd(d, self.rng.randint(3, 8)), c, "h_design_submit")

    def h_design_submit(self, c, d):
        self.ev(c, d, "DESIGN_SUBMITTED", "MAILBOX", "DES-1", "Design consultancy", "Retrofit coordination",
                evidence_version=f"D-v{c.n['returns'] + 1}")
        self.set_state(c, d, "Awaiting RC approval", "RC_APPROVAL_QUEUE")
        prio = 0 if (c.hold or c.score >= 80) else 1
        w = 0.4 if "block_follow" in c.flags else 1.0
        self.servers["RC"].request(d, c, "h_rc_review", prio, w)

    def rc_on(self, d):
        avail = ["RC-01"]
        if not (RC02_LEAVE[0] <= d <= RC02_LEAVE[1]):
            avail.append("RC-02")
        if d >= RC03_START:
            avail.append("RC-03")
        return self.rng.choice(avail)

    def h_rc_review(self, c, d):
        rc = self.rc_on(d)
        c.owner_rc = rc
        p = P["design_return_arc06"] if c.prop.archetype == "ARC-06" else P["design_return_base"]
        if d < date(2025, 12, 1):
            p += P["design_return_early_bonus"]
        if "block_follow" in c.flags:
            p *= 0.4
        if self.rng.random() < p:
            c.n["returns"] += 1
            reason = self.rng.choice(["Ventilation strategy incomplete", "Moisture risk assessment missing",
                                      "U-value calculation inconsistent", "Thermal bridging detail missing",
                                      "Occupancy assessment out of date"])
            self.ev(c, d, "DESIGN_RETURNED", "MAILBOX", rc, "Retrofit coordination", "Design consultancy",
                    reason=reason, evidence_version=f"D-v{c.n['returns']}")
            self.set_state(c, d, "Design rework", "DESIGN_RETURN")
            return self.at(add_wd(d, lognorm(self.rng, 9, 0.4, 3)), c, "h_design_submit")
        self.ev(c, d, "DESIGN_APPROVED", "TRACKER", rc, evidence_version=f"D-v{c.n['returns'] + 1}")
        c.dates["design_approved"] = d
        b = c.prop.building
        if c.prop.archetype == "ARC-03" and b.leaseholders > 0 and b.lease_start is None:
            b.lease_start = d
            b.lease_done = d + timedelta(days=lognorm(self.rng, 110, 0.25, 70))
            self.ev(c, d, "LEASEHOLDER_CONSULTATION_STARTED", "PROGRAMME", "PM-01",
                    notes=f"{b.leaseholders} leaseholders in {b.building_id}")
        self.start_decision(c, d)
