"""Read-only live continuity probe (issue 122). Credentials read at runtime, never printed; only structure is emitted."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
rd = lambda n: open(os.path.join(os.path.expanduser("~"), n)).read().split("\n")[0].strip()
user, pw = rd(".ama-test-user-id"), rd(".ama-test-user")

def shape(v, depth=0):
    if isinstance(v, dict):
        return {k: shape(x, depth + 1) for k, x in v.items()} if depth < 3 else "{...}"
    if isinstance(v, list):
        return [len(v), shape(v[0], depth + 1)] if v else []
    return v if isinstance(v, (bool, int, float)) or v is None else (v if len(str(v)) < 80 and "@" not in str(v) else "<str>")

with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    out = {}
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    page.fill("input[name=loginfmt]", user); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", pw); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP): break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)
    me = c.request.get(APP + "/api/me").json().get("user", {})
    out["role"] = me.get("role")
    for path in ["/api/continuity", "/api/continuity/export"]:
        r = c.request.get(APP + path); out[path] = {"status": r.status}
        if r.status == 200:
            d = r.json(); out[path]["shape"] = shape(d)
            open(f"{OUT}/{path.strip('/').replace('/', '-')}.redacted.json", "w").write(json.dumps(shape(d), indent=1))
        else:
            out[path]["body"] = r.text()[:200]
    b.close()
print(json.dumps(out, indent=1)[:6000])
