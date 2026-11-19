"""Issue 129 live probe: signed-in employee view of the deployed demo. Reads credentials at run time; prints only redacted facts."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")
emp = {"user": rd(".ama-test-user-id")[0].strip(), "pw": rd(".ama-test-user")[0].strip()}
KEYS = re.compile(r"learning|bundle|experiment|atlas", re.I)

with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1366, "height": 900})
    page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    page.fill("input[name=loginfmt]", emp["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", emp["pw"]); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)
    out = {"signed_in": page.url.startswith(APP)}
    me = c.request.get(APP + "/api/me")
    out["me_status"] = me.status
    nav = me.json().get("navigation", []) if me.status == 200 else []
    out["navigation_count"] = len(nav)
    out["navigation_matches_learning_keywords"] = [n for n in nav if KEYS.search(json.dumps(n))]
    out["probe"] = {}
    for path in ["/api/learning", "/api/learning-bundles", "/api/learning-test-bundles", "/learning-bundles",
                 "/api/zz-control-nonexistent", "/api/bundles", "/api/experiments", "/api/atlas/bundles", "/openapi.json", "/docs"]:
        r = c.request.get(APP + path, max_redirects=0)
        out["probe"][path] = r.status
    r = c.request.get(APP + "/openapi.json")
    if r.status == 200:
        paths = list(r.json().get("paths", {}))
        out["openapi_path_count"] = len(paths)
        out["openapi_paths_matching_learning_keywords"] = [x for x in paths if KEYS.search(x)]
    page.goto(APP + "/app", wait_until="networkidle")
    body = page.inner_text("body")
    out["app_text_keyword_hits"] = sorted(set(m.group(0).lower() for m in KEYS.finditer(body)))
    page.evaluate("""()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}""")
    page.screenshot(path=f"{OUT}/employee-workbench.png")
    b.close()
print(json.dumps(out, indent=1))
