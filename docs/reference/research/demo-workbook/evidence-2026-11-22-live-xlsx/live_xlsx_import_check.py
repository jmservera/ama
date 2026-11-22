import hashlib, json, os, re, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
W = Path("/home/azureuser/source/ama-wt/issue-2008-live-20261122T230127Z")
OUT = W / "docs/reference/research/demo-workbook/evidence-2026-11-22-live-xlsx"
OUT.mkdir(parents=True, exist_ok=True)
CSV = W / "docs/reference/research/demo-workbook/demo-case-list.csv"
XLSX = CSV.with_suffix(".xlsx")
user = Path.home().joinpath(".ama-test-user-id").read_text().strip()
pw = Path.home().joinpath(".ama-test-user").read_text().strip()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
rec = {"csv_sha256_before": sha(CSV), "xlsx_sha256_before": sha(XLSX)}
def clean(t):
    for s in (user, pw, user.split("@")[0]):
        t = t.replace(s, "[redacted]")
    return re.sub(r"[\w.+-]+@[\w.-]+", "[identity]", t)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_context(viewport={"width": 1440, "height": 900}).new_page()
    pg.goto(APP + "/app", wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_selector('input[name="loginfmt"]', timeout=60000); pg.fill('input[name="loginfmt"]', user); pg.click('input[type=submit], button[type=submit]')
    pg.wait_for_selector('input[type=password]', timeout=30000); pg.wait_for_timeout(1500)
    pg.fill('input[type=password]', pw); pg.click('input[type=submit], button[type=submit]')
    pg.wait_for_selector('#idBtn_Back', timeout=30000); pg.click('#idBtn_Back')
    pg.wait_for_url(re.compile(r"https://ca-cutover.*"), timeout=60000); pg.wait_for_timeout(8000)
    sub_u = sub_p = True
    rec["landed_on_app_host"] = pg.url.split("/")[2].startswith("ca-cutover")
    if not rec["landed_on_app_host"]:
        rec["stuck_text"] = clean(pg.locator("body").inner_text()[:300]); rec["flags"]=[sub_u,sub_p]; print(json.dumps(rec)); sys.exit(1)
    pg.wait_for_timeout(3000)
    resp = []
    bodies=[]
    def _r(r):
        if "/api/import-check" in r.url:
            resp.append((r.url, r.status)); bodies.append(r.json())
    pg.on("response", _r)
    pg.goto(APP + "/app#/import", wait_until="domcontentloaded"); pg.wait_for_timeout(3000)
    main = pg.locator("main").first if pg.locator("main").count() else pg.locator("body")
    main.screenshot(path=str(OUT / "01-import-page-before-upload.png"))
    rec["accept"]=pg.get_attribute("#f","accept"); pg.set_input_files("#f", str(XLSX))
    pg.wait_for_selector("text=Your file has not been changed", timeout=30000)
    pg.wait_for_timeout(1000)
    rec["import_check_responses"] = [s for _, s in resp]
    rec["result_text"] = clean(pg.locator("main, body").first.inner_text())
    main.screenshot(path=str(OUT / "02-xlsx-mapping-conflicts-rows.png"))
    rec["raw_api"] = {"status": resp[0][1], "body": bodies[0]}
    b.close()
rec["csv_sha256_after"] = sha(CSV); rec["xlsx_sha256_after"] = sha(XLSX)
rec["source_unchanged"] = rec["csv_sha256_before"] == rec["csv_sha256_after"] and rec["xlsx_sha256_before"] == rec["xlsx_sha256_after"]
(OUT / "live-import-check-raw-output.json").write_text(json.dumps(rec, indent=1))
print(json.dumps({k: v for k, v in rec.items() if k != "raw_api"}, indent=1)[:2500])
