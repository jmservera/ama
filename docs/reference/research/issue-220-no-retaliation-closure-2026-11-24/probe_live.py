"""Non-mutating live probe of the challenge route on the demo API (issue 220). Credentials are read at runtime and never written."""
import json, os
from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
u = open(home + "/.ama-test-user-id").read().strip()
p = open(home + "/.ama-test-user").read().strip()
JS = """async ([path, body]) => {
  const r = await fetch(path, {method: body === null ? 'GET' : 'POST', credentials: 'same-origin',
    headers: {'Content-Type': 'application/json', 'X-ZF-CSRF': '1'}, body: body === null ? undefined : JSON.stringify(body)});
  let j = null; try { j = await r.json(); } catch (e) {}
  return {status: r.status, json: j};
}"""
res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    pg.goto(H + "/sign-in")
    for _ in range(4):
        try:
            if pg.locator("input[name=loginfmt]").is_visible(timeout=3000):
                pg.fill("input[name=loginfmt]", u); pg.click("input[type=submit]"); pg.wait_for_timeout(1500)
            if pg.locator("input[name=passwd]").is_visible(timeout=3000):
                pg.fill("input[name=passwd]", p); pg.click("input[type=submit]"); pg.wait_for_timeout(2000)
            if pg.locator("#idBtn_Back").is_visible(timeout=2000):
                pg.click("#idBtn_Back"); pg.wait_for_timeout(2000)
        except Exception:
            pass
    try:
        pg.wait_for_load_state("networkidle", timeout=60000)
    except Exception:
        pass
    pg.goto(H + "/app"); pg.wait_for_timeout(3000)
    me = pg.evaluate(JS, ["/api/me", None])
    res["me"] = {"status": me["status"], "role": (me["json"] or {}).get("role")}
    # Unknown proposal id: the route answers with an error and nothing is created.
    r = pg.evaluate(JS, ["/api/assistants/proposals/NO-SUCH-PROPOSAL-220/challenge",
                         {"action": "open", "revision": "x", "target_kind": "proposal"}])
    res["challenge_unknown_proposal"] = {"status": r["status"], "error": (r["json"] or {}).get("error")}
    pg.screenshot(path=OUT + "/live-app.png")
json.dump(res, open(OUT + "/live-probe-result.json", "w"), indent=2)
print(json.dumps(res))
