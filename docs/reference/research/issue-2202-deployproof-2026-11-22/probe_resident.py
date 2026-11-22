import json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent
URL = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
EMAIL, PASSWORD = (Path.home() / ".ama-resident-test-user").read_text().splitlines()[:2]
QUESTIONS = ["What does Awaab's Law require of a landlord for damp and mould?", "Which documents are missing from my case?"]
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
    res["title"] = page.title()
    page.screenshot(path=str(OUT / "screens/resident-landing.png"))
    page.fill("input[type=email], input[name=email], #email", EMAIL)
    page.fill("input[type=password]", PASSWORD)
    with page.expect_response(lambda x: x.url.endswith("/demo/login")) as ri:
        page.keyboard.press("Enter")
    res["login_status"] = ri.value.status
    page.wait_for_selector("#account:not([hidden])", timeout=90000)
    page.wait_for_timeout(3000)
    page.screenshot(path=str(OUT / "screens/resident-account.png"))
    page.click("#chat-launcher")
    page.wait_for_timeout(800)
    page.check("#assistant-consent")
    answers = []
    for q in QUESTIONS:
        page.fill("#assistant-question", q)
        with page.expect_response(lambda x: x.url.endswith("/demo/assistant"), timeout=150000) as ri:
            page.keyboard.press("Enter")
        r = ri.value
        e = {"question": q, "http": r.status}
        if r.ok:
            j = r.json()
            e.update(label=j.get("label"), routing=j.get("routing"), answer=(j.get("answer") or "")[:400])
        else:
            e["body"] = r.text()[:300]
        answers.append(e)
        page.wait_for_timeout(1500)
    res["chat"] = answers
    page.screenshot(path=str(OUT / "screens/resident-chat.png"))
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    for sel in ("#chat-close", "button:has-text('Close')"):
        try:
            page.locator(sel).first.click(timeout=1500); break
        except Exception:
            pass
    page.get_by_text("Sensors", exact=True).first.click(); page.wait_for_timeout(2500)
    h = page.get_by_text("Temperature history and 24-hour forecast").first
    h.scroll_into_view_if_needed(); page.wait_for_timeout(1000)
    page.screenshot(path=str(OUT / "screens/resident-sensors-chart.png"))
    svg = page.locator("svg:has(text)").filter(has_text="Latest stored").first
    res["chart"] = {
        "svg_found": svg.count() > 0,
        "text_px": svg.evaluate("e => [...e.querySelectorAll('text')].map(t => ({t: t.textContent.trim().slice(0,20), px: Math.round(t.getBoundingClientRect().height)}))") if svg.count() else None,
        "circles": svg.evaluate("e => e.querySelectorAll('circle').length") if svg.count() else None,
        "legend": page.get_by_text("Solid line with circles").count(),
        "latest_stored_text": page.get_by_text("Latest stored").count(),
    }
    try:
        svg.screenshot(path=str(OUT / "screens/resident-chart-svg.png"))
    except Exception:
        pass
    s = json.dumps(res, indent=1)
    assert EMAIL not in s and PASSWORD not in s
    (OUT / "probe-resident-result.json").write_text(s)
    print(s[:4000])
    b.close()
