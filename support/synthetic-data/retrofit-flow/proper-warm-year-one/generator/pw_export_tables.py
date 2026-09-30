"""SYNTHETIC DATA ONLY. Export tables, part 1: property register, tracker,
event log, CRM contacts, appointments and resident journey."""
from datetime import date, timedelta

from pw_model import ARCHETYPES, CODE_V2_FROM, LOCALITIES, SNAP, add_wd, stable_rand
from pw_export_rules import (NOTES, delay_code, iso, rag, swapped, tracker_owner, tracker_status, uk)

SYN = {"is_synthetic": "true"}


def property_rows(props, cands_by_prop, rec):
    er = rec.erng
    rows = []
    lease_bad = set()
    blds = sorted({p.building.building_id for p in props if p.archetype == "ARC-03"})
    for bid in er.sample(blds, min(3, len(blds))):
        lease_bad.add(bid)
    for p in props:
        c = cands_by_prop.get(p.property_id)
        band = p.epc_band
        if er.random() < 0.02:
            band = er.choice([band.lower(), band + " "])
            rec.anom("property-register", p.property_id, "current_epc", "Formatting variant", p.epc_band, band)
        lodged = iso(p.epc_lodged)
        if er.random() < 0.03:
            lodged = uk(p.epc_lodged)
            rec.anom("property-register", p.property_id, "epc_lodgement_date", "Mixed date format", iso(p.epc_lodged), lodged)
        yb = str(p.year_built)
        if p.archetype == "ARC-01" and er.random() < 0.25:
            yb = "pre-1919"
        elif er.random() < 0.03:
            yb = ""
            rec.anom("property-register", p.property_id, "year_built", "Missing value", p.year_built, "")
        uprn = p.uprn
        if er.random() < 0.05:
            uprn = ""
            rec.anom("property-register", p.property_id, "uprn", "Missing identifier", p.uprn, "")
        lh = p.building.leaseholders if p.archetype == "ARC-03" else ""
        if p.building.building_id in lease_bad and p.building.flats[0] is p:
            lh2 = max(0, p.building.leaseholders + er.choice([-1, 1, 2]))
            rec.anom("property-register", p.property_id, "leaseholders_in_building",
                     "Inconsistent building attribute", lh, lh2)
            lh = lh2
        occ = "Void" if c and c.state == "Void" else "Occupied"
        rows.append(dict(
            property_id=p.property_id, legacy_ref=p.legacy_ref, uprn=uprn,
            parent_building_id=p.building.building_id, shared_system_id=p.building.shared_system_id,
            heritage_org=p.heritage, locality=LOCALITIES[p.locality], archetype_id=p.archetype,
            archetype_label=ARCHETYPES[p.archetype][0], property_type=p.property_type,
            construction_type=ARCHETYPES[p.archetype][2], year_built=yb, tenure=p.tenure,
            heating_fuel=ARCHETYPES[p.archetype][3], current_epc=band, epc_sap=p.epc_sap,
            epc_lodgement_date=lodged, roof_renewal_due_year=p.roof_due,
            windows_renewal_due_year=p.windows_due, damp_reports_24m=p.damp_reports,
            occupancy_status=occ, leaseholders_in_building=lh, address_legacy=p.address_legacy, **SYN))
    # duplicate records from the merger of the two heritage registers
    dup_src = er.sample([p for p in props if p.archetype != "ARC-03"], 16)
    dups = []
    for i, p in enumerate(dup_src):
        base = dict(next(r for r in rows if r["property_id"] == p.property_id))
        base["property_id"] = f"SYN-PROP-9{i + 1:05d}"
        base["legacy_ref"] = (f"HB/{80000 + i * 13}" if p.heritage == "Heritage A" else f"HA-{90000 + i * 11:06d}")
        base["heritage_org"] = "Heritage B" if p.heritage == "Heritage A" else "Heritage A"
        base["address_legacy"] = (p.address_legacy.replace("Walk", "Wk").replace("Close", "Cl")
                                  .replace("Terrace", "Terr").replace("Grove", "Gr"))
        base["uprn"] = p.uprn if er.random() < 0.6 else ""
        if er.random() < 0.5:
            base["current_epc"] = p.epc_band if p.epc_band == "G" else chr(ord(p.epc_band) + 1)
        rec.anom("property-register", base["property_id"], "*", "Duplicate property from heritage merge",
                 p.property_id, base["property_id"])
        dups.append((p, base))
    rows.extend(b for _, b in dups)
    return rows, dups


def tracker_rows(cands, rec, dups):
    er = rec.erng
    rows = []
    for c in cands:
        hist = c.history
        since, state, cat = hist[-1]
        stale = False
        if not c.closed and len(hist) >= 2 and er.random() < 0.07:
            psn, ps, pc = hist[-2]
            if V_DIFF(ps, state):
                stale = True
                rec.anom("candidate-lifecycle", c.cid, "current_status", "Status not updated",
                         state, ps)
                state, cat, since = ps, pc, psn
        entered = rec.entry_date(c, since)
        v1 = entered < CODE_V2_FROM
        hold = bool(c.hold and c.hold["placed"] <= SNAP and not c.hold["released"]) and not c.closed
        status = tracker_status(state, hold, v1)
        closure = ""
        if c.closed and c.exit_type in ("Withdrawn", "Excluded"):
            closure = c.exit_reason
            if "tracker_says_declined" in c.flags:
                closure = "Resident declined"
                rec.anom("candidate-lifecycle", c.cid, "closure_reason", "Misclassified exit",
                         c.exit_reason, closure)
        days = (SNAP - since).days
        code = "" if c.closed and c.exit_type == "Accepted handover" else delay_code(c.cid, since, cat, v1)
        if hold:
            code = "SAFETY" if v1 else "DLY-SAFETY-HOLD"
        note_opts = NOTES.get(cat, [""])
        note = "" if c.closed else note_opts[int(stable_rand(c.cid, since, "note") * len(note_opts))]
        if "aftercare_hazard_signal" in c.flags and state == "Reopened - aftercare":
            note = "Aftercare - fan off, resident mentions condensation"
        nad = ""
        if not c.closed:
            nad = add_wd(entered, 10 + int(stable_rand(c.cid, "nad") * 10))
        ref = c.prop.property_id
        u = er.random()
        if u < 0.10:
            ref = c.prop.legacy_ref
        elif u < 0.11:
            ref = rec.ref_variant(c.prop)
            rec.anom("candidate-lifecycle", c.cid, "property_ref", "Identifier typo", c.prop.property_id, ref)

        def dcol(key):
            d = c.dates.get(key)
            if not d or d > SNAP:
                return ""
            r = er.random()
            if r < 0.02:
                rec.anom("candidate-lifecycle", c.cid, key, "Milestone not entered", iso(d), "")
                return ""
            if r < 0.03 and swapped(d):
                rec.anom("candidate-lifecycle", c.cid, key, "Day-month swap", iso(d), uk(swapped(d)))
                return uk(swapped(d))
            if r < 0.035:
                rec.anom("candidate-lifecycle", c.cid, key, "Free-text date", iso(d), f"w/c {uk(d - timedelta(days=d.weekday()))}")
                return f"w/c {uk(d - timedelta(days=d.weekday()))}"
            return uk(d)
        rows.append(dict(
            candidate_id=c.cid, property_ref=ref, wave=c.wave, candidate_identified_date=uk(c.identified),
            selection_rule_version=c.rule, priority_score=c.score,
            locality=LOCALITIES[c.prop.locality].split(" - ")[0], archetype_id=c.prop.archetype,
            measures=c.measures, lead_supplier=c.supplier, current_status=status,
            status_last_updated=uk(entered), owner=tracker_owner(c, state, cat, rec),
            rag_status="" if c.closed else rag(c, days, cat), delay_code=code, delay_notes=note,
            next_action_due=uk(nad) if nad else "", closure_reason=closure,
            survey_date=dcol("survey"), design_approved_date=dcol("design_approved"),
            work_order_date=dcol("work_order"), practical_completion_date=dcol("install_complete"),
            handover_date=dcol("handover"), **SYN))
    # properties re-added in a later wave list under their other heritage reference
    by_prop = {c.prop.property_id: c for c in cands}
    n = 0
    for p, base in dups[:12]:
        c = by_prop.get(p.property_id)
        if not c:
            continue
        n += 1
        flagged = er.random() < 0.5
        rows.append(dict(
            candidate_id=f"CAND-D-{n:03d}", property_ref=base["legacy_ref"], wave="Wave 3",
            candidate_identified_date=uk(date(2026, 1, 12)), selection_rule_version="SEL-2026.1",
            priority_score=c.score, locality=LOCALITIES[p.locality].split(" - ")[0], archetype_id=p.archetype,
            measures=c.measures, lead_supplier=c.supplier,
            current_status="Excluded" if flagged else "01 Identified",
            status_last_updated=uk(date(2026, 1, 30) if flagged else date(2026, 1, 12)),
            owner="PS-01", rag_status="" if flagged else "Green", delay_code="" if flagged else "DLY-DATA",
            delay_notes="Possible duplicate of earlier wave" if flagged else "", next_action_due="" if flagged else uk(date(2026, 1, 26)),
            closure_reason="Duplicate record" if flagged else "", survey_date="", design_approved_date="",
            work_order_date="", practical_completion_date="", handover_date="", **SYN))
        rec.anom("candidate-lifecycle", f"CAND-D-{n:03d}", "*", "Duplicate candidate from heritage record",
                 c.cid, f"CAND-D-{n:03d}")
    return rows


def V_DIFF(a, b):
    from pw_export_rules import V2_STATUS
    return V2_STATUS.get(a, a) != V2_STATUS.get(b, b)


# Detail held in the source-specific tables rather than the stage event log.
DETAIL_ONLY = {"RESIDENT_CONTACTED", "EVIDENCE_SUBMITTED", "EVIDENCE_REJECTED", "QA_FAILED",
               "HAZARD_OBSERVED", "HAZARD_REFERRED", "REPAIR_COMPLETED", "SURVEY_ATTENDED",
               "DATA_CHECK_COMPLETE"}


def event_rows(cands, rec):
    er = rec.erng
    rows = []
    n = 0
    for c in cands:
        assessed = {e["date"] for e in c.events if e["type"] == "ASSESSMENT_COMPLETED"}
        handed = {e["date"] for e in c.events if e["type"] == "HANDOFF_SENT"}
        for e in sorted(c.events, key=lambda x: x["date"]):
            d = e["date"]
            if d > SNAP or e["type"] in DETAIL_ONLY:
                continue
            if e["type"] == "HANDOFF_SENT" and d in assessed:
                continue
            if e["type"] == "ASSESSMENT_COMPLETED" and d in handed:
                e = dict(e, from_team="Retrofit assessor", to_team="Design consultancy",
                         notes="Assessment report issued to shared design mailbox")
            if e["type"] == "HANDOFF_ACCEPTED" and stable_rand(c.cid, d, "ack") > 0.60:
                continue
            if e["type"] not in ("CANDIDATE_IDENTIFIED",) and er.random() < 0.015:
                rec.anom("lifecycle-events", c.cid, e["type"], "Event missing from source extract", iso(d), "")
                continue
            ref = c.prop.property_id
            if e["source"] in ("REPAIRS", "HOUSING_MGMT") or er.random() < 0.05:
                ref = c.prop.legacy_ref
            ds = uk(d) if e["source"] == "CONTRACTOR_PORTAL" else iso(d)
            if e["source"] == "CONTRACTOR_PORTAL" and er.random() < 0.02 and swapped(d):
                ds = iso(swapped(d))
                rec.anom("lifecycle-events", c.cid, e["type"], "Day-month swap on import", iso(d), ds)
            n += 1
            row = dict(event_id=f"EV-{n:06d}", candidate_id=c.cid, property_ref=ref, event_date=ds,
                       event_type=e["type"], source_system=e["source"], actor=e["actor"],
                       from_team=e["from_team"], to_team=e["to_team"], outcome=e["outcome"],
                       reason=e["reason"], evidence_version=e["evidence_version"], notes=e["notes"], **SYN)
            rows.append(row)
            if er.random() < 0.01:
                n += 1
                dup = dict(row)
                dup["event_id"] = f"EV-{n:06d}"
                rows.append(dup)
                rec.anom("lifecycle-events", dup["event_id"], "*", "Duplicate event", row["event_id"], dup["event_id"])
    return rows


PURPOSE = {"survey": "Survey booking", "rebook_survey": "Rebook survey", "decision": "Works decision",
           "rebook_install": "Rebook installation", "handover": "Handover", "aftercare": "Aftercare"}


def contact_rows(cands, rec):
    er = rec.erng
    rows = []
    for c in cands:
        for k in sorted(c.contacts, key=lambda x: x["dt"]):
            if k["dt"].date() > SNAP:
                continue
            staff = k["staff"]
            if er.random() < 0.01:
                rec.anom("resident-contacts", c.cid, "staff_code", "Missing value", staff, "")
                staff = ""
            rows.append(dict(contact_id=f"CT-{len(rows) + 1:06d}", candidate_id=c.cid,
                             property_ref=c.prop.property_id, contact_datetime=k["dt"].strftime("%Y-%m-%d %H:%M"),
                             purpose=PURPOSE.get(k["purpose"], k["purpose"]), channel=k["channel"],
                             direction=k["direction"], outcome=k["outcome"],
                             adjustment_recorded=k["adj_recorded"], adjustment_met=k["adj_met"],
                             staff_code=staff, note=k["note"], **SYN))
    return rows


JOBPFX = {"SUP-F1": "F1J", "SUP-F2": "EW", "SUP-HP": "HP-", "SUP-HT": "HT/", "SUP-RA": "RA"}


def appointment_rows(cands, rec):
    er = rec.erng
    rows = []
    for c in cands:
        for i, a in enumerate(c.appts):
            if a["booked"] > SNAP:
                continue
            ref = c.prop.property_id
            u = er.random()
            if u < 0.13:
                ref = c.prop.legacy_ref
            elif u < 0.145:
                ref = rec.ref_variant(c.prop)
                rec.anom("appointments", f"{c.cid}#{i}", "property_ref", "Identifier typo", c.prop.property_id, ref)
            cid = "" if er.random() < 0.25 else c.cid
            outcome = a["outcome"] if a["date"] <= SNAP else "BOOKED"
            if a["outcome"] == "REF" and "No" in a["note"]:
                rec.anom("appointments", f"{c.cid}#{i}", "outcome_code", "No access recorded as refusal", "NA", "REF")
            rows.append(dict(appointment_id=f"AP-{len(rows) + 1:06d}", supplier_id=a["supplier"],
                             supplier_job_ref=f"{JOBPFX[a['supplier']]}{20000 + len(rows) * 3}",
                             property_ref=ref, candidate_id=cid, appointment_type=a["type"],
                             booked_on=uk(a["booked"]), appointment_date=uk(a["date"]), slot=a["slot"],
                             outcome_code=outcome, outcome_note=a["note"] if a["date"] <= SNAP else "", **SYN))
    return rows


def resident_rows(cands):
    rows = []
    for c in cands:
        hh = c.hh
        ks = [k for k in c.contacts if k["dt"].date() <= SNAP]
        ok = [k for k in ks if k["outcome"] in ("Contacted", "Handover visit completed")]
        dec = c.dates.get("decision")
        if dec and dec <= SNAP:
            wds = "Accepted"
        elif c.exit_reason == "Resident declined works":
            wds = "Declined"
        elif "design_approved" in c.dates:
            wds = "Pending"
        else:
            wds = "Not yet requested"
        last = max((k["dt"].date() for k in ks), default=None)
        rows.append(dict(
            candidate_id=c.cid, property_ref=c.prop.property_id, resident_ref=hh.resident_ref,
            preferred_channel=hh.channel,
            accessible_format=hh.adjustment if hh.adjustment_recorded else "",
            access_constraints="Not available weekdays 08:00-17:00" if hh.working_hours_recorded else "",
            priority_support_flag="Y" if hh.priority_support else "N",
            authorised_representative="Y" if hh.auth_rep else "N",
            contact_attempts_total=len([k for k in ks if k["direction"] == "Outbound"]),
            last_successful_contact=iso(max((k["dt"].date() for k in ok), default=None)),
            works_decision_status=wds, works_decision_date=iso(dec) if dec and dec <= SNAP else "",
            last_update_sent=iso(last),
            next_update_due=iso(add_wd(last, 20)) if last and not c.closed else "", **SYN))
    return rows
