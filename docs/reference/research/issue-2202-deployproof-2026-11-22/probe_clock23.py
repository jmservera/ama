"""Item 1 detail: per-case hazard clock text on the safety list (23 cases). Sign-in read at run time, never printed."""
import json, os, re
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe_staff.py")).read().split("res = {}")[0])
res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1440, "height": 900}); pg = c.new_page()
    login(pg)
    pg.goto(H + "/app#/all"); pg.wait_for_timeout(7000)
    pg.get_by_label("Show only").select_option(label="Safety issue open"); pg.wait_for_timeout(5000)
    t = txt(pg, "main", 600000)
    parts = re.split(r"(?=ZF-\d{4}-\d{4})", t)
    rows = {}
    for s in parts:
        m = re.match(r"(ZF-\d{4}-\d{4})", s)
        if not m or m.group(1) in rows:
            continue
        h = re.search(r"Hazard clock: [^.]*\.[^.]*\.?", s)
        o = re.search(r"Accountable owner: ([A-Z][a-z]+ [A-Z][a-z]+)", s)
        rows[m.group(1)] = {"clock": h.group(0)[:160] if h else None, "owner_named": bool(o)}
    res["cases"] = rows
    res["n_cases"] = len(rows)
    res["with_hours"] = sum(1 for r in rows.values() if r["clock"] and "hours elapsed" in r["clock"])
    res["unknown"] = sum(1 for r in rows.values() if r["clock"] and "unknown" in r["clock"])
    res["no_clock_text"] = [k for k, r in rows.items() if not r["clock"]]
    res["running"] = len(re.findall(r"response open", t)); res["overdue"] = len(re.findall(r"response overdue", t))
    res["owner_named"] = sum(1 for r in rows.values() if r["owner_named"])
    s = json.dumps(res, indent=1); assert u not in s and p not in s
    open(OUT + "/probe-clock23-result.json", "w").write(s); print(s[:3500]); b.close()
