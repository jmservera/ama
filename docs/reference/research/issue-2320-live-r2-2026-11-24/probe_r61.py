"""Live probe of revision 0000061 (issues 2320, 145, 2245). Sign-in values are read at run time and never written."""
import json
import os
import sys
import time

from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
u = open(home + "/.ama-test-user-id").read().strip()
p = open(home + "/.ama-test-user").read().strip()
CASE = "ZF-2025-0031"
ASKS = int(sys.argv[1]) if len(sys.argv) > 1 else 2

JS = """async ([path, body]) => {
  const t0 = performance.now();
  const r = await fetch(path, {method: body === null ? 'GET' : 'POST', credentials: 'same-origin',
    headers: {'Content-Type': 'application/json', 'X-ZF-CSRF': '1'}, body: body === null ? undefined : JSON.stringify(body)});
  let j = null; try { j = await r.json(); } catch (e) {}
  return {status: r.status, ms: Math.round(performance.now() - t0), json: j};
}"""


def login(page):
    page.goto(H + "/sign-in")
    for _ in range(4):
        try:
            if page.locator("input[name=loginfmt]").is_visible(timeout=3000):
                page.fill("input[name=loginfmt]", u)
                page.click("input[type=submit]")
                page.wait_for_timeout(1500)
            if page.locator("input[name=passwd]").is_visible(timeout=3000):
                page.fill("input[name=passwd]", p)
                page.click("input[type=submit]")
                page.wait_for_timeout(2000)
            if page.locator("#idBtn_Back").is_visible(timeout=2000):
                page.click("#idBtn_Back")
                page.wait_for_timeout(2000)
        except Exception:
            pass
    try:
        page.wait_for_load_state("networkidle", timeout=60000)
    except Exception:
        pass


def call(pg, path, body=None):
    return pg.evaluate(JS, [path, body])


def shape(r):
    j = r["json"]
    out = {"status": r["status"], "seconds": round(r["ms"] / 1000, 2)}
    if isinstance(j, dict):
        out["keys"] = sorted(j)[:25]
        for k in ("source", "error", "release", "notice", "hold", "held", "reason", "message", "disclosure"):
            if k in j:
                out[k] = str(j[k])[:240]
    elif isinstance(j, list):
        out["list_len"] = len(j)
    return out


res = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "calls": [], "asks": []}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    login(pg)
    pg.goto(H + "/app")
    pg.wait_for_timeout(3000)
    res["me"] = {"role": (call(pg, "/api/me")["json"] or {}).get("role")}
    for path in ["/api/stats"] + ["/api/briefing"] * 6 + ["/api/briefing?mode=workflow", "/api/retention",
                                                         "/api/assistants/forecast", "/api/assistants",
                                                         "/api/chat/status", "/api/stats"]:
        row = {"path": path, **shape(call(pg, path))}
        res["calls"].append(row)
    full = call(pg, "/api/briefing")["json"] or {}
    res["briefing_excerpt"] = json.dumps(full, default=str)[:1500]
    pg.goto(H + "/app")
    pg.wait_for_timeout(4000)
    pg.screenshot(path=os.path.join(OUT, "screens", "overview-briefing.png"))
    for i in range(ASKS):
        t = call(pg, "/api/chat/threads", {"case_id": CASE})
        tid = (t["json"] or {}).get("id")
        e = {"create_status": t["status"]}
        if tid:
            a = call(pg, f"/api/chat/threads/{tid}/ask",
                     {"content": "Summarise in two sentences what is known about this home and who owns the next step."})
            j = a["json"] or {}
            e.update(status=a["status"], seconds=round(a["ms"] / 1000, 2), model=j.get("model"),
                     skill=j.get("skill"), text_head=str(j.get("content") or j.get("text") or j)[:300])
            call(pg, f"/api/chat/threads/{tid}/delete", {})
        res["asks"].append(e)
    s = json.dumps(res, indent=1, default=str)
    assert u not in s and p not in s
    open(os.path.join(OUT, "probe-r61.json"), "w").write(s)
    print(s[:7000])
    b.close()
