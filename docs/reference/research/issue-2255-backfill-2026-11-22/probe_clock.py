"""Staff safety-queue clock probe for #2255. Usage: python3 probe_clock.py before|after.

Sign-in values are read from the owner's home files at run time and never printed or stored.
"""
import json
import os
import re
import sys

from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
label = sys.argv[1]
home = os.path.expanduser("~")
u = open(home + "/.ama-test-user-id").read().strip()
p = open(home + "/.ama-test-user").read().strip()


def login(page):
    page.goto(H + "/sign-in")
    for _ in range(4):
        try:
            if page.locator("input[name=loginfmt]").is_visible(timeout=3000):
                page.fill("input[name=loginfmt]", u)
                page.click("input[type=submit]")
                page.wait_for_timeout(1500)
            if page.locator("input[name=passwd]").is_visible(timeout=3000):
                page.fill("input[name=passwd]", p)
                page.click("input[type=submit]")
                page.wait_for_timeout(2000)
            if page.locator("#idBtn_Back").is_visible(timeout=2000):
                page.click("#idBtn_Back")
                page.wait_for_timeout(2000)
        except Exception:
            pass
    page.wait_for_load_state("networkidle")


res = {"label": label}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    login(pg)
    pg.goto(H + "/app#/all")
    pg.wait_for_timeout(7000)
    pg.get_by_label("Show only").select_option(label="Safety issue open")
    pg.wait_for_timeout(5000)
    t = re.sub(r"\s+", " ", pg.inner_text("main"))
    res["cases_listed"] = re.findall(r"All open cases (\d+) cases?", t)
    res["clock_unknown"] = len(
        re.findall(r"Hazard clock: elapsed time unknown; no response target window recorded", t)
    )
    res["clock_with_elapsed_hours"] = len(re.findall(r"Hazard clock: \d+ hours elapsed", t))
    res["named_owners"] = len(re.findall(r"Accountable owner: [A-Z][a-z]+ [A-Z][a-z]+", t))
    res["clock_samples"] = sorted(set(re.findall(r"Hazard clock: [^.;]*", t)))[:6]
    for key, pat in (("running_sample", r"Hazard clock: \d{1,2} hours elapsed.{0,330}"),
                     ("overdue_sample", r"Hazard clock: \d{4,} hours elapsed.{0,330}")):
        m = re.search(pat, t)
        res[key] = m.group(0) if m else None
    res["status_words"] = {w: len(re.findall(w, t)) for w in ("overdue", "running", "Overdue", "Running")}
    pg.screenshot(path=f"{OUT}/screens/safety-queue-{label}.png")
    api = c.request.get(H + "/api/cases?view=all&flag=hazard&sort=urgent")
    res["api_status"] = api.status
    if api.ok:
        res["api_total"] = api.json().get("total")
    s = json.dumps(res, indent=1)
    assert u not in s and p not in s
    open(f"{OUT}/probe-{label}.json", "w").write(s)
    print(s)
    b.close()
