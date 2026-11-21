from playwright.sync_api import sync_playwright
H = open("<session-dir>/H").read().strip()
with sync_playwright() as pw:
    c = pw.chromium.launch().new_context(storage_state="<session-dir>/state-staff.json")
    g = lambda p: c.request.get(H + p).json()
    st = g("/api/stats"); team = st["team"]; print("team sample keys", list(team[0]) if team else None)
    for t in team:
        code = t.get("code") or t.get("owner_code")
        sql = g(f"/api/cases?view=all&owner={code}&limit=1")["total"]
        mem = g(f"/api/cases?view=all&owner={code}&limit=1&flag=nodecision")["total"]
        print(code, "stats", {k: v for k, v in t.items() if isinstance(v, int)}, "sql-filter", sql, "memory-filter(nodecision)", mem)
