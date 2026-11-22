"""Live demo proof for issue 2257: the first /api/map request is aborted at the network level; compare the deployed app.js with the patched one served through route interception. Credentials are read at runtime and never printed."""
import json, os, sys
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "live_probe.py")).read().split("results = []")[0])
PATCHED = open(os.path.join(OUT, "../../../../src/api/src/zava_forward/api/web/app.js")).read()
out = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, patched in (("deployed", False), ("patched", True)):
        ctx = b.new_context(viewport={"width": 1366, "height": 1000}); page = ctx.new_page(); login(page)
        seen = []; state = {"n": 0}

        def maps(route):
            state["n"] += 1
            if state["n"] == 1:
                seen.append("aborted"); route.abort("connectionreset")
            else:
                route.continue_()
        page.route("**/api/map?*", maps)
        page.on("response", lambda r: seen.append(r.status) if "/api/map" in r.url else None)
        if patched:
            page.route("**/app.js*", lambda r: r.fulfill(status=200, content_type="text/javascript", body=PATCHED))
        page.goto(EMP + "/app#/overview", wait_until="load")
        try:
            page.wait_for_function("()=>document.querySelectorAll('.leaflet-interactive,.leaflet-marker-icon').length>0 || /Map unavailable/.test(document.body.innerText)", timeout=60000)
        except Exception:
            pass
        page.wait_for_timeout(1500)
        out[name] = {"map_requests": seen, "markers": page.evaluate("()=>document.querySelectorAll('.leaflet-interactive,.leaflet-marker-icon').length"),
                     "unavailable": page.evaluate("()=>/Map unavailable/.test(document.body.innerText)")}
        page.screenshot(path=os.path.join(OUT, f"map-after-reset-{name}.png"))
        ctx.close()
    b.close()
json.dump(out, open(os.path.join(OUT, "recovery-proof-result.json"), "w"), indent=1); print(json.dumps(out))
