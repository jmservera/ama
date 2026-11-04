import json, os, re, sys, time
from playwright.sync_api import sync_playwright

BASE = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = sys.argv[1]
lines = open(os.path.expanduser("~/.ama-resident-test-user")).read().splitlines()
U, P = lines[0].strip(), lines[1].strip()


def red(s):
    s = str(s).replace(U, "[REDACTED-USER]").replace(P, "[REDACTED-PW]")
    local = U.split("@")[0]
    return s.replace(local, "[REDACTED-LOCAL]") if local else s


def note(k, v):
    print(k, "|", red(v)[:700])


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900}, timezone_id="Europe/London")
    ctx.set_default_timeout(90000)
    page = ctx.new_page()
    reqs = []
    page.on("response", lambda r: reqs.append((r.request.method, re.sub(r"\?.*", "", r.url.replace(BASE, "")), r.status)))
    page.goto(BASE + "/", wait_until="load", timeout=180000)
    page.wait_for_selector("#signin:not([hidden])")
    page.fill("#email", U)
    page.fill("#password", P)
    page.click("#signin-button")
    page.wait_for_selector("#content:not([hidden])")
    page.wait_for_timeout(1500)
    masks = lambda: [page.locator("#email"), page.locator("#account-email")]

    # callback slot search (read-only)
    reqs.clear()
    page.click("text=Find callback times")
    page.wait_for_timeout(6000)
    note("after find slots reqs", reqs)
    note("status", page.locator("#status").inner_text())
    sec = page.locator("section:has(h2:text('Synthetic callbacks'))")
    note("callbacks section text", sec.inner_text()[-900:])
    page.screenshot(path=f"{OUT}/05-find-callbacks.png", full_page=True, mask=masks())
    # check my callbacks without consent checkbox
    reqs.clear()
    page.click("text=Check my callbacks")
    page.wait_for_timeout(4000)
    note("check callbacks without box reqs", reqs)
    note("callbacks section text 2", sec.inner_text()[-500:])
    # chat widget open, no message sent
    page.locator("button[aria-label*='hat' i]").first.click()
    page.wait_for_timeout(2500)
    note("dialog text", page.locator("[role=dialog]").first.inner_text() if page.locator("[role=dialog]").count() else "no dialog; body tail: " + page.inner_text("body")[-600:])
    page.screenshot(path=f"{OUT}/06-chat-open.png", mask=masks())
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    # keyboard tab order from top
    page.goto(BASE + "/")
    page.wait_for_selector("#content:not([hidden])")
    order = []
    for _ in range(14):
        page.keyboard.press("Tab")
        order.append(page.evaluate("(document.activeElement.innerText||document.activeElement.id||document.activeElement.tagName).slice(0,30)"))
    note("tab order", order)
    # mobile 320
    page.set_viewport_size({"width": 320, "height": 640})
    page.wait_for_timeout(800)
    ov = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    note("320px horizontal overflow px", ov)
    page.screenshot(path=f"{OUT}/07-mobile-320.png", full_page=True, mask=masks())
    page.set_viewport_size({"width": 1280, "height": 900})
    # sign out
    reqs.clear()
    page.locator("#account > summary").click()
    page.click("#signout")
    page.wait_for_selector("#signin:not([hidden])")
    note("signout reqs", reqs)
    note("signout status", page.locator("#status").inner_text())
    page.screenshot(path=f"{OUT}/08-signed-out.png", mask=masks())
    page.go_back()
    page.wait_for_timeout(2500)
    note("after back: signin visible", page.locator("#signin").is_visible())
    note("after back: content visible", page.locator("#content").is_visible())
    r = ctx.request.get(BASE + "/demo/view")
    note("view after signout", r.status)
    b.close()
