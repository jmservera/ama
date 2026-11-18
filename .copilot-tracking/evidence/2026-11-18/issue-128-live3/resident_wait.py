import os, re
from playwright.sync_api import sync_playwright
R = os.environ["DEMO_RESIDENT_URL"]
rr = [x.strip() for x in open(os.path.expanduser("~/.ama-resident-test-user")).read().split("\n") if x.strip()]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_context(viewport={"width":1366,"height":900}).new_page()
    pg.goto(R + "/", wait_until="domcontentloaded", timeout=120000)
    pg.click("#email"); pg.keyboard.type(rr[0]); pg.keyboard.press("Tab"); pg.keyboard.type(rr[1]); pg.keyboard.press("Enter")
    for t in (10, 30, 60, 120):
        pg.wait_for_timeout((t - (0 if t == 10 else {30:10,60:30,120:60}[t])) * 1000)
        txt = re.sub(r"[\w.+-]+@[\w.-]+", "[email]", pg.locator("body").inner_text())
        print(t, "s still_signing_in=", bool(re.search("still signing you in", txt, re.I)), "manual_route=", bool(re.search(r"phone|letter|visit|person can help|paper", txt, re.I)), "len=", len(txt))
    pg.screenshot(path="resident-wait-120s.png"); b.close()
