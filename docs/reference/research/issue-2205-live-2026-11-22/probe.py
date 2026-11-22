"""Live read of the staff assistants registry for issue 2205. Credentials are read at runtime and never printed."""
import json, os, re
from playwright.sync_api import sync_playwright

EMP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")
user, pw = rd(".ama-test-user-id")[0].strip(), rd(".ama-test-user")[0].strip()
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")
scrub = lambda x: json.loads(EMAIL.sub("[email]", json.dumps(x)))

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_context(viewport={"width": 1366, "height": 1000}).new_page()
    page.goto(EMP + "/api/me", wait_until="domcontentloaded", timeout=120000)
    page.fill("input[name=loginfmt]", user); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", pw); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(EMP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(EMP)), timeout=60000)
    page.goto(EMP + "/api/assistants", wait_until="networkidle")
    js = "async p=>{const x=await fetch(p,{headers:{'X-ZF-CSRF':'1'}});return [x.status,await x.json()]}"
    s, j = page.evaluate(js, "/api/assistants")
    page.screenshot(path=f"{OUT}/registry.png")
    keys = sorted(j) if isinstance(j, dict) else None
    out = {"status": s, "keys": keys, "quality_scope": j.get("quality_scope") if isinstance(j, dict) else None}
    items = j.get("assistants") if isinstance(j, dict) else None
    if items is None and isinstance(j, dict):
        items = j.get("items")
    out["quality_entries"] = [x for x in (items or []) if "quality" in json.dumps(x).lower()][:3]
    json.dump(scrub(out), open(f"{OUT}/registry.json", "w"), indent=2)
    b.close()
