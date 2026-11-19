import json
from playwright.sync_api import sync_playwright
H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
with sync_playwright() as pw:
    c = pw.chromium.launch().new_context(storage_state="<session-dir>/state-staff.json")
    d = c.request.get(H + "/api/continuity").json()
    print(json.dumps({k: d[k] for k in ("epoch", "suspended", "history_valid") if k in d}, default=str)[:600])
    print(json.dumps(d.get("suspensions"), default=str)[:700])
