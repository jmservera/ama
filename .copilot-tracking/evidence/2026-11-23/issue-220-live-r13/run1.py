"""Issue 220 r13 live probe: adverse-key variants against the live revision (synthetic case)."""
import hashlib
from playwright.sync_api import sync_playwright
from common import *

CID = "ZF-2025-0331"
PROT = ("stage", "days_in_stage", "closed", "resident", "hazards", "measure_decisions", "resident_reviews",
        "resident_scopes", "resident_update", "tenure_review_required", "tenure_reports")
VARIANTS = ("Retaliation_Flag", " refusal", "hazard-pause", "HAZARD_PAUSE", "priority penalty")
res = {"case": CID}


def snap(pg):
    s, d = call(pg, "GET", f"/api/cases/{CID}")
    return d, {k: hashlib.sha256(json.dumps(d.get(k), sort_keys=True).encode()).hexdigest()[:12] for k in PROT if k in d}


with sync_playwright() as p:
    b, pg = session(p)
    d0, h0 = snap(pg)
    res["n_before"] = len(d0.get("nomination_records") or [])
    owner = d0["nomination_permissions"]["staff_owners"][0]["email"]
    base = dict(case_id=CID, kind="Self-referral", reported_subject_ref="SYN-REF-220-B",
                account="Synthetic r13 probe: key-variant check.", source="Synthetic call note 220-B",
                channel="staff_recorded_non_digital", assisted_channel="phone", owner=owner,
                acknowledgement_ref="Synthetic acknowledgement 220-B", next_update="2026-12-02",
                non_digital_route="Housing office phone line, staffed weekdays", hazard_concern=False)
    res["variants"] = {}
    for v in VARIANTS:
        s, j = call(pg, "POST", f"/api/cases/{CID}/resident", dict(action="nomination_record", **dict(base, **{v: True})))
        res["variants"][v] = scrub({"status": s, "err": j.get("error") if isinstance(j, dict) else None})
    d1, h1 = snap(pg)
    res["n_after"] = len(d1.get("nomination_records") or [])
    res["protected_hashes_equal"] = h1 == h0
    b.close()
json.dump(res, open(f"{OUT}/run1.json", "w"), indent=1, default=str)
print(json.dumps(res, indent=1, default=str))
