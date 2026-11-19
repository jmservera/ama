"""Fourth-run live re-check for issue 153 (read-only, desktop 1440x900). Session state stays in ~/.cache/ama153."""
import json, os, re
from playwright.sync_api import sync_playwright

STAFF = os.environ["DEMO_API_URL"]
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.expanduser("~/.cache/ama153/state-staff.json")
BANNED = re.compile(r"\b(gates?|holds?|held|provenance|traces?|snapshots?|envelopes?|human-approved|ai-drafted|"
                    r"pending|unassigned|consent pending|hazard unresolved)\b", re.I)
home = os.path.expanduser("~")
secrets = []
for f in (".ama-test-user-id", ".ama-resident-test-user"):
    try:
        secrets += [x.strip() for x in open(os.path.join(home, f)).read().splitlines()[:1] if "@" in x]
    except OSError:
        pass
secrets += [s.split("@")[0] for s in secrets if len(s.split("@")[0]) > 3]


def clean(t):
    for s in secrets:
        t = t.replace(s, "[redacted]")
    return re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[redacted-email]", t)


MASK = """(s)=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);const n=[];while(w.nextNode())n.push(w.currentNode);
for(const t of n){let v=t.nodeValue;for(const e of s)v=v.split(e).join('[redacted]');v=v.replace(/[\\w.+-]+@[\\w-]+\\.[\\w.-]+/g,'[redacted-email]');t.nodeValue=v;}}"""

res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    for name, path in [("staff-all", "/app#/all"), ("staff-finance", "/app#/finance"),
                       ("staff-handoff-waiting", "/app#/handoff-waiting")]:
        pg.goto(STAFF + path); pg.wait_for_timeout(5000)
        pg.evaluate(MASK, secrets)
        t = clean(pg.inner_text("body"))
        pg.screenshot(path=f"{OUT}/screens/{name}.png")
        res[name] = {"signed_in": "sign" not in pg.title().lower() or len(t) > 400, "chars": len(t),
                     "hit_lines": [l.strip() for l in t.splitlines() if BANNED.search(l)][:10]}
    pg.goto(STAFF + "/app#/"); pg.wait_for_timeout(5000)
    links = pg.eval_on_selector_all("a[href^='#/case/']", "e=>e.map(x=>x.getAttribute('href'))")
    pg.goto(STAFF + "/app" + sorted(set(links))[0]); pg.wait_for_timeout(6000)
    pg.get_by_role("tab", name=re.compile("^Quality and handover")).first.click(timeout=4000); pg.wait_for_timeout(1500)
    pg.evaluate(MASK, secrets)
    t = clean(pg.inner_text("body"))
    pg.screenshot(path=f"{OUT}/screens/staff-case-quality-and-handover.png")
    res["staff-case-quality"] = {"chars": len(t), "hit_lines": [l.strip() for l in t.splitlines() if BANNED.search(l)][:10]}
    cid = sorted(set(links))[0].split("/")[-1]
    probes = [("GET unknown case", "get", f"/api/cases/NO-SUCH-CASE", None),
              ("GET unknown route", "get", "/api/no-such-route", None),
              ("POST empty body to case resident", "post", f"/api/cases/{cid}/resident", {})]
    for lbl, m, p, body in probes:
        r = getattr(c.request, m)(STAFF + p, **({"data": body} if body is not None else {}))
        res[lbl] = {"status": r.status, "body": clean(r.text())[:400]}
    anon = b.new_context().request.get(STAFF + "/api/cases", max_redirects=0)
    res["GET /api/cases unauthenticated"] = {"status": anon.status, "body": clean(anon.text())[:300]}
    b.close()
json.dump(res, open(f"{OUT}/recheck-results.json", "w"), indent=1)
print(json.dumps(res, indent=1))
