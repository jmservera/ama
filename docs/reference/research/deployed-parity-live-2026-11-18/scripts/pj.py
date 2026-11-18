import json,sys
from playwright.sync_api import sync_playwright
H="https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
who=sys.argv[1]
with sync_playwright() as pw:
    c=pw.chromium.launch().new_context(storage_state=f"/tmp/state-{who}.json")
    for p in sys.argv[2:]:
        r=c.request.get(H+p,max_redirects=0); print(p,r.status); open("/tmp/out_"+p.strip("/").replace("/","_").replace("?","_")+".json","w").write(r.text())
