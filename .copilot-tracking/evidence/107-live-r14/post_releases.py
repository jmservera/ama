"""POST one actual release per assistant on the demo API. Credentials read at runtime, never printed."""
import copy, json, sys, time
sys.path[:0] = ["../../../src/core/tests"]
from datetime import datetime, timedelta, timezone
from playwright.sync_api import sync_playwright
from login_lib import *
import release_support as rs
from zava_forward.core import rai_release

OWNER = "Juan Manuel Servera, project owner"
APPROVAL = "OWNER-DECISION-2026-11-25"
BOUND = ("registry_version","schema_version","provider","endpoint","deployment","prompt_version","policy_version","data_version","provenance_version","permission_version","model_version","task_contract_version","evaluation_version")
G = "async(p)=>{const r=await fetch(p,{credentials:'same-origin'});return [r.status,await r.json()]}"
P = "async([p,b])=>{const r=await fetch(p,{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json','X-ZF-CSRF':'1'},body:JSON.stringify(b)});let j=null;try{j=await r.json()}catch(e){};return [r.status,j]}"
out = {}
with sync_playwright() as p:
    b, page = login(p)
    st, d = page.evaluate(G, "/api/assistants")
    exp = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
    for a in d["assistants"]:
        task = a["id"]
        bind = a["binding"]
        rec = rs.fixture(task, bind, bind["model_version"], "actual", expires=time.time() + 1)
        body = {k: rec[k] for k in ("task","scope","monitoring_declaration","intended_use","prohibited_uses","affected_stakeholders","material_change_triggers","evaluation_decision","residual_risk_decision")}
        body.update({k: bind[k] for k in BOUND})
        for ind in body["monitoring_declaration"]["indicators"].values():
            if isinstance(ind.get("threshold"), dict):
                ind["threshold"]["approved_by"] = OWNER
        ev = ["owner-decision:2026-11-18 synthetic demo, all AI approved for demo", "owner-decision:2026-11-25 demo API release approvers set"]
        body.update(evidence_class="actual", evidence=ev, residual_risk_note="Synthetic demo only; owner accepted residual risk for the demo, desktop only.",
                    serving_model=bind["model_version"], release_version="demo-r14-2026-11-25", accountable_owner=OWNER,
                    impact_assessment="Synthetic constructed demo data; bounded proposals only; no real resident reliance.",
                    evaluation_summary=dict(evaluation_version=rai_release.EVALUATION_VERSION, decision="Pass", summary="Demo evaluation recorded by the owner for the synthetic demo.", evidence_digest=rai_release.digest(ev)),
                    consumption=dict(max_calls=100, max_tokens=2000000, alert_threshold_percent=80, alert_contact=OWNER),
                    approved_by=OWNER, named_approval_id=APPROVAL, expires=exp)
        s, j = page.evaluate(P, ["/api/assistants/releases", body])
        out[task] = dict(status=s, response=j)
    st2, d2 = page.evaluate(G, "/api/assistants")
    out["listing_after"] = {x["id"]: (x["release"] if not (isinstance(x["release"], dict) and x["release"].get("id")) else dict(id=x["release"]["id"], keys=sorted(x["release"]))) for x in d2["assistants"]}
    json.dump(d2, open("listing_after_raw.json", "w"))
    b.close()
t = redact(json.dumps(out, indent=1))
open("post_releases.json", "w").write(t); print(t[:6000])
