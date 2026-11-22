"""Issue 2245 UI first-ask probe: ask immediately after the workbench loads and time every /api request. Credentials are read at run time and never printed."""
import json, os, re, sys, time
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
TAG = sys.argv[1] if len(sys.argv) > 1 else "run"
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
emp = {"user": rd(".ama-test-user-id")[0], "pw": rd(".ama-test-user")[0]}
QS0 = [
    ("general", "Tell me what you can help with"),
    ("explain", "Explain in two sentences why airtightness testing matters before retrofit insulation."),
    ("stock", "Which stock should we prioritise by EPC ranking?"),
    ("funding", "Can you check the grant claim and invoice?"),
    ("quality", "Is the quality inspection evidence complete?"),
]
R = {"tag": TAG, "asks": [], "chat_http": []}
mask = lambda s: re.sub(r"[\w.+-]+@[\w.-]+", "[email]", s)
QUESTION = "Which homes should I prioritise first by EPC and stock facts?"
R = {"tag": TAG, "requests": []}
mask = lambda s: re.sub(r"[\w.+-]+@[\w.-]+", "[email]", s)
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    page = c.new_page()
    T0 = {}
    def on_req(r):
        if "/api/" in r.url:
            T0[r] = time.time()
    def on_done(r):
        if r in T0:
            R["requests"].append({"t": round(T0[r] - T_START[0], 1), "m": r.method, "path": re.sub(r"(threads|cases)/[^/]+", r"\\1/<id>", r.url.split("//")[1].split("/", 1)[1])[:70], "secs": round(time.time() - T0[r], 2), "status": (r.response().status if r.response() else None)})
    T_START = [time.time()]
    page.on("request", on_req); page.on("requestfinished", on_done); page.on("requestfailed", on_done)
    page.goto(APP + "/sign-in", wait_until="networkidle", timeout=90000)
    page.wait_for_url(re.compile(r"login\.microsoftonline\.com"), timeout=60000)
    page.fill("input[name=loginfmt]", emp["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd], input[name=pass]", timeout=30000)
    page.fill("input[name=passwd], input[name=pass]", emp["pw"]); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)
    T_START[0] = time.time()
    page.goto(APP + "/app", wait_until="commit", timeout=90000)
    page.wait_for_selector("#employee-chat-launcher:not([hidden])", timeout=60000)
    page.locator("#employee-chat-launcher").click()
    dialog = page.get_by_role("dialog", name="Employee assistant")
    dialog.wait_for(timeout=15000)
    q = page.get_by_label("Your work question", exact=True)
    send = dialog.get_by_role("button", name="Send", exact=True)
    send.and_(page.locator(":enabled")).wait_for(timeout=60000)
    q.fill(QUESTION)
    t_ask = time.time()
    R["ask_started_after_load_secs"] = round(t_ask - T_START[0], 1)
    send.click()
    answered = None
    while time.time() - t_ask < 150:
        txt = dialog.get_by_role("log").inner_text()
        if "Skill:" in txt or "AI answers are on hold" in txt or "cannot" in txt.lower():
            answered = round(time.time() - t_ask, 1)
            break
        page.wait_for_timeout(500)
    R["answered_after_secs"] = answered
    R["log_tail"] = mask(dialog.get_by_role("log").inner_text())[-500:]
    page.screenshot(path=f"{OUT}/{TAG}-ui.png")
    b.close()
txt = json.dumps(R, indent=1)
for v in emp.values():
    assert v not in txt
open(f"{OUT}/{TAG}_ui_probe.json", "w").write(txt)
print(R["ask_started_after_load_secs"], R["answered_after_secs"])
for r in sorted(R["requests"], key=lambda x: -x["secs"])[:6]:
    print(r)
