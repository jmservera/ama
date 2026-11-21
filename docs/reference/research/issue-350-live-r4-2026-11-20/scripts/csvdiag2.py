import csv, io, collections
from playwright.sync_api import sync_playwright
H = open("<session-dir>/H").read().strip()
with sync_playwright() as pw:
    c = pw.chromium.launch().new_context(storage_state="<session-dir>/state-staff.json")
    rows = list(csv.DictReader(io.StringIO(c.request.get(H + "/api/cases.csv?view=mine").text())))
    print("owner values in csv mine:", collections.Counter(r["Owner"] for r in rows).most_common(5))
    allr = list(csv.DictReader(io.StringIO(c.request.get(H + "/api/cases.csv?view=all").text())))
    print("owner distribution all:", len(collections.Counter(r["Owner"] for r in allr)), "owners; top", collections.Counter(r["Owner"] for r in allr).most_common(3))
    me = c.request.get(H + "/api/me").json(); print("me counts", me["counts"])
    for p in ["/api/cases?view=mine&limit=100", "/api/cases?view=mine&limit=100&sort=id", "/api/cases?view=mine&limit=100&flag=nodecision"]:
        print(p, c.request.get(H + p).json()["total"])
