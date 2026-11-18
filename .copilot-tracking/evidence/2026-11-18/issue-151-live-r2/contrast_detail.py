"""Detail of failing contrast nodes (disabled state and colours)."""
import json
from playwright.sync_api import sync_playwright
from common import *
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_context(viewport={"width":1366,"height":900}).new_page(); login(pg)
    pg.goto(APP+"/app",wait_until="networkidle"); pg.wait_for_timeout(4000); out={}
    for s,sel in (("capacity","button,a"),("assistants","button")):
        pg.evaluate(f"location.hash='#/{s}'"); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(3000)
        out[s]=pg.evaluate("""(sel)=>[...document.querySelectorAll(sel)].filter(e=>/^(Previous packages|Next packages|Accept|Edit)$/.test(e.textContent.trim())).map(e=>{const c=getComputedStyle(e);return {t:e.textContent.trim(),disabled:e.disabled||e.getAttribute('aria-disabled'),color:c.color,bg:c.backgroundColor,opacity:c.opacity,parentBg:getComputedStyle(e.parentElement).backgroundColor}})""",sel)
    json.dump(out,open("contrast-detail.json","w"),indent=1); print(json.dumps(out)[:900]); b.close()
