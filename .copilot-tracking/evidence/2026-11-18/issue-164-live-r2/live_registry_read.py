"""Live demo chat UI probe for issue 164 (second pass). Credentials are read at run time and never printed or saved."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")[0].strip()
USER, PW = rd(".ama-test-user-id"), rd(".ama-test-user")
SECRETS = [USER, PW]
PATTERNS = [(re.compile(r"[\w.+-]+@[\w.-]+"), "[email]"),
            (re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"), "[guid]")]


def scrub(text):
    for s in SECRETS:
        if s:
            text = text.replace(s, "[redacted]")
    for rx, rep in PATTERNS:
        text = rx.sub(rep, text)
    return text



raw = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    pg.goto(APP + "/api/me", wait_until="domcontentloaded")
    pg.fill("input[name=loginfmt]", USER); pg.click("#idSIButton9")
    pg.wait_for_selector("input[name=passwd]", timeout=30000)
    pg.fill("input[name=passwd]", PW); pg.click("#idSIButton9")
    pg.wait_for_selector("#idSIButton9"); pg.click("#idSIButton9")
    pg.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000, wait_until="commit")
    pg.wait_for_timeout(3000)
    pg.goto(APP + "/app", wait_until="networkidle")
    g = lambda path: json.loads(scrub(json.dumps(pg.evaluate("async(p)=>{const r=await fetch(p);return await r.json()}", path))))
    rep = g("/api/ai/report")
    reg = rep.get("registry") or rep
    raw["chat_status"] = g("/api/chat/status")
    raw["memory_status"] = g("/api/chat/memory/status")
    raw["ai_report_keys"] = list(rep.keys())
    def find(o):
        if isinstance(o, dict):
            if o.get("task") == "chat-case-conversation" or o.get("id") == "chat-case-conversation": return o
            for v in o.values():
                r = find(v)
                if r: return r
        if isinstance(o, list):
            for v in o:
                r = find(v)
                if r: return r
    raw["chat_registry_entry"] = find(rep)
    pg.goto(APP + "/app", wait_until="networkidle")
    b.close()
json.dump(raw, open(os.path.join(OUT, "live_registry_read.json"), "w"), indent=1)
print(list(raw), bool(raw["chat_registry_entry"]))
