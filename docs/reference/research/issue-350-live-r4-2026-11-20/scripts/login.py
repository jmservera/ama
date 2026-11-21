import os, sys, re
from playwright.sync_api import sync_playwright
H = sys.argv[2]
who = sys.argv[1]
h = os.path.expanduser("~")
if who == "staff":
    u = open(h + "/.ama-test-user-id").read().strip(); p = open(h + "/.ama-test-user").read().strip()
else:
    l = open(h + "/.ama-resident-test-user").read().splitlines(); u, p = l[0].strip(), l[1].strip()
out = f"<session-dir>/state-{who}.json"
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1440, "height": 900}); pg = c.new_page()
    pg.goto(H + "/sign-in" if who == "staff" else H + "/")
    for _ in range(4):
        try:
            if pg.locator("input[name=loginfmt]").is_visible(timeout=3000):
                pg.fill("input[name=loginfmt]", u); pg.click("input[type=submit]"); pg.wait_for_timeout(1500)
            if pg.locator("input[name=passwd]").is_visible(timeout=3000):
                pg.fill("input[name=passwd]", p); pg.click("input[type=submit]"); pg.wait_for_timeout(2000)
            if pg.locator("#idBtn_Back").is_visible(timeout=2000): pg.click("#idBtn_Back"); pg.wait_for_timeout(2000)
        except Exception:
            pass
    pg.wait_for_load_state("networkidle")
    print("final", re.sub(r"\?.*", "", pg.url).split("//")[-1].split("/", 1)[-1], pg.title())
    c.storage_state(path=out); os.chmod(out, 0o600)
