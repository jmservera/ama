"""SYNTHETIC DATA ONLY. Export tables, part 2: safety holds, quality and
evidence, grant and finance, capacity, programme board snapshots, issues log
and the delay-code dictionary."""
from collections import Counter, defaultdict
from datetime import date, timedelta

from zf_model import (CODE_V2_FROM, HP_CONSTRAINT, RC02_LEAVE, SNAP, SIM_START, in_shutdown, is_wd,
                      month_ends, stable_rand)
from zf_export_rules import delay_code, iso, tracker_status, uk
from zf_sim_core import cap_geo, cap_qa, cap_rc, cap_supplier, cap_survey, fte_rc

SYN = {"is_synthetic": "true"}


def hold_rows(sim, rec):
    er = rec.erng
    rows = []
    by = sim.by_cid
    for i, h in enumerate(sorted(sim.hazards, key=lambda x: x["aware"])):
        if h["aware"] > SNAP:
            continue
        c = by[h["cid"]]
        cid = c.cid if er.random() > 0.20 else ""
        rel = h["released"]
        rows.append(dict(
            hold_id=f"HLD-{i + 1:04d}", candidate_id=cid, repairs_property_ref=c.prop.legacy_ref,
            hazard_observed_date=iso(h["aware"]), observed_by="Retrofit assessor",
            referral_sent_date=iso(h["referral"]) if h["referral"] <= SNAP else "",
            repairs_job_ref=h["job"], hazard_category=h["category"], repairs_priority=h["priority"],
            investigation_date=iso(h["investigation"]) if h["investigation"] <= SNAP else "",
            repair_completed_date=iso(h["repair"]) if h["repair"] <= SNAP else "",
            retrofit_hold_placed_date=iso(h["placed"]) if h["placed"] <= SNAP else "",
            retrofit_hold_released_date=iso(rel) if rel else "",
            hold_status_in_tracker="Released" if rel else "Open",
            release_evidence_ref=(h["job"] if rel and er.random() < 0.7 else ("see email" if rel else "")),
            **SYN))
    return rows


def quality_rows(cands, rec):
    rows = []
    for c in cands:
        for q in sorted(c.quality, key=lambda x: x["date"]):
            if q["date"] > SNAP:
                continue
            rows.append(dict(record_id=f"QE-{len(rows) + 1:06d}", candidate_id=c.cid,
                             property_ref=c.prop.property_id, supplier_id=c.supplier, record_type=q["type"],
                             record_date=iso(q["date"]), attempt_no=q["attempt"], result=q["result"],
                             defects_found=q["defects"], max_defect_severity=q["severity"],
                             reason=q["reason"], reviewer=q["reviewer"], **SYN))
    return rows


def unit_cost(c):
    m = c.measures.lower()
    u = stable_rand(c.cid, "cost")
    if "block" in m:
        return int(14000 + u * 5000)
    if "external wall" in m:
        return int(24000 + u * 8000)
    if "internal wall" in m:
        return int(15000 + u * 5000)
    if "heat pump" in m:
        return int(12000 + u * 4000)
    if "boiler" in m:
        return int(4000 + u * 2000)
    return int(3000 + u * 2000)


def money(v, rec, key, field):
    u = rec.erng.random()
    if u < 0.10:
        s = f"\u00a3{v:,}"
    elif u < 0.15:
        s = f"{v}.00"
    else:
        return str(v)
    rec.anom("grant-and-finance", key, field, "Currency formatting variant", v, s)
    return s


def finance_rows(sim, rec):
    rows = []
    claims = defaultdict(list)
    for cl in sim.claims:
        claims[cl["cid"]].append(cl)
    for c in sim.cands:
        d = c.dates
        route = c.funding_route if d.get("funding") or c.funding_route else ""
        cost = unit_cost(c)
        budget = money(cost, rec, c.cid, "approved_budget") if "design_approved" in d else ""
        committed = str(cost) if "work_order" in d else ""
        inv, inv_status = "", "Not invoiced"
        if d.get("install_complete") and d["install_complete"] <= SNAP:
            inv = str(int(cost * (0.95 + stable_rand(c.cid, "inv") * 0.1)))
            if c.supplier == "SUP-F2":
                inv_status = "Paid" if d.get("evidence_accepted") and d["evidence_accepted"] <= SNAP else "Part-paid (interim valuation)"
            else:
                inv_status = "Paid" if d.get("evidence_accepted") and d["evidence_accepted"] <= SNAP else "Invoiced - on hold pending evidence"
        grant = min(7500, cost // 2) if route == "WH:SHF Wave 3" else 0
        ea = d.get("evidence_accepted")
        cls = [x for x in claims.get(c.cid, []) if x["submitted"] <= SNAP]
        pending_cl = [x for x in claims.get(c.cid, []) if x["submitted"] > SNAP]
        if route != "WH:SHF Wave 3":
            cstat, cq, crec, hold = "Not applicable", "", "", ""
        elif cls and cls[-1]["status"] == "Received" and cls[-1]["received"] <= SNAP:
            cstat, cq, crec, hold = "Received", cls[-1]["quarter"], iso(cls[-1]["received"]), ""
        elif cls and cls[-1]["status"] == "Received":
            cstat, cq, crec, hold = "Submitted", cls[-1]["quarter"], "", ""
        elif cls:
            cstat, cq, crec, hold = "Rejected by funder", cls[-1]["quarter"], "", cls[-1]["reason"]
        elif pending_cl:
            cstat, cq, crec, hold = "In preparation", pending_cl[-1]["quarter"], "", ""
        elif d.get("install_complete") and d["install_complete"] <= SNAP:
            cstat, cq, crec, hold = "Awaiting evidence", "", "", "Documentary acceptance outstanding"
        else:
            cstat, cq, crec, hold = "Not yet claimable", "", "", ""
        if "budget_profile_hold" in c.flags and not d.get("work_order"):
            hold = "Quarterly budget profile fully committed"
        elig = {"WH:SHF Wave 3": "Eligible", "Internal capital": "Not grant funded"}.get(route, "")
        if "post_survey_band_c" in c.flags:
            elig = "Not eligible - band C after survey"
        rows.append(dict(candidate_id=c.cid, property_ref=c.prop.property_id, funding_route=route,
                         eligibility_status=elig, approved_budget=budget, committed_cost=committed,
                         invoiced_amount=inv, invoice_status=inv_status if route else "",
                         grant_eligible_amount=grant if grant else "",
                         evidence_accepted_date=iso(ea) if ea and ea <= SNAP else "",
                         claim_quarter=cq, claim_status=cstat, claim_received_date=crec,
                         hold_reason=hold, **SYN))
    # one claim line entered twice by hand
    rec_rows = [r for r in rows if r["claim_status"] == "Received"]
    if rec_rows:
        dup = dict(rec_rows[len(rec_rows) // 2])
        rows.append(dup)
        rec.anom("grant-and-finance", dup["candidate_id"], "*", "Duplicate claim line", "", "duplicate row")
    return rows


def months():
    out = []
    d = date(SIM_START.year, SIM_START.month, 1)
    while d <= SNAP:
        nxt = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
        out.append((d, min(nxt - timedelta(days=1), SNAP)))
        d = nxt
    return out


def capacity_rows(sim):
    rows = []
    contract = {"SUP-F1": 60, "SUP-F2": 32, "SUP-HP": 22, "SUP-HT": 40}
    wo = Counter((d.strftime("%Y-%m"), s) for d, _, s in sim.work_orders)
    st = Counter((d.strftime("%Y-%m"), s) for d, _, s in sim.install_starts)
    cp = Counter((d.strftime("%Y-%m"), s) for d, _, s in sim.install_completes)
    srv = sim.servers
    arr = {k: Counter(a[0].strftime("%Y-%m") for a in s.arrivals) for k, s in srv.items()}
    done = {k: Counter(l[0].strftime("%Y-%m") for l in s.log) for k, s in srv.items()}
    for m0, m1 in months():
        key = m0.strftime("%Y-%m")
        wds = [m0 + timedelta(days=i) for i in range((m1 - m0).days + 1)]
        wds = [x for x in wds if is_wd(x)]
        for s, name in [("SUP-F1", "Fabric: cavity, loft, internal wall"), ("SUP-F2", "Fabric: external wall"),
                        ("SUP-HP", "Air source heat pumps"), ("SUP-HT", "Heating: boilers and controls")]:
            note = ""
            if s == "SUP-HP" and HP_CONSTRAINT[0] <= m1 and m0 <= HP_CONSTRAINT[1]:
                note = "Supplier reports controls lead times"
            if s == "SUP-F2" and m0.month in (12, 1, 2):
                note = "Weather-dependent working"
            rows.append(dict(month=key, resource_id=s, resource_type="Supplier", trade_or_role=name,
                             committed_capacity=contract[s], work_released=wo[(key, s)],
                             jobs_started=st[(key, s)], jobs_completed=cp[(key, s)],
                             available_fte="", note=note, **SYN))
        internal = [
            ("SURVEY", "SUP-RA", "Framework", "Retrofit assessment (framework)", lambda x: 6.5 if x >= date(2025, 10, 1) else 4.0),
            ("RC", "TEAM-RC", "Internal competent role", "Retrofit coordination: design review and sign-off", lambda x: 2.0 * 1.25),
            ("QA", "TEAM-QA", "Internal team", "Quality inspection", lambda x: 3.0),
            ("GEO", "TEAM-GEO", "Internal team", "Grants and evidence review", lambda x: 3.0),
        ]
        for sk, rid, rtype, name, plan in internal:
            planned = round(sum(plan(x) for x in wds if not in_shutdown(x)))
            fte = ""
            note = ""
            if sk == "RC":
                fte = round(sum(fte_rc(x) for x in wds) / max(1, len(wds)), 2)
                if m0 <= RC02_LEAVE[1] and m1 >= RC02_LEAVE[0]:
                    note = "One coordinator on planned leave"
                if key >= "2026-04":
                    note = (note + "; " if note else "") + "Framework coordinator added part time"
            if sk == "QA":
                fte = 1.0
            if sk == "GEO":
                fte = 0.8
            if sk == "GEO" and key == "2026-08":
                note = "Officer on annual leave two weeks"
            framework = sk == "SURVEY"
            # Internal teams keep a leave planner, not throughput counts.
            rows.append(dict(month=key, resource_id=rid, resource_type=rtype, trade_or_role=name,
                             committed_capacity=planned if framework else "",
                             work_released=arr[sk][key] if framework else "",
                             jobs_started="", jobs_completed=done[sk][key] if framework else "",
                             available_fte=fte, note=note, **SYN))
        des = Counter(e["date"].strftime("%Y-%m") for c in sim.cands for e in c.events
                      if e["type"] == "DESIGN_SUBMITTED")
        rows.append(dict(month=key, resource_id="DES-1", resource_type="Consultancy",
                         trade_or_role="Retrofit design consultancy", committed_capacity=70,
                         work_released="", jobs_started="", jobs_completed=des[key], available_fte="",
                         note="Designs and revisions submitted", **SYN))
    return rows


def board_rows(sim):
    rows = []
    claims = sim.claims
    by = sim.by_cid
    for i, me in enumerate(month_ends()):
        snap = sim.month_snaps.get(me, [])
        v1 = me < CODE_V2_FROM
        sc, dc = Counter(), Counter()
        for cid, state, cat, since, closed, dates, hold in snap:
            s = tracker_status(state, hold, v1)
            sc[s] += 1
            if not closed:
                code = delay_code(cid, since, cat, v1)
                if hold:
                    code = "SAFETY" if v1 else "DLY-SAFETY-HOLD"
                dc[code or "(blank)"] += 1
        key = me.strftime("%Y-%m")
        for k, v in sorted(sc.items()):
            rows.append(dict(month_end=iso(me), section="Status count", item=k, value=v, note="", **SYN))
        for k, v in sorted(dc.items()):
            rows.append(dict(month_end=iso(me), section="Delay code count (open cases)", item=k, value=v, note="", **SYN))
        pc = sum(1 for c in sim.cands if c.dates.get("install_complete") and c.dates["install_complete"] <= me)
        ho = sum(1 for c in sim.cands if c.dates.get("accepted") and c.dates["accepted"] <= me)
        sv = sum(1 for c in sim.cands if c.dates.get("survey") and c.dates["survey"] <= me)
        idd = sum(1 for c in sim.cands if c.identified <= me)
        months_in = (me.year - 2025) * 12 + me.month - 9
        plan = max(0, min(600, round(600 * months_in / 12)))
        claimed = sum(min(7500, _cost(by[x["cid"]]) // 2) for x in claims if x["submitted"] <= me)
        received = sum(min(7500, _cost(by[x["cid"]]) // 2) for x in claims
                       if x["received"] and x["received"] <= me)
        for item, v, note in [
            ("Candidates identified (cumulative)", idd, ""),
            ("Surveys completed (cumulative)", sv, ""),
            ("Completions reported (cumulative)", pc, "Counted at practical completion"),
            ("Plan - completions (cumulative)", plan, "Year-one delivery plan"),
            ("Cases closed (cumulative)", ho, ""),
            ("Grant claimed GBP (cumulative)", claimed, ""),
            ("Grant received GBP (cumulative)", received, ""),
        ]:
            rows.append(dict(month_end=iso(me), section="KPI", item=item, value=v, note=note, **SYN))
    return rows


def _cost(c):
    return unit_cost(c)


ISSUE_EVENTS = {
    "DESIGN_RETURNED": ("Design", "Design returned by coordinator"),
    "QA_FAILED": ("Quality", "Failed QA inspection"),
    "EVIDENCE_REJECTED": ("Evidence", "Evidence pack rejected"),
    "AFTERCARE_REPORTED": ("Aftercare", "Aftercare report after handover"),
    "INSTALL_ABORTED": ("Installation", "Installation aborted on site"),
    "WITHDRAWAL_CHALLENGED": ("Resident", "Resident disputes recorded refusal"),
    "BLOCK_PROCEEDED_WITHOUT": ("Programme", "Block released without flat"),
    "PM_DEPENDENCY_IDENTIFIED": ("Design", "Planned maintenance dependency"),
    "FUNDING_HELD": ("Funding", "Quarterly budget profile fully committed"),
}


def issue_rows(sim, rec):
    er = rec.erng
    rows = []
    for c in sim.cands:
        evs = sorted([e for e in c.events if e["date"] <= SNAP], key=lambda e: e["date"])
        seen = Counter()
        for j, e in enumerate(evs):
            if e["type"] not in ISSUE_EVENTS:
                continue
            seen[e["type"]] += 1
            if e["type"] in ("DESIGN_RETURNED", "EVIDENCE_REJECTED") and seen[e["type"]] < 2:
                continue
            if e["type"] == "QA_FAILED" and e["outcome"] == "Minor":
                continue
            if er.random() > 0.6:
                continue
            nxt = next((x["date"] for x in evs[j + 1:] if x["type"] not in ISSUE_EVENTS), None)
            cat, summ = ISSUE_EVENTS[e["type"]]
            detail = e["reason"] or e["notes"]
            rows.append(dict(issue_id="", raised_date=e["date"], candidate_id=c.cid, stage=c.state if not nxt else "",
                             category=cat, summary=f"{summ}: {detail}" if detail else summ,
                             raised_by=e["actor"], owner="PM-01" if cat in ("Programme", "Funding") else e["actor"],
                             status="Closed" if nxt else "Open", closed_date=iso(nxt) if nxt else "", **SYN))
        h = c.hold
        if h and h["stale"] and h["repair"] + timedelta(days=30) <= SNAP and er.random() < 0.5:
            rel = h["released"]
            if not rel or (rel - h["repair"]).days > 30:
                rows.append(dict(issue_id="", raised_date=h["repair"] + timedelta(days=30), candidate_id=c.cid,
                                 stage="", category="Safety",
                                 summary="Hold still open - repairs status unclear, chase repairs team",
                                 raised_by="PS-01", owner="BSL-01", status="Closed" if rel else "Open",
                                 closed_date=iso(rel) if rel else "", **SYN))
    rows.sort(key=lambda r: r["raised_date"])
    for i, r in enumerate(rows):
        r["issue_id"] = f"ISS-{i + 1:04d}"
        r["raised_date"] = iso(r["raised_date"])
    return rows


def delay_dictionary():
    v1 = [("CONTRACTOR", "Waiting on contractor or supplier"), ("RESIDENT", "Waiting on resident"),
          ("DESIGN", "Design stage delay"), ("FUNDING", "Funding or budget"), ("SAFETY", "Safety hold"),
          ("OTHER", "Any other reason")]
    v2 = [("DLY-SUP-CAP", "Supplier capacity or start date", "CONTRACTOR"),
          ("DLY-SUP-EVID", "Supplier evidence outstanding", "CONTRACTOR"),
          ("DLY-RES-ACCESS", "Resident contact or access", "RESIDENT"),
          ("DLY-RES-DECISION", "Resident decision pending", "RESIDENT"),
          ("DLY-RES-ADJUST", "Reasonable adjustment being arranged", "RESIDENT"),
          ("DLY-DES-QUEUE", "Design awaited", "DESIGN"),
          ("DLY-DES-RETURN", "Design returned for amendment", "DESIGN"),
          ("DLY-PM-DEP", "Planned maintenance dependency", "OTHER"),
          ("DLY-LEASE", "Lease or leaseholder consultation", "OTHER"),
          ("DLY-SAFETY-HOLD", "Safety or hazard hold", "SAFETY"),
          ("DLY-FUND", "Funding or budget", "FUNDING"),
          ("DLY-QA-DEFECT", "Quality defect remediation", "CONTRACTOR"),
          ("DLY-DATA", "Data check or record issue", "OTHER"),
          ("DLY-OTHER", "Any other reason", "OTHER")]
    rows = [dict(code=c, version="v1", label=l, definition=l, introduced="2025-07-01", retired="2026-02-01",
                 maps_to_v2="", v1_equivalent="", **SYN) for c, l in v1]
    for c, l, e in v2:
        rows.append(dict(code=c, version="v2", label=l, definition=l, introduced="2026-02-02", retired="",
                         maps_to_v2="", v1_equivalent=e, **SYN))
    for r in rows[:6]:
        r["maps_to_v2"] = ";".join(c for c, _, e in v2 if e == r["code"])
    return rows
