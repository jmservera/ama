"""Live all-role proof (issue 2204). Assigns each ZavaForward.* role to the test account one at a
time through Graph (az rest), signs in with Playwright, probes, removes it, and finally restores
the original ProgrammeManager assignment. Credentials are read at run time and never printed."""
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
    "Coordinator": "2191b707-fcd8-5a23-b72c-4025d788334b",
    "LiaisonOfficer": "a492bc48-2bd0-53f4-a4cd-96fd66be082d",
    "SafetyLiaison": "e12f2723-1ed6-5717-a5dd-6c0fc295f1b1",
    "QualityInspector": "58b0dc55-8659-5e42-9c8b-d87a0a672a9b",
    "GrantsOfficer": "25062a8c-d472-5052-97d2-7a3618e19ec6",
    "SupportOfficer": "30ae68cc-e9cb-5326-859d-2d99f30694a3",
    "Contractor": "58b54965-87e5-584f-814b-9c8f60ed5888",
    "ApplicationAdmin": "706473cd-4503-5e71-bf57-aed4e5d535b2",
    "RuleAuthor": "168c7718-7863-5a8a-915f-05fd235b31a0",
    "RuleOwner": "83f054b6-1ace-5bb9-801d-4ef82aa9d41b",
    "RegulatoryChat": "6f87a406-60d6-5449-a20f-1099e8f4c41f",
    "AIRestart": "c08639e0-7735-5e01-b985-1e159ddffccf",
}
PM = ROLES["ProgrammeManager"]
only = sys.argv[1:] or list(ROLES)


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


def unassign(aid):
    rest("DELETE", f"{G}/users/{UID}/appRoleAssignments/{aid}")


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
    res = {"role": name}
    with sync_playwright() as p:
        b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
        page.goto(APP + "/api/me", wait_until="domcontentloaded")
        res["entra_redirect"] = "login.microsoftonline.com" in page.url
        login(page)
        me = c.request.get(APP + "/api/me"); res["me_status"] = me.status
        try:
            d = me.json()
        except Exception:
            d = {}
        u = d.get("user", {}) if isinstance(d, dict) else {}
        if u:
            res["me"] = {"role": u.get("role"), "app_roles": u.get("app_roles"), "app_admin": u.get("app_admin"),
                         "view_only": u.get("view_only"), "identity_source": u.get("identity_source"),
                         "navigation": [{"label": n["label"], "access": n.get("access")} for n in d.get("navigation", [])]}
        else:
            res["me_error"] = {k: (v if isinstance(v, (str, int)) else None) for k, v in (d if isinstance(d, dict) else {}).items()
                               if k in ("error", "code", "message")}
        probes = {}
        for path in ["/api/cases", "/api/stats", "/api/finance", "/api/packages", "/api/funding", "/api/work-orders",
                     "/api/audit-check", "/api/retention", "/api/admin/simulator-control"]:
            probes[path] = c.request.get(APP + path).status
        res["probes"] = probes
        res["views"] = {}
        for tag, route in {"workbench": "/app#/", "denied-simulator": "/app#/simulator"}.items():
            page.goto(APP + route, wait_until="networkidle"); page.reload(wait_until="networkidle"); page.wait_for_timeout(2000)
            page.evaluate(MASK)
            page.evaluate("()=>{const a=document.getElementById('account');if(a)a.style.visibility='hidden'}")
            body = page.inner_text("body").lower()
            res["views"][tag] = {"h": [h.inner_text()[:80] for h in page.query_selector_all("h1,h2")][:3],
                                 "nothing_changed": "nothing was changed" in body}
            page.screenshot(path=f"{OUT}/live-{name}-{tag}.png")
        b.close()
    return res


results = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "roles": []}
prior = f"{OUT}/live-all-roles.json"
if os.path.exists(prior) and sys.argv[1:]:
    results["roles"] = [r for r in json.load(open(prior))["roles"] if r["role"] not in only]
orig = mine()
results["original"] = [{"role_id": a["appRoleId"], "is_pm": a["appRoleId"] == PM} for a in orig]
fail = None
try:
    for a in orig:
        unassign(a["id"])
    assert not mine(), "assignments remain"
    for name in only:
        aid = assign(ROLES[name]); rec = None
        try:
            held = [x["appRoleId"] for x in mine()]
            time.sleep(20)
            for attempt in range(1, 6):
                try:
                    rec = probe(name); rec["attempt"] = attempt
                    if rec.get("me", {}).get("app_roles") == [f"ZavaForward.{name}"] or rec.get("me_status") != 200 and attempt >= 3:
                        break
                    rec["stale_claim_retry"] = True
                    time.sleep(45)
                except Exception as e:
                    rec = {"role": name, "attempt": attempt, "error": type(e).__name__, "detail": str(e).splitlines()[0][:160]}
                    time.sleep(10)
            rec["only_role_held"] = held == [ROLES[name]]
        finally:
            unassign(aid)
            rec = rec or {"role": name, "error": "no result"}
            rec["removed"] = not mine()
        results["roles"].append(rec)
        json.dump(results, open(f"{OUT}/live-all-roles.json", "w"), indent=1)
        print(name, rec.get("me_status"), rec.get("me", {}).get("role"), flush=True)
except Exception as e:
    fail = f"{type(e).__name__}: {str(e)[:200]}"
finally:
    for a in mine():
        unassign(a["id"])
    assign(PM)
    final = mine()
    results["restored"] = {"count": len(final), "only_pm": [a["appRoleId"] for a in final] == [PM]}
    results["failure"] = fail
    json.dump(results, open(f"{OUT}/live-all-roles.json", "w"), indent=1)
    print("restored", results["restored"], "failure", fail)
