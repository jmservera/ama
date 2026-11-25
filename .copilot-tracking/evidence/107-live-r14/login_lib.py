"""Shared sign-in for r14 probes. Reads sign-in values at runtime; never prints them."""
import os, re
from playwright.sync_api import sync_playwright
APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
EMP = {"user": rd(".ama-test-user-id")[0], "pw": rd(".ama-test-user")[0]}

def redact(t):
    for v in EMP.values():
        t = t.replace(v, "[redacted]")
    return t

def login(p):
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    page = c.new_page()
    page.goto(APP + "/", wait_until="networkidle", timeout=90000)
    page.click("a[href='/sign-in']")
    page.wait_for_url(re.compile(r"login\.microsoftonline\.com"), timeout=60000)
    page.fill("input[name=loginfmt]", EMP["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", EMP["pw"]); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)
    page.wait_for_load_state("networkidle")
    return b, page
