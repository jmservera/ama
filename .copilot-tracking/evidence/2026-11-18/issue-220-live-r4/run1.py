"""Issue 220 live proof: non-retaliation, no inferred refusal, no delayed hazard response (synthetic case)."""
import hashlib
from playwright.sync_api import sync_playwright
from common import *

CID = "ZF-2025-0331"
PROT = ("stage", "days_in_stage", "closed", "resident", "hazards", "measure_decisions", "resident_reviews",
        "resident_scopes", "resident_update", "tenure_review_required", "tenure_reports")
res = {"case": CID}


def snap(pg):
    s, d = call(pg, "GET", f"/api/cases/{CID}")
    sh = {k: hashlib.sha256(json.dumps(d.get(k), sort_keys=True).encode()).hexdigest()[:12] for k in PROT if k in d}
    return d, sh


def act(pg, body):
    s, j = call(pg, "POST", f"/api/cases/{CID}/resident", body)
    return s, j


with sync_playwright() as p:
    b, pg = session(p)
    d0, h0 = snap(pg)
    res["before"] = {"hashes": h0, "stage": d0.get("stage"), "days_in_stage": d0.get("days_in_stage"),
                     "hazard_state": [(h.get("state"), h.get("noticed"), h.get("hold")) for h in d0.get("hazards", [])],
                     "awaiting_hazard_action": d0.get("awaiting_hazard_action"),
                     "n_nominations": len(d0.get("nomination_records") or [])}
    base = dict(case_id=CID, kind="Self-referral", reported_subject_ref="SYN-REF-220-A",
                account="Synthetic demo: resident disputes the recorded damp finding and asks for a correction.",
                source="Synthetic phone call note 220-A", channel="staff_recorded_non_digital", assisted_channel="phone",
                owner=None, acknowledgement_ref="Synthetic acknowledgement call 220-A",
                next_update="2026-12-02", non_digital_route="Housing office phone line, staffed weekdays",
                hazard_concern=False)
    perms = d0["nomination_permissions"]["staff_owners"]
    res["owner_options"] = len(perms)
    owner_email = perms[0]["email"]
    base["owner"] = owner_email
    s, j = act(pg, dict(action="nomination_record", **base))
    res["record"] = scrub({"status": s, "err": j.get("error") if isinstance(j, dict) else j})
    d1, h1 = snap(pg)
    noms = d1.get("nomination_records") or []
    res["after_record"] = {"hashes_equal": h1 == h0, "n_nominations": len(noms)}
    nid = noms[-1]["id"] if noms else None
    if nid:
        n = noms[-1]
        res["record_view"] = scrub({k: n.get(k) for k in ("id", "version", "owner", "next_update", "non_digital_route", "review_status")}
                                   | {"channel": n["original"].get("channel"), "route_mode": n["original"].get("route_mode")})
        s, j = act(pg, dict(action="nomination_correct", case_id=CID, id=nid, expected_version=n["version"],
                            reported_subject_ref="SYN-REF-220-A", account="Synthetic corrected account: the mould was cleared in March.",
                            source="Synthetic correction evidence 220-A", channel="digital", next_update="2026-12-09",
                            challenge_id=None, raised_by="Officer", hazard_concern=False))
        res["correct"] = scrub({"status": s, "err": j.get("error") if isinstance(j, dict) else None})
        d2, h2 = snap(pg)
        n2 = next((x for x in d2.get("nomination_records", []) if x["id"] == nid), {})
        res["after_correct"] = {"hashes_equal_to_before": h2 == h0, "assurance": n2.get("assurance"),
                                "review_status": n2.get("review_status"),
                                "re_review": (n2.get("corrections") or [{}])[-1].get("re_review"),
                                "stage": d2.get("stage"), "days_in_stage": d2.get("days_in_stage"),
                                "hazards_state": [(h.get("state"), h.get("hold", {}).get("status")) for h in d2.get("hazards", [])]}
        res["guarantees"] = d2.get("challenge_guarantees"); res["assurance_block"] = d2.get("challenge_assurance")
    # adverse inputs
    s, j = act(pg, dict(action="nomination_record", **dict(base, hazard_concern=True)))
    res["hazard_true"] = scrub({"status": s, "keys": sorted(j.keys()), "route": {k: j.get(k) for k in ("action", "endpoint", "message")}})
    d3, h3 = snap(pg); res["after_hazard_true"] = {"hashes_equal": h3 == h0, "n_nominations": len(d3.get("nomination_records") or [])}
    for fld in ("retaliation_flag", "refusal", "hazard_pause", "priority_penalty"):
        s, j = act(pg, dict(action="nomination_record", **dict(base, **{fld: True})))
        res.setdefault("forbidden_fields", {})[fld] = scrub({"status": s, "err": j.get("error")})
    s, j = act(pg, dict(action="nomination_record", **{k: v for k, v in base.items() if k != "hazard_concern"}))
    res["hazard_missing"] = scrub({"status": s, "keys": sorted(j.keys())})
    d4, h4 = snap(pg); res["final_hashes_equal"] = h4 == h0
    res["final_n_nominations"] = len(d4.get("nomination_records") or [])
    s, h = call(pg, "GET", f"/api/cases/{CID}?view=nomination-routes-html")
    res["html_has_protection"] = ("will not change your tenancy" in str(h)) or ("not be held against" in str(h)) or ("hazard" in str(h).lower())
    pg.goto(APP + f"/api/cases/{CID}?view=nomination-routes-html", wait_until="networkidle")
    pg.screenshot(path=f"{OUT}/route-view.png", full_page=True)
    b.close()
json.dump(res, open(f"{OUT}/run1.json", "w"), indent=1, default=str); print(json.dumps(res, indent=1, default=str)[:7000])
