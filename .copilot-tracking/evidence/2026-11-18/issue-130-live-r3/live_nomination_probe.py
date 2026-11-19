"""Read-only live probe for epic 104. Credentials are read at run time and never printed or saved."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.<app-fqdn-suffix>"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")[0].strip()
USER, PW = rd(".ama-test-user-id"), rd(".ama-test-user")
PATTERNS = [(re.compile(r"[\w.+-]+@[\w.-]+"), "[email]"),
            (re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"), "[guid]")]


def scrub(text):
    for s in (USER, PW):
        if s:
            text = text.replace(s, "[redacted]")
    for rx, rep in PATTERNS:
        text = rx.sub(rep, text)
    return text


raw = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1366, "height": 900})
    pg = c.new_page()
    pg.goto(APP + "/api/me", wait_until="domcontentloaded")
    pg.fill("input[name=loginfmt]", USER); pg.click("#idSIButton9")
    pg.wait_for_selector("input[name=passwd]", timeout=30000)
    pg.fill("input[name=passwd]", PW); pg.click("#idSIButton9")
    pg.wait_for_selector("#idSIButton9"); pg.click("#idSIButton9")
    try:
        pg.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000, wait_until="commit")
    except Exception:
        print("login stuck at:", pg.url.split("?")[0], "| title:", pg.title(), "| text:", scrub(pg.inner_text("body"))[:300].replace("\n", " "))
        raise
    pg.wait_for_timeout(3000)
    pg.goto(APP + "/app", wait_until="networkidle")

    def get(path):
        r = pg.evaluate("async(p)=>{const r=await fetch(p);let b=null;try{b=await r.json()}catch(e){};return {status:r.status,body:b}}", path)
        return json.loads(scrub(json.dumps(r)))

    cases = get("/api/cases")
    raw["/api/cases"] = {"status": cases["status"], "shape": type(cases["body"]).__name__}
    body = cases["body"]
    items = body if isinstance(body, list) else (body.get("cases") or body.get("items") or [])
    raw["case_count"] = len(items)
    cid = items[0].get("id") if items else None
    if cid:
        d = get("/api/cases/%s?view=nomination-routes" % cid)
        raw["route_detail"] = {"status": d["status"], "keys": sorted((d["body"] or {}).keys())[:40]}
        raw["nomination_routes_block"] = (d["body"] or {}).get("nomination_routes")
        pg.goto(APP + "/api/cases/%s?view=nomination-routes-html" % cid, wait_until="networkidle")
        raw["html_title"] = scrub(pg.title())
        raw["html_text"] = scrub(pg.inner_text("body"))[:3000]
        pg.screenshot(path=os.path.join(OUT, "nomination-routes-1366.png"), full_page=True)
    b.close()
json.dump(raw, open(os.path.join(OUT, "live_nomination_probe.json"), "w"), indent=1)
print({k: v["status"] for k, v in raw.items()})
