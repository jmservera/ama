import os,re,hashlib,subprocess,json
from playwright.sync_api import sync_playwright
exec(open("live_531_probe.py").read().split("with sync_playwright")[0])
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(); pg=c.new_page()
    pg.goto(APP+"/api/me",wait_until="domcontentloaded"); login(pg)
    out={}
    for f in ("app.js","style.css"):
        out[f]=hashlib.sha256(c.request.get(f"{APP}/{f}").body()).hexdigest()
    b.close()
json.dump(out,open("deployed_hashes.json","w"))
