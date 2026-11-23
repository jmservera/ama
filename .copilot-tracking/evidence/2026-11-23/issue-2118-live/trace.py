"""Issue 2118: reading identity and provenance for one live-fed home. Reads sign-in at runtime; prints no credential."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "2026-11-18", "issue-155-live"))
from common import APP, login
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); page = b.new_context(viewport={"width": 1440, "height": 900}).new_page(); login(page)
    page.goto(APP + "/app#/overview", wait_until="domcontentloaded"); page.wait_for_timeout(6000)
    r = page.evaluate("""async()=>{const r=await fetch('/api/cases/ZF-2025-0030/sensors');return await r.json()}""")
    m = page.evaluate("""async()=>{const r=await fetch('/api/map?zoom=14');const j=await r.json();return j.items.filter(i=>i.case_id==='ZF-2025-0030'||i.id==='ZF-2025-0030').map(i=>i.sensor)}""")
    rd = r.get("readings") or []
    out = {"now": page.evaluate("new Date().toISOString()"), "provenance": r.get("provenance"), "freshness_text": r.get("freshness_text"),
           "age_seconds": r.get("age_seconds"), "latest": r.get("latest"),
           "reading_ids": [x.get("reading_id") or x.get("id") for x in rd][-4:], "reading_keys": sorted(rd[0]) if rd else [],
           "map_sensor": m}
    json.dump(out, open(os.path.join(HERE, "trace-result.json"), "w"), indent=1, default=str)
    print(json.dumps(out, default=str)[:2500]); b.close()
