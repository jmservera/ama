import json,sys
from playwright.sync_api import sync_playwright
H="https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
def session():
    pw=sync_playwright().start()
    return pw, pw.chromium.launch().new_context(storage_state="/tmp/state-staff.json")
def post(c,p,b):
    r=c.request.post(H+p,data=json.dumps(b),headers={"Content-Type":"application/json","X-ZF-CSRF":"1"},max_redirects=0)
    try: return r.status,r.json()
    except Exception: return r.status,r.text()[:300]
def get(c,p):
    r=c.request.get(H+p,max_redirects=0)
    try: return r.status,r.json()
    except Exception: return r.status,r.text()[:300]
