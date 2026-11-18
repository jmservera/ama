"""Cropped keyboard-focus screenshots (header and composer only; the log is never captured, so no names)."""
from playwright.sync_api import sync_playwright
H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1440, "height": 900}, storage_state="<tmp>/state-staff.json"); pg = c.new_page()
    pg.goto(f"{H}/app#/case/ZF-2025-0122"); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(2500)
    pg.focus("#employee-chat-launcher"); pg.keyboard.press("Tab"); pg.keyboard.press("Shift+Tab")
    pg.locator("#employee-chat-launcher").screenshot(path="shots/01-launcher-keyboard-focus.png")
    pg.keyboard.press("Enter"); pg.wait_for_function("() => !document.querySelector('#employee-chat textarea').disabled", timeout=30000)
    pg.locator("#employee-chat .chat-widget-header").screenshot(path="shots/02-dialog-open-heading-focus.png")
    pg.focus("#employee-chat textarea")
    pg.locator("#employee-chat form").screenshot(path="shots/03-composer-keyboard-focus.png")
    print(pg.locator("#employee-chat").aria_snapshot()[:1500])
