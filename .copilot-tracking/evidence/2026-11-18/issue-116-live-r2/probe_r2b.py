"""Round 2b: me shape, and where literal reason values from case detail appear (counts only)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ["R2_IMPORT_ONLY"] = "1"
from playwright.sync_api import sync_playwright
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe_r2.py")).read().split("out = {}")[0]
exec(src)
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded"); login(page)
    me = c.request.get(APP + "/api/me").json()
    out["me_top_keys"] = sorted(me.keys())
    def pick(o):
        return {k: v for k, v in o.items() if k in ("role", "app_roles", "view_only", "identity_source", "provider") and not isinstance(v, dict)}
    out["me_flat"] = pick(me); 
    for k, v in me.items():
        if isinstance(v, dict): out["me_flat"][k] = pick(v)
    items = c.request.get(APP + "/api/cases").json()["items"]
    vals = set()
    for it in items:
        d = c.request.get(APP + "/api/cases/" + it["id"]).json()
        for f in ("adjustment", "priority_support"):
            v = d.get("resident", {}).get(f)
            if isinstance(v, str) and len(v) > 3: vals.add(v)
            elif v not in (None, "", [], False): out.setdefault("nonstring_forms", set()).add(type(v).__name__)
    out["distinct_reason_values"] = len(vals)
    out["nonstring_forms"] = sorted(out.get("nonstring_forms", []))
    surf = {"cases_csv": "/api/cases.csv", "proposals": "/api/assistants/proposals", "proposals_csv": "/api/assistants/proposals.csv",
            "ai_report": "/api/ai/report", "assistants": "/api/assistants", "audit_check": "/api/audit-check", "rai_metrics": "/api/assistants/rai-metrics"}
    out["literal_reason_value_hits"] = {k: sum(c.request.get(APP + u).text().count(v) for v in vals) for k, u in surf.items()}
    out["reason_value_sample_lengths"] = sorted(len(v) for v in vals)[:5]
    b.close()
json.dump(out, open(os.path.dirname(os.path.abspath(__file__)) + "/probe_r2b.json", "w"), indent=1)
print(json.dumps(out, indent=1))
