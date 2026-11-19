"""Read-only live probe: structural summary of ranking and AI priority output.

Credentials are read from the owner files at runtime and never printed. Only
key names, list lengths and status codes are written; identifiers are dropped.
"""

import json
import os
import re
import sys

from playwright.sync_api import sync_playwright

BASE = os.environ.get("DEMO_API_BASE", "https://<demo-api-host>")
HOME = os.path.expanduser("~")
OUT = sys.argv[1]


def shape(v, depth=0):
    if isinstance(v, dict):
        return {k: shape(x, depth + 1) for k, x in list(v.items())[:40]} if depth < 3 else "object"
    if isinstance(v, list):
        return {"list_len": len(v), "item": shape(v[0], depth + 1) if v else None}
    return type(v).__name__


user = open(HOME + "/.ama-test-user-id").read().strip()
pw_ = open(HOME + "/.ama-test-user").read().strip()
result = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    pg.goto(BASE + "/sign-in")
    for _ in range(4):
        try:
            if pg.locator("input[name=loginfmt]").is_visible(timeout=3000):
                pg.fill("input[name=loginfmt]", user)
                pg.click("input[type=submit]")
                pg.wait_for_timeout(1500)
            if pg.locator("input[name=passwd]").is_visible(timeout=3000):
                pg.fill("input[name=passwd]", pw_)
                pg.click("input[type=submit]")
                pg.wait_for_timeout(2000)
            if pg.locator("#idBtn_Back").is_visible(timeout=2000):
                pg.click("#idBtn_Back")
                pg.wait_for_timeout(2000)
        except Exception:
            pass
    pg.wait_for_load_state("networkidle")
    result["landed"] = re.sub(r"\?.*", "", pg.url).replace(BASE, "<demo-api>")
    for path in ("/api/ranking/policy", "/api/ranking/snapshot", "/api/ai/priority"):
        r = c.request.get(BASE + path)
        entry = {"status": r.status}
        try:
            entry["shape"] = shape(r.json())
        except Exception:
            entry["shape"] = "non-json"
        result[path] = entry
    b.close()
json.dump(result, open(OUT, "w"), indent=2)
print(json.dumps(result)[:1500])
