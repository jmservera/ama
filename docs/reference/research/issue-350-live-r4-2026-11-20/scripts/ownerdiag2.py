import collections
from playwright.sync_api import sync_playwright
H = open("<session-dir>/H").read().strip()
with sync_playwright() as pw:
    c = pw.chromium.launch().new_context(storage_state="<session-dir>/state-staff.json")
    g = lambda p: c.request.get(H + p).json()
    first = g("/api/cases?view=all&limit=1")["items"][0]; print("summary keys has owner_code:", "owner_code" in first, [k for k in first if "owner" in k])
    items, off = [], 0
    while True:
        pg = g(f"/api/cases?view=all&limit=100&offset={off}"); items += pg["items"]; off += 100
        if off >= pg["total"]: break
    print("paged items", len(items))
    key = "owner_code" if "owner_code" in first else "owner"
    cnt = collections.Counter(i.get(key) for i in items)
    print("body-derived owner counts via SQL page path:", sorted(cnt.values(), reverse=True))
    me = g("/api/me")["user"]; print("me keys", sorted(me)[:8]) if isinstance(me, dict) else None
