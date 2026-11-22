import json, os
from collections import Counter
from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
u = open(home + "/.ama-test-user-id").read().strip()
p = open(home + "/.ama-test-user").read().strip()
HOOK = """
(() => { let real; Object.defineProperty(window, 'L', { configurable: true,
  set(v) { real = v; if (v && v.Map && v.Map.addInitHook) v.Map.addInitHook(function () { window.__map = this; }); },
  get() { return real; } }); })();
"""


def login(page):
    page.goto(H + "/sign-in")
    for _ in range(4):
        try:
            if page.locator("input[name=loginfmt]").is_visible(timeout=3000):
                page.fill("input[name=loginfmt]", u); page.click("input[type=submit]"); page.wait_for_timeout(1500)
            if page.locator("input[name=passwd]").is_visible(timeout=3000):
                page.fill("input[name=passwd]", p); page.click("input[type=submit]"); page.wait_for_timeout(2000)
            if page.locator("#idBtn_Back").is_visible(timeout=2000):
                page.click("#idBtn_Back"); page.wait_for_timeout(2000)
        except Exception:
            pass
    page.wait_for_load_state("networkidle")


res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    login(pg)
    seen = []
    pg.on("response", lambda r: seen.append((r.status, r.url.split("/api/")[-1][:50])) if "/api/chat/" in r.url else None)
    pg.goto(H + "/app#/case/ZF-2025-0031")
    pg.wait_for_timeout(5000)
    launcher = pg.locator("#chat-launcher, button:has-text('Help')").first
    res["launchers"] = pg.locator("button[id*=chat], button[class*=chat-widget-launcher]").evaluate_all("els => els.map(e => e.id + ':' + e.textContent.trim())")
    launcher = pg.locator("button[id*=chat-launcher], button[class*=launcher]").first
    launcher.click(); pg.wait_for_timeout(2500)
    out = {}
    for q in ("Which homes should I prioritise first by EPC and stock facts?", "What is the status of the funding grant claim?", "Show a quality defect inspection note on the sensor readings"):
        box = pg.locator("textarea:visible, #employee-chat-question, input[type=text]:visible").last
        box.fill(q)
        before = len(seen)
        pg.keyboard.press("Enter")
        try:
            pg.wait_for_function("() => document.querySelectorAll('.chat-widget-routing').length >= %d" % (len(out) + 1), timeout=150000)
        except Exception:
            pass
        out[q] = pg.locator(".chat-widget-routing").all_inner_texts()[len(out):]
        pg.wait_for_timeout(1500)
    res["employee_chat_routing"] = out
    res["chat_responses"] = seen
    res["answers_tail"] = pg.locator("[class*=chat-widget-message], .chat-widget-log").first.inner_text()[-1500:]
    res["status_line"] = pg.locator("[class*=chat-widget] [role=status]").all_inner_texts()[:3]
    pg.screenshot(path=f"{OUT}/screens/employee-chat-routing.png")
    s = json.dumps(res, indent=1, default=str)
    assert u not in s and p not in s
    open(OUT + "/probe-staff-chat-result.json", "w").write(s)
    print(s[:3000])
    b.close()
