"""Issue 154 follow-up probe: representative-view and resident-view responses for listed cases (read-only GETs, credentials read at runtime)."""
import json, os, re
from playwright.sync_api import sync_playwright
OUT = os.path.dirname(os.path.abspath(__file__))
EMPAPP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
rd = lambda n: [x.strip() for x in open(os.path.join(os.path.expanduser("~"), n)).read().split("\n") if x.strip()]
u, w = rd(".ama-test-user-id")[0], rd(".ama-test-user")[0]
mk = lambda s: re.sub(r"[\w.+-]+@[\w.-]+", "[email]", s)
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1366, "height": 900}); pg.set_default_timeout(90000)
    pg.goto(EMPAPP + "/api/me", wait_until="domcontentloaded")
    pg.fill("input[name=loginfmt]", u); pg.click("#idSIButton9")
    pg.wait_for_selector("input[name=passwd]"); pg.fill("input[name=passwd]", w); pg.click("#idSIButton9")
    for _ in range(3):
        try:
            pg.wait_for_selector("#idSIButton9, #idBtn_Back", timeout=6000)
            if pg.url.startswith(EMPAPP): break
            (pg.query_selector("#idSIButton9") or pg.query_selector("#idBtn_Back")).click()
        except Exception:
            break
    pg.wait_for_load_state("domcontentloaded")
    items = pg.evaluate("fetch('/api/cases').then(r=>r.json())")["items"]
    out["item_keys"] = sorted(items[0].keys())[:25]
    allids = [i.get("case_id") or i.get("id") or (i.get("case") or {}).get("id") for i in items]
    ids = allids[:3]
    out["probes"] = {}
    def walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if "represent" in k.lower() or "authorit" in k.lower(): yield path + "/" + k, v
                yield from walk(v, path + "/" + k)
        elif isinstance(o, list):
            for i, v in enumerate(o[:5]): yield from walk(v, path + f"[{i}]")
    det = pg.evaluate("p=>fetch(p).then(r=>r.json())", f"/api/cases/{ids[0]}")
    out["representative_keys_in_case_detail"] = {k: (json.dumps(v)[:160] if v else v) for k, v in walk(det)}
    out["case_detail_top_keys"] = sorted(det.keys())
    for cid in ids:
        for suffix in ["", "representative-view", "representative-view?representative_ref=none"]:
            r = pg.evaluate("p=>fetch(p).then(async r=>({s:r.status,t:await r.text()}))", f"/api/cases/{cid}" + (f"/{suffix}" if suffix else ""))
            out["probes"][f"{cid}/{suffix or '(case)'}"] = {"status": r["s"], "body": mk(r["t"])[:120]}
    scan = {}
    for cid in allids:
        d = pg.evaluate("p=>fetch(p).then(r=>r.json())", f"/api/cases/{cid}")
        scan[cid] = {"resident_representative_set": bool((d.get("resident") or {}).get("representative")), "rep_authorities": len((d.get("nomination_permissions") or {}).get("representative_authorities") or [])}
    out["scan_all_listed_cases"] = scan
    json.dump(out, open(os.path.join(OUT, "rep-probe.json"), "w"), indent=1); print(json.dumps(out, indent=1)[:3500]); b.close()
