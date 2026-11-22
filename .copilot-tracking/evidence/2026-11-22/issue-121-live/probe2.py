"""Live demo probe for issue 121 re-check on revision 0000053. Reads credentials at runtime; GET only; redacts emails."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")
emp = {"user": rd(".ama-test-user-id")[0].strip(), "pw": rd(".ama-test-user")[0].strip()}
CANARY = re.compile(r"vulnerab|disabilit|health|medical|adjustment|reason", re.I)

def login(page):
    page.fill("input[name=loginfmt]", emp["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", emp["pw"]); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP): break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)

def keys(o, pre=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield pre + k
            yield from keys(v, pre + k + ".")
    elif isinstance(o, list):
        for v in o[:5]:
            yield from keys(v, pre + "[].")

def redact(t):
    return re.sub(r"[\w.+-]+@[\w.-]+", "[email]", t)

out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded"); login(page)
    for path in ["/api/me", "/api/data-protection", "/api/retention", "/api/audit-check", "/api/documents", "/api/rights"]:
        r = c.request.get(APP + path)
        try: j = r.json()
        except Exception: j = {"raw": redact(r.text())[:300]}
        out[path] = {"status": r.status, "body": json.loads(redact(json.dumps(j)))}
    page.goto(APP + "/api/data-protection"); page.screenshot(path="docs/reference/research/issue-121-live-data-protection-register-2026-11-22.png")
    b.close()
json.dump(out, open(f"{OUT}/probe2.json", "w"), indent=1)
print({k: v["status"] for k, v in out.items()})
