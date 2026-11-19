import json
from playwright.sync_api import sync_playwright
from common import *
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width":1366,"height":900}); pg = c.new_page()
    login(pg)
    me = c.request.get(APP + "/api/me").json()
    print(json.dumps(me.get("navigation"), indent=0)[:2500])
    pg.goto(APP + "/app", wait_until="networkidle"); pg.wait_for_timeout(4000)
    print(pg.url, pg.title())
    print(pg.evaluate("()=>[...document.querySelectorAll('nav a, nav button, [role=tab]')].map(e=>(e.textContent||'').trim().slice(0,40)+'|'+(e.getAttribute('href')||e.id||''))"))
    b.close()
