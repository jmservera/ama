"""Diagnose why identity-override views differ from the baseline view (no secrets printed)."""

import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
EMAIL, PASSWORD = (Path.home() / ".ama-resident-test-user").read_text().splitlines()[:2]
out = {}


def diff(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        return [d for k in sorted(set(a) | set(b)) for d in diff(a.get(k), b.get(k), path + "/" + k)]
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in diff(x, y, path + "/%d" % i)]
    return [] if a == b else [path]


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    csrf = ctx.request.get(URL + "/demo/session", timeout=90000).json()["csrf"]
    r = ctx.request.post(URL + "/demo/login", data=json.dumps({"email": EMAIL, "password": PASSWORD}),
                         headers={"Origin": URL, "Content-Type": "application/json", "X-CSRF-Token": csrf})
    out["login"] = r.status
    sh = {"X-Resident-Session": ctx.request.get(URL + "/demo/session").json()["session_id"]}
    g = lambda q="", h=None: ctx.request.get(URL + "/demo/view" + q, headers=sh | (h or {})).json()
    base1 = g()
    time.sleep(2)
    base2 = g()
    out["baseline_vs_baseline_diff_paths"] = diff(base1, base2)
    out["case_override_diff_paths"] = diff(base1, g("?case=OTHER"))
    out["case_id_override_diff_paths"] = diff(base1, g("?case_id=OTHER"))
    out["email_override_diff_paths"] = diff(base1, g("?email=other@example.invalid"))
    out["x_case_id_diff_paths"] = diff(base1, g("", {"X-Case-Id": "OTHER"}))
    out["x_forwarded_user_diff_paths"] = diff(base1, g("", {"X-Forwarded-User": "other@example.invalid"}))
    out["base1_keys"] = sorted(base1)
    out["account_email_is_signed_in_user"] = base1.get("account", {}).get("email") == EMAIL
    out["override_account_email_unchanged"] = g("?email=other@example.invalid").get("account", {}).get("email") == EMAIL
    b.close()
blob = json.dumps(out)
assert PASSWORD not in blob
Path(__file__).with_name("override-diagnosis.json").write_text(json.dumps(out, indent=1))
print(blob)
