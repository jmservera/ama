"""Issue 130 live UI: referral form fields, representative controls, submit outcome."""
from playwright.sync_api import sync_playwright
from common import *
CID = "ZF-2025-0331"
res = {}
with sync_playwright() as p:
    b, pg = session(p)
    pg.goto(APP + "/sign-in", wait_until="domcontentloaded"); pg.wait_for_timeout(3000)
    if "microsoftonline" in pg.url:
        if pg.locator("input[name=loginfmt]").count(): login(pg)
        else:
            pg.get_by_text(emp["user"]).first.click(); pg.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)
    pg.goto(APP + f"/app#/case/{CID}", wait_until="networkidle"); pg.wait_for_timeout(3000)
    pg.get_by_role("tab", name="Resident").first.click(); pg.wait_for_timeout(1000)
    forms = pg.locator("form").evaluate_all("fs=>fs.map(f=>({id:f.id,labels:[...f.querySelectorAll('label')].map(l=>l.innerText.trim().slice(0,80))}))")
    res["forms"] = [f for f in forms if f["id"].startswith(("nomination", "challenge", "ru-"))]
    rep = pg.get_by_role("heading", name="Representative authority").first.locator("xpath=ancestor::section[1]")
    res["rep_section_text"] = scrub(rep.inner_text()[:800]) if rep.count() else None
    nom = pg.get_by_role("heading", name="Nominations and self-referrals").first.locator("xpath=ancestor::section[1]")
    res["nom_section_text"] = scrub(nom.inner_text()[:2500]) if nom.count() else None
    chal = pg.get_by_role("heading", name="Challenge a suggestion or ask for a correction").first.locator("xpath=ancestor::section[1]")
    res["challenge_text"] = scrub(chal.inner_text()[:1200]); chal.screenshot(path=f"{OUT}/challenge-panel.png")
    nom.scroll_into_view_if_needed()
    nom.screenshot(path=f"{OUT}/nomination-panel.png")
    rep.screenshot(path=f"{OUT}/representative-panel.png")
    b.close()
json.dump(res, open(f"{OUT}/ui2.json", "w"), indent=1); print(json.dumps(res, indent=1)[:5000])
