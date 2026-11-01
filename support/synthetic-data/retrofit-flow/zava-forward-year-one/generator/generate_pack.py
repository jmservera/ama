"""SYNTHETIC DATA ONLY. Generate the Zava Forward year-one synthetic evidence
pack and its separate answer key.

Usage:
    python generate_pack.py --seed 1341953496

By default the pack is written to docs/reference/research/retrofit-synthetic-data
and the ground truth to ../answer-key (git-ignored). Omit --seed to draw a new
random seed; it is printed and written to both manifests so the same version
can be regenerated.
"""
import argparse
import csv
import json
import os
import random
import secrets
import statistics
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta

from zf_model import (P, RULE_V2_FROM, SIM_START, SNAP, BASELINE_START, BASELINE_END,
                      make_household, make_properties, measures_for, priority_score)
from zf_sim_core import Cand, SimCore
from zf_flow_a import FlowA
from zf_flow_b import FlowB
from zf_export_rules import Recorder
from zf_manifest import file_sha256, generator_revision
from zf_export_tables import (appointment_rows, contact_rows, event_rows, property_rows,
                              resident_rows, tracker_rows)
from zf_export_other import (board_rows, capacity_rows, delay_dictionary, finance_rows,
                             hold_rows, issue_rows, quality_rows)

WAVES = [("Wave 1", date(2025, 7, 7), 280), ("Wave 2", date(2025, 10, 6), 240),
         ("Wave 3", date(2026, 1, 12), 240), ("Wave 4", date(2026, 4, 13), 120)]
N_ADHOC, N_LATE = 55, 45
WORK_CATS = {"DESIGN_WORK", "INSTALL_WORK", "ASSESSMENT_WORK", "EXIT", "DATA_CHECK"}


class Sim(FlowA, FlowB, SimCore):
    pass


def build(rng):
    props, buildings = make_properties(rng, 980)
    blocks = defaultdict(list)
    for p in props:
        blocks[p.building.building_id].append(p)
    groups = list(blocks.values())
    rng.shuffle(groups)
    houses = [g for g in groups if len(g) == 1]
    flats = [g for g in groups if len(g) > 1]
    cands, n = [], 0

    def add(p, wave, when):
        nonlocal n
        n += 1
        hh = make_household(rng, n)
        rule = "SEL-2025.1" if when < RULE_V2_FROM else "SEL-2026.1"
        m, s = measures_for(rng, p.archetype)
        cands.append(Cand(cid=f"CAND-{when.year}-{n:04d}", prop=p, hh=hh, wave=wave, identified=when,
                          rule=rule, score=priority_score(p, hh, rule, rng), measures=m, supplier=s))

    adhoc = houses[:N_ADHOC]
    late = houses[N_ADHOC:N_ADHOC + N_LATE]
    pool = flats + houses[N_ADHOC + N_LATE:]
    rng.shuffle(pool)
    wi, filled = 0, 0
    for g in pool:
        if wi >= len(WAVES):
            break
        wave, when, target = WAVES[wi]
        for p in g:
            add(p, wave, when)
        filled += len(g)
        if filled >= target:
            wi, filled = wi + 1, 0
    for g in adhoc:
        when = date(2025, 8, 1) + timedelta(days=rng.randint(0, 330))
        add(g[0], "Ad hoc", when)
    for g in late:
        when = date(2026, 7, 1) + timedelta(days=rng.randint(0, 76))
        add(g[0], "Ad hoc", when)
    used = {c.prop.property_id for c in cands}
    props = [p for p in props if p.property_id in used]
    for b in buildings:
        b.flats = [p for p in b.flats if p.property_id in used]
    buildings = [b for b in buildings if b.flats]
    cands.sort(key=lambda c: (c.identified, c.cid))
    return props, buildings, cands


def write_csv(path, rows):
    if not rows:
        return 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def validate(sim, tables):
    errs = []
    order = ["survey", "design_approved", "decision", "funding", "work_order", "install_start",
             "install_complete", "handover", "accepted"]
    for c in sim.cands:
        ds = [(k, c.dates[k]) for k in order if k in c.dates]
        for (k1, d1), (k2, d2) in zip(ds, ds[1:]):
            if d2 < d1:
                errs.append(f"{c.cid} chronology {k1}>{k2}")
        if c.dates.get("identified") and c.dates.get("survey") and c.dates["survey"] < c.identified:
            errs.append(f"{c.cid} survey before identification")
        if "work_order" in c.dates and c.hold:
            h = c.hold
            wo = c.dates["work_order"]
            if h["placed"] <= wo and (h["released"] is None or h["released"] > wo):
                errs.append(f"{c.cid} work order while safety hold active")
        if "accepted" in c.dates and not ("qa_pass" in c.dates and "evidence_accepted" in c.dates):
            errs.append(f"{c.cid} accepted without gates")
        if "work_order" in c.dates and "decision" not in c.dates:
            errs.append(f"{c.cid} released without resident decision")
    for name, rows in tables.items():
        if rows and "is_synthetic" not in rows[0]:
            errs.append(f"{name} missing is_synthetic")
        if len(rows) >= 10000:
            errs.append(f"{name} has {len(rows)} rows")
    for name, key in [("lifecycle-events", "event_id"), ("resident-contacts", "contact_id"),
                      ("appointments", "appointment_id"), ("quality-evidence", "record_id"),
                      ("safety-holds", "hold_id")]:
        ids = [r[key] for r in tables[name]]
        if len(ids) != len(set(ids)):
            errs.append(f"{name} duplicate primary keys")
    return errs


def ground_truth(sim):
    cases, segs = [], []
    total = Counter()
    for c in sim.cands:
        per = Counter()
        for cat, s, e, state, status in c.segments:
            days = (e - s).days
            segs.append(dict(candidate_id=c.cid, category=cat, state=state, start=s.isoformat(),
                             end=e.isoformat(), days=days, segment_status=status, is_synthetic="true"))
            if cat not in WORK_CATS:
                per[cat] += days
        if BASELINE_START <= c.identified <= BASELINE_END:
            total.update(per)
        primary = per.most_common(1)[0][0] if per else ""
        tracker_reason = c.exit_reason
        if "tracker_says_declined" in c.flags:
            tracker_reason = "Resident declined"
        cases.append(dict(
            candidate_id=c.cid, property_id=c.prop.property_id, identified=c.identified.isoformat(),
            in_baseline_window="Y" if BASELINE_START <= c.identified <= BASELINE_END else "N",
            true_state_at_snapshot=c.state, true_wait_category_now="" if c.closed else c.cat,
            accepted_handover="Y" if "accepted" in c.dates else "N", exit_type=c.exit_type,
            true_exit_reason=c.exit_reason, tracker_closure_reason=tracker_reason,
            primary_constraint=primary, primary_constraint_days=per[primary] if primary else 0,
            elapsed_days=((c.dates.get("accepted") or SNAP) - c.identified).days,
            lead_supplier=c.supplier, archetype=c.prop.archetype, locality=c.prop.locality,
            flags=";".join(sorted(c.flags)), is_synthetic="true"))
    return cases, segs, total


def stats(sim, cases, total):
    cs = sim.cands
    acc = [c for c in cs if "accepted" in c.dates]
    inst = [c for c in cs if c.dates.get("install_complete")]
    out = {}
    out["candidates"] = len(cs)
    out["accepted_handovers"] = len(acc)
    out["practical_completions"] = len(inst)
    out["installed_not_accepted"] = len([c for c in inst if "accepted" not in c.dates])
    out["exits"] = dict(Counter(f"{c.exit_type}: {c.exit_reason}" for c in cs if c.closed and c.exit_type != "Accepted handover"))
    out["open_by_state"] = dict(Counter(c.state for c in cs if not c.closed))
    tw = sum(total.values())
    out["baseline_wait_share_pct"] = {k: round(100 * v / tw, 1) for k, v in total.most_common()}
    out["primary_constraint_counts"] = dict(Counter(r["primary_constraint"] for r in cases if r["primary_constraint"]).most_common())

    def waits(etype_a, etype_b, filt=lambda c: True):
        res = []
        for c in cs:
            if not filt(c):
                continue
            evs = sorted(c.events, key=lambda e: e["date"])
            for i, e in enumerate(evs):
                if e["type"] == etype_a:
                    nxt = next((x for x in evs[i + 1:] if x["type"] in etype_b), None)
                    if nxt:
                        res.append((e["date"], (nxt["date"] - e["date"]).days))
        return res

    rcw = waits("DESIGN_SUBMITTED", ("DESIGN_APPROVED", "DESIGN_RETURNED"))
    bym = defaultdict(list)
    for d, w in rcw:
        bym[d.strftime("%Y-%m")].append(w)
    out["rc_queue_median_days_by_submission_month"] = {k: statistics.median(v) for k, v in sorted(bym.items())}
    for sup in ("SUP-F1", "SUP-F2", "SUP-HP", "SUP-HT"):
        v = [((c.dates.get("accepted")) - c.dates["install_complete"]).days for c in cs
             if c.supplier == sup and c.dates.get("install_complete") and c.dates.get("accepted")]
        out[f"install_to_accepted_median_{sup}"] = statistics.median(v) if v else None
        o = [(SNAP - c.dates["install_complete"]).days for c in cs if c.supplier == sup
             and c.dates.get("install_complete") and "accepted" not in c.dates and not c.closed]
        out[f"installed_open_count_{sup}"] = len(o)
    wh = [c for c in cs if c.hh.working_hours_unavailable]
    nwh = [c for c in cs if not c.hh.working_hours_unavailable]
    out["no_access_per_case_working_hours_unavailable"] = round(sum(c.n["na"] for c in wh) / max(1, len(wh)), 2)
    out["no_access_per_case_other"] = round(sum(c.n["na"] for c in nwh) / max(1, len(nwh)), 2)
    out["withdrawn_on_misrecorded_refusal"] = sum("withdrawn_on_misrecorded_refusal" in c.flags for c in cs)
    out["withdrawn_no_contact_labelled_declined"] = sum("tracker_says_declined" in c.flags for c in cs)
    hz = sim.hazards
    stale = [h for h in hz if h["stale"] and h["repair"] <= SNAP]
    out["safety_holds"] = len(hz)
    out["stale_holds_repair_done"] = len(stale)
    out["holds_open_after_repair_complete_at_snapshot"] = sum(1 for h in hz if h["repair"] <= SNAP and not h["released"])
    rl = [(h["referral"] - h["aware"]).days for h in hz if h["aware"] >= date(2025, 10, 27)]
    out["hazard_referral_lag_days_over_7_since_awaab_phase1"] = sum(1 for x in rl if x > 7)
    out["pm_dependency_cases"] = sum("pm_dependency" in c.flags for c in cs)
    out["pm_found_on_site"] = sum("pm_found_on_site" in c.flags for c in cs)
    out["post_survey_band_c"] = sum("post_survey_band_c" in c.flags for c in cs)
    out["void_window_missed"] = sum("void_window_missed" in c.flags for c in cs)
    out["block_left_behind"] = sum("block_left_behind" in c.flags for c in cs)
    out["aftercare_hazard_signal"] = sum("aftercare_hazard_signal" in c.flags for c in cs)
    sup_util = {}
    for s in ("SUP-F1", "SUP-F2", "SUP-HP", "SUP-HT"):
        sup_util[s] = len([1 for x in sim.install_starts if x[2] == s])
    out["install_starts_by_supplier"] = sup_util
    out["candidates_by_supplier"] = dict(Counter(c.supplier for c in cs))
    out["accepted_by_supplier"] = dict(Counter(c.supplier for c in acc))
    out["open_cat_counts"] = dict(Counter(c.cat for c in cs if not c.closed).most_common())
    return out


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.abspath(os.path.join(here, *[".."] * 5))
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--pack-dir", default=os.path.join(repo, "docs", "reference", "research", "retrofit-synthetic-data"))
    ap.add_argument("--key-dir", default=os.path.join(here, "..", "answer-key"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--as-of", type=date.fromisoformat, default=SNAP,
                    help="Recorded in the manifest as generated_at; never read from the clock")
    a = ap.parse_args()
    seed = a.seed if a.seed is not None else secrets.randbelow(2**31)
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

    rec = Recorder(random.Random(seed + 1))
    prop_rows, dups = property_rows(props, sim.by_prop, rec)
    tables = {
        "property-register": prop_rows,
        "candidate-lifecycle": tracker_rows(cands, rec, dups),
        "lifecycle-events": event_rows(cands, rec),
        "resident-journey": resident_rows(cands),
        "resident-contacts": contact_rows(cands, rec),
        "appointments": appointment_rows(cands, rec),
        "safety-holds": hold_rows(sim, rec),
        "quality-evidence": quality_rows(cands, rec),
        "grant-and-finance": finance_rows(sim, rec),
        "contractor-capacity": capacity_rows(sim),
        "programme-board-snapshots": board_rows(sim),
        "edge-case-returns": issue_rows(sim, rec),
        "delay-code-dictionary": delay_dictionary(),
    }
    errs = validate(sim, tables)
    cases, segs, total = ground_truth(sim)
    st = stats(sim, cases, total)
    print(json.dumps({"seed": seed, "rows": {k: len(v) for k, v in tables.items()}, "errors": errs[:20],
                      "n_errors": len(errs), "stats": st}, indent=1, default=str))
    if a.dry_run or errs:
        return
    os.makedirs(a.pack_dir, exist_ok=True)
    os.makedirs(a.key_dir, exist_ok=True)
    counts = {}
    for name, rows in tables.items():
        counts[name + ".csv"] = write_csv(os.path.join(a.pack_dir, name + ".csv"), rows)
    manifest = dict(
        warning="SYNTHETIC DATA. Fictional records for design and analysis practice. Not Zava North Homes data.",
        scenario="zava-forward-year-one", version="2.0.0", seed=seed,
        generated_at=datetime.combine(a.as_of, datetime.min.time()).isoformat(timespec="seconds"),
        as_of=a.as_of.isoformat(), generator_revision=generator_revision(),
        extract_date=SNAP.isoformat(), baseline_window=[BASELINE_START.isoformat(), BASELINE_END.isoformat()],
        simulation_start=SIM_START.isoformat(), row_counts=counts,
        file_sha256={n: file_sha256(os.path.join(a.pack_dir, n)) for n in sorted(counts)},
        generator="Held outside the knowledge base with the answer key so analysis can stay blind",
        is_synthetic=True)
    with open(os.path.join(a.pack_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    write_csv(os.path.join(a.key_dir, "ground-truth-cases.csv"), cases)
    write_csv(os.path.join(a.key_dir, "ground-truth-segments.csv"), segs)
    write_csv(os.path.join(a.key_dir, "ground-truth-anomalies.csv"), rec.anoms)
    with open(os.path.join(a.key_dir, "ground-truth-summary.json"), "w", encoding="utf-8") as f:
        json.dump(dict(seed=seed, version=manifest["version"], generator_revision=manifest["generator_revision"],
                       parameters=P, stats=st, anomaly_counts=dict(Counter(x["anomaly_type"] for x in rec.anoms)),
                       is_synthetic=True), f, indent=2, default=str)


if __name__ == "__main__":
    main()
