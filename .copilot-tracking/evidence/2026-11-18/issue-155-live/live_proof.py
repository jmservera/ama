"""Issue 155 live read-only proof: signed-in workbench, and a search for usability or per-person measure surfaces."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import APP, OUT, login, mask_emails
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1366, "height": 900})
    login(pg); pg.wait_for_load_state("networkidle")
    me = pg.evaluate("fetch('/api/me').then(r=>r.json())")
    nav = pg.evaluate("fetch('/api/me').then(r=>r.json()).then(j=>JSON.stringify(j))")
    res = {"role": me["user"]["role"], "identity_source": me["user"]["identity_source"], "me_top_keys": sorted(me.keys())}
    pg.goto(APP + "/#/"); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(1500)
    mask_emails(pg)
    text = pg.inner_text("body").lower()
    res["body_mentions"] = {k: (k in text) for k in ["usability", "sus score", "survey", "participant", "audit-use", "session recording"]}
    pg.screenshot(path=os.path.join(OUT, "workbench-signed-in.png"))
    probes = {}
    for path in ["/api/usability", "/api/usability-programme", "/api/telemetry/users", "/usability", "/api/zz-nonexistent-control"]:
        probes[path] = pg.evaluate("p=>fetch(p).then(r=>r.status)", path)
    res["route_probes_status"] = probes
    json.dump(res, open(os.path.join(OUT, "live-proof.json"), "w"), indent=1)
    print(json.dumps(res, indent=1)); b.close()
