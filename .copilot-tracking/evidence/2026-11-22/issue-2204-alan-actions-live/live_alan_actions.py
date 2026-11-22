"""Live rule-action proof with a second identity (issue 2204). Account A (the demo test account) holds the
Programme Manager and RuleAuthor app roles for the run; account B (Alan Steiner) holds RuleOwner plus
Programme Manager (the API refuses a principal with only a capability role). Roles change through Graph
(az rest); sign-in uses Playwright; API calls run from the signed-in page with the CSRF header.
Credentials are read at run time and never printed or written; emails are not recorded."""
import json, os, re, subprocess, time
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
SP = "5e7542e4-4497-4568-85f5-f43438a95798"
OUT = os.path.dirname(os.path.abspath(__file__))
G = "https://graph.microsoft.com/v1.0"
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")[0].strip()
A = {"user": rd(".ama-test-user-id"), "pw": rd(".ama-test-user"), "oid": "982d30b9-6db1-4f3d-ac26-50b237c7fa7f"}
B = {"user": rd(".ama-test-user-id-2"), "pw": rd(".ama-test-user-2"), "oid": "a68ea8e3-1638-431a-be2f-fc57c4209c67"}
PM, AUTHOR, OWNER = "b854f84f-0135-5474-b2e4-b0ae2029a987", "168c7718-7863-5a8a-915f-05fd235b31a0", "83f054b6-1ace-5bb9-801d-4ef82aa9d41b"
CARD = "exercise-rules-alan-2204"
MASK = """()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}"""
log = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "steps": []}
STATE = {}


def rest(method, url, body=None):
    cmd = ["az", "rest", "--method", method, "--url", url, "-o", "json"]
    if body is not None:
        cmd += ["--headers", "Content-Type=application/json", "--body", json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"{method} {url.split('?')[0]} failed: {r.stderr.strip()[:200]}")
    return json.loads(r.stdout) if r.stdout.strip() else {}


def mine(oid):
    return [a for a in rest("GET", f"{G}/users/{oid}/appRoleAssignments")["value"] if a["resourceId"] == SP]


def assign(oid, role):
    return rest("POST", f"{G}/users/{oid}/appRoleAssignments", {"principalId": oid, "resourceId": SP, "appRoleId": role})["id"]


def clear(oid):
    for a in mine(oid):
        rest("DELETE", f"{G}/users/{oid}/appRoleAssignments/{a['id']}")


def setroles(oid, roles):
    clear(oid)
    for r in roles:
        assign(oid, r)


def login(page, who):
    page.fill("input[name=loginfmt]", who["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", who["pw"]); page.click("#idSIButton9")
    for _ in range(4):
        try:
            page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=8000)
            break
        except Exception:
            if page.url.startswith(APP):
                break
            body = page.inner_text("body")
            btn = page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")
            if btn and "Stay signed in" in body:
                btn.click()
            else:
                print("login stuck:", page.url.split("?")[0][-60:], body[:200].replace("\n", " ").replace(who["user"], "[user]"), flush=True)
                raise RuntimeError("sign-in blocked")
    page.wait_for_timeout(3000)


def api(page, method, path, body=None):
    js = """async ([m,p,b])=>{const r=await fetch(p,{method:m,headers:{'Content-Type':'application/json','X-ZF-CSRF':'1'},body:b?JSON.stringify(b):undefined});
    let t=await r.text();let j=null;try{j=JSON.parse(t)}catch(e){};return {status:r.status,json:j,text:j?null:t.slice(0,120)}}"""
    return page.evaluate(js, [method, path, body])


def session(who, label, expect_roles, actions):
    """Sign in once the token carries exactly the expected app roles, then run the actions."""
    time.sleep(20)
    rec = {"label": label}
    for attempt in range(1, 5):
        with sync_playwright() as p:
            b = p.chromium.launch(); page = b.new_context(viewport={"width": 1366, "height": 900}).new_page()
            page.goto(APP + "/api/me", wait_until="domcontentloaded")
            login(page, who)
            page.goto(APP + "/api/me", wait_until="networkidle")
            me = api(page, "GET", "/api/me")
            u = (me["json"] or {}).get("user", {})
            rec.update(attempt=attempt, me_status=me["status"], app_roles=u.get("app_roles"), rule_roles=u.get("rule_roles"), role=u.get("role"))
            if sorted(u.get("app_roles") or []) == sorted(expect_roles) or attempt == 4:
                STATE[who["oid"]] = u.get("email")
                rec["results"] = actions(page, u)
                b.close()
                break
            b.close()
        time.sleep(45)
    log["steps"].append(rec)
    json.dump(log, open(f"{OUT}/live-alan-actions.json", "w"), indent=1)


def shot(page, name, path):
    page.goto(APP + path, wait_until="networkidle"); page.evaluate(MASK)
    page.screenshot(path=f"{OUT}/{name}.png")


CARD_BODY = dict(card_id=CARD, title="Exercise rules Alan live 2204 (synthetic)", trigger="Synthetic trigger for a live demo exercise",
                 applicability="Synthetic demo stock only", provisions=["uk-gdpr-current-text, Article 22 (illustrative citation)"],
                 clock="No clock; exercise only", safe_default="Route to a named human reviewer", escalation_role="Compliance lead",
                 effective="2025-10-27")
BASE = lambda: f"/api/law/cards/{CARD}/{STATE['v']}"


def brief(x):
    return {"status": x["status"], "error": (x["json"] or {}).get("error")}


def history(page):
    h = api(page, "GET", f"/api/law/cards/{CARD}")
    vs = (h["json"] or {}).get("versions", [])
    last = vs[-1] if vs else {}
    return {"state": last.get("state"), "events": [(e["state"], e["role"]) for e in last.get("events", [])]}


def b_pre(page, u):
    return {"GET cards": api(page, "GET", "/api/law/cards")["status"],
            "RuleOwner propose (wrong role)": brief(api(page, "POST", "/api/law/cards", dict(CARD_BODY, approver=u["email"])))}


def a_author(page, u):
    r = {"GET cards": api(page, "GET", "/api/law/cards")["status"]}
    prop = api(page, "POST", "/api/law/cards", dict(CARD_BODY, approver=STATE[B["oid"]]))
    r["RuleAuthor propose naming the second identity as owner"] = prop["status"]
    if prop["json"]:
        STATE["v"] = prop["json"].get("version"); r["version"] = STATE["v"]
        r["draft state"] = prop["json"]["versions"][-1].get("state")
    r["author approves own card (wrong role)"] = brief(api(page, "POST", f"{BASE()}/approve", {}))
    r["author activates (wrong role)"] = brief(api(page, "POST", f"{BASE()}/activate", {}))
    return r


def b_actions(page, u):
    r = {"identity matches named owner": STATE[B["oid"]] == u.get("email")}
    seq = [("approve", "approve", {}, "approved"),
           ("approve again (already approved)", "approve", {}, None),
           ("activate", "activate", {}, "active"),
           ("hold", "hold", {"note": "Synthetic hold for the live proof"}, "held"),
           ("release", "release", {}, "active"),
           ("hold again", "hold", {"note": "Synthetic hold before retirement"}, "held"),
           ("retire", "retire", {}, "retired"),
           ("release after retire (invalid)", "release", {}, None)]
    for label, verb, body, want in seq:
        x = api(page, "POST", f"{BASE()}/{verb}", body)
        h = history(page)
        r[label] = dict(brief(x), state_after=h["state"])
        if label == "activate":
            shot(page, "live-alan-active", f"/api/law/cards/{CARD}")
    r["final events (state, role)"] = history(page)["events"]
    shot(page, "live-alan-history", f"/api/law/cards/{CARD}")
    return r


orig = {A["oid"]: [a["appRoleId"] for a in mine(A["oid"])], B["oid"]: [a["appRoleId"] for a in mine(B["oid"])]}
log["original_roles_known"] = {"A_is_PM_only": orig[A["oid"]] == [PM], "B_is_RuleOwner_only": orig[B["oid"]] == [OWNER]}
fail = None
try:
    setroles(B["oid"], [PM, OWNER])
    session(B, "B RuleOwner+PM pre-check", ["ZavaForward.ProgrammeManager", "ZavaForward.RuleOwner"], b_pre)
    setroles(A["oid"], [PM, AUTHOR])
    session(A, "A PM+RuleAuthor", ["ZavaForward.ProgrammeManager", "ZavaForward.RuleAuthor"], a_author)
    session(B, "B RuleOwner+PM actions", ["ZavaForward.ProgrammeManager", "ZavaForward.RuleOwner"], b_actions)
except Exception as e:
    fail = f"{type(e).__name__}: {str(e)[:200]}"
finally:
    for oid, roles in ((A["oid"], [PM]), (B["oid"], [OWNER])):
        setroles(oid, roles)
    log["restored"] = {k: [a["appRoleId"] for a in mine(oid)] == roles for k, (oid, roles) in
                       {"A_PM_only": (A["oid"], [PM]), "B_RuleOwner_only": (B["oid"], [OWNER])}.items()}
    log["failure"] = fail
    json.dump(log, open(f"{OUT}/live-alan-actions.json", "w"), indent=1)
    print("done", log["restored"], "failure", fail)
