import json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent
URL = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
EMAIL, PASSWORD = (Path.home() / ".ama-resident-test-user").read_text().splitlines()[:2]
QUESTIONS = ["Which documents are missing from my case?", "I can see damp and mould in my bedroom, who can help?"]
res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
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
    page.wait_for_selector("#account:not([hidden])", timeout=90000)
    page.wait_for_timeout(3000)
    cb = page.locator("#sensor-consent")
    res["sensor_consent_checkbox_count"] = cb.count()
    if cb.count():
        res["sensor_consent_checked"] = cb.is_checked()
        res["sensor_consent_status"] = page.locator("#sensor-consent-status").inner_text()
        res["sensor_consent_label"] = page.locator("label.check:has(#sensor-consent)").inner_text()
        cb.scroll_into_view_if_needed()
        page.screenshot(path=str(OUT / "screens/resident-consent-checkbox.png"))
        original = cb.is_checked()
        steps = []
        for wanted in (False, True):
            if cb.is_checked() == wanted:
                steps.append({"wanted": wanted, "skipped": "already in that state"})
                continue
            with page.expect_response(lambda x: x.url.endswith("/demo/sensor-consent"), timeout=150000) as rc:
                cb.set_checked(wanted)
            page.wait_for_timeout(1500)
            steps.append({"wanted": wanted, "http": rc.value.status, "checked_after": cb.is_checked(),
                          "status": page.locator("#sensor-consent-status").inner_text()})
            page.screenshot(path=str(OUT / f"screens/resident-consent-{'granted' if wanted else 'declined'}.png"))
        res["consent_toggle"] = steps
        res["consent_original"] = original
        res["consent_final_checked"] = cb.is_checked()
    res["sensor_section"] = page.locator("#sec-sensors").inner_text()[:700] if page.locator("#sec-sensors").count() else None
    page.click("#chat-launcher")
    page.wait_for_timeout(800)
    page.check("#assistant-consent")
    answers = []
    for q in QUESTIONS:
        page.fill("#assistant-question", q)
        with page.expect_response(lambda x: x.url.endswith("/demo/assistant"), timeout=120000) as ri:
            page.keyboard.press("Enter")
        r = ri.value
        entry = {"question": q, "http": r.status}
        if r.ok:
            j = r.json()
            entry.update(label=j.get("label"), routing=j.get("routing"), answer=(j.get("answer") or "")[:300])
        else:
            entry["body"] = r.text()[:300]
        answers.append(entry)
        page.wait_for_timeout(1500)
    res["chat"] = answers
    page.screenshot(path=str(OUT / "screens/resident-chat-routing.png"))
    s = json.dumps(res, indent=1)
    assert EMAIL not in s and PASSWORD not in s
    (OUT / "probe-resident-result.json").write_text(s)
    print(s[:4500])
    b.close()
