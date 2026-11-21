import json, os, time
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT = Path(__file__).parent
URL = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
EMAIL, PASSWORD = (Path.home() / ".ama-resident-test-user").read_text().splitlines()[:2]
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1440, "height": 900}); page = ctx.new_page()
    for _ in range(8):
        try:
            if page.request.get(URL + "/demo/session", timeout=60000).status == 200:
                break
        except Exception:
            time.sleep(5)
    page.goto(URL + "/", wait_until="networkidle", timeout=90000)
    page.fill("input[type=email], input[name=email], #email", EMAIL)
    page.fill("input[type=password]", PASSWORD)
    with page.expect_response(lambda x: x.url.endswith("/demo/login")) as ri:
        page.keyboard.press("Enter")
    res["login_status"] = ri.value.status
    page.wait_for_selector("#account:not([hidden])", timeout=90000); page.wait_for_timeout(2500)
    sec = page.locator("#sec-sensors")
    res["sensors_section"] = sec.inner_text() if sec.count() else None
    res["sensor_consent_checkbox_count"] = page.locator("#sec-sensors input[type=checkbox]").count()
    hs = page.locator("section:has(h2:text('Help with your case'))")
    res["chat_copy"] = hs.inner_text()[:1100]
    res["chat_control_ids"] = [e.evaluate("e => e.id") for e in hs.locator("input, textarea, select").all()]
    res["headings"] = page.locator("h2").all_inner_texts()[:14]
    page.screenshot(path=str(OUT / "screens/resident-signed-in.png"), full_page=True)
    s = json.dumps(res, indent=1)
    assert EMAIL not in s and PASSWORD not in s
    (OUT / "probe-resident-result.json").write_text(s); print(s[:3500])
    b.close()
