"""Issue 130 run 4: form-encoded submission and UI form on the Resident tab (synthetic demo)."""
from playwright.sync_api import sync_playwright
from common import *

CID = "ZF-2025-0331"
res = {}
with sync_playwright() as p:
    b, pg = session(p)
    d = call(pg, "GET", f"/api/cases/{CID}")[1]
    owner = d["nomination_permissions"]["staff_owners"][0]["email"]
    form = pg.evaluate("""async([cid,owner])=>{
      const body=new URLSearchParams({action:'nomination_record',case_id:cid,kind:'Nomination',reported_subject_ref:'SYN-REF-130-B',
       account:'Synthetic form-encoded nomination',source:'Synthetic note 130-B',channel:'staff_recorded_non_digital',assisted_channel:'phone',
       owner:owner,acknowledgement_ref:'Synthetic ack 130-B',next_update:'2026-12-02',non_digital_route:'Housing office phone line',hazard_concern:'false'});
      const x=await fetch('/api/cases/'+cid+'/resident',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded','X-ZF-CSRF':'1'},body});
      const t=await x.text();return [x.status,t.slice(0,400)]}""", [CID, owner])
    res["form_encoded"] = scrub(form)
    pg.goto(APP + f"/app#/case/{CID}", wait_until="networkidle")
    pg.wait_for_timeout(2500)
    try:
        pg.get_by_role("tab", name="Resident").click(timeout=8000)
    except Exception as e:
        res["tab_click"] = str(e)[:200]
    pg.wait_for_timeout(1500)
    res["panels"] = {t: pg.get_by_text(t).count() for t in ["Representative authority", "Nominations and self-referrals", "Challenge a suggestion or ask for a correction"]}
    res["rep_options"] = pg.locator("select[name=representative_ref] option").count()
    pg.screenshot(path=f"{OUT}/resident-tab-1366.png", full_page=True)
    res["n_records_after"] = len(call(pg, "GET", f"/api/cases/{CID}")[1].get("nomination_records") or [])
    b.close()
json.dump(res, open(f"{OUT}/probe2.json", "w"), indent=1, default=str); print(json.dumps(res, indent=1, default=str)[:3000])
