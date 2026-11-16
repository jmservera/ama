import os, sys, json
from pathlib import Path
from checks.design_system_browser_check import main
from checks import map_fullscreen_browser_check as m
from playwright.sync_api import sync_playwright, expect

AXE = Path("/tmp/1828/axe.js").read_text()
RATE = float(os.environ.get("RATE", "1"))
HOOK = """
Error.stackTraceLimit = 60; const ost = window.setTimeout; window.setTimeout = function(f, d, ...a){ if (d === 200) window.__maplog.push({t: performance.now(), url: 'SETTIMEOUT200', stack: new Error().stack}); return ost.call(this, f, d, ...a); }; const orig = window.fetch;
window.__maplog = [];
window.fetch = function(url, ...a){ if (String(url).includes('/api/map?')) window.__maplog.push({t: performance.now(), url: String(url), stack: new Error().stack}); return orig.call(this, url, ...a); };
window.addEventListener('keydown', e => window.__maplog.push({t: performance.now(), key: e.key + ' c' + +e.ctrlKey + ' m' + +e.metaKey + ' a' + +e.altKey + ' s' + +e.shiftKey + ' ' + e.target.id + e.target.className}), true);
window.addEventListener('resize', () => window.__maplog.push({t: performance.now(), resize: innerWidth + 'x' + innerHeight}));
"""
def run(base):
    out = Path("/tmp/1828/probe-out"); out.mkdir(exist_ok=True, parents=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); ctx = b.new_context(viewport={"width":1280,"height":900})
        page = ctx.new_page()
        if RATE != 1:
            s = ctx.new_cdp_session(page); s.send("Emulation.setCPUThrottlingRate", {"rate": RATE})
        page.goto(base + "/app")
        page.locator("#email").fill("sam@example.test"); page.locator("#pw").fill("synthetic-check")
        page.get_by_role("button", name="Sign in", exact=True).click()
        page.get_by_role("heading", name="My cases today").wait_for()
        page.get_by_role("link", name="Overview", exact=True).click()
        page.locator(".map-cluster").first.wait_for()
        page.locator("#mapArea").select_option(label="Point examples")
        expect(page.locator(".map-marker")).to_have_count(3)
        page.evaluate(HOOK)
        m.check_expanded_filters(page, base, AXE, out, [])
        print("LOG after filters:", json.dumps(page.evaluate("window.__maplog.map(e=>({t:Math.round(e.t),url:e.url,resize:e.resize}))")))
        page.evaluate("window.__maplog.length=0")
        try:
            m.check_browser_shortcuts(page, "embedded")
            print("shortcuts PASS")
        except AssertionError as e:
            print("shortcuts FAIL", e)
        evs = page.evaluate("window.__maplog")
        print("SUMMARY", [(round(e["t"]), (e.get("key") or e.get("resize") or "FETCH")[:12]) for e in evs if not e.get("key") or e["key"].startswith("=")][:12], "nkeys", sum(1 for e in evs if e.get("key")), "first/last key t", [round(e["t"]) for e in evs if e.get("key")][::len([1 for e in evs if e.get("key")])-1] if any(e.get("key") for e in evs) else None)
        for e in [x for x in evs if not x.get("key")]:
            print("EVENT", e.get("t"), e.get("url") or e.get("resize") or e.get("key")); print((e.get("stack") or "")[:6000])
        b.close()
main(run)
