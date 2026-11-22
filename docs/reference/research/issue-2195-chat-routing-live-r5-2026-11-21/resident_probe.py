"""Issue 2195 resident live routing probe. Credentials read at runtime, never printed."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
lines = [x.strip() for x in open(os.path.expanduser("~/.ama-resident-test-user")).read().split("\n") if x.strip()]
email, pw = lines[0], lines[1]
R = {"http": []}
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_context(viewport={"width": 1280, "height": 900}).new_page()
    page.on("response", lambda r: R["http"].append([r.request.method, re.sub(r"^https?://[^/]+", "", r.url)[:50], r.status]) if r.request.method == "POST" else None)
    page.goto(APP + "/", wait_until="load", timeout=120000)
    page.fill("#email", email); page.fill("#password", pw)
    page.click("#signin-form button[type=submit]")
    page.wait_for_selector("#content:not([hidden])", timeout=60000)
    R["buttons"] = [x.strip() for x in page.locator("button").all_inner_texts() if x.strip()][:20]
    page.get_by_role("button", name=re.compile("Help with your case|Ask|chat", re.I)).first.click()
    box = page.get_by_role("dialog").first
    box.wait_for(timeout=15000)
    R["dialog_text"] = box.inner_text()[:400]
    R["qs"] = []
    for key, text in [("status", "How is my case going?"), ("documents", "Which documents do I need to upload?"), ("none", "What is the weather like?")]:
        n0 = len(R["http"])
        page.check("#assistant-consent")
        ta = page.locator("#assistant-question")
        ta.fill(text); ta.press("Enter")
        n_before = len(re.findall(r"(Routed to the|Handled by the)", box.inner_text()))
        try:
            page.wait_for_function("n => (document.body.innerText.match(/(Routed to the|Handled by the)/g) || []).length > n", arg=n_before, timeout=45000)
        except Exception:
            pass
        page.wait_for_timeout(1000)
        r = re.findall(r"(?:Routed to the|Handled by the)[^\n]*", box.inner_text())
        R["qs"].append({"key": key, "question": text, "routing": r[-1] if r else None, "dialog_tail": re.sub(r"[\w.+-]+@[\w.-]+", "[email]", box.inner_text())[-500:]})
        page.screenshot(path=f"{OUT}/resident-{key}.png")
    b.close()
txt = json.dumps(R, indent=1)
assert email not in txt and pw not in txt
open(f"{OUT}/resident_probe.json", "w").write(txt)
print(txt[:2500])
