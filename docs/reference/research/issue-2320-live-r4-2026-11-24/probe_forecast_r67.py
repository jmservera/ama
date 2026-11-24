"""Repeat forecast probe (#2304/#2320): body fields that say whether the answer is fresh or last-good. Sign-in read at run time."""
import json, os, time
from playwright.sync_api import sync_playwright
H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
u = open(home + "/.ama-test-user-id").read().strip()
p = open(home + "/.ama-test-user").read().strip()

def login(page):
    page.goto(H + "/sign-in")
    for _ in range(4):
        try:
            if page.locator("input[name=loginfmt]").is_visible(timeout=3000):
                page.fill("input[name=loginfmt]", u)
                page.click("input[type=submit]")
                page.wait_for_timeout(1500)
            if page.locator("input[name=passwd]").is_visible(timeout=3000):
                page.fill("input[name=passwd]", p)
                page.click("input[type=submit]")
                page.wait_for_timeout(2000)
            if page.locator("#idBtn_Back").is_visible(timeout=2000):
                page.click("#idBtn_Back")
                page.wait_for_timeout(2000)
        except Exception:
            pass
    try:
        page.wait_for_load_state("networkidle", timeout=60000)
    except Exception:
        pass



JS = """async (path) => {const t0=performance.now();const r=await fetch(path,{credentials:'same-origin'});let j=null;try{j=await r.json()}catch(e){}return {status:r.status,ms:Math.round(performance.now()-t0),json:j}}"""
out = []
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(); pg = c.new_page()
    login(pg); pg.goto(H + "/app"); pg.wait_for_timeout(3000)
    for i in range(8):
        r = pg.evaluate(JS, "/api/assistants/forecast"); j = r["json"] or {}
        out.append({"utc": time.strftime("%H:%M:%S", time.gmtime()), "status": r["status"], "seconds": round(r["ms"]/1000, 2),
                    "basis": str(j.get("basis"))[:160], "stale_seconds": j.get("stale_seconds"), "state": j.get("state"),
                    "keys": sorted(j)[:6] if r["status"] != 200 else None})
    s = json.dumps(out, indent=1); assert u not in s and p not in s
    open(os.path.join(OUT, "probe-forecast-r67.json"), "w").write(s); print(s)
    b.close()
