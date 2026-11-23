"""Item 2 (employee chat): ask through the widget, record the ask response fields. Sign-in read at run time, never printed."""
import json, os, re
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe_staff.py")).read().split("res = {}")[0])
QS = ["Which homes should I prioritise first by EPC and stock facts?", "What is the status of the funding grant claim?"]
res = {"asks": []}
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1440, "height": 900}); pg = c.new_page()
    login(pg)
    st = c.request.get(H + "/api/chat/status", timeout=60000)
    res["status_http"] = st.status
    try:
        res["status"] = {k: (v if not isinstance(v, (dict, list)) else str(v)[:200]) for k, v in st.json().items()}
    except Exception:
        res["status_body"] = st.text()[:120]
    pg.goto(H + "/app#/case/ZF-2025-0031"); pg.wait_for_timeout(5000)
    pg.locator("#employee-chat-launcher").click(); pg.wait_for_timeout(2500)
    for q in QS:
        box = pg.locator("textarea:visible, input[type=text]:visible").last
        box.fill(q)
        try:
            with pg.expect_response(lambda r: r.url.endswith("/ask"), timeout=120000) as ri:
                pg.keyboard.press("Enter")
            r = ri.value
            e = {"q": q, "http": r.status}
            if r.ok:
                j = r.json()
                e["keys"] = sorted(j.keys())
                e["kind"] = j.get("kind")
                e["reply"] = (j.get("reply") or "")[:350]
                e["attribution"] = {k: j[k] for k in j if k in ("model", "model_calls", "tokens", "provider", "label", "usage", "route", "routing", "ai") }
            else:
                e["body"] = r.text()[:200]
        except Exception as ex:
            e = {"q": q, "error": repr(ex)[:200]}
        pg.wait_for_timeout(2500)
        e["widget_routing"] = pg.locator(".chat-widget-routing").all_inner_texts()[-1:]
        res["asks"].append(e)
    pg.screenshot(path=f"{OUT}/screens/employee-chat.png")
    s = json.dumps(res, indent=1, default=str); assert u not in s and p not in s
    open(OUT + "/probe-staff-chat-result.json", "w").write(s); print(s); b.close()
