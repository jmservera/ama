"""Issue 130 live probe: nomination route read and write attempts (synthetic demo)."""
from playwright.sync_api import sync_playwright
from common import *

CID = "ZF-2025-0331"
res = {}
with sync_playwright() as p:
    b, pg = session(p)
    s, d = call(pg, "GET", f"/api/cases/{CID}")
    res["case_status"] = s
    res["permission_keys"] = sorted((d.get("nomination_permissions") or {}).keys())
    perms = d["nomination_permissions"]
    res["perms_scrubbed"] = scrub({k: (v if not isinstance(v, list) else f"list[{len(v)}]") for k, v in perms.items()})
    res["n_records"] = len(d.get("nomination_records") or [])
    owners = perms["staff_owners"]
    base = dict(action="nomination_record", case_id=CID, kind="Nomination", reported_subject_ref="SYN-REF-130-A",
                account="Synthetic demo: officer nominates this home after a resident phone call.",
                source="Synthetic call note 130-A", channel="staff_recorded_non_digital", assisted_channel="phone",
                owner=owners[0]["email"], acknowledgement_ref="Synthetic acknowledgement 130-A",
                next_update="2026-12-02", non_digital_route="Housing office phone line, staffed weekdays",
                hazard_concern=False)
    def post(body):
        s, j = call(pg, "POST", f"/api/cases/{CID}/resident", body)
        return scrub({"status": s, "err": j.get("error") if isinstance(j, dict) else j})
    res["record_valid"] = post(base)
    res["record_owner_not_staff"] = post(dict(base, owner="nobody.synthetic@example.invalid"))
    res["record_owner_role_name"] = post(dict(base, owner="Retrofit Programme Manager"))
    res["record_unknown_hazard_null"] = post(dict(base, hazard_concern=None))
    res["record_representative_fields"] = post(dict(base, representative_ref="SYN-REP-1", raised_by="Representative"))
    s, d2 = call(pg, "GET", f"/api/cases/{CID}")
    res["n_records_after"] = len(d2.get("nomination_records") or [])
    res["stage_unchanged"] = (d.get("stage"), d.get("days_in_stage")) == (d2.get("stage"), d2.get("days_in_stage"))
    s, h = call(pg, "GET", f"/api/cases/{CID}?view=nomination-routes-html")
    res["html_status"] = s
    res["html_excerpt"] = scrub(str(h)[:1500])
    pg.goto(APP + f"/api/cases/{CID}?view=nomination-routes-html", wait_until="networkidle")
    pg.screenshot(path=f"{OUT}/route-view.png", full_page=True)
    b.close()
json.dump(res, open(f"{OUT}/probe1.json", "w"), indent=1, default=str); print(json.dumps(res, indent=1, default=str)[:6000])
