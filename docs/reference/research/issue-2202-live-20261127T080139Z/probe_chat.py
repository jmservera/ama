"""Issue 2195 live routing proof on the deployed demo API. Credentials read at runtime, never printed."""
import json, os, re, time
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
emp = {"user": rd(".ama-test-user-id")[0], "pw": rd(".ama-test-user")[0]}
QS = [
    ("quality", "Is the quality inspection evidence complete?"),
    ("funding", "Can you check the grant claim and invoice?"),
    ("stock", "Which stock should we prioritise by EPC ranking?"),
    ("tie", "Is the grant claim quality checked and which defect?"),
    ("general", "Tell me what you can help with"),
    ("refused", "Approve the funding claim for this home"),
]
R = {"questions": [], "chat_http": []}
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1280, "height": 900})
    page = c.new_page()
    def on_resp(r):
        if "/api/chat/" in r.url and r.request.method == "POST":
            body = ""
            if r.status >= 400:
                try: body = r.text()[:300]
                except Exception: pass
            R["chat_http"].append({"path": re.sub(r"threads/[^/]+", "threads/<id>", r.url.split("//")[1].split("/",1)[1]), "status": r.status, "error_body": body})
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
    page.goto(APP + "/app", wait_until="load", timeout=90000); page.wait_for_selector("#employee-chat-launcher", timeout=60000)
    R["title"] = page.title()
    page.locator("#employee-chat-launcher").click()
    dialog = page.get_by_role("dialog", name="Employee assistant")
    dialog.wait_for(timeout=15000)
    R["selects"] = [{"label": s.get_attribute("aria-label") or s.get_attribute("id"), "options": s.locator("option").all_inner_texts()} for s in dialog.locator("select").all()]
    sk = c.request.get(APP + "/api/chat/skills")
    R["api_chat_skills"] = {"status": sk.status, "ids": [x.get("id") for x in sk.json().get("skills", [])] if sk.ok else None}
    am = c.request.get(APP + "/api/assistants")
    R["api_assistants_status"] = am.status
    q = page.get_by_label("Your work question", exact=True)
    try:
        dialog.get_by_role("button", name="Send", exact=True).and_(page.locator(":enabled")).wait_for(timeout=20000)
    except Exception:
        q.fill("x")
        R["send_disabled_dump"] = {"chat_http": R["chat_http"], "dialog_text": re.sub(r"[\w.+-]+@[\w.-]+", "[email]", dialog.inner_text())[:1500]}
        page.screenshot(path=f"{OUT}/send-disabled.png")
        print(json.dumps(R["send_disabled_dump"], indent=1)); raise SystemExit(1)
    R["retries_after_500"] = 0
    for key, text in QS:
        for attempt in range(4):
            t0 = time.time()
            try:
                dialog.get_by_role("button", name="Send", exact=True).and_(page.locator(":enabled")).wait_for(timeout=90000)
            except Exception:
                R.setdefault("send_stuck", []).append({"key": key, "waited_s": round(time.time() - t0)})
                print(json.dumps(R.get("send_stuck")), json.dumps(R["chat_http"][-3:]))
                raise
            R.setdefault("send_wait_s", {})[key] = round(time.time() - t0, 1)
            before = len(dialog.locator(".chat-widget-routing").all_inner_texts())
            q.fill(text)
            dialog.get_by_role("button", name="Send", exact=True).click()
            try:
                page.wait_for_function("n => document.querySelectorAll('.chat-widget-routing').length > n", arg=before, timeout=90000)
                break
            except Exception:
                R["retries_after_500"] += 1
                page.wait_for_timeout(3000)
        page.wait_for_timeout(1500)
        routing = dialog.locator(".chat-widget-routing").all_inner_texts()
        R["questions"].append({"key": key, "question": text, "routing_line": routing[-1] if len(routing) > before else None, "attempts": attempt + 1})
        page.evaluate("""()=>{for(const e of document.querySelectorAll('body *')){if(e.children.length===0&&/@/.test(e.textContent||''))e.textContent=e.textContent.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}""")
        page.screenshot(path=f"{OUT}/live-{key}.png")
    R["log_text"] = re.sub(r"[\w.+-]+@[\w.-]+", "[email]", dialog.get_by_role("log").inner_text())[:3000]
    b.close()
txt = json.dumps(R, indent=1)
for v in emp.values():
    assert v not in txt
open(f"{OUT}/live_routing_probe.json", "w").write(txt)
print(txt[:4000])
