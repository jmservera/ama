"""Issue 350 pass 9: retry the two endpoints that returned 503. GET only; credentials read at runtime, never printed."""
import os, re, time, json
from playwright.sync_api import sync_playwright
APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
home = os.path.expanduser("~")
user = open(os.path.join(home, ".ama-test-user-id")).read().split("\n")[0].strip()
pw = open(os.path.join(home, ".ama-test-user")).read().split("\n")[0].strip()
out = []
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    page.fill("input[name=loginfmt]", user); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", pw); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP): break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception: break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)
    for i in range(6):
        for ep in ("/api/assistants", "/api/briefing", "/api/assistants/forecast"):
            t = time.time(); r = c.request.get(APP + ep, timeout=60000)
            out.append({"try": i, "ep": ep, "status": r.status, "secs": round(time.time() - t, 1), "retry_after": r.headers.get("retry-after")})
        time.sleep(10)
    b.close()
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw", "06-retry.json"), "w").write(json.dumps(out, indent=1))
print(json.dumps(out))
