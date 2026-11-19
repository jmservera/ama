"""Drive the staff SPA: click each navigation control, scan visible copy. No secrets printed."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from audit import *

with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1440, "height": 900}); pg = c.new_page()
    u = open(home + "/.ama-test-user-id").read().strip(); p = open(home + "/.ama-test-user").read().strip()
    login(pg, u, p, H + "/sign-in")
    pg.goto(H + "/app"); pg.wait_for_timeout(2500)
    text = pg.inner_text("body")
    for m in re.finditer(r"measure_decisions", text):
        print("CONTEXT:", text[max(0, m.start()-200):m.end()+120].replace("\n", " | "))
    navs = pg.eval_on_selector_all("nav a, nav button, [role=tab], aside a, aside button, header button, header a",
                                   "els=>els.map(e=>(e.textContent||'').trim().replace(/\\s+/g,' ').slice(0,40))")
    navs = [n for n in dict.fromkeys(navs) if n]
    print("NAV:", navs)
    findings = []; seen = set()
    for i, n in enumerate(navs[:30]):
        if re.search(r"sign out|log ?out|AI suggestions|without AI", n, re.I) or n in seen: continue
        seen.add(n)
        try:
            pg.get_by_role("link", name=n, exact=True).or_(pg.get_by_role("button", name=n, exact=True)).or_(pg.get_by_role("tab", name=n, exact=True)).first.click(timeout=4000)
            scan(pg, "nav:" + n, findings, f"staff-nav-{i:02d}")
        except Exception as e:
            findings.append({"surface": "nav:" + n, "error": type(e).__name__})
    json.dump(findings, open(OUT + "/staff-spa-audit.json", "w"), indent=1)
    for f in findings: print(json.dumps({k: f.get(k) for k in ("surface", "terms", "snake_case", "error")}))
    b.close()
