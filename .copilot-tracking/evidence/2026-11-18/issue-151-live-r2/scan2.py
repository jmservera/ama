"""Round 2 live axe 4.10.3 + keyboard + contrast-sample evidence for the demo (issue 151).
Desktop Chromium 1366x900. Credentials read at runtime, never printed. Raw axe output is
retained gzipped with e-mail addresses and GUIDs redacted before writing."""
import gzip, hashlib, json, os, re, sys
from playwright.sync_api import sync_playwright

OUT = os.path.dirname(os.path.abspath(__file__))
APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
RES = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
EU, EP = rd(".ama-test-user-id")[0], rd(".ama-test-user")[0]
RU, RP = rd(".ama-resident-test-user")[:2]
raw = open(os.path.join(home, ".local/share/ama/phase-witness/axe.min.js"), "rb").read()
AXE_SHA = hashlib.sha256(raw).hexdigest()
AXE = raw.decode()
TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']
SECRETS = [EU, EP, RU, RP]
RED = [(re.compile(r"[\w.+-]+@[\w.-]+"), "[email]"),
       (re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I), "[guid]")]


def redact(s):
    for rx, rep in RED:
        s = rx.sub(rep, s)
    for v in SECRETS:
        s = s.replace(v, "[redacted]")
    return s


FOCUS_JS = """() => {
  const e = document.activeElement; if (!e || e === document.body) return null;
  const s = getComputedStyle(e), r = e.getBoundingClientRect();
  const name = (e.getAttribute('aria-label') || e.textContent || e.getAttribute('title') || e.getAttribute('placeholder') || '').trim().replace(/\\s+/g,' ').slice(0,40);
  e.dataset.kbdSeen = String((parseInt(e.dataset.kbdSeen || '0')) + 1);
  const ol = s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0;
  const bs = s.boxShadow && s.boxShadow !== 'none';
  return {tag: e.tagName.toLowerCase(), name, seen: parseInt(e.dataset.kbdSeen), indicator: ol || bs,
    visible: r.width > 0 && r.height > 0 && r.bottom > 0 && r.top < innerHeight,
    uid: (e.dataset.kbdUid = e.dataset.kbdUid || String(Math.random()))};
}"""

CONTRAST_JS = """(sels) => {
  const parse = c => { const m = c.match(/rgba?\\(([^)]+)\\)/); if (!m) return null; const p = m[1].split(/[ ,\\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; };
  const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const over = (top, bot) => { const a = top[3]; return [0, 1, 2].map(i => top[i] * a + bot[i] * (1 - a)).concat([1]); };
  const out = {sampled: 0, unresolved: 0, below: [], min: null};
  for (const sel of sels) {
    let el; try { el = document.querySelector(sel); } catch (e) { out.unresolved++; continue; }
    if (!el) { out.unresolved++; continue; }
    let chain = [], n = el, img = false;
    while (n && n.nodeType === 1) { const s = getComputedStyle(n); if (s.backgroundImage !== 'none') img = true; const bg = parse(s.backgroundColor); if (bg && bg[3] > 0) { chain.push(bg); if (bg[3] === 1) break; } n = n.parentElement; }
    if (img) { out.unresolved++; continue; }
    let bg = chain.length && chain[chain.length - 1][3] === 1 ? chain.pop() : [255, 255, 255, 1];
    while (chain.length) bg = over(chain.pop(), bg);
    const cs = getComputedStyle(el); let fg = parse(cs.color); if (!fg) { out.unresolved++; continue; }
    let op = 1, m = el; while (m && m.nodeType === 1) { op *= parseFloat(getComputedStyle(m).opacity); m = m.parentElement; }
    fg = over([fg[0], fg[1], fg[2], fg[3] * op], bg);
    const L1 = lum(fg), L2 = lum(bg), ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    const px = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight) >= 700, large = px >= 24 || (px >= 18.66 && bold);
    const need = large ? 3 : 4.5; out.sampled++;
    if (out.min === null || ratio < out.min) out.min = Math.round(ratio * 100) / 100;
    if (ratio < need) out.below.push({sel: sel.slice(0, 80), ratio: Math.round(ratio * 100) / 100, need, text: (el.textContent || '').trim().slice(0, 30)});
  }
  out.below = out.below.slice(0, 15); return out;
}"""


def axe_scan(pg, name, store):
    pg.evaluate(AXE)
    r = pg.evaluate("async t => await axe.run(document, {runOnly:{type:'tag', values:t}, resultTypes:['violations','incomplete']})", TAGS)
    data = redact(json.dumps({k: r[k] for k in ("testEngine", "url", "timestamp", "violations", "incomplete")}, default=str))
    with gzip.open(f"{OUT}/raw-axe-{name}.json.gz", "wt") as f:
        f.write(data)
    slim = lambda xs: [{"id": x["id"], "impact": x.get("impact"), "nodes": len(x["nodes"])} for x in xs]
    summary = {"violations": slim(r["violations"]), "incomplete": slim(r["incomplete"])}
    cc = [x for x in r["incomplete"] if x["id"] == "color-contrast"]
    if cc:
        sels = [n["target"][0] for n in cc[0]["nodes"] if isinstance(n["target"][0], str)][:700]
        summary["contrast_sample"] = pg.evaluate(CONTRAST_JS, sels)
    return summary


def keyboard(pg, max_stops=120):
    pg.evaluate("()=>{document.activeElement&&document.activeElement.blur();window.scrollTo(0,0)}")
    stops = []; cycled = False; repeat = 0
    for _ in range(max_stops):
        pg.keyboard.press("Tab")
        f = pg.evaluate(FOCUS_JS)
        if f is None:
            break
        if stops and stops[-1]["uid"] == f["uid"]:
            repeat += 1
            if repeat > 8:
                return {"stops": len(stops), "trap": True, "element": f["tag"] + ":" + f["name"]}
            continue
        repeat = 0
        if f["seen"] >= 2:
            cycled = True; break
        stops.append(f)
    return {"stops": len(stops), "trap": False, "completed_cycle": cycled,
            "without_indicator": sum(1 for s in stops if not s["indicator"]),
            "not_in_viewport": sum(1 for s in stops if not s["visible"]),
            "unnamed": sum(1 for s in stops if not s["name"])}


def page_facts(pg):
    return pg.evaluate("""()=>({title:document.title,h1:[...document.querySelectorAll('h1')].map(e=>e.textContent.trim().slice(0,60)),
      landmarks:['main','nav','header'].map(t=>t+':'+document.querySelectorAll(t+',[role='+t+']').length),
      live:[...document.querySelectorAll('[role=status],[role=alert],[aria-live]')].length,
      lang:document.documentElement.lang, text:document.body.innerText.trim().slice(0,160)})""")


def mask(pg):
    pg.evaluate("""()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}""")


def scan(pg, name, res, shot=True):
    try:
        r = page_facts(pg); r["text"] = redact(r["text"])
        r["axe"] = axe_scan(pg, name, res)
        r["keyboard"] = keyboard(pg)
        pg.set_viewport_size({"width": 320, "height": 256}); pg.wait_for_timeout(800)
        r["reflow_320_horizontal_scroll"] = pg.evaluate("()=>document.documentElement.scrollWidth>innerWidth+1")
        pg.set_viewport_size({"width": 1366, "height": 900}); pg.wait_for_timeout(500)
        pg.evaluate("window.scrollTo(0,0)"); mask(pg)
        if shot:
            pg.screenshot(path=f"{OUT}/screen-{name}.png")
    except Exception as e:
        import traceback; r = {"error": type(e).__name__, "detail": redact(traceback.format_exc()[-400:])}
    res[name] = r
    a = r.get("axe")
    print(name, r.get("error") or (len(a["violations"]), len(a["incomplete"]), r["keyboard"]["stops"], r["keyboard"].get("trap")), flush=True)


def employee_login(pg):
    pg.goto(APP + "/api/me", wait_until="domcontentloaded")
    pg.fill("input[name=loginfmt]", EU); pg.click("#idSIButton9")
    pg.wait_for_selector("input[name=passwd]", timeout=30000)
    pg.fill("input[name=passwd]", EP); pg.click("#idSIButton9")
    for _ in range(3):
        try:
            pg.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if pg.url.startswith(APP):
                break
            (pg.query_selector("#idSIButton9") or pg.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    pg.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)


which = sys.argv[1]
res = {"axe": "4.10.3", "axe_sha256": AXE_SHA, "tags": TAGS, "viewport": "1366x900", "target": which, "screens": {}}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    if which == "employee":
        employee_login(pg)
        me = c.request.get(APP + "/api/me").json()
        res["me_nav_count"] = len(me.get("navigation", []))
        res["role"] = me.get("role")
        pg.goto(APP + "/app", wait_until="networkidle"); pg.wait_for_timeout(4000)
        routes = sys.argv[2].split(",") if len(sys.argv) > 2 else ["", "all", "overview", "progress", "visits", "funding", "finance", "capacity", "closed", "assistants", "time", "aftercare", "screens", "case/ZF-2025-0331"]
        for s in routes:
            name = (s or "my-cases").replace("/", "-")
            pg.evaluate(f"location.hash = '#/{s}'"); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(5000)
            scan(pg, name, res["screens"])
    else:
        pg.goto(RES + "/", wait_until="domcontentloaded", timeout=120000)
        pg.wait_for_selector("#email", timeout=60000); pg.wait_for_timeout(1500)
        scan(pg, "resident-signin", res["screens"])
        pg.click("#email"); pg.keyboard.type(RU); pg.keyboard.press("Tab"); pg.keyboard.type(RP); pg.keyboard.press("Enter")
        pg.wait_for_selector("#signin", state="hidden", timeout=90000)
        pg.wait_for_function("()=>document.querySelector('#status').textContent.includes('signed in')", timeout=60000)
        pg.wait_for_timeout(4000)
        res["signed_in"] = c.request.get(RES + "/demo/session").json().get("signed_in")
        scan(pg, "resident-home", res["screens"])
    b.close()
out = redact(json.dumps(res, indent=1))
open(f"{OUT}/axe-results-{which}{sys.argv[3] if len(sys.argv) > 3 else ''}.json", "w").write(out)
