"""Issue 2245 chat ask latency probe (timed API asks after a browser sign-in). Credentials are read at run time and never printed."""
import json, os, re, sys
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
TAG = sys.argv[1] if len(sys.argv) > 1 else "run"
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
emp = {"user": rd(".ama-test-user-id")[0], "pw": rd(".ama-test-user")[0]}
QS0 = [
    ("general", "Tell me what you can help with"),
    ("explain", "Explain in two sentences why airtightness testing matters before retrofit insulation."),
    ("stock", "Which stock should we prioritise by EPC ranking?"),
    ("funding", "Can you check the grant claim and invoice?"),
    ("quality", "Is the quality inspection evidence complete?"),
]
R = {"tag": TAG, "asks": [], "chat_http": []}
mask = lambda s: re.sub(r"[\w.+-]+@[\w.-]+", "[email]", s)
QS = [("refused-control", "Approve the grant claim for me now"), ("refused-control-2", "Please send the resident a letter now")] + QS0 + [
    ("epc-stock", "Which homes should I prioritise first by EPC and stock facts?"),
    ("funding-status", "What is the status of the funding grant claim?"),
    ("quality-note", "Show a quality defect inspection note on the sensor readings"),
]
R = {"tag": TAG, "asks": []}
mask = lambda s: re.sub(r"[\w.+-]+@[\w.-]+", "[email]", s)
JS = """async ([path, body, ms]) => {
  const ctl = new AbortController(); const t0 = performance.now();
  const to = setTimeout(() => ctl.abort(), ms);
  try {
    const r = await fetch(path, {method: 'POST', headers: {'content-type': 'application/json', 'X-ZF-CSRF': '1'}, body: JSON.stringify(body), signal: ctl.signal});
    const txt = await r.text(); clearTimeout(to);
    return {status: r.status, secs: (performance.now() - t0) / 1000, text: txt.slice(0, 60000)};
  } catch (e) { return {status: 0, secs: (performance.now() - t0) / 1000, error: String(e).slice(0, 120)}; }
}"""
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
    st = c.request.get(APP + "/api/chat/status")
    R["status"] = {"http": st.status, "body": mask(st.text())[:900]}
    th = page.evaluate(JS, ["/api/chat/threads", {}, 60000])
    R["thread"] = {"status": th["status"], "secs": round(th["secs"], 2)}
    tid = json.loads(th["text"])["id"] if th["status"] == 200 else None
    for key, text in QS:
        if not tid:
            break
        r = page.evaluate(JS, [f"/api/chat/threads/{tid}/ask", dict({"content": text}, skill="general"), 150000])
        row = {"key": key, "status": r["status"], "secs": round(r["secs"], 2), "error": r.get("error")}
        try:
            j = json.loads(r.get("text") or "")
            row["kind"] = j.get("kind")
            row["answer_head"] = mask(str(j.get("answer") or j.get("content") or j))[:300]
            m = re.search(r"Model calls: (\d+)", json.dumps(j))
            row["model_calls"] = m.group(1) if m else None
            row["skill"] = re.findall(r"Skill: ([\w-]+)", json.dumps(j))[:1]
        except Exception:
            row["body"] = mask(r.get("text") or "")[:200]
        R["asks"].append(row)
        print(row["key"], row["status"], row["secs"], row.get("model_calls"), flush=True)
    b.close()
txt = json.dumps(R, indent=1)
for v in emp.values():
    assert v not in txt
open(f"{OUT}/{TAG}_probe.json", "w").write(txt)
