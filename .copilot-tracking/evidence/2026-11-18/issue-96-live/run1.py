"""Read-only live probe of form schemas on the demo API (issue 96). Credentials are read at run time."""
import json
import pathlib
from playwright.sync_api import sync_playwright

BASE = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = pathlib.Path(__file__).parent
home = pathlib.Path.home()
user = (home / ".ama-test-user-id").read_text().strip()
pw = (home / ".ama-test-user").read_text().strip()
result = {}

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1366, "height": 900})
    page = ctx.new_page()
    page.goto(BASE + "/sign-in", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    try:
        page.fill("input[type=email]", user)
        page.click("input[type=submit]")
        page.wait_for_selector("input[type=password]", timeout=20000)
        page.fill("input[type=password]", pw)
        page.click("input[type=submit]")
        page.wait_for_timeout(3000)
        for sel in ("#idBtn_Back", "input[type=submit]"):
            if page.locator(sel).count():
                page.locator(sel).first.click()
                break
    except Exception as e:  # recorded, not fatal
        result["login_note"] = type(e).__name__
    page.wait_for_url(BASE + "/**", timeout=40000)
    page.goto(BASE + "/app", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    for name, path in (("me", "/api/me"), ("schemas", "/api/form-schemas"), ("csv", "/api/form-schemas.csv")):
        r = ctx.request.get(BASE + path)
        body = r.text()
        result[name] = {"status": r.status, "length": len(body), "body": body[:6000]}
    page.screenshot(path=str(OUT / "workbench.png"))
    b.close()

for v in (user, pw):
    assert v not in json.dumps(result), "credential leaked"
(OUT / "run1.json").write_text(json.dumps(result, indent=1))
print({k: (v["status"], v["length"]) if isinstance(v, dict) else v for k, v in result.items()})
