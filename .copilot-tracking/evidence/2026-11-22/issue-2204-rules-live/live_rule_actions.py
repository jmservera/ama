"""Live RuleAuthor and RuleOwner proof (issue 2204). Account A is the demo test account; B is a
throwaway Entra user created and deleted here. Roles are assigned one at a time through Graph (az rest),
sign-in uses Playwright, API calls run from the signed-in page with the CSRF header. Credentials are
read or generated at run time and never printed or written."""
import json, os, re, secrets, subprocess, sys, time
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
SP = "5e7542e4-4497-4568-85f5-f43438a95798"
OUT = os.path.dirname(os.path.abspath(__file__))
G = "https://graph.microsoft.com/v1.0"
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")[0].strip()
A = {"user": rd(".ama-test-user-id"), "pw": rd(".ama-test-user"), "oid": "982d30b9-6db1-4f3d-ac26-50b237c7fa7f"}
PM, AUTHOR, OWNER = "b854f84f-0135-5474-b2e4-b0ae2029a987", "168c7718-7863-5a8a-915f-05fd235b31a0", "83f054b6-1ace-5bb9-801d-4ef82aa9d41b"
CARD = "exercise-rules-live-2204"
MASK = """()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){n.nodeValue=n.nodeValue.replace(/[\\w.+-]+@[\\w.-]+/g,'[email]')}}"""
log = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "steps": []}


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


def login(page, who):
    page.fill("input[name=loginfmt]", who["user"]); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", who["pw"]); page.click("#idSIButton9")
    for _ in range(4):
        try:
            page.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if page.url.startswith(APP):
                break
            (page.query_selector("#idSIButton9") or page.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    try:
        page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000)
    except Exception:
        print("login stuck at", page.url.split("?")[0][:100], page.inner_text("body")[:160].replace("\n", " ").replace(who["user"], "[user]"), flush=True)
        raise


def api(page, method, path, body=None):
    js = """async ([m,p,b])=>{const r=await fetch(p,{method:m,headers:{'Content-Type':'application/json','X-ZF-CSRF':'1'},body:b?JSON.stringify(b):undefined});
    let t=await r.text();let j=null;try{j=JSON.parse(t)}catch(e){};return {status:r.status,json:j,text:j?null:t.slice(0,120)}}"""
    return page.evaluate(js, [method, path, body])


def session(who, label, expect_roles, actions):
    """Sign in once the token carries exactly the expected capability claims, then run actions."""
    time.sleep(20)
    rec = {"label": label}
    for attempt in range(1, 5):
        with sync_playwright() as p:
            b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); page = c.new_page()
            page.goto(APP + "/api/me", wait_until="domcontentloaded")
            login(page, who)
            me = api(page, "GET", "/api/me")
            u = (me["json"] or {}).get("user", {})
            rec.update(attempt=attempt, me_status=me["status"], app_roles=u.get("app_roles"), rule_roles=u.get("rule_roles"), role=u.get("role"))
            if sorted(u.get("app_roles") or []) == sorted(expect_roles) or attempt == 4:
                rec["identity"] = u.get("email")
                rec["results"] = actions(page, u)
                for tag, path in rec.get("shots", {}).items():
                    pass
                b.close()
                break
            b.close()
        time.sleep(45)
    ident = rec.pop("identity", None)
    log["steps"].append(rec)
    json.dump(log, open(f"{OUT}/live-rule-actions.json", "w"), indent=1)
    return ident


def shot(page, name, path):
    page.goto(APP + path, wait_until="networkidle"); page.evaluate(MASK)
    page.evaluate("()=>{const a=document.getElementById('account');if(a)a.style.visibility='hidden'}")
    page.screenshot(path=f"{OUT}/{name}.png")


CARD_BODY = dict(card_id=CARD, title="Exercise rules live 2204 (synthetic)", trigger="Synthetic trigger for a live demo exercise",
                 applicability="Synthetic demo stock only", provisions=["uk-gdpr-current-text, Article 22 (illustrative citation)"],
                 clock="No clock; exercise only", safe_default="Route to a named human reviewer", escalation_role="Compliance lead",
                 effective="2025-10-27")
STATE = {}


def a_baseline(page, u):
    STATE["a_email"] = u.get("email")
    r = {"GET cards": api(page, "GET", "/api/law/cards")["status"],
         "POST propose without RuleAuthor": api(page, "POST", "/api/law/cards", dict(CARD_BODY, approver=u["email"]))["status"]}
    return r


def a_author(page, u):
    r = {"GET cards": api(page, "GET", "/api/law/cards")["status"]}
    prop = api(page, "POST", "/api/law/cards", dict(CARD_BODY, approver=STATE["a_email"]))
    r["RuleAuthor propose (POST /api/law/cards)"] = prop["status"]
    if prop["json"]:
        STATE["v"] = prop["json"].get("version"); r["version"] = STATE["v"]
        r["draft state"] = prop["json"]["versions"][-1].get("state")
        r["recorded role"] = prop["json"]["versions"][-1]["events"][-1]["role"]
    r["approve with RuleAuthor only (wrong role)"] = api(page, "POST", f"/api/law/cards/{CARD}/{STATE.get('v', 1)}/approve", {})["status"]
    shot(page, "live-A-author-cards", f"/api/law/cards/{CARD}")
    return r


def a_owner(page, u):
    v, base, r = STATE["v"], f"/api/law/cards/{CARD}/{STATE['v']}", {}
    r["propose with RuleOwner only (wrong role)"] = api(page, "POST", "/api/law/cards", dict(CARD_BODY, approver=u["email"]))["status"]
    for label, path, body in [("approve own authored card", f"{base}/approve", {}),
                              ("approve seed card (unassigned owner)", "/api/law/cards/hazard-awareness-clock/1/approve", {}),
                              ("activate a draft", f"{base}/activate", {}),
                              ("hold a draft", f"{base}/hold", {"note": "Synthetic hold"}),
                              ("retire a draft", f"{base}/retire", {})]:
        x = api(page, "POST", path, body)
        r["RuleOwner " + label] = {"status": x["status"], "error": (x["json"] or {}).get("error")}
    hist = api(page, "GET", f"/api/law/cards/{CARD}")
    last = (hist["json"] or {}).get("versions", [{}])[-1]
    r["state after owner attempts"] = last.get("state")
    r["events"] = [(e["state"], e["role"]) for e in last.get("events", [])]
    shot(page, "live-A-owner-history", f"/api/law/cards/{CARD}")
    return r


orig = [a["appRoleId"] for a in mine(A["oid"])]
fail = None
try:
    clear(A["oid"]); assign(A["oid"], PM)
    session(A, "A PM only", ["ZavaForward.ProgrammeManager"], a_baseline)
    clear(A["oid"]); assign(A["oid"], PM); assign(A["oid"], AUTHOR)
    session(A, "A PM+RuleAuthor", ["ZavaForward.ProgrammeManager", "ZavaForward.RuleAuthor"], a_author)
    clear(A["oid"]); assign(A["oid"], PM); assign(A["oid"], OWNER)
    session(A, "A PM+RuleOwner", ["ZavaForward.ProgrammeManager", "ZavaForward.RuleOwner"], a_owner)
except Exception as e:
    fail = f"{type(e).__name__}: {str(e)[:200]}"
finally:
    clear(A["oid"]); assign(A["oid"], PM)
    final = mine(A["oid"])
    log["restored"] = {"count": len(final), "only_pm": [a["appRoleId"] for a in final] == [PM], "original_was_pm_only": orig == [PM]}
    log["failure"] = fail
    json.dump(log, open(f"{OUT}/live-rule-actions.json", "w"), indent=1)
    print("done", log["restored"], "failure", fail)
