"""Issue 154 round 3: network trace of the live resident showcase, signed in, panels expanded.
Credentials are read at run time and never printed or written. Request bodies are not stored; only method, host, path and status."""
import json, os
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

OUT = os.path.dirname(os.path.abspath(__file__))
RES = os.environ["DEMO_RESIDENT_URL"]
rcred = [x.strip() for x in open(os.path.expanduser("~/.ama-resident-test-user")).read().split("\n") if x.strip()]
em, pw = rcred[0], rcred[1]
reqs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1366, "height": 900})
    pg.on("request", lambda r: reqs.append({"method": r.method, "host": urlparse(r.url).netloc, "path": urlparse(r.url).path, "type": r.resource_type}))
    pg.goto(RES + "/"); pg.wait_for_load_state("networkidle")
    pg.fill("#email", em); pg.fill("#password", pw); pg.click("#signin-button")
    pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(2500)
    for bt in pg.query_selector_all("button[aria-expanded=false]"):
        try: bt.click(timeout=2000)
        except Exception: pass
    pg.wait_for_timeout(1500)
    dom = pg.evaluate("""()=>({
      links_scheme:[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href').split(':')[0]).filter(s=>['mailto','tel','sms'].includes(s)),
      forms:[...document.querySelectorAll('form')].map(f=>f.getAttribute('action')),
      textareas:document.querySelectorAll('textarea').length,
      text_inputs:[...document.querySelectorAll('input')].filter(i=>['text','email','tel','search'].includes(i.type||'text')).length})""")
    b.close()
hosts = sorted({r["host"] for r in reqs})
write = [r for r in reqs if r["method"] not in ("GET", "HEAD", "OPTIONS")]
json.dump({"hosts": hosts, "request_count": len(reqs), "non_get_requests": write, "requests": reqs, "dom": dom}, open(os.path.join(OUT, "network-trace-raw.json"), "w"), indent=1)
print(len(reqs), hosts, write, dom)
