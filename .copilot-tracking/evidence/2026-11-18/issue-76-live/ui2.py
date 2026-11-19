"""Issue 76 live UI proof 2: visible safety block text and the collapsed task context."""
import json, os
from playwright.sync_api import sync_playwright
APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
r = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 1000}, storage_state="/tmp/s76.json"); page = c.new_page()
    page.goto(APP + "/app#/case/ZF-2025-0331", wait_until="networkidle"); page.wait_for_timeout(3500)
    h = page.get_by_text("Safety referrals and stopped retrofit work").first
    sec = h.locator("xpath=ancestor::section[1] | ancestor::div[contains(@class,'safety')][1]").first
    t = sec.inner_text() if sec.count() else ""
    r["safety_block_visible_text"] = t[:2500]
    h.scroll_into_view_if_needed(); page.screenshot(path=f"{OUT}/hazard-safety-block.png")
    el = page.query_selector(".safety-clock")
    r["clock_ancestor_chain"] = page.evaluate("e=>{const o=[];let n=e;while(n&&n!==document.body){o.push(n.tagName.toLowerCase()+(n.className?'.'+String(n.className).split(' ')[0]:'')+(n.tagName==='DETAILS'?(n.open?'[open]':'[closed]'):''));n=n.parentElement}return o}", el)
    b.close()
print(json.dumps(r, indent=1))
