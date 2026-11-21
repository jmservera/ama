import json
from playwright.sync_api import sync_playwright
H = open("<session-dir>/H").read().strip()
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(storage_state="<session-dir>/state-staff.json", viewport={"width": 1440, "height": 900})
    g = lambda p: c.request.get(H + p).json()
    t = g("/api/time/status"); print("time", {k: t[k] for k in ("enabled", "flag_on", "dpia_recorded", "consultation_recorded") if k in t}, "reason:", str(t.get("reason") or t.get("blockers") or t.get("note"))[:200])
    a = g("/api/assistants"); print("assistants", len(a["assistants"]), "tasks", len(a["registered_tasks"]), "proactive", a["proactive"], "gate", str(a["real_ai_delivery_gate"])[:160])
    gv = g("/api/governance"); print("governance releases", gv.get("releases"), "release_gaps", len(gv.get("release_gaps") or []))
    ct = g("/api/continuity"); print("continuity epoch", ct["epoch"], "suspended", ct["suspended"], "valid", ct["history_valid"], "suspensions", len(ct["suspensions"]))
    m = g("/api/me"); print("services", m["services"], "map", str(m["map"])[:200])
    pg = c.new_page(); pg.goto(H + "/app"); pg.wait_for_timeout(5000)
    tiles = []
    pg.on("response", lambda r: tiles.append(r.status) if "tile" in r.url or ".png" in r.url else None)
    pg.screenshot(path="<session-dir>/screens/staff-app-r4.png")
    print("title", pg.title())
