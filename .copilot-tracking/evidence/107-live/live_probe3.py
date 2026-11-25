"""Issue 107 r12 probe 2026-11-25. GET only. Reads sign-in values at runtime; prints structural facts only."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
emp = {"user": rd(".ama-test-user-id")[0], "pw": rd(".ama-test-user")[0]}
G = """async(p)=>{const r=await fetch(p,{credentials:'same-origin'});let t=await r.text();let j=null;try{j=JSON.parse(t)}catch(e){}
const sh=(v,d)=>{if(Array.isArray(v))return {len:v.length,first:v.length&&d<2?sh(v[0],d+1):null};if(v&&typeof v==='object')return Object.fromEntries(Object.entries(v).slice(0,25).map(([k,x])=>[k,d<2?sh(x,d+1):typeof x==='string'?'str':typeof x==='number'||typeof x==='boolean'?x:typeof x]));return typeof v==='string'?'str':v};
return [r.status,sh(j,0)]}"""
R = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    page = c.new_page()
    page.goto(APP + "/", wait_until="networkidle", timeout=90000)
    page.click("a[href='/sign-in']")
    page.wait_for_url(re.compile(r"login\.microsoftonline\.com"), timeout=60000)
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
    page.wait_for_load_state("networkidle")
    G2 = "async(p)=>{const r=await fetch(p,{credentials:'same-origin'});return [r.status,await r.json()]}"
    R["samples"]=[]
    for i in range(12):
        st, d = page.evaluate(G2, "/api/assistants")
        g = d.get("real_ai_delivery_gate", {})
        R["samples"].append({"keys_sql_path": "registered_tasks" in d, "disabled": d.get("disabled"), "durable_sql_release_store": g.get("checks", {}).get("durable_sql_release_store", {}).get("passed")})
        page.wait_for_timeout(700)
    b.close()
txt = json.dumps(R, indent=1)
for v in emp.values():
    txt = txt.replace(v, "[redacted]")
open(f"{OUT}/live_probe3.json", "w").write(txt)
print(txt[:6000])
