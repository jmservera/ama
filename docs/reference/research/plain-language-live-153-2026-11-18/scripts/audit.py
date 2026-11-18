"""Live copy audit for #153. Reads sign-in values at runtime; never prints them."""
import json, os, re, sys
from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
R = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
home = os.path.expanduser("~")
OUT = os.path.join(os.path.dirname(__file__), "..")
TERMS = re.compile(r"\b(gate|gates|hold|provenance|trace|traces|payload|stub|null|undefined|NaN|exception|traceback)\b", re.I)
SNAKE = re.compile(r"\b[a-z]+(?:_[a-z0-9]+)+\b")

def login(page, user, pw, start):
    page.goto(start)
    for _ in range(4):
        try:
            if page.locator("input[name=loginfmt]").is_visible(timeout=3000):
                page.fill("input[name=loginfmt]", user); page.click("input[type=submit]"); page.wait_for_timeout(1500)
            if page.locator("input[name=passwd]").is_visible(timeout=3000):
                page.fill("input[name=passwd]", pw); page.click("input[type=submit]"); page.wait_for_timeout(2000)
            if page.locator("#idBtn_Back").is_visible(timeout=2000):
                page.click("#idBtn_Back"); page.wait_for_timeout(2000)
        except Exception:
            pass
    page.wait_for_load_state("networkidle")

def scan(page, label, findings, shot):
    page.wait_for_timeout(1200)
    text = page.inner_text("body")
    page.screenshot(path=f"{OUT}/screens/{shot}.png")
    hits = sorted({m.group(0).lower() for m in TERMS.finditer(text)})
    snakes = sorted(set(SNAKE.findall(text)))
    ai = [l.strip() for l in text.splitlines() if re.search(r"\bAI\b", l)][:6]
    findings.append({"surface": label, "url": re.sub(r"\?.*", "", page.url), "title": page.title(),
                     "terms": hits, "snake_case": snakes, "ai_lines": ai, "chars": len(text),
                     "headings": [h.strip() for h in page.locator("h1,h2").all_inner_texts()][:12]})
    return text

if __name__ == "__main__":
    who = sys.argv[1]
    findings = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        c = b.new_context(viewport={"width": 1440, "height": 900})
        pg = c.new_page()
        if who == "staff":
            u = open(home + "/.ama-test-user-id").read().strip(); p = open(home + "/.ama-test-user").read().strip()
            login(pg, u, p, H + "/sign-in")
            base = H
        else:
            l = open(home + "/.ama-resident-test-user").read().splitlines()
            login(pg, l[0].strip(), l[1].strip(), R + "/")
            base = R
        scan(pg, "landing after sign-in", findings, f"{who}-00-landing")
        links = pg.eval_on_selector_all("a[href]", "els=>els.map(e=>[e.textContent.trim().slice(0,40),e.getAttribute('href')])")
        routes = []
        for t, h in links:
            if h.startswith("/") and not h.startswith("//") and h not in routes and not re.search(r"sign-?out|logout|\.(png|css|js)", h):
                routes.append(h)
        for i, h in enumerate(routes[:25], 1):
            try:
                pg.goto(base + h); scan(pg, h, findings, f"{who}-{i:02d}")
            except Exception as e:
                findings.append({"surface": h, "error": type(e).__name__})
        # unknown route as a plain error probe
        pg.goto(base + "/no-such-page-153"); scan(pg, "unknown route", findings, f"{who}-99-unknown")
        b.close()
    json.dump({"who": who, "routes": routes, "findings": findings}, open(f"{OUT}/{who}-audit.json", "w"), indent=1)
    print(who, "routes", len(routes), "surfaces", len(findings))
