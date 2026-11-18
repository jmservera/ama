"""Live isolation probe for #162 on the synthetic demo. Reads credentials from the owner's files at runtime; prints none.

Run login.py staff first (writes /tmp/state-staff.json). Output goes to stdout; identifiers are redacted.
"""
import base64
import json
import os
import re
import sys
from playwright.sync_api import sync_playwright

API = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
RES = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
HERE = os.path.dirname(os.path.abspath(__file__))
FETCH = """async ([m,p,b,h])=>{const o={method:m,headers:Object.assign({'X-ZF-CSRF':'1','Content-Type':'application/json'},h||{}),credentials:'same-origin'};
if(b!==null&&b!==undefined)o.body=JSON.stringify(b);const r=await fetch(p,o);return [r.status,(await r.text()).slice(0,60000)]}"""


def red(text):
    text = re.sub(r"CT-[0-9a-f]{16}", lambda m: m.group(0)[:5] + "<id>", str(text))
    text = re.sub(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "<guid>", text)
    text = re.sub(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", "<email>", text)
    return text


def say(label, *vals):
    print(label, "|", " ".join(red(v) for v in vals), flush=True)


def jbody(t):
    try:
        return json.loads(t)
    except ValueError:
        return None


with sync_playwright() as pw:
    b = pw.chromium.launch()

    # 1. Anonymous: no session at all
    anon = b.new_context()
    for p in ("/api/chat/threads", "/api/chat/memory", "/api/chat/status", "/api/chat/threads/CT-0000000000000000"):
        r = anon.request.get(API + p, max_redirects=0)
        say("ANON GET " + p, r.status, (r.headers.get("location") or "")[:60].split("?")[0])
    r = anon.request.post(API + "/api/chat/memory", data=json.dumps({"content": "x", "task": ""}), max_redirects=0,
                          headers={"X-ZF-CSRF": "1", "Content-Type": "application/json"})
    say("ANON POST /api/chat/memory", r.status)
    anon.close()

    # 2. Resident session (resident portal) replayed against the staff API
    h = os.path.expanduser("~")
    lines = open(h + "/.ama-resident-test-user").read().splitlines()
    rc = b.new_context(viewport={"width": 1440, "height": 900})
    rp = rc.new_page()
    rp.goto(RES + "/", timeout=90000)
    rp.wait_for_load_state("networkidle")
    rp.fill("#email", lines[0].strip())
    rp.fill("#password", lines[1].strip())
    rp.click("#signin-button")
    rp.wait_for_timeout(4000)
    cookies = rc.cookies()
    say("RESIDENT sign-in on resident app", "cookies:", ",".join(sorted(c["name"] for c in cookies)))
    rp.screenshot(path=HERE + "/shots/resident-signed-in-resident-app.png")
    for p in ("/api/chat/threads", "/api/chat/memory"):
        s = rc.request.get(RES + p, max_redirects=0)
        say("RESIDENT app GET " + p, s.status)
    sess = "; ".join(f"{c['name']}={c['value']}" for c in cookies)
    for p in ("/api/chat/threads", "/api/chat/memory"):
        r = b.new_context().request.get(API + p, max_redirects=0, headers={"Cookie": sess})
        say("RESIDENT cookie replayed to staff API GET " + p, r.status, (r.headers.get("location") or "")[:60].split("?")[0])
    rp.evaluate("async()=>{await fetch('/demo/logout',{method:'POST',headers:{'X-CSRF-Token':(document.cookie.match(/__Host-zfdemo-csrf=([^;]+)/)||[])[1]||''},credentials:'same-origin'})}")
    rc.close()

    # 3. Staff: own thread and memory, then forged and cross-owner attempts
    c = b.new_context(storage_state="/tmp/state-staff.json", viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    pg.goto(API + "/app")
    pg.wait_for_load_state("networkidle")
    call = lambda m, p, body=None, hdr=None: pg.evaluate(FETCH, [m, p, body, hdr])
    me = jbody(call("GET", "/api/me")[1]) or {}
    me_acc = json.dumps(me.get("account"), sort_keys=True)
    say("STAFF /api/me has account block", bool(me.get("account")), "keys", len(me))

    st0 = call("GET", "/api/chat/memory/status?task=")
    say("STAFF memory status before", st0[0], st0[1][:200])
    mem0 = jbody(call("GET", "/api/chat/memory")[1]) or []
    th0 = jbody(call("GET", "/api/chat/threads")[1]) or []
    say("STAFF before counts", "threads", len(th0), "memory", len(mem0))
    ids0 = {t["id"] for t in th0}

    cr = call("POST", "/api/chat/threads", {})
    tid = (jbody(cr[1]) or {}).get("id", "")
    say("STAFF create thread", cr[0], tid)
    ack = call("POST", "/api/chat/memory/opt-in", {"acknowledged": True})
    say("STAFF memory opt-in", ack[0], ack[1][:120])
    mm = call("POST", "/api/chat/memory", {"content": "ISOLATION-PROBE synthetic memory item", "task": "stock-prioritisation"})
    mid = (jbody(mm[1]) or {}).get("id", "")
    say("STAFF add memory", mm[0], mm[1][:160])
    pg.screenshot(path=HERE + "/shots/staff-app-before-probes.png")

    forged = base64.b64encode(json.dumps({
        "auth_typ": "aad", "name_typ": "x", "role_typ": "roles",
        "claims": [{"typ": "oid", "val": "00000000-0000-0000-0000-000000000001"},
                   {"typ": "tid", "val": "00000000-0000-0000-0000-000000000002"},
                   {"typ": "preferred_username", "val": "other.user@example.invalid"},
                   {"typ": "roles", "val": "ZavaForward.ProgrammeManager"}]}).encode()).decode()
    for label, hdr in (("forged X-MS-CLIENT-PRINCIPAL", {"X-MS-CLIENT-PRINCIPAL": forged}),
                       ("forged X-MS-CLIENT-PRINCIPAL-NAME/-ID", {"X-MS-CLIENT-PRINCIPAL-NAME": "other.user@example.invalid",
                                                                   "X-MS-CLIENT-PRINCIPAL-ID": "00000000-0000-0000-0000-000000000001"})):
        r = call("GET", "/api/chat/threads", None, hdr)
        got = jbody(r[1])
        same = isinstance(got, list) and {t["id"] for t in got} == ids0 | {tid}
        say("STAFF " + label + " GET threads", r[0], "same-owner-view:", same)
        r = call("GET", "/api/chat/memory", None, hdr)
        got = jbody(r[1])
        say("STAFF " + label + " GET memory", r[0], "same-owner-view:", isinstance(got, list) and {m["id"] for m in got} == {m["id"] for m in mem0} | {mid})
        r = call("GET", "/api/me", None, hdr)
        say("STAFF " + label + " GET /api/me unchanged", r[0], json.dumps((jbody(r[1]) or {}).get("account"), sort_keys=True) == me_acc)

    # Client-chosen owner parameters are refused or ignored
    for q in ("owner=other.user@example.invalid", "user=other.user@example.invalid", "user_id=1", "email=other.user@example.invalid"):
        r = call("GET", "/api/chat/threads?" + q)
        got = jbody(r[1])
        say("STAFF GET threads?" + q.split("=")[0], r[0], "same-owner-view:", isinstance(got, list) and {t["id"] for t in got} == ids0 | {tid})
    for field in ("owner", "user", "email"):
        r = call("POST", "/api/chat/threads/" + tid + "/ask", {"content": "hi", field: "other.user@example.invalid"})
        say("STAFF POST ask with body field " + field, r[0], r[1][:100])

    # Foreign-looking ids: never-issued thread and memory ids give 404, not data or a different error class
    fake = "CT-" + "0" * 16
    for m, p, body in (("GET", "/api/chat/threads/" + fake, None), ("POST", "/api/chat/threads/" + fake + "/ask", {"content": "hi"}),
                       ("POST", "/api/chat/threads/" + fake + "/messages", {"content": "hi"}),
                       ("POST", "/api/chat/threads/" + fake + "/archive", {}), ("POST", "/api/chat/threads/" + fake + "/delete", {}),
                       ("POST", "/api/chat/memory/" + "0" * 32 + "/edit", {"content": "x"}),
                       ("POST", "/api/chat/memory/" + "0" * 32 + "/delete", {})):
        r = call(m, p, body)
        say(f"STAFF {m} {re.sub(r'CT-0+', 'CT-<nonexistent>', p)}", r[0], r[1][:80])

    # Own-thread positive control so the 404s above are not just a broken route
    r = call("GET", "/api/chat/threads/" + tid)
    say("STAFF positive control own thread GET", r[0], "id-matches:", (jbody(r[1]) or {}).get("id") == tid)
    r = call("GET", "/api/chat/memory")
    say("STAFF positive control own memory list", r[0], "contains-own:", mid in {m["id"] for m in (jbody(r[1]) or [])})
    pg.screenshot(path=HERE + "/shots/staff-app-after-probes.png")

    # Cleanup: only what this script created
    if mid:
        say("CLEANUP delete own memory item", *call("POST", "/api/chat/memory/" + mid + "/delete", {})[:1])
    if tid:
        say("CLEANUP delete own thread", *call("POST", "/api/chat/threads/" + tid + "/delete", {})[:1])
    if not mem0 and "not opted in" in st0[1]:
        say("CLEANUP memory opt-out (user had no items and was not opted in)", call("POST", "/api/chat/memory/opt-out", {})[0])
    after_t = jbody(call("GET", "/api/chat/threads")[1]) or []
    after_m = jbody(call("GET", "/api/chat/memory")[1]) or []
    say("STAFF after cleanup counts", "threads", len(after_t), "memory", len(after_m), "restored:", len(after_t) == len(th0) and len(after_m) == len(mem0))
    say("STAFF memory status after", *call("GET", "/api/chat/memory/status?task=")[:2])
    b.close()
