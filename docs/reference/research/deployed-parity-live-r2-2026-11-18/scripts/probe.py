"""GET-only probe of the demo API with a saved Playwright session; prints status and a short body summary."""
import json
import sys

from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
who = sys.argv[1]


def summary(text: str) -> str:
    try:
        d = json.loads(text)
    except ValueError:
        return text[:160].replace("\n", " ")
    if isinstance(d, dict):
        parts = []
        for k, v in list(d.items())[:12]:
            if isinstance(v, list):
                parts.append(f"{k}=[{len(v)}]")
            elif isinstance(v, dict):
                parts.append(f"{k}={{{','.join(list(v)[:6])}}}")
            else:
                parts.append(f"{k}={str(v)[:60]}")
        return "; ".join(parts)
    if isinstance(d, list):
        return f"list[{len(d)}]"
    return str(d)[:100]


with sync_playwright() as pw:
    c = pw.chromium.launch().new_context(storage_state=f"/tmp/state-{who}.json")
    for p in sys.argv[2:]:
        r = c.request.get(H + p, max_redirects=0)
        body = r.text()
        print(f"{r.status} {p} | {summary(body)}")
