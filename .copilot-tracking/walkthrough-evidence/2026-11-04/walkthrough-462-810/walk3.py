import os, re, sys
from playwright.sync_api import sync_playwright
BASE = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = sys.argv[1]
L = open(os.path.expanduser("~/.ama-resident-test-user")).read().splitlines()
U, P = L[0].strip(), L[1].strip()
def red(s):
    s = str(s).replace(U, "[REDACTED-USER]").replace(P, "[REDACTED-PW]")
    return s.replace(U.split("@")[0], "[REDACTED-LOCAL]")
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width":1280,"height":900}); ctx.set_default_timeout(90000)
    page = ctx.new_page(); reqs=[]
    page.on("response", lambda r: reqs.append((r.request.method, re.sub(r"\?.*","",r.url.replace(BASE,"")), r.status)))
    page.goto(BASE+"/", timeout=180000); page.wait_for_selector("#signin:not([hidden])")
    page.fill("#email",U); page.fill("#password",P); page.click("#signin-button"); page.wait_for_selector("#content:not([hidden])")
    page.wait_for_timeout(1500)
    sec = page.locator("section:has(h2:text('Synthetic callbacks'))")
    page.fill("input[type=date]", "2026-11-20")
    reqs.clear(); page.click("text=Find callback times"); page.wait_for_timeout(8000)
    print("find no consent", reqs); print(red(sec.inner_text()[-500:]))
    page.check("#callback-consent")
    reqs.clear(); page.click("text=Find callback times"); page.wait_for_timeout(8000)
    print("find consent", reqs); print(red(sec.inner_text()[-900:]))
    page.screenshot(path=f"{OUT}/09-find-with-date.png", full_page=True, mask=[page.locator("#account-email")])
    reqs.clear(); page.click("text=Check my callbacks"); page.wait_for_timeout(8000)
    print("check", reqs); print(red(sec.inner_text()[-500:]))
    page.locator("#account > summary").click(); page.click("#signout"); page.wait_for_selector("#signin:not([hidden])")
    page.go_back(); page.wait_for_timeout(3000)
    print("back url", page.url, "| body:", red(page.inner_text("body"))[:500].replace("\n"," / "))
    page.screenshot(path=f"{OUT}/10-after-back.png")
    page.reload(); page.wait_for_timeout(3000)
    print("reload signin visible", page.locator("#signin").is_visible())
    b.close()
