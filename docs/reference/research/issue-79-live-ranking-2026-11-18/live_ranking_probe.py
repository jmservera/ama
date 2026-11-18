"""Live demo probe for #79: sign in, read ranking endpoints twice, compare order. Credentials are read at runtime and never printed."""
import hashlib, json, os, re, sys
from playwright.sync_api import sync_playwright
H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
h = os.path.expanduser("~")
u = open(h + "/.ama-test-user-id").read().strip(); p = open(h + "/.ama-test-user").read().strip()
shots = sys.argv[1]
def get(pg, path):
    return pg.evaluate("async p => { const r = await fetch(p, {credentials:'include'}); return {status:r.status, body: await r.text()}; }", path)
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1440, "height": 900}); pg = c.new_page()
    pg.goto(H + "/sign-in")
    for _ in range(4):
        try:
            if pg.locator("input[name=loginfmt]").is_visible(timeout=3000):
                pg.fill("input[name=loginfmt]", u); pg.click("input[type=submit]"); pg.wait_for_timeout(1500)
            if pg.locator("input[name=passwd]").is_visible(timeout=3000):
                pg.fill("input[name=passwd]", p); pg.click("input[type=submit]"); pg.wait_for_timeout(2000)
            if pg.locator("#idBtn_Back").is_visible(timeout=2000): pg.click("#idBtn_Back"); pg.wait_for_timeout(2000)
        except Exception: pass
    pg.wait_for_load_state("networkidle")
    print("final", re.sub(r"\?.*", "", pg.url))
    out = {}
    for name, path in [("policy", "/api/ranking/policy"), ("snap1", "/api/ranking/snapshot"), ("snap2", "/api/ranking/snapshot"), ("publication", "/api/ranking/publication")]:
        r = get(pg, path); out[name] = r
        print(name, r["status"], len(r["body"]), hashlib.sha256(r["body"].encode()).hexdigest()[:16])
    json.dump(out, open("raw.json", "w"))
    try:
        pg.get_by_text(re.compile(r"Rank 1:")).first.wait_for(timeout=20000)
    except Exception as e:
        print("rank text not found", type(e).__name__)
    print("rank lines", pg.get_by_text(re.compile(r"^Rank \d+:")).count())
    pg.get_by_text(re.compile(r"^Rank \d+:")).first.scroll_into_view_if_needed()
    pg.screenshot(path=shots + "/case-list-rank-reasons.png")
    b.close()
