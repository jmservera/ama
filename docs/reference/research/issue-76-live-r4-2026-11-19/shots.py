import os, re
from playwright.sync_api import sync_playwright
H = os.environ["DEMO_API_URL"]
O = "docs/reference/research/issue-76-live-r4-2026-11-19/shots/"
os.makedirs(O, exist_ok=True)
MASK = r"(owner: )[^.;]+"
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(storage_state=os.environ["I76_SCRATCH"] + "/state-staff.json", viewport={"width": 1440, "height": 900})
    p = c.new_page()
    for case, name in (("ZF-2025-0148", "01-safeguarding-clock-owner"), ("ZF-2025-0331", "02-hazard-clock-owner")):
        p.goto(H + "/app#/case/" + case, timeout=90000)
        p.wait_for_timeout(6000)
        sel = ".safeguarding-clock:visible, .safety-clock:visible"
        print(case, "matches:", p.locator(sel).count())
        p.evaluate("""(m) => document.querySelectorAll('.safeguarding-clock,.safety-clock').forEach(e => {
            e.textContent = e.textContent.replace(new RegExp(m, 'gi'), '$1[synthetic owner name masked]'); })""", MASK)
        for i in range(p.locator(sel).count()):
            print(" text:", re.sub(r"\s+", " ", p.locator(sel).nth(i).inner_text()))
        p.locator(sel).first.screenshot(path=O + name + ".png")
