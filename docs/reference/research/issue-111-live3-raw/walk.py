import json, os, hashlib
from playwright.sync_api import sync_playwright
H=os.environ["DEMO_API_URL"]
rd=lambda p:open(os.path.expanduser(p)).read().strip()
u=rd("~/.ama-test-user-id"); p=rd("~/.ama-test-user")
out=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(); c=b.new_context(viewport={"width":1366,"height":900}); pg=c.new_page()
    pg.goto(H+"/app")
    pg.wait_for_selector("input[type=email]",timeout=30000); pg.fill("input[type=email]",u); pg.click("input[type=submit]")
    pg.wait_for_selector("input[type=password]",timeout=30000); pg.fill("input[type=password]",p); pg.click("input[type=submit]")
    try:
        pg.wait_for_selector("#idBtn_Back",timeout=8000); pg.click("#idBtn_Back")
    except Exception: pass
    pg.wait_for_url(H+"/**",timeout=45000); pg.wait_for_load_state("networkidle")
    out.append("app url path: "+pg.url.replace(H,""))
    pg.screenshot(path=os.environ["OUT_DIR"]+"/workbench.png")
    r=c.request.get(H+"/api/me"); out.append(f"/api/me {r.status}")
    cs=c.request.get(H+"/api/cases"); out.append(f"/api/cases {cs.status}")
    raw=cs.json(); out.append("shape "+type(raw).__name__+" "+str(sorted(raw.keys()) if isinstance(raw,dict) else ""))
    cases=raw if isinstance(raw,list) else next((v for v in raw.values() if isinstance(v,list)),[])
    out.append(f"cases {len(cases)}")
    done=False
    for cs_ in cases:
        cid=cs_.get("id") or cs_.get("case_id") or cs_.get("reference")
        a=c.request.get(f"{H}/api/cases/{cid}/sensors")
        if a.status==200 and a.text() not in ("null","{}"):
            d=a.json(); a2=c.request.get(f"{H}/api/cases/{cid}/sensors")
            dk=[k for k in d if d[k]!=a2.json().get(k)]; out.append("differing keys between two calls: "+str(dk)); out.append(f"sensors 200 keys={sorted(d.keys())[:12]} identical={a.text()==a2.text()} sha={hashlib.sha256(a.body()).hexdigest()[:16]}")
            for k in ("schema","version","calibrated","freshness","state","label","analysis_version","signal","signals"):
                if k in d: out.append(f"  {k}={json.dumps(d[k])[:300]}")
            open(os.environ["OUT_DIR"]+"/sensors.json","w").write(json.dumps(d,indent=1)); done=True; break
    out.append(f"sensor payload found={done}")
    for path in ("/api/sensor-drafts","/api/sensor-review-drafts"):
        x=c.request.get(H+path); out.append(f"{path} {x.status} {x.text()[:200]}")
    b.close()
open(os.environ["OUT_DIR"]+"/walk.txt","w").write("\n".join(out)); print("\n".join(out))
