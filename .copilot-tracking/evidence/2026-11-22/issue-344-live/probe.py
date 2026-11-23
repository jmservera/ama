"""Issue 344 ninth-pass live probe. Reads credentials at runtime; prints only redacted facts."""
import hashlib, json, os, re, time, urllib.request, urllib.error
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(OUT, "../../../../src/api/src/zava_forward/api/web"))
home = os.path.expanduser("~")
rd = lambda n: [x.strip() for x in open(os.path.join(home, n)).read().split("\n") if x.strip()]
emp = {"user": rd(".ama-test-user-id")[0], "pw": rd(".ama-test-user")[0]}
R = {"t0": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def anon(path, accept=None, extra=None):
    h = dict(extra or {})
    if accept:
        h["Accept"] = accept
    op = urllib.request.build_opener(NoRedirect)
    try:
        return op.open(urllib.request.Request(APP + path, headers=h), timeout=30).status
    except urllib.error.HTTPError as e:
        return f"{e.code} -> {e.headers.get('Location','')[:60]}" if e.code in (301, 302, 303, 307) else e.code


R["anon"] = {
    p: anon(p) for p in ["/healthz", "/readyz", "/", "/welcome.html", "/sign-in", "/api/me", "/api/cases",
                         "/api/time/status", "/app", "/index.html", "/law.html"]}
R["anon_json"] = {p: anon(p, "application/json") for p in ["/api/me", "/api/cases", "/app"]}
R["anon_xhr"] = {p: anon(p, "application/json", {"X-Requested-With": "XMLHttpRequest"}) for p in ["/api/me", "/api/cases"]}

with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    page = c.new_page()
    errs, bad = [], []
    page.on("console", lambda m: errs.append(m.text[:140]) if m.type == "error" else None)
    page.on("response", lambda r: bad.append(f"{r.status} {re.sub(r'^https?://[^/]+', '', r.url)[:70]}") if r.status >= 400 else None)
    r = page.goto(APP + "/", wait_until="networkidle", timeout=90000)
    R["landing"] = {"status": r.status, "title": page.title(), "signin_href": page.get_attribute("a[href='/sign-in']", "href")}
    page.screenshot(path=f"{OUT}/1-landing.png")
    R["browser_fetch_anon"] = page.evaluate("""async()=>{const o={};for(const [k,h] of [['default',{}],['json',{Accept:'application/json'}],['xhr',{'X-Requested-With':'XMLHttpRequest'}]]){
      for(const m of ['manual','follow']){try{const r=await fetch('/api/me',{headers:h,redirect:m});o[k+'_'+m]=r.type==='opaqueredirect'?'redirect':r.status}catch(e){o[k+'_'+m]='error:'+e.name}}}return o}""")
    page.click("a[href='/sign-in']")
    page.wait_for_url(re.compile(r"login\.microsoftonline\.com"), timeout=60000)
    R["signin_reaches_entra"] = True
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
    page.wait_for_load_state("networkidle")
    R["after_signin"] = {"path": re.sub(r"^https?://[^/]+", "", page.url)[:40], "title": page.title()}
    page.wait_for_timeout(3000)

    redact = """()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}"""
    page.evaluate(redact)
    page.screenshot(path=f"{OUT}/2-workbench.png")
    navs = page.eval_on_selector_all("#nav a, #nav button", "els=>els.map(e=>({t:(e.textContent||'').trim().slice(0,40),h:e.getAttribute('href')}))")
    R["nav_items"] = navs
    walk = []
    for i, n in enumerate(navs):
        before = len(bad)
        try:
            page.locator("#nav").locator("a, button").nth(i).click(timeout=8000)
            page.wait_for_load_state("networkidle", timeout=15000)
            page.wait_for_timeout(1200)
            page.evaluate(redact)
            heading = page.evaluate("()=>{const h=document.querySelector('#app h1, #app h2, main h1, main h2');return h?h.textContent.trim().slice(0,60):null}")
            txt = page.evaluate("()=>document.querySelector('#app')?.innerText.length||0")
            page.screenshot(path=f"{OUT}/walk-{i+1:02d}.png")
            walk.append({"item": n["t"], "heading": heading, "app_text_len": txt, "new_http_errors": bad[before:]})
        except Exception as e:
            walk.append({"item": n["t"], "error": type(e).__name__})
    R["walk"] = walk
    R["console_errors"] = sorted(set(errs))[:15]
    R["http_errors_seen"] = sorted(set(bad))[:30]
    R["signed_in_asset_hash"] = {}
    for f in sorted(os.listdir(WEB)):
        fp = os.path.join(WEB, f)
        if os.path.isfile(fp):
            resp = c.request.get(APP + "/" + f)
            same = hashlib.sha256(resp.body()).digest() == hashlib.sha256(open(fp, "rb").read()).digest()
            R["signed_in_asset_hash"][f] = [resp.status, "match" if same else "differs"]
    b.close()
txt = json.dumps(R, indent=1)
for v in emp.values():
    assert v not in txt
open(f"{OUT}/probe_result.json", "w").write(txt)
print(txt)
