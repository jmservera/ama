import json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent
URL = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
EMAIL, PASSWORD = (Path.home() / ".ama-resident-test-user").read_text().splitlines()[:2]
QUESTIONS = ["Which documents are missing from my case?", "How is my case going?"]
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
    page.screenshot(path=str(OUT / "screens/resident-landing-rev26.png"))
    page.fill("input[type=email], input[name=email], #email", EMAIL)
    page.fill("input[type=password]", PASSWORD)
    with page.expect_response(lambda x: x.url.endswith("/demo/login")) as ri:
        page.keyboard.press("Enter")
    res["login_status"] = ri.value.status
    page.wait_for_selector("#account:not([hidden])", timeout=90000)
    page.wait_for_timeout(3000)
    page.screenshot(path=str(OUT / "screens/resident-account-rev26.png"))
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
    page.screenshot(path=str(OUT / "screens/resident-chat-rev26.png"))
    s = json.dumps(res, indent=1)
    assert EMAIL not in s and PASSWORD not in s
    (OUT / "probe-resident-ai-rev26-result.json").write_text(s)
    print(s[:4000])
    b.close()
