"""SYNTHETIC DATA ONLY. Build the Zava Forward MVP working dataset.

Runs the year-one simulation, gives every household, contractor and staff
member a name, and places each home on a real address from the private
stock-geography register. Dates are shifted so the data ends on today's date.

The output (mvp/data/zavaforward.json) contains real OpenStreetMap addresses
with invented residents. It is git-ignored and must stay on this machine.

Usage:
    python3 build_mvp_dataset.py --seed 20260901
"""
import argparse
import csv
import json
import os
import random
from collections import defaultdict
from datetime import date, datetime, timedelta

import zf_names as names
from generate_pack import Sim, build
from zf_export_rules import Recorder, tracker_owner
from zf_model import SIM_START, SNAP
from zf_names import STAFF_NAMES

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *[".."] * 5))
REGISTER = os.path.join(HERE, "..", "stock-geography", "private-north-east-stock-register.csv")

STAGE = {
    "Identified": "Home identified", "Lease review": "Checking lease", "Deferred (resequenced)": "Rescheduled",
    "Contact paused": "Contact paused", "Survey queue": "Survey being booked", "Survey booked": "Survey booked",
    "Assessment write-up": "Survey write-up", "Awaiting designer pickup": "Design starting",
    "In design": "Design in progress", "Awaiting RC approval": "Design awaiting approval",
    "Design rework": "Design being corrected", "PM dependency hold": "Waiting on other works",
    "Awaiting resident decision": "Waiting for resident decision", "Resident pause": "Resident paused works",
    "Funding check": "Funding check", "Funding decision": "Funding check",
    "Awaiting release gate": "Final checks before ordering", "On hold - missed block programme": "Waiting for block programme",
    "Supplier queue": "With contractor", "Install booked": "Install booked", "On site": "Works under way",
    "Awaiting resident handover": "Handover to arrange", "Awaiting QA and evidence": "Quality check",
    "Awaiting closure": "Closing down", "Accepted handover": "Completed", "Reopened - aftercare": "Aftercare issue",
}
REASON = {
    "RES_ACCESS": "to agree access", "RES_ADJUST": "to confirm their support needs",
    "RES_DECISION": "to confirm whether they want the works",
    "RC_APPROVAL_QUEUE": "to approve the design", "DESIGN_WORK": "to finish the design",
    "DESIGN_RETURN": "to correct the design", "HANDOFF_LAG": "to pick this up",
    "PM_DEPENDENCY": "to confirm the other works", "ASSESSMENT_WORK": "to finish the survey write-up",
}
ROLE_TITLE = {
    "PM": "Retrofit Programme Manager", "PS": "Programme Support Officer", "RC": "Retrofit Coordinator",
    "RLO": "Resident Liaison Officer", "GEO": "Grants and Evidence Officer", "QA": "Quality Inspector",
    "BSL": "Building Safety Liaison",
}
OUTCOME = {"ATT": "Attended", "NA": "No access", "REF": "Refused", "CAN": "Cancelled", "RES": "Rescheduled"}
FORM = {"flat": {"apartments"}, "bungalow": {"bungalow"},
        "terrace": {"terrace", "house", "residential"}, "semi": {"semidetached_house", "house", "residential"},
        "detached": {"detached", "house", "residential"}}


def load_register():
    with open(REGISTER, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def theme(code):
    return {"LA": "Locality A", "LB": "Locality B", "LC": "Locality C"}[code]


def form_key(ptype):
    p = ptype.lower()
    if "flat" in p:
        return "flat"
    if "bungalow" in p:
        return "bungalow"
    if "semi" in p:
        return "semi"
    if "detached" in p:
        return "detached"
    return "terrace"


class AddressPool:
    def __init__(self, rows, rng):
        self.rng = rng
        self.free = defaultdict(list)
        for r in rows:
            if r["portfolio_category"] not in ("General needs - social rent", "General needs - affordable rent"):
                continue
            if not (r["postcode"] and r["address_street_or_place"]):
                continue
            for fk, forms in FORM.items():
                if r["building_form_osm"] in forms:
                    self.free[(r["locality_theme"][:10], fk)].append(r)
        for v in self.free.values():
            rng.shuffle(v)
        self.used = set()
        self.block = {}

    def take(self, loc, fk, building_id=None, flat_no=None):
        if building_id and building_id in self.block:
            base = self.block[building_id]
        else:
            pool = self.free[(theme(loc), fk if fk != "flat" else "flat")] or self.free[(theme(loc), "terrace")]
            if fk == "flat" and not self.free[(theme(loc), "flat")]:
                pool = self.free[(theme(loc), "terrace")]
            base = None
            while pool:
                r = pool.pop()
                if r["synthetic_home_id"] not in self.used:
                    base = r
                    break
            if base is None:
                raise RuntimeError("stock register exhausted")
            self.used.add(base["synthetic_home_id"])
            if building_id:
                self.block[building_id] = base
        line1 = f"{base['address_house_number']} {base['address_street_or_place']}".strip()
        if flat_no:
            line1 = f"Flat {flat_no}, {line1}"
        return dict(line1=line1, town=base["address_locality"] or base["local_authority"], postcode=base["postcode"],
                    area=base["local_authority"], lat=float(base["latitude"]), lon=float(base["longitude"]))


def shift(d, off):
    if d is None:
        return None
    if isinstance(d, datetime):
        return (d + timedelta(days=off)).isoformat(timespec="minutes")
    return (d + timedelta(days=off)).isoformat()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260901)
    ap.add_argument("--out", default=os.path.join(REPO, "mvp", "data", "zavaforward.json"))
    a = ap.parse_args()
    seed = a.seed
    rng = random.Random(seed)
    props, buildings, cands = build(rng)
    sim = Sim(rng, cands, buildings)
    sim.by_prop = {c.prop.property_id: c for c in cands}
    sim.by_cid = {c.cid: c for c in cands}
    sim.block_list = [b for b in buildings if len(b.flats) > 1]
    sim.hh_seq = len(cands)
    for c in cands:
        sim.at(c.identified, c, "h_identified")
    sim.run(SIM_START)

    off = (date.today() - SNAP).days
    rec = Recorder(random.Random(seed + 1))
    pool = AddressPool(load_register(), random.Random(seed + 2))
    haz_by = defaultdict(list)
    for h in sim.hazards:
        haz_by[h["cid"]].append(h)

    staff_codes = sorted(STAFF_NAMES)
    cases = []
    flat_idx = defaultdict(int)
    for c in cands:
        if c.identified > SNAP:
            continue
        p = c.prop
        fk = form_key(p.property_type)
        flat_no = None
        bid = None
        if fk == "flat":
            bid = p.building.building_id
            flat_idx[bid] += 1
            flat_no = flat_idx[bid]
        addr = pool.take(p.locality, fk, bid, flat_no)
        res = names.resident(seed, c.hh.resident_ref)
        rep = names.representative(seed, c.hh.resident_ref, res["last"]) if c.hh.auth_rep else None
        owner_code = tracker_owner(c, c.state, c.cat, rec)
        if owner_code not in STAFF_NAMES:
            owner_code = {"Resident Liaison": "RLO-01", "Retrofit Coord": "RC-01", "Grants": "GEO-01",
                          "Programme": "PM-01"}.get(owner_code, "PM-01")
        con = names.contractor(c.supplier)
        if owner_code == "RLO-03":
            owner_code = "RLO-02"
        owner = names.staff(owner_code)
        stage = STAGE.get(c.state) or ("Contacting resident" if c.state.startswith("Contacting") else c.state)
        waiting, reason = owner["name"], REASON.get(c.cat, "to take the next step")
        if c.state in ("Supplier queue", "Install booked", "On site"):
            waiting, reason = f"{names.operative(seed, c.supplier, c.cid)} at {con['name']}", "to complete the installation"
        elif c.state in ("Awaiting QA and evidence", "Awaiting closure"):
            reason = "to check the work and sign it off"
        elif c.state.startswith("Contacting") or c.state in ("Contact paused", "Survey queue"):
            reason = REASON.get(c.cat, "to agree a visit with the resident")
        closed = c.closed or c.state == "Accepted handover"
        since = c.since or c.identified
        days_in_stage = max(0, (SNAP - since).days)
        contacts = []
        for k in sorted(c.contacts, key=lambda x: x["dt"]):
            if k["dt"].date() > SNAP:
                continue
            by = k["staff"] if k["staff"] in STAFF_NAMES else owner_code
            contacts.append(dict(at=shift(k["dt"], off), purpose=k["purpose"].replace("_", " ").capitalize(),
                                 channel=k["channel"], direction=k["direction"], outcome=k["outcome"], note=k["note"],
                                 by=names.staff(by)["name"]))
        appts = []
        for ap_ in c.appts:
            if ap_["booked"] > SNAP:
                continue
            appts.append(dict(type=ap_["type"], date=shift(ap_["date"], off), slot=ap_["slot"],
                              outcome=OUTCOME.get(ap_["outcome"], ap_["outcome"]) if ap_["date"] <= SNAP else "Booked",
                              note=ap_["note"] if ap_["date"] <= SNAP else "",
                              who=con["name"], person=names.operative(seed, c.supplier, c.cid)))
        hazards = []
        for h in haz_by.get(c.cid, []):
            if h["aware"] > SNAP:
                continue
            hazards.append(dict(category=h["category"], priority=h["priority"], noticed=shift(h["aware"], off),
                                referred=shift(h["referral"], off) if h["referral"] <= SNAP else None,
                                repaired=shift(h["repair"], off) if h["repair"] <= SNAP else None,
                                released=bool(h["released"]), job=h["job"], owner=names.staff("BSL-01")["name"]))
        dec = c.dates.get("decision")
        if dec and dec <= SNAP:
            decision = "Accepted"
        elif c.exit_reason == "Resident declined works":
            decision = "Declined"
        elif "design_approved" in c.dates:
            decision = "Not yet asked" if False else "Waiting"
        else:
            decision = "Not yet asked"
        route = c.funding_route or ""
        fund_ok = bool(c.dates.get("funding") and c.dates["funding"] <= SNAP)
        if fund_ok:
            fstatus = "Confirmed"
        elif route.startswith("WH:SHF") or c.state in ("Funding check", "Funding decision", "Awaiting release gate"):
            fstatus = "To prepare"
        else:
            fstatus = "Not started"
        docs = [("EPC certificate", "EPC", c.identified)]
        for key, label, kind in (("survey", "Retrofit assessment report", "Survey"), ("design_approved", "Retrofit design", "Design"),
                                 ("decision", "Resident agreement to works", "Consent"), ("funding", "Funding evidence pack", "Funding evidence")):
            if key in c.dates and c.dates[key] <= SNAP:
                docs.append((label, kind, c.dates[key]))
        documents = [dict(id=f"D{i + 1}", name=f"{nm}.pdf", kind=kind, at=shift(dt, off),
                          by=owner["name"], generated=True) for i, (nm, kind, dt) in enumerate(docs)]
        cases.append(dict(
            documents=documents,
            funding=dict(route=route or "Not decided", status=fstatus, reference="", draft="", approved_by=None),
            id=c.cid.replace("CAND-", "ZF-"), wave=c.wave, closed=closed, stage=stage,
            stage_since=shift(since, off), days_in_stage=days_in_stage,
            waiting_on=waiting, reason=reason,
            owner_code=owner_code, owner=owner["name"], owner_role=ROLE_TITLE[owner_code.split("-")[0]],
            resident=dict(title=res["title"], name=res["full"], formal=res["formal"], phone=res["phone"],
                          email=res["email"], preferred=c.hh.channel, adjustment=c.hh.adjustment,
                          priority_support=c.hh.priority_support,
                          unavailable="Weekdays 08:00-17:00" if c.hh.working_hours_unavailable else "",
                          representative=None if not rep else dict(name=rep["full"], relationship=rep["relationship"],
                                                                   phone=rep["phone"])),
            home=dict(address=addr["line1"], town=addr["town"], postcode=addr["postcode"], area=addr["area"],
                      type=p.property_type, built=p.year_built, epc=p.epc_band, tenure=p.tenure,
                      lat=addr["lat"], lon=addr["lon"]),
            measures=c.measures, contractor=dict(name=con["name"], phone=con["phone"], scope=con["scope"],
                                                 contact=names.operative(seed, c.supplier, c.cid)),
            decision=dict(status=decision, by=None, at=shift(dec, off) if dec and dec <= SNAP else None),
            funding_ok=fund_ok,
            contacts=contacts, appointments=appts, hazards=hazards, history=[]))

    staff = []
    for code in [x for x in staff_codes if x != "RLO-03"]:
        s = names.staff(code)
        staff.append(dict(code=code, name=s["name"], email=s["email"], role=ROLE_TITLE[code.split("-")[0]]))
    out = dict(built=date.today().isoformat(), staff=staff, cases=cases)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    open_cases = sum(not x["closed"] for x in cases)
    print(f"wrote {a.out}: {len(cases)} cases ({open_cases} open), {len(staff)} staff")


if __name__ == "__main__":
    main()
