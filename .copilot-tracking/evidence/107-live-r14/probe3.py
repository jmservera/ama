from playwright.sync_api import sync_playwright
from login_lib import *
G = "async(p)=>{const r=await fetch(p,{credentials:'same-origin'});return [r.status,await r.json()]}"
with sync_playwright() as p:
    b, page = login(p)
    st, d = page.evaluate(G, "/api/me"); b.close()
open("/home/azureuser/.copilot/session-state/3018d061-182c-42a3-afdd-d6723dc3d455/files/app-identity.txt","w").write(d["user"]["email"])
print("saved; shape:", __import__("re").sub(r"[0-9a-f]","h",d["user"]["email"]))
