import os, sys, json, time, collections, concurrent.futures as cf
import requests
from playwright.sync_api import sync_playwright
R = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
A = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
L = open(os.path.expanduser("~/.ama-resident-test-user")).read().splitlines()
U, P = L[0].strip(), L[1].strip()
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(); ctx.set_default_timeout(90000); page = ctx.new_page()
    page.goto(R + "/", timeout=180000); page.wait_for_selector("#signin:not([hidden])")
    page.fill("#email", U); page.fill("#password", P); page.click("#signin-button"); page.wait_for_selector("#content:not([hidden])")
    cookies = {c["name"]: c["value"] for c in ctx.cookies()}; b.close()
SID = requests.get(R+'/demo/session', cookies=cookies, timeout=60).json().get('session_id','')

def one(base, path, ck):
    s = requests.Session()
    for k, v in (ck or {}).items(): s.cookies.set(k, v, domain=base.split("//")[1])
    for attempt in range(1):
        try:
            r = s.get(base + path, timeout=60, allow_redirects=False, headers={'X-Resident-Session': SID} if ck else {})
            return (r.status_code, len(r.content), "x-ms-middleware-request-id" in r.headers)
        except Exception as e:
            return ("EXC:" + type(e).__name__, 0, False)

def burst(label, base, path, ck, rounds=4, n=30):
    tot = collections.Counter(); empty500 = 0; per = []
    for r in range(rounds):
        with cf.ThreadPoolExecutor(n) as ex: res = list(ex.map(lambda _: one(base, path, ck), range(n)))
        c = collections.Counter(str(x[0]) for x in res); per.append(dict(c))
        tot.update(c); empty500 += sum(1 for x in res if x[0] == 500 and x[1] == 0)
    out = {"target": label, "path": path, "requests": rounds * n, "status_counts": dict(tot), "empty_body_500": empty500, "per_round": per}
    print(json.dumps(out)); return out

res = []
res.append(burst("resident (signed in)", R, "/demo/view", cookies))
res.append(burst("resident (signed in)", R, "/demo/session", cookies))
res.append(burst("resident (signed in)", R, "/demo.js", cookies))
res.append(burst("resident (anon)", R, "/healthz", None))
res.append(burst("api (Easy Auth, anon)", A, "/healthz", None))
res.append(burst("api (Easy Auth, anon)", A, "/readyz", None))
res.append(burst("api (Easy Auth, anon)", A, "/welcome.html", None))
res.append(burst("api (Easy Auth, anon)", A, "/workspace-shell.js", None))
res.append(burst("api (Easy Auth, anon)", A, "/api/whoami", None))
json.dump(res, open("/tmp/wt/burst-results.json", "w"), indent=1)
