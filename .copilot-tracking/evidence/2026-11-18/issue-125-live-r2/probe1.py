"""Issue 125 live probe: is a discovery assistant reachable or writable on the deployed demo API?"""
from playwright.sync_api import sync_playwright
from common import *

res = {}
paths = ["/openapi.json", "/docs", "/api/discovery", "/api/discovery-assistant", "/api/discovery/assistant",
         "/api/assistant/discovery", "/api/discovery-demo", "/api/retrofit-flow-evidence-assistant",
         "/api/evidence-assistant", "/api/me", "/api/health", "/api/version"]
with sync_playwright() as p:
    b, pg = session(p)
    for path in paths:
        s, d = call(pg, "GET", path)
        res["GET " + path] = {"status": s, "snippet": scrub(str(d)[:160])}
    for path in ["/api/discovery", "/api/discovery-assistant", "/api/discovery/assistant"]:
        for m in ("POST",):
            s, d = call(pg, m, path, {"tool": "write_source_system"})
            res[f"{m} {path}"] = {"status": s, "snippet": scrub(str(d)[:160])}
    s, d = call(pg, "GET", "/api/cases")
    res["cases_list_status"] = s
    pg.goto(APP + "/app", wait_until="networkidle")
    body = pg.inner_text("body").lower()
    res["ui_mentions_discovery_assistant"] = ("discovery assistant" in body, "evidence assistant" in body)
    pg.screenshot(path=f"{OUT}/workbench-home.png")
    b.close()
json.dump(res, open(f"{OUT}/probe1.json", "w"), indent=1, default=str); print(json.dumps(res, indent=1, default=str)[:6000])
