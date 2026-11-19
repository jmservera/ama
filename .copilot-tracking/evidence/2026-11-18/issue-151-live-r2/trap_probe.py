"""Describe the element at the case-detail Tab trap (issue 151 r2). No credentials printed."""
import sys, json, re
sys.argv = ["x", "none"]
import importlib.util
src = open("scan2.py").read().split("which = sys.argv[1]")[0]
exec(src)
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    employee_login(pg)
    pg.goto(APP + "/app#/case/ZF-2025-0331", wait_until="networkidle"); pg.wait_for_timeout(6000)
    pg.evaluate("document.activeElement.blur();window.scrollTo(0,0)")
    last = None
    for i in range(40):
        pg.keyboard.press("Tab")
        d = pg.evaluate("()=>{const e=document.activeElement;return {tag:e.tagName,type:e.type||null,id:e.id,cls:(e.className||'').toString().slice(0,50),label:e.labels&&e.labels[0]?e.labels[0].textContent.trim().slice(0,40):null,aria:e.getAttribute('aria-label'),outer:e.outerHTML.slice(0,160)}}")
        d["outer"] = redact(d["outer"])
        if last and last["outer"] == d["outer"]:
            print("REPEAT at press", i + 1, json.dumps(d)); 
        last = d
        if i >= 13: print(i + 1, json.dumps(d))
    b.close()
