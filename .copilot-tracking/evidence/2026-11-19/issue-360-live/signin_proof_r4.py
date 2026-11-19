"""Issue 360 live proof: direct ingress sign-in, role, persistence read and AI call. Credentials are read at runtime and never printed."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")[0].strip()
emp = {"user": rd(".ama-test-user-id"), "pw": rd(".ama-test-user")}

def login(page):
    page.fill("input[name=loginfmt]", emp["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", emp["pw"]); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP): break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)

out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    page.goto(APP + "/", wait_until="networkidle")
    out["welcome_title"] = page.title()
    page.screenshot(path=f"{OUT}/1-welcome-anonymous.png")
    page.goto(APP + "/app", wait_until="domcontentloaded")
    out["app_anonymous_url_host"] = re.sub(r"^https?://([^/]+).*", r"\1", page.url)
    page.screenshot(path=f"{OUT}/2-entra-redirect.png")
    try:
        login(page)
        out["callback_returned_to_app"] = page.url.startswith(APP)
        page.goto(APP + "/app", wait_until="networkidle")
        out["app_title"] = page.title()
        page.evaluate("()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}")
        page.screenshot(path=f"{OUT}/3-workbench-signed-in.png")
        me = c.request.get(APP + "/api/me"); out["me_status"] = me.status
        if me.status == 200:
            u = me.json().get("user", {})
            out["me"] = {k: u.get(k) for k in ("role", "app_roles", "view_only", "identity_source", "auth_provider")}
        st = c.request.get(APP + "/api/stats"); out["stats_status"] = st.status
        if st.status == 200:
            j = st.json(); out["stats_keys"] = sorted(j.keys())[:15]; out["stats"] = {k: j[k] for k in j if isinstance(j[k], (int, float))}
        h = {"Origin": APP, "Content-Type": "application/json", "X-ZF-CSRF": "1"}
        stat = c.request.get(APP + "/api/chat/status"); out["chat_status_http"] = stat.status
        if stat.status == 200: out["chat_activation"] = stat.json().get("activation")
        r = page.evaluate("""async()=>{const H={'Content-Type':'application/json','X-ZF-CSRF':'1'};const j=async(m,u,b)=>{const r=await fetch(u,{method:m,headers:H,body:b?JSON.stringify(b):undefined});const t=await r.text();let o=null;try{o=JSON.parse(t)}catch(e){}return {s:r.status,o,t:t.slice(0,300)}};
const cs=await j('GET','/api/cases?view=all');const cid=cs.o&&(cs.o.items||cs.o.cases||[])[0];const cr=cid?(cid.id||cid.reference||cid.ref):null;const th=await j('POST','/api/chat/threads',cr?{case_id:cr}:{});const res={thread:th.s};if(th.o&&th.o.id){const a=await j('POST','/api/chat/threads/'+th.o.id+'/messages',{content:'Summarise this case status in one sentence.'});res.ask=a.s;res.ask_keys=a.o?Object.keys(a.o).slice(0,12):null;res.model=a.o?a.o.model:null;res.consumption=a.o?a.o.consumption:null;res.withheld=a.o?a.o.withheld:null;res.answer_excerpt=a.o?String(a.o.answer||a.o.content||a.o.text||JSON.stringify(a.o)).slice(0,300):a.t;res.thread_id=th.o.id}else{res.body=th.t}return res}""")
        out["ai"] = r
        ca = c.request.get(APP + "/api/cases?view=all"); out["cases_all_total"] = ca.json().get("total") if ca.status == 200 else ca.status
        for path in ("/api/sensors",):
            out.setdefault("role_probe", {})[path] = c.request.get(APP + path).status
        for hdr in ({"X-ZF-Role": "Admin"}, {"X-MS-CLIENT-PRINCIPAL-NAME": "forged@example.com"}):
            fr = c.request.get(APP + "/api/me", headers=hdr); out.setdefault("forged_with_session", []).append(fr.json().get("user", {}).get("role") if fr.status == 200 else fr.status)
        tid = out["ai"].get("thread_id")
        if tid:
            c2 = b.new_context(viewport={"width": 1366, "height": 900}); p2 = c2.new_page()
            p2.goto(APP + "/app", wait_until="domcontentloaded"); login(p2)
            p2.goto(APP + "/app", wait_until="networkidle")
            out["persistence"] = p2.evaluate("""async(tid)=>{const H={'Content-Type':'application/json','X-ZF-CSRF':'1'};const g=await fetch('/api/chat/threads');const o=await g.json();const ids=(o.threads||[]).map(t=>t.id);const th=await fetch('/api/chat/threads/'+tid);const d=await fetch('/api/chat/threads/'+tid+'/delete',{method:'POST',headers:H,body:'{}'});const g2=await (await fetch('/api/chat/threads')).json();return {second_session_sees_thread:ids.includes(tid),thread_get:th.status,delete:d.status,still_listed_after_delete:(g2.threads||[]).some(t=>t.id==tid)}}""", tid)
            cr2 = c2.request.get(APP + "/api/cases?view=all"); out["persistence"]["new_session_cases_total"] = cr2.json().get("total")
            for old in os.environ.get("CLEAN_IDS", "").split(","):
                if old: out.setdefault("cleanup", {})[old] = p2.evaluate("async(i)=>(await fetch('/api/chat/threads/'+i+'/delete',{method:'POST',headers:{'Content-Type':'application/json','X-ZF-CSRF':'1'},body:'{}'})).status", old)
            c2.close()
    except Exception as e:
        out["error"] = type(e).__name__ + ": " + str(e)[:120].replace(emp["user"], "[x]")
        page.screenshot(path=f"{OUT}/err.png")
    br = b.new_context(user_agent="Mozilla/5.0 (X11; Linux x86_64) Chrome/120 Safari/537.36", extra_http_headers={"Accept": "application/json"})
    out["anon_browser_mode"] = {pp: br.request.get(APP + pp, max_redirects=0).status for pp in ("/api/me", "/api/cases")}
    b.close()
print(json.dumps(out, indent=1))
