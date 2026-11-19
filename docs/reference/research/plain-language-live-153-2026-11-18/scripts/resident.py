"""Resident demo form sign-in at runtime, then scan visible copy. No secrets printed."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from audit import *
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1440, "height": 900}); pg = c.new_page()
    l = open(home + "/.ama-resident-test-user").read().splitlines()
    pg.goto(R + "/")
    pg.get_by_label("Email address").fill(l[0].strip()); pg.get_by_label("Password").fill(l[1].strip())
    pg.get_by_role("button", name="Sign in").click(); pg.wait_for_timeout(45000)
    f = []
    t = scan(pg, "resident signed in", f, "resident-10-signed-in")
    for i, n in enumerate(["Your home", "Your works", "Help with your case"]):
        pass
    links = pg.eval_on_selector_all("a[href],button", "els=>els.map(e=>(e.textContent||'').trim().replace(/\\s+/g,' ').slice(0,40))")
    print("CONTROLS:", list(dict.fromkeys(links)))
    open(OUT + "/resident-signed-in-text.txt", "w").write(t)
    json.dump(f, open(OUT + "/resident-signed-in.json", "w"), indent=1)
    print(json.dumps({k: f[0][k] for k in ("title", "terms", "snake_case", "headings", "ai_lines")}))
    b.close()
