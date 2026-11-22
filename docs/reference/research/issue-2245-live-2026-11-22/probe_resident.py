"""Issue 2243 live resident chat probe. Credentials are read at run time and never printed."""
import json, os, re, sys
from playwright.sync_api import sync_playwright

RES = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
TAG = sys.argv[1] if len(sys.argv) > 1 else "run"
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")
ru, rp = [x.strip() for x in rd(".ama-resident-test-user")[:2]]
mask = lambda s: re.sub(r"[\w.+-]+@[\w.-]+", "[email]", s)
QS = ["How is my case going?", "I smelled something odd near the vent, what should I do?"]
R = {"tag": TAG, "http": [], "asks": []}
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    page = c.new_page()

    def on_resp(r):
        if r.request.method == "POST" and "/demo/" in r.url and "login" not in r.url:
            row = {"path": r.url.split("//")[1].split("/", 1)[1][:60], "status": r.status}
            try:
                j = r.json()
                row["keys"] = sorted(j.keys())[:20]
                for k in ("label", "model", "source", "answer_source", "ai_used", "generated"):
                    if k in j:
                        row[k] = j[k]
            except Exception:
                pass
            R["http"].append(row)

    page.on("response", on_resp)
    page.goto(RES + "/", wait_until="load", timeout=180000)
    page.wait_for_selector("#signin:not([hidden]), #content:not([hidden])", timeout=120000)
    if page.locator("#signin").is_visible():
        page.fill("#email", ru); page.fill("#password", rp); page.click("#signin-button")
    page.wait_for_selector("#content:not([hidden])", timeout=120000)
    page.wait_for_timeout(2500)
    page.locator("#chat-launcher").click()
    page.wait_for_selector("#assistant-question", state="visible", timeout=30000)
    box = page.locator("#assistant-consent")
    if not box.is_checked():
        box.check()
    for q in QS:
        page.fill("#assistant-question", q)
        page.get_by_role("button", name="Send", exact=True).click()
        page.wait_for_timeout(12000)
        R["asks"].append({"question": q, "result": mask(page.locator("#assistant-result").inner_text())[-1200:]})
        page.screenshot(path=f"{OUT}/{TAG}-resident.png")
    b.close()
txt = json.dumps(R, indent=1)
assert ru not in txt and rp not in txt
open(f"{OUT}/{TAG}_resident_probe.json", "w").write(txt)
print(txt[:3500])
