"""Live demo probe for issue 2257: fresh employee sessions and the first /api/map request. Credentials are read at runtime and never printed."""
import json, os, re, sys, time
from playwright.sync_api import sync_playwright

EMP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
rd = lambda n: open(os.path.join(os.path.expanduser("~"), n)).read().split("\n")[0].strip()
user, pw = rd(".ama-test-user-id"), rd(".ama-test-user")
RUNS = int(sys.argv[1]) if len(sys.argv) > 1 else 8
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")


def login(page):
    page.goto(EMP + "/api/me", wait_until="domcontentloaded", timeout=120000)
    page.fill("input[name=loginfmt]", user); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", pw); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(EMP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(EMP)), timeout=60000)


results = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for i in range(RUNS):
        ctx = b.new_context(viewport={"width": 1366, "height": 1000}); page = ctx.new_page()
        ev = []; t0 = time.time()
        page.on("requestfailed", lambda r: ev.append({"t": round(time.time() - t0, 2), "url": EMAIL.sub("[email]", r.url.split("?")[0].replace(EMP, "")), "failure": r.failure}))
        page.on("response", lambda r: ev.append({"t": round(time.time() - t0, 2), "url": r.url.split("?")[0].replace(EMP, ""), "status": r.status}) if "/api/map" in r.url else None)
        rec = {"run": i + 1, "start_utc": time.strftime("%H:%M:%S", time.gmtime())}
        try:
            login(page); t1 = time.time()
            page.goto(EMP + "/app#/overview", wait_until="load")
            try:
                page.wait_for_function("()=>document.querySelectorAll('.leaflet-marker-icon, .leaflet-interactive').length>0 || /Map unavailable/.test(document.body.innerText)", timeout=90000)
            except Exception:
                pass
            rec["map_wait_s"] = round(time.time() - t1, 1)
            rec["markers"] = page.evaluate("()=>document.querySelectorAll('.leaflet-marker-icon, .leaflet-interactive').length")
            rec["unavailable"] = page.evaluate("()=>/Map unavailable/.test(document.body.innerText)")
        except Exception as e:
            rec["error"] = type(e).__name__
        rec["events"] = ev
        results.append(rec); print(json.dumps(rec)[:400], flush=True)
        ctx.close()
    b.close()
json.dump(results, open(os.path.join(OUT, f"probe-result-{time.strftime('%H%M%S')}.json"), "w"), indent=1)
