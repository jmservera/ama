"""Live desktop sign-in proof for ca-resident-demo. Credentials are read at runtime and never printed."""
import json, subprocess, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1])
fqdn = subprocess.run(["az","containerapp","show","-g","ama","-n","ca-resident-demo","--query","properties.configuration.ingress.fqdn","-o","tsv"],capture_output=True,text=True).stdout.strip()
email, password = Path.home().joinpath(".ama-resident-test-user").read_text().split("\n")[:2]
email, password = email.strip(), password.strip()
res = {}
def scrub(s): return s.replace(password, "[pw]").replace(email, "[email]")
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_context(viewport={"width":1280,"height":900}).new_page()
    pg.goto(f"https://{fqdn}/", timeout=120000)
    pg.get_by_label("Email address").fill(email)
    pg.get_by_label("Password").fill(password)
    pg.evaluate("""() => document.querySelectorAll('input').forEach(i => { if (i.type==='password'||i.type==='email'||i.id==='email') i.style.color='transparent'; })""")
    pg.screenshot(path=str(OUT/"01-signin-filled-masked.png"))
    pg.get_by_role("button", name="Sign in").click()
    pg.locator("#account > summary").wait_for(timeout=60000)
    pg.screenshot(path=str(OUT/"02-signed-in.png"))
    s = pg.evaluate("() => fetch('/demo/session').then(r=>r.json())")
    res["session_keys"] = sorted(s.keys())
    res["signed_in"] = s.get("signed_in")
    text = pg.inner_text("body")
    res["password_in_page"] = password in text
    res["title"] = pg.title()
    res["view_status_without_session_binding_header"] = pg.evaluate("() => fetch('/demo/view').then(r=>r.status)")
    res["session_cookie_attrs"] = [{k:c[k] for k in ("name","secure","httpOnly","sameSite","expires")} for c in pg.context.cookies() if c["name"].startswith("__Host")]
    pg.locator("#account > summary").click(); pg.click("#signout")
    pg.wait_for_timeout(1500)
    res["after_signout_signed_in"] = pg.evaluate("() => fetch('/demo/session').then(r=>r.json()).then(j=>j.signed_in)")
    b.close()
res["fqdn_host_only"] = fqdn.split(".")[0]
out = scrub(json.dumps(res, indent=1))
(OUT/"live-checks.json").write_text(out)
print(out)
