import os
from playwright.sync_api import sync_playwright
H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
O = "docs/reference/research/issue-76-live-r2-2026-11-18/shots/"
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(storage_state=os.environ["I76_SCRATCH"] + "/state-staff.json", viewport={"width": 1440, "height": 900})
    p = c.new_page()
    p.goto(H + "/app#/case/ZF-2025-0331", timeout=90000)
    p.wait_for_selector(".safety-clock", state="attached", timeout=60000)
    # mask the owner's name in the DOM before capture; the label and the fact "named" stay visible
    p.evaluate("""() => document.querySelectorAll('.safety-clock').forEach(e => {
        e.textContent = e.textContent.replace(/(owner: )[^.;]+/g, '$1[synthetic owner name masked]'); })""")
    print("visible clock text:", p.locator(".safety-clock:visible").first.inner_text().replace("\n", " "))
    p.locator(".safety-clock:visible").first.screenshot(path=O + "01-hazard-clock-owner-block.png")
    p.goto(H + "/app", timeout=90000)
    p.wait_for_timeout(5000)
    p.locator("summary", has_text="Queue definitions").click()
    side = p.locator("text=Reset my queue").locator("xpath=ancestor::*[contains(@class,'filter') or self::aside or self::form][1]")
    print("sidebar matches:", side.count())
    side.first.screenshot(path=O + "02-queue-filter-reset-definitions.png")
    print("definitions:", p.locator("details:has(summary:has-text('Queue definitions'))").inner_text().replace("\n", " | ")[:1500])
