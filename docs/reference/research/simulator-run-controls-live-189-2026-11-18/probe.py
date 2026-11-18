import json, re
from playwright.sync_api import sync_playwright
H="https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
P="/api/admin/simulator-control"
def scrub(t): return re.sub(r"[\w.+-]+@[\w.-]+","<email>",t)[:700]
with sync_playwright() as pw:
    b=pw.chromium.launch(); c=b.new_context(storage_state="/tmp/state-staff.json",viewport={"width":1440,"height":900}); r=c.request
    for name,m,path,body in [("me","GET","/api/me",None),("status","GET",P,None),
        ("start-no-body","POST",P+"/start",{}),("stop-no-body","POST",P+"/stop",{}),("unknown","GET",P+"/nope",None)]:
        kw={"headers":{"Content-Type":"application/json"},"data":json.dumps(body)} if m=="POST" else {}
        x=r.fetch(H+path,method=m,**kw)
        t=x.text()
        if name=="me":
            d=json.loads(t); t=json.dumps({k:d.get(k) for k in ("role","roles","app_admin","view_only") if k in d})
        print(name,m,path,x.status,scrub(t))
    b.close()
