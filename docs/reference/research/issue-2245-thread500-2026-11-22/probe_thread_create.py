"""Issue 2245 thread-creation probe: sign in once, create threads repeatedly (cold and after idle), time each call, then take one skill ask. Credentials are read at run time and never printed."""
import json, os, re, sys, time
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
TAG = sys.argv[1] if len(sys.argv) > 1 else "run"
ROUNDS = int(sys.argv[2]) if len(sys.argv) > 2 else 12
IDLE = int(sys.argv[3]) if len(sys.argv) > 3 else 20
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
emp = {"user": rd(".ama-test-user-id")[0], "pw": rd(".ama-test-user")[0]}
mask = lambda s: re.sub(r"[\w.+-]+@[\w.-]+", "[email]", s)
JS = """async ([path, body, ms]) => {
  const ctl = new AbortController(); const t0 = performance.now();
  const to = setTimeout(() => ctl.abort(), ms);
  try {
    const r = await fetch(path, {method: 'POST', headers: {'content-type': 'application/json', 'X-ZF-CSRF': '1'}, body: JSON.stringify(body), signal: ctl.signal});
    const txt = await r.text(); clearTimeout(to);
    return {status: r.status, secs: (performance.now() - t0) / 1000, text: txt.slice(0, 20000)};
  } catch (e) { return {status: 0, secs: (performance.now() - t0) / 1000, error: String(e).slice(0, 120)}; }
}"""
R = {"tag": TAG, "utc_start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "creates": []}
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    page = c.new_page()
    page.goto(APP + "/sign-in", wait_until="networkidle", timeout=90000)
    page.wait_for_url(re.compile(r"login\.microsoftonline\.com"), timeout=60000)
    page.fill("input[name=loginfmt]", emp["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd], input[name=pass]", timeout=30000)
    page.fill("input[name=passwd], input[name=pass]", emp["pw"]); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)
    page.goto(APP + "/app", wait_until="load", timeout=90000)
    page.wait_for_selector("#employee-chat-launcher", timeout=60000)
    page.screenshot(path=f"{OUT}/{TAG}-workbench.png")
    tid = None
    for i in range(ROUNDS):
        t = time.strftime("%H:%M:%S", time.gmtime())
        r = page.evaluate(JS, ["/api/chat/threads", {}, 90000])
        row = {"n": i + 1, "utc": t, "status": r["status"], "secs": round(r["secs"], 2), "error": r.get("error")}
        if r["status"] == 200:
            tid = json.loads(r["text"])["id"]
        else:
            row["body"] = mask(r.get("text") or "")[:200]
        R["creates"].append(row)
        print(row, flush=True)
        time.sleep(IDLE if i % 3 == 2 else 1)
    if tid:
        r = page.evaluate(JS, [f"/api/chat/threads/{tid}/ask", {"content": "Which homes should I prioritise first by EPC and stock facts?", "skill": "general"}, 150000])
        txt = r.get("text") or ""
        m = re.search(r"Model calls: (\d+)", txt)
        R["ask"] = {"status": r["status"], "secs": round(r["secs"], 2), "model_calls": m.group(1) if m else None, "head": mask(txt)[:300]}
        print(R["ask"], flush=True)
    st = c.request.get(APP + "/api/chat/status")
    R["status"] = {"http": st.status, "body": mask(st.text())[:900]}
    b.close()
txt = json.dumps(R, indent=1)
for v in emp.values():
    assert v not in txt
open(f"{OUT}/{TAG}_probe.json", "w").write(txt)
