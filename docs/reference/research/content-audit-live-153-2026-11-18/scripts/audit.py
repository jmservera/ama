"""Visible-text copy audit of the deployed demo screens (read-only, desktop 1440x900).

Reads session state from ~/.cache/ama153 (state-staff.json, state-resident.json) (never committed).
Masks sign-in identifiers in the DOM before each screenshot and in the retained text.
"""
import json, os, re, sys
from playwright.sync_api import sync_playwright

STAFF = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
RES = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANNED = re.compile(
    r"\b(gates?|holds?|on hold|provenance|traces?|snapshots?|envelopes?|human-approved|ai-drafted|"
    r"pending|unassigned|advance|consent pending|hazard unresolved)\b", re.I)
home = os.path.expanduser("~")
secrets = []
for f in (".ama-test-user-id", ".ama-resident-test-user"):
    try:
        secrets += [l.strip() for l in open(os.path.join(home, f)).read().splitlines()[:1] if l.strip()]
    except OSError:
        pass
secrets = [s for s in secrets if "@" in s]
local_parts = [s.split("@")[0] for s in secrets if len(s.split("@")[0]) > 3]
MASK_JS = """([emails, parts]) => {
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); const n = [];
  while (w.nextNode()) n.push(w.currentNode);
  for (const t of n) { let v = t.nodeValue;
    for (const e of emails.concat(parts)) v = v.split(e).join('[redacted]');
    v = v.replace(/[\\w.+-]+@[\\w-]+\\.[\\w.-]+/g, '[redacted-email]');
    v = v.replace(/(Flat|House|Maisonette)\\s+\\d+[^\\n]{0,80}?(Newcastle upon Tyne,?\\s*)?[A-Z]{1,2}\\d[A-Z\\d]?\\s*\\d[A-Z]{2}/g, '[redacted-address]');
    v = v.replace(/\\b0\\d{3}\\s?\\d{3}\\s?\\d{4}\\b/g, '[redacted-phone]'); t.nodeValue = v; }
  for (const i of document.querySelectorAll('input')) { if (i.type !== 'password' && /@/.test(i.value)) i.value = '[redacted]'; }
}"""


def clean(txt):
    for s in secrets + local_parts:
        txt = txt.replace(s, "[redacted]")
    txt = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[redacted-email]", txt)
    txt = re.sub(r"(Flat|House|Maisonette)\s+\d+[^\n]{0,80}?(Newcastle upon Tyne,?\s*)?[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}", "[redacted-address]", txt)
    return re.sub(r"\b0\d{3}\s?\d{3}\s?\d{4}\b", "[redacted-phone]", txt)


def visit(pg, name, url, results, wait=4000, click=None):
    pg.goto(url)
    pg.wait_for_timeout(wait)
    if click:
        try:
            pg.locator(click).first.click(timeout=3000)
            pg.wait_for_timeout(2500)
        except Exception:
            pass
    pg.evaluate(MASK_JS, [secrets, local_parts])
    txt = clean(pg.inner_text("body"))
    pg.screenshot(path=os.path.join(OUT, "screens", f"{name}.png"), full_page=False)
    hits = sorted({m.group(0).lower() for m in BANNED.finditer(txt)})
    lines = [l.strip() for l in txt.splitlines() if BANNED.search(l)]
    results[name] = {"url": re.sub(r"\?.*", "", pg.url), "title": pg.title(), "chars": len(txt),
                     "banned_hits": hits, "hit_lines": lines[:12], "text": txt}
    print(name, len(txt), hits)


def main():
    results = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        c = b.new_context(storage_state=os.path.expanduser("~/.cache/ama153/state-staff.json"), viewport={"width": 1440, "height": 900})
        pg = c.new_page()
        pg.goto(STAFF + "/app")
        pg.wait_for_timeout(4000)
        links = pg.eval_on_selector_all("a[href^='#/'], a[href^='/']", "e=>e.map(x=>x.getAttribute('href'))")
        print("links", sorted(set(links))[:60])
        routes = [("staff-cases", "/app#/"), ("staff-overview", "/app#/overview"), ("staff-progress", "/app#/progress"),
                  ("staff-visits", "/app#/visits"), ("staff-funding", "/app#/funding"),
                  ("staff-finance", "/app#/finance"), ("staff-time", "/app#/time"),
                  ("staff-assistants", "/app#/assistants"), ("staff-capacity", "/app#/capacity"),
                  ("staff-aftercare", "/app#/aftercare"), ("staff-closed", "/app#/closed"),
                  ("staff-law", "/law.html"), ("staff-all", "/app#/all"),
                  ("staff-handoff-waiting", "/app#/handoff-waiting"), ("staff-import", "/app#/import"),
                  ("staff-screens", "/app#/screens")]
        for n, u in routes:
            visit(pg, n, STAFF + u, results)
        extra = sorted({l for l in links if l.startswith("#/case/")})[:3]
        tabs = ["Blockers and safety", "Survey and assessment", "Funding", "Resident", "Contractor and works", "Quality and handover", "AI assistance", "History"]
        for i, l in enumerate(extra):
            visit(pg, f"staff-case-{i+1}", STAFF + "/app" + l, results, wait=6000)
            for t in tabs:
                try:
                    pg.get_by_role("tab", name=re.compile(r"^" + t)).first.click(timeout=3000)
                    pg.wait_for_timeout(1500)
                    pg.evaluate(MASK_JS, [secrets, local_parts])
                    txt = clean(pg.inner_text("body"))
                    nm = f"staff-case-{i+1}-{re.sub('[^a-z]+','-',t.lower())}"
                    pg.screenshot(path=os.path.join(OUT, "screens", nm + ".png"))
                    hits = sorted({m.group(0).lower() for m in BANNED.finditer(txt)})
                    results[nm] = {"url": re.sub(r"\?.*", "", pg.url), "title": pg.title(), "chars": len(txt),
                        "banned_hits": hits, "hit_lines": [x.strip() for x in txt.splitlines() if BANNED.search(x)][:12], "text": txt}
                    print(nm, len(txt), hits)
                except Exception as e:
                    print("tab fail", t, type(e).__name__)
        r = b.new_context(storage_state=os.path.expanduser("~/.cache/ama153/state-resident.json"), viewport={"width": 1440, "height": 900})
        rp = r.new_page()
        rp.goto(RES + "/"); rp.wait_for_timeout(5000)
        try:
            l = open(os.path.join(home, ".ama-resident-test-user")).read().splitlines()
            rp.fill("input[type=email], input[name=email], #email", l[0].strip())
            rp.fill("input[type=password]", l[1].strip())
            rp.click("button:has-text('Sign in')")
            rp.wait_for_timeout(5000)
        except Exception as e:
            print("resident form fail", type(e).__name__)
        rp.wait_for_timeout(8000)
        visit(rp, "resident-home", RES + "/", results, wait=9000)
        rl = rp.eval_on_selector_all("a[href]", "e=>e.map(x=>x.getAttribute('href'))")
        print("resident links", sorted(set(rl))[:40])
        for t in ["Status", "Needed from you", "Timeline", "Documents", "Funding", "Help", "Sensors", "Showcase limits"]:
            try:
                rp.get_by_role("tab", name=re.compile("^" + t)).first.click(timeout=3000)
            except Exception:
                try:
                    rp.get_by_text(t, exact=True).first.click(timeout=3000)
                except Exception:
                    print("resident tab fail", t)
                    continue
            rp.wait_for_timeout(1500)
            rp.evaluate(MASK_JS, [secrets, local_parts])
            txt = clean(rp.inner_text("body"))
            nm = "resident-" + re.sub("[^a-z]+", "-", t.lower())
            rp.screenshot(path=os.path.join(OUT, "screens", nm + ".png"))
            results[nm] = {"url": re.sub(r"\?.*", "", rp.url), "title": rp.title(), "chars": len(txt),
                "banned_hits": sorted({m.group(0).lower() for m in BANNED.finditer(txt)}),
                "hit_lines": [x.strip() for x in txt.splitlines() if BANNED.search(x)][:12], "text": txt}
            print(nm, len(txt), results[nm]["banned_hits"])
        results["_links"] = {"staff": sorted(set(links)), "resident": sorted(set(rl))}
        b.close()
    json.dump(results, open(os.path.expanduser("~/.cache/ama153/audit-results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
