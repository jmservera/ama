"""Live demo probe 2 for #221 (after probe 1 left scope all suspended). Reads sign-in values at runtime; never prints them. Synthetic demo only.

Read-only checks and refused AI, restart-propose and restart-decide requests while the demo is suspended.
"""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "plain-language-live-153-2026-11-18", "scripts"))
from audit import login, H
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(__file__), "..")
home = os.path.expanduser("~")
log = []

def post(pg, path, data):
    return pg.evaluate("""async ([p, b]) => { const r = await fetch(p, {method: "POST", headers: {"Content-Type": "application/json", "X-ZF-CSRF": "1"}, body: JSON.stringify(b)}); return {status: r.status, text: await r.text()}; }""", [path, data])

def redact(s):
    s = re.sub(r"\bE-[A-Za-z0-9]+", "E-REDACTED", s)
    s = re.sub(r"[\w.+-]+@[\w.-]+", "REDACTED@redacted.invalid", s)
    s = re.sub(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", "NAME-REDACTED", s)  # synthetic staff names (title-case pairs)
    return re.sub(r"\b[0-9a-f]{8}-[0-9a-f-]{27}\b", "OID-REDACTED", s)

def rec(step, status, text):
    try:
        body = json.loads(text)
    except Exception:
        body = text[:300]
    log.append({"step": step, "status": status, "body": json.loads(redact(json.dumps(body)))})
    print(step, status, redact(json.dumps(body))[:200])

BASE = dict(scope="all", reason="Demo probe: negative test", incident_owner="Demo owner", containment="None; probe is refused",
            comms_owner="Demo owner", comms_audience="Demo staff", trigger="guardrail breach", evidence="SYN-221-PROBE",
            resident_impact="None", remediation="None")

with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1440, "height": 900}); pg = c.new_page()
    u = open(home + "/.ama-test-user-id").read().strip(); p = open(home + "/.ama-test-user").read().strip()
    login(pg, u, p, H + "/sign-in")
    pg.screenshot(path=OUT + "/screens/02-signed-in-while-suspended.png")
    r = c.request.get(H + "/api/continuity"); reg = r.json(); rec("continuity-register", r.status, r.text())
    sid = reg["suspensions"][0]["id"] if reg.get("suspensions") else "SUS-1"
    r = c.request.get(H + "/api/cases"); t = r.text(); rec("manual-cases-readable", r.status, json.dumps({"bytes": len(t)}))
    cases = r.json(); items = cases.get("cases") or cases.get("items") or cases if isinstance(cases, (dict, list)) else []
    cid = items[0].get("id") if isinstance(items, list) and items else None
    if cid:
        d = post(pg, f"/api/cases/{cid}/ai", {"task": "summary"}); rec("ai-run-while-suspended", d["status"], d["text"])
    d = post(pg, "/api/continuity/restart-propose", {"id": sid, "evidence_class": "constructed-fixture", "result": "Pass", "corrective_evidence": "SYN-221 probe corrective test record", "test_id": "SYN-221-T1"}); rec("restart-propose-incomplete", d["status"], d["text"])
    d = post(pg, "/api/continuity/restart-decide", {"id": sid, "decision": "Restart", "epoch": 1, "proposal_digest": "0" * 64, "authority_ref": "Building Safety Lead"}); rec("restart-decide-no-proposal", d["status"], d["text"])
    d = post(pg, "/api/continuity/restart-propose", {"id": sid, "auto_restart": True}); rec("restart-automatic-flag", d["status"], d["text"])
    r = c.request.get(H + "/api/continuity"); rec("continuity-register-after", r.status, r.text())
    json.dump(log, open(OUT + "/live-probe-2-while-suspended.json", "w"), indent=1)
    b.close()
