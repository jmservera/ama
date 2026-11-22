"""Item 2 (resident): one non-safety question, record the label. Sign-in read at run time, never printed. Usage: probe_resident_ai.py [tag]"""
import json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent
URL = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
EMAIL, PASSWORD = (Path.home() / ".ama-resident-test-user").read_text().splitlines()[:2]
tag = sys.argv[1] if len(sys.argv) > 1 else "a"
Q = "How is my case going?"
res = {"tag": tag, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
with sync_playwright() as p:
    b = p.chromium.launch(); page = b.new_context(viewport={"width": 1440, "height": 900}).new_page()
    page.goto(URL + "/", wait_until="networkidle", timeout=90000)
    page.fill("input[type=email], input[name=email], #email", EMAIL); page.fill("input[type=password]", PASSWORD)
    page.keyboard.press("Enter"); page.wait_for_selector("#account:not([hidden])", timeout=90000); page.wait_for_timeout(3000)
    page.click("#chat-launcher"); page.wait_for_timeout(800); page.check("#assistant-consent")
    page.fill("#assistant-question", Q)
    with page.expect_response(lambda x: x.url.endswith("/demo/assistant"), timeout=150000) as ri:
        page.keyboard.press("Enter")
    r = ri.value; res["http"] = r.status
    if r.ok:
        j = r.json(); res.update(label=j.get("label"), routing=(j.get("routing") or {}).get("agent"), answer=(j.get("answer") or "")[:500])
    page.wait_for_timeout(1500)
    page.screenshot(path=str(OUT / f"screens/resident-ai-{tag}.png"))
    s = json.dumps(res, indent=1); assert EMAIL not in s and PASSWORD not in s
    (OUT / f"probe-resident-ai-{tag}.json").write_text(s); print(s); b.close()
