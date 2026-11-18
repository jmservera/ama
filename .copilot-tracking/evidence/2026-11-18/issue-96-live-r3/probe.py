"""Read-only live probe of form schemas on the demo API (issue 96, run 3). Credentials are read at run time and never written."""
import json, os, re
from playwright.sync_api import sync_playwright

import os
APP = os.environ["DEMO_API_URL"]
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")[0].strip()
user, pw = rd(".ama-test-user-id"), rd(".ama-test-user")


def login(page):
    page.fill("input[name=loginfmt]", user); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", pw); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)


out = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1366, "height": 900})
    page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    login(page)
    me = c.request.get(APP + "/api/me").json()
    out["role"] = me["user"]["role"]
    for path in ("/api/form-schemas", "/api/form-schemas.csv"):
        r = c.request.get(APP + path)
        t = r.text()
        ent = {"status": r.status, "ctype": (r.headers.get("content-type") or "")[:40], "len": len(t), "body": t[:300]}
        if r.status == 200 and "json" in ent["ctype"]:
            ent["schema_count"] = len(r.json().get("schemas", []))
        out[path] = ent
    page.goto(APP + "/api/form-schemas", wait_until="domcontentloaded")
    page.screenshot(path=f"{OUT}/form-schemas-response.png")
    b.close()
blob = json.dumps(out, indent=1)
assert user not in blob and pw not in blob
open(f"{OUT}/probe.json", "w").write(blob)
print(blob)
