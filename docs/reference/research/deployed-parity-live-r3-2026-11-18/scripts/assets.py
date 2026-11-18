"""Fetch each of the 16 historical web assets from the deployed app and compare sha256 with the repository copy."""
import hashlib
import pathlib
from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
W = pathlib.Path("/home/azureuser/source/ama-wt/issue-350-live-20261118T1403Z/src/api/src/zava_forward/api/web")
names = ["app.js", "assistants.js", "index.html", "law.html", "law.js", "ops.js", "panels.js", "style.css", "timecapture.js",
         "welcome.html", "zava-logo.png", "vendor/LICENSE", "vendor/leaflet.css", "vendor/leaflet.js",
         "vendor/images/layers.png", "vendor/images/marker-icon.png"]
with sync_playwright() as pw:
    c = pw.chromium.launch().new_context(storage_state="<session-dir>/state-staff.json")
    for n in names:
        r = c.request.get(f"{H}/{n}", max_redirects=0)
        served = hashlib.sha256(r.body()).hexdigest()[:16]
        f = W / n
        local = hashlib.sha256(f.read_bytes()).hexdigest()[:16] if f.exists() else "missing"
        print(f"{n} | {r.status} | {len(r.body())} bytes | served {served} | repo {local} | {'match' if served == local else 'DIFF'}")
