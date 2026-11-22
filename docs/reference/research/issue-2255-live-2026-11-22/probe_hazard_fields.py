"""Read-only probe: which hazard timing fields does the live API return for open safety cases."""
import json, os, re
from collections import Counter
from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
u = open(home + "/.ama-test-user-id").read().strip()
p = open(home + "/.ama-test-user").read().strip()
res = {}


def login(page):
    page.goto(H + "/sign-in")
    for _ in range(4):
        try:
            if page.locator("input[name=loginfmt]").is_visible(timeout=3000):
                page.fill("input[name=loginfmt]", u); page.click("input[type=submit]"); page.wait_for_timeout(1500)
            if page.locator("input[name=passwd]").is_visible(timeout=3000):
                page.fill("input[name=passwd]", p); page.click("input[type=submit]"); page.wait_for_timeout(2000)
            if page.locator("#idBtn_Back").is_visible(timeout=2000):
                page.click("#idBtn_Back"); page.wait_for_timeout(2000)
        except Exception:
            pass
    page.wait_for_load_state("networkidle")


with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1440, "height": 900}); pg = c.new_page()
    login(pg)
    r = c.request.get(H + "/api/cases?view=all&flag=hazard&sort=urgent&limit=100")
    res["status"] = r.status
    j = r.json() if r.ok else {}
    res["total"] = j.get("total")
    rows = j.get("cases") or j.get("items") or j.get("rows") or []
    res["row_keys"] = sorted(rows[0].keys()) if rows else []
    res["row_count"] = len(rows)
    ids = [x.get("id") or x.get("case_id") for x in rows]
    fields = Counter(); detail_hazard_keys = Counter(); samples = []; clock_values = Counter()
    for cid in ids:
        d = c.request.get(f"{H}/api/cases/{cid}")
        if not d.ok:
            fields["detail_http_" + str(d.status)] += 1; continue
        dj = d.json(); case = dj.get("case", dj)
        for i, h in enumerate(case.get("hazards") or []):
            clock_values[f"{h.get('clock_status')}|{h.get('clock_basis')}"] += 1
            for k, v in h.items():
                detail_hazard_keys[k] += 1
                if v not in (None, "", "Unknown"):
                    fields["non_empty:" + k] += 1
        if len(samples) < 3:
            samples.append({k: (v if k in ("category", "priority", "aware_at", "response_due_at", "resident_update_due_at", "released") else "<present>" if v else v) for h in (case.get("hazards") or [])[:1] for k, v in h.items()})
    res["hazard_keys_seen"] = dict(detail_hazard_keys)
    res["non_empty_field_counts"] = dict(fields)
    res["clock_status_basis_counts"] = dict(clock_values)
    res["samples"] = samples
    s = json.dumps(res, indent=1); assert u not in s and p not in s
    open(OUT + "/probe-hazard-fields-result.json", "w").write(s); print(s); b.close()
