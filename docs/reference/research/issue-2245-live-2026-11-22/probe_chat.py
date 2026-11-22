"""Issue 2245 live employee chat probe. Credentials are read at run time and never printed."""
import json, os, re, sys
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
TAG = sys.argv[1] if len(sys.argv) > 1 else "run"
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
emp = {"user": rd(".ama-test-user-id")[0], "pw": rd(".ama-test-user")[0]}
QS = [
    ("general", "Tell me what you can help with"),
    ("explain", "Explain in two sentences why airtightness testing matters before retrofit insulation."),
    ("stock", "Which stock should we prioritise by EPC ranking?"),
    ("funding", "Can you check the grant claim and invoice?"),
    ("quality", "Is the quality inspection evidence complete?"),
]
R = {"tag": TAG, "asks": [], "chat_http": []}
mask = lambda s: re.sub(r"[\w.+-]+@[\w.-]+", "[email]", s)
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    page = c.new_page()

    def on_resp(r):
        if "/api/chat/" in r.url and r.request.method == "POST":
            row = {"path": re.sub(r"threads/[^/]+", "threads/<id>", r.url.split("//")[1].split("/", 1)[1]), "status": r.status}
            try:
                j = r.json()
                row["keys"] = sorted(j.keys())[:30]
                for k in ("kind", "model", "answer_source", "label", "consumption", "workflow_only"):
                    if k in j:
                        row[k] = j[k]
                a = j.get("answer") or j.get("reply") or {}
                if isinstance(a, dict):
                    for k in ("kind", "model", "answer_source", "consumption"):
                        if k in a:
                            row["a_" + k] = a[k]
                if r.status >= 400:
                    row["error_body"] = mask(json.dumps(j))[:400]
            except Exception:
                try:
                    row["body"] = mask(r.text())[:300]
                except Exception:
                    pass
            R["chat_http"].append(row)

    page.on("response", on_resp)
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
    R["status"] = {"http": st.status, "body": mask(st.text())[:800]}
    page.locator("#employee-chat-launcher").click()
    dialog = page.get_by_role("dialog", name="Employee assistant")
    dialog.wait_for(timeout=15000)
    R["banner"] = mask(dialog.inner_text())[:700]
    q = page.get_by_label("Your work question", exact=True)
    dialog.get_by_role("button", name="Send", exact=True).and_(page.locator(":enabled")).wait_for(timeout=30000)
    for key, text in QS:
        n = len(R["chat_http"])
        q.fill(text)
        dialog.get_by_role("button", name="Send", exact=True).click()
        page.wait_for_timeout(12000)
        log = mask(dialog.get_by_role("log").inner_text())
        R["asks"].append({"key": key, "question": text, "http_rows": R["chat_http"][n:], "log_tail": log[-900:]})
        page.screenshot(path=f"{OUT}/{TAG}-{key}.png")
    b.close()
txt = json.dumps(R, indent=1)
for v in emp.values():
    assert v not in txt
open(f"{OUT}/{TAG}_probe.json", "w").write(txt)
print(txt[:6000])
