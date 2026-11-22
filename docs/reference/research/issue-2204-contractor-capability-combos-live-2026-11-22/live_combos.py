"""Live combination proof (issue 2204): Contractor with a roster binding, and each capability role
stacked on ProgrammeManager. Assigns through Graph (az rest), signs in with Playwright, probes,
removes, and always restores the original ProgrammeManager assignment. Credentials are read at run
time and never printed."""
import json, os, re, subprocess, sys, time
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
SP = "5e7542e4-4497-4568-85f5-f43438a95798"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")[0].strip()
emp = {"user": rd(".ama-test-user-id"), "pw": rd(".ama-test-user")}
UID = "982d30b9-6db1-4f3d-ac26-50b237c7fa7f"
G = "https://graph.microsoft.com/v1.0"
MASK = """()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}"""
ROLES = {
    "ProgrammeManager": "b854f84f-0135-5474-b2e4-b0ae2029a987",
    "Contractor": "58b54965-87e5-584f-814b-9c8f60ed5888",
    "RuleAuthor": "168c7718-7863-5a8a-915f-05fd235b31a0",
    "RuleOwner": "83f054b6-1ace-5bb9-801d-4ef82aa9d41b",
    "RegulatoryChat": "6f87a406-60d6-5449-a20f-1099e8f4c41f",
    "AIRestart": "c08639e0-7735-5e01-b985-1e159ddffccf",
}
PM = ROLES["ProgrammeManager"]
CASES = {
    "Contractor-bound": ["Contractor"],
    "PM-baseline": ["ProgrammeManager"],
    "PM+RuleAuthor": ["ProgrammeManager", "RuleAuthor"],
    "PM+RuleOwner": ["ProgrammeManager", "RuleOwner"],
    "PM+RegulatoryChat": ["ProgrammeManager", "RegulatoryChat"],
    "PM+AIRestart": ["ProgrammeManager", "AIRestart"],
}
only = sys.argv[1:] or list(CASES)


def rest(method, url, body=None):
    cmd = ["az", "rest", "--method", method, "--url", url, "-o", "json"]
    if body is not None:
        cmd += ["--headers", "Content-Type=application/json", "--body", json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"{method} {url.split('?')[0]} failed: {r.stderr.strip()[:200]}")
    return json.loads(r.stdout) if r.stdout.strip() else {}


def mine():
    items = rest("GET", f"{G}/users/{UID}/appRoleAssignments")["value"]
    return [a for a in items if a["resourceId"] == SP]


def assign(role_id):
    return rest("POST", f"{G}/users/{UID}/appRoleAssignments",
                {"principalId": UID, "resourceId": SP, "appRoleId": role_id})["id"]


def login(page):
    page.fill("input[name=loginfmt]", emp["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", emp["pw"]); page.click("#idSIButton9")
    for _ in range(3):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)


def probe(name):
    res = {"case": name}
    with sync_playwright() as p:
        b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
        page.goto(APP + "/api/me", wait_until="domcontentloaded")
        login(page)
        me = c.request.get(APP + "/api/me"); res["me_status"] = me.status
        try:
            d = me.json()
        except Exception:
            d = {}
        u = d.get("user", {}) if isinstance(d, dict) else {}
        if u:
            res["me"] = {"role": u.get("role"), "app_roles": u.get("app_roles"), "rule_roles": u.get("rule_roles"),
                         "contractor": u.get("contractor"), "view_only": u.get("view_only"),
                         "app_admin": u.get("app_admin"),
                         "navigation": [n["label"] for n in d.get("navigation", [])]}
        probes = {}
        for path in ["/api/cases", "/api/workorders", "/api/stats", "/api/finance", "/api/admin/simulator-control",
                     "/api/chat/regulatory/status", "/api/law/cards"]:
            r = c.request.get(APP + path); probes["GET " + path] = [r.status, "" if r.status == 200 else r.text()[:110]]
            if path == "/api/cases" and r.status == 200:
                try:
                    j = r.json(); lst = j if isinstance(j, list) else j.get("cases", [])
                    res["cases_count"] = len(lst)
                    res["case_companies"] = sorted({(x.get("contractor") or {}).get("name") if isinstance(x.get("contractor"), dict) else x.get("contractor") for x in lst})[:5]
                except Exception:
                    pass
        for path, body in [("/api/law/cards", {"zz_probe": 1}), ("/api/law/cards/ZZ-PROBE/1/approve", {"zz_probe": 1}),
                           ("/api/continuity/restart-decide", {})]:
            r = c.request.post(APP + path, data=json.dumps(body), headers={"Content-Type": "application/json"})
            probes["POST " + path] = [r.status, r.text()[:110]]
        res["probes"] = probes
        res["views"] = {}
        for tag, route in {"workbench": "/app#/", "chat": "/app#/chat"}.items():
            page.goto(APP + route, wait_until="networkidle"); page.reload(wait_until="networkidle"); page.wait_for_timeout(2500)
            page.evaluate(MASK)
            page.evaluate("()=>{const a=document.getElementById('account');if(a)a.style.visibility='hidden'}")
            body = page.inner_text("body")
            res["views"][tag] = {"h": [h.inner_text()[:80] for h in page.query_selector_all("h1,h2")][:3],
                                 "not_available": "not available for your role" in body.lower(),
                                 "synthetic_lookup": "synthetic source lookup available" in body.lower()}
            page.screenshot(path=f"{OUT}/live-{name}-{tag}.png")
        b.close()
    return res


results = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "cases": []}
prior = f"{OUT}/live-combos.json"
if os.path.exists(prior) and sys.argv[1:]:
    results["cases"] = [r for r in json.load(open(prior))["cases"] if r["case"] not in only]
orig = mine()
results["original"] = [{"is_pm": a["appRoleId"] == PM} for a in orig]
fail = None
try:
    for name in only:
        want = CASES[name]
        for a in mine():
            rest("DELETE", f"{G}/users/{UID}/appRoleAssignments/{a['id']}")
        for r in want:
            assign(ROLES[r])
        held = sorted(a["appRoleId"] for a in mine())
        rec = None
        time.sleep(20)
        expect = sorted(f"ZavaForward.{r}" for r in want)
        for attempt in range(1, 5):
            try:
                rec = probe(name); rec["attempt"] = attempt
                got = sorted(rec.get("me", {}).get("app_roles") or [])
                if got == expect or (rec.get("me_status") != 200 and attempt >= 3):
                    break
                rec["stale_claim_retry"] = True
                time.sleep(45)
            except Exception as e:
                rec = {"case": name, "attempt": attempt, "error": type(e).__name__, "detail": str(e).splitlines()[0][:160]}
                time.sleep(10)
        rec["assigned_exactly"] = held == sorted(ROLES[r] for r in want)
        rec["expected_app_roles"] = expect
        results["cases"].append(rec)
        json.dump(results, open(f"{OUT}/live-combos.json", "w"), indent=1)
        print(name, rec.get("me_status"), rec.get("me", {}).get("role"), rec.get("me", {}).get("rule_roles"), flush=True)
except Exception as e:
    fail = f"{type(e).__name__}: {str(e)[:200]}"
finally:
    for a in mine():
        rest("DELETE", f"{G}/users/{UID}/appRoleAssignments/{a['id']}")
    assign(PM)
    final = mine()
    results["restored"] = {"count": len(final), "only_pm": [a["appRoleId"] for a in final] == [PM]}
    results["failure"] = fail
    json.dump(results, open(f"{OUT}/live-combos.json", "w"), indent=1)
    print("restored", results["restored"], "failure", fail)
