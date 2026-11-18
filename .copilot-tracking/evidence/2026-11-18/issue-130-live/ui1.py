"""Issue 130 live UI probe: Resident tab, referral form, submit attempt."""
from playwright.sync_api import sync_playwright
from common import *
CID = "ZF-2025-0331"
res = {}
with sync_playwright() as p:
    b, pg = session(p)
    res["me_status"] = call(pg, "GET", "/api/me")[0]
    pg.goto(APP + "/sign-in", wait_until="domcontentloaded")
    if "microsoftonline" in pg.url:
        pg.wait_for_timeout(3000)
        if pg.locator("input[name=loginfmt]").count(): login(pg)
        else:
            pg.get_by_text(emp["user"]).first.click()
            pg.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)
    pg.wait_for_timeout(2000)
    res["after_signin_url_path"] = pg.url.replace(APP, "")[:60]
    pg.goto(APP + f"/app#/case/{CID}", wait_until="networkidle")
    pg.wait_for_timeout(3000)
    tab = pg.get_by_role("tab", name="Resident")
    res["resident_tab"] = tab.count()
    if tab.count():
        tab.first.click(); pg.wait_for_timeout(1000)
    heads = pg.locator("h2, h3").all_inner_texts()
    res["headings_with_referral"] = [t for t in heads if any(w in t.lower() for w in ("referral", "nominat", "challenge", "represent"))]
    forms = pg.locator("form").evaluate_all("fs=>fs.map(f=>({id:f.id,fields:[...f.elements].map(e=>e.name).filter(Boolean)}))")
    res["forms"] = [f for f in forms if any("nomin" in (n or "") or n in ("reported_subject_ref","account","channel","owner") for n in f["fields"]) or "nomin" in f["id"]]
    res["rep_selector_options"] = pg.locator("select[name='representative_ref'] option").all_inner_texts()
    pg.screenshot(path=f"{OUT}/resident-tab.png", full_page=True)
    b.close()
json.dump(scrub(res), open(f"{OUT}/ui1.json", "w"), indent=1); print(json.dumps(scrub(res), indent=1)[:3500])
