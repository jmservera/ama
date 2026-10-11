"""SYNTHETIC DATA ONLY. Export helpers, part 1: record-keeping behaviour of
the team's tracker, event log, property register, CRM and contractor portal.
Every intentional imperfection is recorded as an anomaly for the answer key."""
from datetime import date, timedelta

from zf_model import (CODE_V2_FROM, SNAP, add_wd, is_wd, last_wd_of_month, stable_rand, pick,
                      RLO03_LEFT)

V2_STATUS = {
    "Identified": "01 Identified", "Lease review": "01 Identified", "Deferred (resequenced)": "01 Identified",
    "Contacting (survey)": "02 Contacting resident", "Contacting (rebook_survey)": "02 Contacting resident",
    "Contact paused": "02 Contacting resident",
    "Survey queue": "03 Survey booked", "Survey booked": "03 Survey booked",
    "Assessment write-up": "04 Survey complete", "Awaiting designer pickup": "04 Survey complete",
    "In design": "05 In design", "Awaiting RC approval": "05 In design", "Design rework": "05 In design",
    "PM dependency hold": "On hold",
    "Contacting (decision)": "06 Awaiting resident decision",
    "Awaiting resident decision": "06 Awaiting resident decision", "Resident pause": "On hold",
    "Funding check": "07 Ready to order", "Funding decision": "07 Ready to order",
    "Awaiting release gate": "07 Ready to order", "On hold - missed block programme": "On hold",
    "Supplier queue": "08 Ordered", "Install booked": "08 Ordered",
    "Contacting (rebook_install)": "08 Ordered",
    "On site": "09 On site",
    "Awaiting QA and evidence": "10 Practical completion",
    "Contacting (handover)": "10 Practical completion",
    "Awaiting resident handover": "10 Practical completion",
    "Awaiting closure": "11 Handed over",
    "Accepted handover": "12 Closed", "Reopened - aftercare": "Reopened",
    "Void": "On hold", "Withdrawn": "Withdrawn", "Excluded": "Excluded",
}
V1_OF_V2 = {
    "01 Identified": "Identified", "02 Contacting resident": "Contacting", "03 Survey booked": "Survey",
    "04 Survey complete": "Survey done", "05 In design": "Design", "06 Awaiting resident decision": "Consent",
    "07 Ready to order": "Ready", "08 Ordered": "Ordered", "09 On site": "On site",
    "10 Practical completion": "Complete", "11 Handed over": "Complete", "12 Closed": "Closed",
    "On hold": "Hold", "Withdrawn": "Withdrawn", "Excluded": "Excluded", "Reopened": "Reopened",
}

CODE_BIAS = {
    "RES_ACCESS": [("DLY-RES-ACCESS", .70), ("DLY-RES-DECISION", .15), ("DLY-OTHER", .05), ("", .10)],
    "RES_ADJUST": [("DLY-RES-ACCESS", .60), ("DLY-RES-ADJUST", .20), ("", .20)],
    "RES_DECISION": [("DLY-RES-DECISION", .75), ("", .25)],
    "SURVEY_CAPACITY": [("DLY-SUP-CAP", .55), ("DLY-OTHER", .15), ("", .30)],
    "ASSESSMENT_WORK": [("", .70), ("DLY-SUP-CAP", .30)],
    "HANDOFF_LAG": [("DLY-DES-QUEUE", .30), ("DLY-SUP-CAP", .25), ("", .45)],
    "DESIGN_WORK": [("DLY-DES-QUEUE", .35), ("", .65)],
    "RC_APPROVAL_QUEUE": [("DLY-DES-QUEUE", .35), ("DLY-SUP-CAP", .20), ("DLY-OTHER", .15), ("", .30)],
    "DESIGN_RETURN": [("DLY-DES-RETURN", .60), ("DLY-DES-QUEUE", .20), ("", .20)],
    "PM_DEPENDENCY": [("DLY-PM-DEP", .60), ("DLY-OTHER", .25), ("", .15)],
    "LEASE_REVIEW": [("DLY-LEASE", .70), ("DLY-OTHER", .30)],
    "LEASE_BLOCK_SYNC": [("DLY-LEASE", .35), ("DLY-SUP-CAP", .35), ("DLY-OTHER", .15), ("", .15)],
    "SAFETY_HOLD_ACTIVE": [("DLY-SAFETY-HOLD", .90), ("", .10)],
    "SAFETY_HOLD_STALE": [("DLY-SAFETY-HOLD", .90), ("", .10)],
    "FUNDING_CHECK": [("DLY-FUND", .50), ("", .50)],
    "FUNDING_DECISION": [("DLY-FUND", .80), ("", .20)],
    "SUPPLIER_CAPACITY": [("DLY-SUP-CAP", .85), ("", .15)],
    "INSTALL_WORK": [("", .85), ("DLY-SUP-CAP", .15)],
    "QA_QUEUE": [("", .70), ("DLY-QA-DEFECT", .10), ("DLY-SUP-CAP", .20)],
    "QA_DEFECT": [("DLY-QA-DEFECT", .70), ("DLY-SUP-CAP", .20), ("", .10)],
    "EVIDENCE_SUBMISSION": [("", .55), ("DLY-SUP-EVID", .20), ("DLY-SUP-CAP", .15), ("DLY-FUND", .10)],
    "EVIDENCE_REJECTION": [("", .35), ("DLY-SUP-EVID", .35), ("DLY-SUP-CAP", .20), ("DLY-FUND", .10)],
    "HANDOVER_LAG": [("", .80), ("DLY-RES-ACCESS", .20)],
    "ADMIN_CLOSURE": [("", 1.0)],
    "VOID_RELET": [("DLY-OTHER", .60), ("DLY-RES-ACCESS", .20), ("", .20)],
    "RESIDENT_PAUSE": [("DLY-RES-DECISION", .60), ("DLY-OTHER", .40)],
    "RESEQUENCED": [("DLY-OTHER", .70), ("", .30)],
    "DATA_CHECK": [("", .80), ("DLY-DATA", .20)],
    "AFTERCARE": [("DLY-QA-DEFECT", .60), ("DLY-SUP-CAP", .20), ("", .20)],
}
V1_CODE = {"DLY-SUP-CAP": "CONTRACTOR", "DLY-SUP-EVID": "CONTRACTOR", "DLY-RES-ACCESS": "RESIDENT",
           "DLY-RES-DECISION": "RESIDENT", "DLY-RES-ADJUST": "RESIDENT", "DLY-DES-QUEUE": "DESIGN",
           "DLY-DES-RETURN": "DESIGN", "DLY-FUND": "FUNDING", "DLY-SAFETY-HOLD": "SAFETY",
           "DLY-PM-DEP": "OTHER", "DLY-LEASE": "OTHER", "DLY-QA-DEFECT": "CONTRACTOR",
           "DLY-DATA": "OTHER", "DLY-OTHER": "OTHER"}
NOTES = {
    "RES_ACCESS": ["Tried x3 no answer", "Card left, awaiting call back", "Resident works days - try evening?",
                   "Letter sent", "No response to texts"],
    "RES_ADJUST": ["Awaiting large print pack", "Interpreter booking requested", "Waiting for advocate availability"],
    "RES_DECISION": ["Resident considering", "Pack delivered, chasing decision", "Wants to discuss with family"],
    "SURVEY_CAPACITY": ["Awaiting survey slot", "Assessor chasing", "In framework queue"],
    "HANDOFF_LAG": ["Sent to designer", "Survey report sent", "Chased designer"],
    "DESIGN_WORK": ["With designer", "Design in progress"],
    "RC_APPROVAL_QUEUE": ["Design with RC", "Awaiting sign off", "Design submitted", "Chase designer"],
    "DESIGN_RETURN": ["Design returned for amendments", "Back with designer - vent strategy", "Revised design due"],
    "PM_DEPENDENCY": ["Roof first", "Awaiting planned works", "Windows programme dependency"],
    "LEASE_REVIEW": ["With legal", "Lease check"],
    "LEASE_BLOCK_SYNC": ["Waiting rest of block", "S20 consultation running", "Block not complete"],
    "SAFETY_HOLD_ACTIVE": ["Damp job raised with repairs", "Repairs to attend", "Hold - damp"],
    "SAFETY_HOLD_STALE": ["Hold - damp", "Check repairs status", "Repairs job raised"],
    "FUNDING_CHECK": ["Grant check", "Budget check"],
    "FUNDING_DECISION": ["Budget reprofile", "Awaiting funding decision", "Band C post survey - PM to decide"],
    "SUPPLIER_CAPACITY": ["Awaiting contractor date", "Contractor to confirm start", "Heat pump controls on order"],
    "INSTALL_WORK": ["On site", "Works progressing"],
    "QA_QUEUE": ["QA to book", "Awaiting QA"],
    "QA_DEFECT": ["Snags to clear", "Remedials booked", "Failed QA - contractor returning"],
    "EVIDENCE_SUBMISSION": ["Awaiting docs from contractor", "Evidence due", ""],
    "EVIDENCE_REJECTION": ["Docs rejected - resubmit", "Missing photos", "Certificates outstanding"],
    "HANDOVER_LAG": ["Handover visit to book", ""],
    "ADMIN_CLOSURE": [""],
    "VOID_RELET": ["Property void - lettings first", "New tenant, restart"],
    "RESIDENT_PAUSE": ["Resident asked to pause", "Pause until after new year"],
    "RESEQUENCED": ["Moved to Wave 4", "Deprioritised under new rule"],
    "DATA_CHECK": ["Desk check"],
    "AFTERCARE": ["Aftercare - fan noise", "Aftercare visit booked", "Controls revisit"],
}


def iso(d):
    return d.isoformat() if d else ""


def uk(d):
    return d.strftime("%d/%m/%Y") if d else ""


def swapped(d):
    if d and d.day <= 12 and d.day != d.month:
        return date(d.year, d.day, d.month)
    return None


class Recorder:
    def __init__(self, erng):
        self.erng = erng
        self.anoms = []

    def anom(self, table, key, field, kind, true_value, recorded):
        self.anoms.append(dict(anomaly_id=f"ANOM-{len(self.anoms) + 1:05d}", table=table, record_key=key,
                               field=field, anomaly_type=kind, true_value=str(true_value),
                               recorded_value=str(recorded)))

    def ref_variant(self, p):
        """A realistic typo in a property reference."""
        r = self.erng.random()
        s = p.property_id
        if r < 0.35:
            return s.lower()
        if r < 0.7:
            digits = s[-6:]
            i = self.erng.randint(0, 4)
            t = digits[:i] + digits[i + 1] + digits[i] + digits[i + 2:]
            return s[:-6] + t
        return p.legacy_ref.replace("-", "").replace("/", " ")

    def entry_date(self, c, since):
        """When the tracker cell was actually updated for a change on `since`."""
        u = stable_rand(c.cid, since, "entry")
        if u < 0.40:
            e = add_wd(since, 0 if u < 0.25 else 1)
        elif u < 0.75:
            e = since + timedelta(days=(4 - since.weekday()) % 7)
        else:
            e = last_wd_of_month(since)
            if e < since:
                e = since
        return min(e, SNAP)


def tracker_status(state, hold_active, v1):
    s = V2_STATUS.get(state, state)
    if hold_active and s not in ("Withdrawn", "Excluded", "12 Closed", "11 Handed over"):
        s = "On hold"
    return V1_OF_V2.get(s, s) if v1 else s


def delay_code(cid, since, cat, v1):
    pairs = CODE_BIAS.get(cat, [("", 1.0)])
    u = stable_rand(cid, since, cat, "code")
    acc, code = 0.0, ""
    for v, w in pairs:
        acc += w
        if u < acc:
            code = v
            break
    if v1:
        if not code:
            return "OTHER" if stable_rand(cid, since, "v1blank") < 0.3 else ""
        return V1_CODE[code]
    return code


def tracker_owner(c, state, cat, rec):
    u = stable_rand(c.cid, "owner", state)
    if u < 0.03:
        return ""
    early = ("Contact", "Survey", "Identified", "Lease", "Deferred", "Void", "Resident")
    if state.startswith(early) or cat in ("RES_ACCESS", "RES_DECISION", "RES_ADJUST"):
        o = c.owner_rlo or "RLO-01"
        if o == "RLO-03" and c.since and c.since >= RLO03_LEFT and u > 0.4:
            o = "RLO-02"
    elif cat in ("RC_APPROVAL_QUEUE", "DESIGN_WORK", "DESIGN_RETURN", "HANDOFF_LAG", "PM_DEPENDENCY",
                 "ASSESSMENT_WORK"):
        o = c.owner_rc or ("RC-01" if u < 0.5 else "RC-02")
    elif cat.startswith("SAFETY"):
        o = "BSL-01"
    elif cat.startswith("EVIDENCE") or cat.startswith("FUNDING"):
        o = "GEO-01"
    elif cat.startswith("QA"):
        o = "QA-01"
    else:
        o = "PM-01"
    if u > 0.98:
        o = {"RLO-01": "Resident Liaison", "RLO-02": "Resident Liaison", "RC-01": "Retrofit Coord",
             "RC-02": "Retrofit Coord", "GEO-01": "Grants", "PM-01": "Programme"}.get(o, o)
    return o


def rag(c, days, cat):
    u = stable_rand(c.cid, "rag", cat)
    if days < 30:
        return "Green"
    if days < 90:
        return "Green" if u < 0.45 else "Amber"
    return "Amber" if u < 0.5 else "Red"
