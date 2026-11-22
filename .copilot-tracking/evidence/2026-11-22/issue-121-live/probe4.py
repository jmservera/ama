"""One live read-doc on an existing uploaded synthetic document with no derivative: expect a hold, no model call. Credentials read at runtime; output reduced to hold facts."""
import json, os, re
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe2.py")).read().split("out = {}")[0]
exec(src)
from playwright.sync_api import sync_playwright
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded"); login(page)
    rows = c.request.get(APP + "/api/cases").json(); rows = rows if isinstance(rows, list) else rows.get("cases", rows.get("items", []))
    target = None
    for row in rows[:40]:
        d = c.request.get(APP + "/api/cases/" + row["id"]).json()
        for x in d.get("documents", []) or d.get("docs", []):
            m = str(x.get("mime", ""))
            if x.get("generated") is False and (m.startswith("text/") or m.startswith("image/")):
                target = (row["id"], x["id"], m); break
        if target: break
    res["target_found"] = bool(target)
    if target:
        res["mime"] = target[2]
        page.goto(APP + "/")
        out = page.evaluate("""async ([cid, did]) => { const r = await fetch('/api/cases/' + cid + '/read-doc', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-ZF-CSRF': '1'}, body: JSON.stringify({id: did})}); return [r.status, 'T:' + await r.text()]; }""", [target[0], target[1]])
        out = list(out) + [""]
        out[1] = out[1] or ""
        res["status"] = out[0]
        res["raw"] = re.sub(r"[\w.+-]+@[\w.-]+", "[email]", out[1])[:200]
        try: j = json.loads(out[1][2:])
        except Exception: j = {}
        res["source"] = j.get("source"); res["model"] = j.get("model"); res["task"] = j.get("task")
        res["reason"] = re.sub(r"[\w.+-]+@[\w.-]+", "[email]", str(j.get("reason") or j.get("error") or ""))[:300]
        res["text"] = str(j.get("text", ""))[:160]
    b.close()
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe4.json"), "w"), indent=1); print(res)
