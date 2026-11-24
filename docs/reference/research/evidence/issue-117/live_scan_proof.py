import base64, json, os, sys, time
from playwright.sync_api import sync_playwright

H = os.path.expanduser("~")
email = open(H + "/.ama-test-user-id").read().strip()
pw = open(H + "/.ama-test-user").read().strip()
BASE = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = sys.argv[1]
EICAR = (b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$" + b"EICAR-STANDARD-ANTIVIRUS-TEST-FILE" + b"!$H+H*")
CLEAN = b"%PDF-1.4\n% synthetic demo clean test file for issue 117\n%%EOF\n"


def post(page, path, body):
    return page.evaluate(
        """async ([p, b]) => { const r = await fetch(p, {method:'POST', headers:{'content-type':'application/json','X-ZF-CSRF':'1'}, body: JSON.stringify(b)}); let t = await r.text(); return [r.status, t.slice(0, 400)]; }""",
        [path, body],
    )


def get(page, path):
    return page.evaluate(
        """async (p) => { const r = await fetch(p); return [r.status, await r.text()]; }""", path
    )


with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1280, "height": 900})
    page.goto(BASE + "/app")
    page.get_by_role("textbox", name="Email").or_(page.locator("input[type=email]")).first.fill(email)
    page.get_by_role("button", name="Next").click()
    page.wait_for_selector("input[type=password]")
    page.locator("input[type=password]").fill(pw)
    page.get_by_role("button", name="Sign in").click()
    try:
        page.get_by_role("button", name="Yes").click(timeout=4000)
    except Exception:
        pass
    page.wait_for_url(BASE + "/**", timeout=30000)
    page.wait_for_timeout(3000)
    print("url", page.url.split("?")[0])
    st, txt = get(page, "/api/cases")
    print("cases status", st)
    cases = json.loads(txt) if st == 200 else []
    if isinstance(cases, dict):
        print("keys", list(cases)[:10], str(get(page, "/api/me")[1])[:0])
        cases = cases.get("cases") or cases.get("items") or cases.get("rows") or []
    print("n cases", len(cases))
    cid = cases[0]["id"] if cases else None
    print("case", cid)
    log = {}
    if cid:
        for label, data, name in (("eicar", EICAR, "synthetic117-eicar.txt"), ("clean", CLEAN, "synthetic117-clean.pdf")):
            r = post(page, f"/api/cases/{cid}/upload", {"name": name, "kind": "Other", "data": base64.b64encode(data).decode(), "source": "issue 117 demo scan proof", "source_version": "1", "reason": "demo scan proof"})
            print(label, "upload", r[0], r[1][:200])
            log[label] = r
        st, txt = get(page, f"/api/cases/{cid}")
        docs = [d for d in json.loads(txt).get("documents", []) if "synthetic117" in d.get("name", "")] if st == 200 else []
        for d in docs:
            print("doc", d["name"], d.get("scan", {}).get("status"), d.get("scan", {}).get("scanner"))
        for d in docs:
            r = post(page, f"/api/cases/{cid}/read-doc", {"id": d["id"]})
            print("read-before-clean", d["name"], r[0], r[1][:160])
        for i in range(12):
            time.sleep(20)
            for d in docs:
                r = post(page, f"/api/cases/{cid}/rescan-doc", {"id": d["id"]})
                print("rescan", i, d["name"], r[0], r[1][:200])
            if all(x[0] != 200 or '"pending"' not in x[1] for x in [r]):
                pass
            st, txt = get(page, f"/api/cases/{cid}")
            cur = [d for d in json.loads(txt).get("documents", []) if "synthetic117" in d.get("name", "")]
            if cur and all(d.get("scan", {}).get("status") != "pending" for d in cur):
                break
        page.screenshot(path=OUT + "/live-workbench.png")
        st, txt = get(page, f"/api/cases/{cid}")
        for d in json.loads(txt).get("documents", []):
            if "synthetic117" in d.get("name", ""):
                print("final doc", d["name"], d.get("scan", {}).get("status"))
                r = post(page, f"/api/cases/{cid}/read-doc", {"id": d["id"]})
                print("read-final", r[0], r[1][:120])
    b.close()
