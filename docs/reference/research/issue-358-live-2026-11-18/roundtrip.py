"""Live round-trip: real preserve_app_secrets + ARM PATCH on a throwaway app."""
import importlib.util, json, subprocess, sys
spec = importlib.util.spec_from_file_location("se", "infra/scripts/setup-entra.py")
se = importlib.util.module_from_spec(spec); sys.modules["se"] = se; spec.loader.exec_module(se)
SUB = "e51ebc89-79d0-4a52-a82b-01a292eefd5b"
ID = f"/subscriptions/{SUB}/resourceGroups/ama/providers/Microsoft.App/containerApps/ca-358-throwaway"
def rest(method, path, body=None):
    cmd = ["az", "rest", "--method", method, "--url", f"https://management.azure.com{path}{'&' if '?' in path else '?'}api-version={se.API_VERSION}"]
    if body is not None: cmd += ["--body", json.dumps(body), "--headers", "Content-Type=application/json"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit("az rest failed: " + r.stderr[-400:])
    return json.loads(r.stdout) if r.stdout.strip() else {}
def view(rows): return [{k: v for k, v in r.items() if k != "value"} | ({"hasValue": True} if "value" in r else {}) for r in rows]
app = rest("GET", ID)
before = app["properties"]["configuration"].get("secrets") or []
listed = rest("POST", ID + "/listSecrets")
print("listSecrets rows (names, value-bearing only):", [(r["name"], "value" in r, "keyVaultUrl" in r) for r in listed["value"]])
preserved = se.preserve_app_secrets(before, listed)
new = {"name": "new-synthetic-5678", "value": "synthetic-not-secret-new"}
cfg = {**app["properties"]["configuration"], "secrets": [*[p for p in preserved if p["name"] != "new-synthetic-1234"], new]}
rest("PATCH", ID, {"properties": {"configuration": cfg}})
import time
for _ in range(40):
    got = rest("GET", ID)
    if got["properties"]["provisioningState"] == "Succeeded": break
    time.sleep(5)
after = got["properties"]["configuration"].get("secrets") or []
print("before:", json.dumps(view(before)))
print("after :", json.dumps(view(after)))
b = {r["name"]: r for r in before}; a = {r["name"]: r for r in after}
ok = all(a.get(n, {}).get(f) == b[n].get(f) for n in b for f in ("keyVaultUrl", "identity")) and "new-synthetic-5678" in a
print("digest before-ref preserved:", ok, "digest equal subset:", se.secret_reference_digest([r for r in after if r["name"] in b]) == se.secret_reference_digest(before))
print("RESULT", "PASS" if ok else "FAIL")
