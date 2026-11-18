"""Issue 76 live explore. Credentials read at runtime, never printed."""
import json, os, re, sys
from playwright.sync_api import sync_playwright
APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
rd = lambda n: open(os.path.join(os.path.expanduser("~"), n)).read().split("\n")[0].strip()
user, pw = rd(".ama-test-user-id"), rd(".ama-test-user")

def login(page):
    page.fill("input[name=loginfmt]", user); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", pw); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP): break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception: break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)

with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded"); login(page)
    c.storage_state(path="/tmp/s76.json")
    me = c.request.get(APP + "/api/me").json()
    cs = c.request.get(APP + "/api/cases")
    d = cs.json()
    print("cases status", cs.status, type(d).__name__, list(d)[:10] if isinstance(d, dict) else len(d))
    print("me keys", list(me), list(me.get("user", {})))
    json.dump(d, open("/tmp/cases76.json", "w"))
    b.close()
