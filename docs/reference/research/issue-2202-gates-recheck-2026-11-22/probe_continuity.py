"""Item 2 (employee): read-only GET /api/continuity to record the AI suspension state. Sign-in read at run time, never printed."""
import json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe_staff.py")).read().split("res = {}")[0])
res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(); pg = c.new_page(); login(pg)
    r = c.request.get(H + "/api/continuity", timeout=60000)
    res["http"] = r.status
    try:
        j = r.json()
        res["keys"] = sorted(j.keys()) if isinstance(j, dict) else type(j).__name__
        def pick(d):
            return {k: (v if isinstance(v, (str, int, bool, type(None))) else str(v)[:160]) for k, v in d.items() if k in ("scope", "scope_kind", "status", "reason", "recorded_at", "synthetic", "incident_owner", "containment")}
        for k in ("suspensions", "active", "incidents", "items"):
            v = j.get(k) if isinstance(j, dict) else None
            if isinstance(v, list):
                res[k] = [pick(x) for x in v if isinstance(x, dict)][:5]
    except Exception:
        res["body"] = r.text()[:200]
    s = json.dumps(res, indent=1, default=str); assert u not in s and p not in s
    open(OUT + "/probe-continuity-result.json", "w").write(s); print(s); b.close()
