from playwright.sync_api import sync_playwright
from common import *
import re as _re
res = {}
with sync_playwright() as p:
    b, pg = session(p)
    s, d = call(pg, "GET", "/api/cases/ZF-2025-0331")
    res["guarantees"] = d.get("challenge_guarantees"); res["assurance"] = d.get("challenge_assurance")
    res["targets"] = scrub(d.get("challenge_targets")); res["challenges"] = scrub(d.get("affected_challenges"))
    s, h = call(pg, "GET", "/api/cases/ZF-2025-0331?view=nomination-routes-html")
    txt = _re.sub(r"<[^>]+>", " ", h.get("_text", "")); res["html_text"] = scrub(_re.sub(r"\s+", " ", txt))[:1800] if False else _re.sub(r"\s+", " ", txt)[:1800]
    b.close()
json.dump(res, open("run2.json", "w"), indent=1, default=str); print(json.dumps(res, indent=1, default=str)[:4500])
