"""Live employee case view and chat widget keyboard, axe, reflow and reduced-motion proof (issue 619).
Credentials read at runtime, never printed. Output is redacted."""
import json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")[0].strip()
USER, PW = rd(".ama-test-user-id"), rd(".ama-test-user")
AXE = open(os.path.join(home, ".local/share/ama/phase-witness/axe.min.js")).read()
TAGS = "['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']"
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")


def login(page):
    page.goto(APP + "/api/me", wait_until="domcontentloaded")
    page.fill("input[name=loginfmt]", USER); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", PW); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)


def active(page):
    return page.evaluate("""()=>{const a=document.activeElement;return {tag:a.tagName,id:a.id,role:a.getAttribute('role'),name:(a.getAttribute('aria-label')||a.textContent||'').trim().slice(0,50)}}""")


def focus_visible(page):
    return page.evaluate("""()=>{const a=document.activeElement;const s=getComputedStyle(a);const o=s.outlineStyle!=='none'&&parseFloat(s.outlineWidth)>0;const sh=s.boxShadow!=='none';return o||sh}""")


def axe(page, sel=None):
    ctx = f"document.querySelector('{sel}')" if sel else "document"
    return page.evaluate(AXE + f""";(async()=>{{const r=await axe.run({ctx},{{runOnly:{{type:'tag',values:{TAGS}}}}});return {{version:axe.version,violations:r.violations.map(v=>({{id:v.id,impact:v.impact,nodes:v.nodes.length}})),passes:r.passes.length}}}})()""")


def no_hscroll(page):
    return page.evaluate("document.documentElement.scrollWidth<=document.documentElement.clientWidth")


