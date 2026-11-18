"""Live demo probe for issue 117. Reads credentials at runtime; retains only redacted facts.
Uploads only content that must be refused (synthetic marker, type mismatch); no clean file is stored."""
import base64, json, os, re
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.<app-fqdn-suffix>"  # resolve with az containerapp show
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")
emp = {"user": rd(".ama-test-user-id")[0].strip(), "pw": rd(".ama-test-user")[0].strip()}
H = {"X-ZF-CSRF": "1", "Content-Type": "application/json"}


def login(page):
    page.fill("input[name=loginfmt]", emp["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", emp["pw"]); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP): break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)


def redact(o):
    return json.loads(re.sub(r"[\w.+-]+@[\w.-]+", "[email]", json.dumps(o)))


def body(r):
    try: return r.json()
    except Exception: return {"raw": re.sub(r"[\w.+-]+@[\w.-]+", "[email]", r.text())[:200]}


out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded"); login(page)
    me = body(c.request.get(APP + "/api/me"))
    out["me"] = {"role": (me.get("user") or {}).get("role")}
    r = c.request.get(APP + "/api/retention"); j = body(r)
    out["retention"] = {"status": r.status, "keys": sorted(j) if isinstance(j, dict) else None,
                        "label": str(j.get("label") or j.get("note") or "")[:200] if isinstance(j, dict) else None}
    r = c.request.get(APP + "/api/cases"); cases = body(r)
    lst = cases if isinstance(cases, list) else cases.get("items", [])
    out["cases"] = {"status": r.status, "count": len(lst)}
    cid = next((x.get("id") for x in lst if isinstance(x, dict) and x.get("id")), None)

    def docs():
        r = c.request.get(f"{APP}/api/cases/{cid}"); j = body(r)
        return [d.get("id") for d in j.get("documents", [])] if isinstance(j, dict) else None

    before = docs() if cid else None
    marker = b"header " + b"ZF-SYNTHETIC-MALWARE-TEST-MARKER" + b" trailer"
    for label, name, data in (("synthetic_marker_txt", "scan-probe.txt", marker),
                              ("type_mismatch_pdf", "scan-probe.pdf", b"not a pdf at all")):
        res = page.evaluate("""async([path,body])=>{const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json','X-ZF-CSRF':'1'},body:JSON.stringify(body)});return {status:r.status,body:(await r.text()).slice(0,300)}}""",
                            [f"/api/cases/{cid}/upload", {"name": name, "kind": "Other", "source": "issue-117 scan probe", "source_version": "1", "reason": "Prove refusal of unsafe upload on synthetic demo", "data": base64.b64encode(data).decode()}])
        out[label] = {"status": res["status"], "body": re.sub(r"[\w.+-]+@[\w.-]+", "[email]", res["body"])}
    after = docs() if cid else None
    out["documents_unchanged"] = before == after
    out["document_counts"] = [None if before is None else len(before), None if after is None else len(after)]
    b.close()
json.dump(out, open(f"{OUT}/probe.json", "w"), indent=1)
print(json.dumps(out)[:1500])
