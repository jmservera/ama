"""Issue 126 read-only live probe of /api/governance on the deployed demo. Reads credentials at run time; prints only structure."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = os.environ["DEMO_API_URL"]
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")[0].strip()

def shape(v, depth=0):
    if isinstance(v, dict):
        return {k: shape(x, depth + 1) for k, x in v.items()} if depth < 2 else f"dict[{len(v)}]"
    if isinstance(v, list):
        return f"list[{len(v)}]"
    return v if isinstance(v, (bool, int, type(None))) or (isinstance(v, str) and len(v) < 90 and "@" not in v) else "str"

with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1366, "height": 900})
    page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    page.fill("input[name=loginfmt]", rd(".ama-test-user-id")); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", rd(".ama-test-user")); page.click("#idSIButton9")
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
    if me.status == 200:
        out["role"] = me.json().get("role")
    r = c.request.get(APP + "/api/governance")
    out["governance_status"] = r.status
    if r.status == 200:
        g = r.json()
        out["top_level_keys"] = sorted(g)
        rai = g.get("rai") or g.get("rai_evidence") or {}
        out["rai_keys"] = sorted(rai) if isinstance(rai, dict) else str(type(rai))
        if isinstance(rai, dict):
            out["rai_summary"] = {k: rai.get(k) for k in ("history_record_count", "current_disposition_count", "dispositions_complete", "open_count", "acceptance", "live_use", "affected_dispatch") if k in rai}
            out["finding_count"] = len(rai.get("findings", []))
        out["shape"] = shape(g)
    else:
        out["body"] = r.text()[:200]
    b.close()
print(json.dumps(out, indent=1))
