"""Live axe 4.10.3 + keyboard evidence for the demo workbench (issue 151). Desktop Chromium; no credentials printed."""
import hashlib, json, sys
from playwright.sync_api import sync_playwright
from common import *
raw = open("/tmp/axe/axe.min.js", "rb").read()
assert hashlib.sha256(raw).hexdigest() == open(f"{OUT}/axe-4.10.3.sha256").read().strip()
AXE = raw.decode()
SCREENS = ["", "all", "overview", "progress", "visits", "funding", "finance", "capacity", "closed", "assistants", "time", "aftercare", "screens"]
TAGS = ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']
KEY_JS = """async (max) => {
  const stops = []; let trap = false;
  document.activeElement && document.activeElement.blur();
  for (let i = 0; i < max; i++) {
    window.__tab && window.__tab();
    break;
  }
  return stops;
}"""
FOCUS_JS = """() => {
  const e = document.activeElement; if (!e || e === document.body) return null;
  const s = getComputedStyle(e), r = e.getBoundingClientRect();
  const name = (e.getAttribute('aria-label') || e.textContent || e.getAttribute('title') || e.getAttribute('placeholder') || '').trim().replace(/\\s+/g,' ').slice(0,40);
  e.dataset.kbdSeen = String((parseInt(e.dataset.kbdSeen || '0')) + 1);
  const ol = s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0;
  const bs = s.boxShadow && s.boxShadow !== 'none';
  return {tag: e.tagName.toLowerCase(), role: e.getAttribute('role'), name,
    seen: parseInt(e.dataset.kbdSeen), indicator: ol || bs, visible: r.width > 0 && r.height > 0 && r.bottom > 0 && r.top < innerHeight,
    id: e.id || null, uid: (e.dataset.kbdUid = e.dataset.kbdUid || String(Math.random()))};
}"""

def axe_scan(pg):
    pg.evaluate(AXE)
    r = pg.evaluate("async t => await axe.run(document, {runOnly:{type:'tag', values:t}})", TAGS)
    slim = lambda xs: [{"id": x["id"], "impact": x.get("impact"), "help": x["help"], "tags": [t for t in x["tags"] if t.startswith("wcag")], "nodes": len(x["nodes"]),
            "targets": [n["target"] for n in x["nodes"][:5]]} for x in xs]
    return {"violations": slim(r["violations"]), "incomplete": slim(r["incomplete"]), "passes": len(r["passes"]), "inapplicable": len(r["inapplicable"])}

def keyboard(pg, max_stops=80):
    pg.evaluate("()=>{document.activeElement&&document.activeElement.blur();window.scrollTo(0,0)}")
    stops = []; cycled = False; repeat = 0; no_ind = 0; hidden = 0
    for i in range(max_stops):
        pg.keyboard.press("Tab")
        f = pg.evaluate(FOCUS_JS)
        if f is None: break
        if stops and stops[-1]["uid"] == f["uid"]:
            repeat += 1
            if repeat > 5: return {"stops": len(stops), "trap": True, "sample": stops[:5]}
            continue
        repeat = 0
        if f["seen"] >= 2: cycled = True; break
        if not f["indicator"]: no_ind += 1
        if not f["visible"]: hidden += 1
        stops.append(f)
    return {"stops": len(stops), "trap": False, "completed_cycle": cycled, "without_indicator": no_ind, "not_in_viewport": hidden,
            "unnamed": sum(1 for s in stops if not s["name"]), "first": [f"{s['tag']}:{s['name']}" for s in stops[:6]]}

def live_regions(pg):
    return pg.evaluate("()=>[...document.querySelectorAll('[role=status],[role=alert],[aria-live]')].map(e=>(e.getAttribute('role')||'')+'/'+(e.getAttribute('aria-live')||''))")

res = {"axe": "4.10.3", "tags": TAGS, "viewport": "1366x900", "screens": {}}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    login(pg)
    pg.goto(APP + "/app", wait_until="networkidle"); pg.wait_for_timeout(4000)
    for s in SCREENS:
        name = s or "my-cases"
        try:
            pg.evaluate(f"location.hash = '#/{s}'"); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(3500)
            r = {"title": pg.title(), "h1": pg.evaluate("()=>[...document.querySelectorAll('h1')].map(e=>e.textContent.trim().slice(0,60))"),
                 "landmarks": pg.evaluate("()=>['main','nav','header'].map(t=>t+':'+document.querySelectorAll(t+',[role='+t+']').length)")}
            r["axe"] = axe_scan(pg); r["keyboard"] = keyboard(pg); r["live_regions"] = live_regions(pg)
            pg.set_viewport_size({"width": 320, "height": 256}); pg.wait_for_timeout(800)
            r["reflow_320_horizontal_scroll"] = pg.evaluate("()=>document.documentElement.scrollWidth>innerWidth+1")
            pg.set_viewport_size({"width": 1366, "height": 900}); pg.wait_for_timeout(500)
            mask_emails(pg); pg.screenshot(path=f"{OUT}/screen-{name}.png")
        except Exception as e:
            r = {"error": type(e).__name__}
        res["screens"][name] = r
        print(name, r.get("error") or (r["reflow_320_horizontal_scroll"], len(r["axe"]["violations"]), len(r["axe"]["incomplete"]), r["keyboard"]["stops"], r["keyboard"].get("trap")), flush=True)
    b.close()
json.dump(res, open(f"{OUT}/axe-keyboard-results.json", "w"), indent=1)
