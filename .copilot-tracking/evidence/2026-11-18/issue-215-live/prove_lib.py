"""Issue 215 live proof: regulatory alerts panel and regulatory chat on the demo workbench."""
import json, os, urllib.request, hashlib
from common import *

AXE = os.path.join(OUT, "axe.min.js")
if not os.path.exists(AXE):
    urllib.request.urlretrieve("https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.3/axe.min.js", AXE)
TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]
def axe(pg, sel):
    if not pg.evaluate("typeof axe!=='undefined'"):
        pg.add_init_script(path=AXE) if False else pg.evaluate(open(AXE).read())
    r = pg.evaluate("([s,t])=>axe.run(document.querySelector(s),{runOnly:{type:'tag',values:t}})", [sel, TAGS])
    return {"violations": [{"id": v["id"], "n": len(v["nodes"])} for v in r["violations"]],
            "incomplete": [{"id": v["id"], "n": len(v["nodes"])} for v in r["incomplete"]]}

def shot(pg, sel, name):
    pg.evaluate("s=>document.querySelector(s).scrollIntoView({block:'start'})", sel)
    pg.wait_for_timeout(400)
    pg.screenshot(path=os.path.join(OUT, name))

MOCK = {"coverage_status": "partial", "homes": [{"alerts": [
  {"result": "breach risk", "noticed": "Synthetic: hazard report recorded without an acknowledgement time", "safe_action": "Use the human hazard service now and record the awareness time", "decision_owner": "Building Safety Liaison", "escalation_role": "Retrofit Programme Manager", "clock": "Synthetic exercise clock: 24 hours from awareness", "due_at": "2026-11-19T10:00:00Z", "at": "2026-11-18T10:00:00Z", "step": "intake", "card_id": "demo-card", "card_version": "1", "exercise": True, "active_control": True, "latest_result": "breach risk", "latest_evaluated_at": "2026-11-18T10:00:00Z", "usage": True, "requires_acknowledgement": True, "requires_outcome": True,
   "citations": [{"id": "demo-prov-1", "status": "in force", "effective": "2025-10-27", "retrieved": "2026-11-01", "review_status": "demo", "completeness": "excerpt"}]},
  {"result": "unknown", "noticed": "Synthetic: no evidence held", "safe_action": None, "decision_owner": None, "clock": None, "card_id": "demo-card", "card_version": "1", "citations": []},
  {"result": "clear", "noticed": "Synthetic: bounded check clear", "safe_action": "No action beyond ordinary case work", "decision_owner": "Retrofit Coordinator", "escalation_role": "Retrofit Programme Manager", "clock": "None", "card_id": "demo-card", "card_version": "1", "citations": []}]}]}

def tab_walk(pg, root, n=40):
    stops = []
    for _ in range(n):
        pg.keyboard.press("Tab")
        i = pg.evaluate("""r=>{const e=document.activeElement;const root=document.querySelector(r);if(!e||!root.contains(e))return null;
          const cs=getComputedStyle(e);return {tag:e.tagName,name:(e.getAttribute('aria-label')||e.textContent||e.id||'').trim().slice(0,50),
          ring:(cs.outlineStyle!=='none'&&parseFloat(cs.outlineWidth)>0)||cs.boxShadow!=='none'}}""", root)
        if i: stops.append(i)
    return stops

