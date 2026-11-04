import json, os, re, sys, time
from playwright.sync_api import sync_playwright

BASE = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
lines = open(os.path.expanduser("~/.ama-resident-test-user")).read().splitlines()
U, P = lines[0].strip(), lines[1].strip()


def red(s):
    if s is None:
        return s
    s = s.replace(U, "[REDACTED-USER]").replace(P, "[REDACTED-PW]")
    local = U.split("@")[0]
    return s.replace(local, "[REDACTED-LOCAL]") if local else s


log = []


def note(k, v):
    log.append({"step": k, "detail": red(str(v))})
    print(k, "|", red(str(v))[:400])


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900}, timezone_id="Europe/London")
    ctx.set_default_timeout(90000)
    page = ctx.new_page()
    reqs = []
    page.on("response", lambda r: reqs.append((r.request.method, re.sub(r"\?.*", "", r.url.replace(BASE, "")), r.status)))
    cons = []
    page.on("console", lambda m: cons.append((m.type, red(m.text))) if m.type in ("error", "warning") else None)

    def shot(name, full=True):
        masks = [page.locator("#email"), page.locator("#account-email")]
        page.screenshot(path=f"{OUT}/{name}.png", full_page=full, mask=masks)

    t0 = time.time()
    page.goto(BASE + "/", wait_until="load", timeout=180000)
    page.wait_for_selector("#signin:not([hidden]), #content:not([hidden])", timeout=120000)
    note("signin page ready seconds", round(time.time() - t0, 1))
    note("title", page.title())
    shot("01-signin")
    # empty submit validation
    page.click("#signin-button")
    note("empty submit error", page.locator("#signin-error").inner_text())
    shot("02-signin-empty-error")
    # wrong password generic error (wrong value is not the real one)
    page.fill("#email", U)
    page.fill("#password", "wrong-password-for-test")
    page.click("#signin-button")
    page.wait_for_timeout(3000)
    note("wrong password error", page.locator("#signin-error").inner_text())
    # correct
    page.fill("#password", P)
    t1 = time.time()
    page.click("#signin-button")
    page.wait_for_selector("#content:not([hidden])", timeout=120000)
    note("signin to content seconds", round(time.time() - t1, 1))
    page.wait_for_timeout(2000)
    note("status text", page.locator("#status").inner_text())
    note("h1/h2 headings", [red(h.inner_text()) for h in page.locator("h1,h2,h3").all()])
    note("buttons", [(red(x.inner_text()), x.is_disabled()) for x in page.locator("button").all()])
    note("links", [(red(x.inner_text()), x.get_attribute("href")) for x in page.locator("a").all()])
    note("content text", page.locator("#content").inner_text())
    shot("03-signed-in")
    page.locator("#account > summary").click()
    note("account panel text", page.locator("#account").inner_text())
    shot("04-account-open", full=False)
    note("cookies (name,secure,httpOnly,sameSite)", [(c["name"], c["secure"], c["httpOnly"], c["sameSite"]) for c in ctx.cookies()])
    note("requests", reqs)
    note("console", cons)
    json.dump({"log": log}, open(f"{OUT}/walk-log.json", "w"), indent=1)
    ctx.storage_state(path="/tmp/wt/state.json")
    b.close()
