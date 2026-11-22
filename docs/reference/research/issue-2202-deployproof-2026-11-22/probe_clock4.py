"""Item 1 detail: text of the four safety cases whose list row shows no hazard clock. Sign-in read at run time, never printed."""
import json, os, re
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe_staff.py")).read().split("res = {}")[0])
res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1440, "height": 900}); pg = c.new_page()
    login(pg)
    pg.goto(H + "/app#/all"); pg.wait_for_timeout(7000)
    pg.get_by_label("Show only").select_option(label="Safety issue open"); pg.wait_for_timeout(5000)
    t = txt(pg, "main", 600000)
    for cid in ("ZF-2025-0122", "ZF-2025-0257", "ZF-2025-0505", "ZF-2025-0148"):
        i = t.find(cid)
        res[cid] = t[i:i + 420]
    pg.screenshot(path=f"{OUT}/screens/staff-safety-list-top.png")
    s = json.dumps(res, indent=1); assert u not in s and p not in s
    open(OUT + "/probe-clock4-result.json", "w").write(s); print(s); b.close()
