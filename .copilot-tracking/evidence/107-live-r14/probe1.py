import json
from playwright.sync_api import sync_playwright
from login_lib import *
G = "async(p)=>{const r=await fetch(p,{credentials:'same-origin'});return [r.status,await r.json()]}"
with sync_playwright() as p:
    b, page = login(p)
    st, d = page.evaluate(G, "/api/assistants")
    out = {"status": st, "keys": list(d), "assistant0": (d.get("assistants") or [None])[0], "gate": d.get("real_ai_delivery_gate"), "disabled": d.get("disabled")}
    b.close()
t = redact(json.dumps(out, indent=1))
open("probe1.json", "w").write(t); print(t[:7000])
