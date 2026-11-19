"""Issue 76 live UI proof: open the hazard case card and capture the clock text."""
import json, os
from playwright.sync_api import sync_playwright
APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
r = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 1000}, storage_state="/tmp/s76.json"); page = c.new_page()
    page.goto(APP + "/app", wait_until="networkidle"); page.wait_for_timeout(3000)
    loc = page.get_by_text("ZF-2025-0331").first
    r["row_found"] = loc.count() > 0
    if r["row_found"]:
        loc.click(); page.wait_for_timeout(3000)
        txt = page.inner_text("body")
        r["card_hazard_clock_text"] = "Hazard clock: elapsed time unknown" in txt
        r["card_named_owner"] = "Accountable owner: Karen Lawson" in txt
        r["card_owner_status"] = "Named follow-up owner recorded." in txt
        el = page.query_selector(".safety-clock")
        r["safety_clock_element"] = el is not None
        if el: r["safety_clock_visible"] = el.is_visible(); r["safety_clock_text"] = (el.text_content() or "")[:700]; r["sections_in_card"] = page.evaluate("()=>[...document.querySelectorAll('h2,h3')].map(e=>e.textContent.trim()).slice(0,20)")
        page.screenshot(path=f"{OUT}/hazard-case-card.png")
    r["url_path"] = page.url.replace(APP, "")[:60]
    b.close()
print(json.dumps(r, indent=1))
