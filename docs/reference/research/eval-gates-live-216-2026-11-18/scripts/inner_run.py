"""Runs inside ca-cutover-test-demo-api (same image, same live model identity) against a throwaway local
server instance on 127.0.0.1:8099 with a temporary store; the deployed store and its demo meter are not touched."""
import base64, json, os, secrets, subprocess, sys, time, urllib.request, http.cookiejar, shutil
BUNDLE = json.loads(base64.b64decode(open("/tmp/r216.bundle").read()))
W = "/tmp/zf216"; shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
case = BUNDLE["case"]
USER = {"code": "E-216", "name": "Eval Demo User", "email": "eval216@example.invalid", "role": "Retrofit Programme Manager"}
json.dump({"staff": [USER], "cases": [case]}, open(W + "/data.json", "w"))
src = {}
for e in open("/proc/1/environ", "rb").read().split(b"\0"):
    if b"=" in e:
        k, v = e.split(b"=", 1); src[k.decode()] = v.decode()
keep = ("AI_", "IDENTITY_", "MSI_", "AZURE_CLIENT_ID", "ZF_CHAT_DEMO_ACTIVATION", "ZF_DEPLOYMENT_PROFILE", "CHAT_", "PATH", "HOME", "PYTHONPATH", "LANG", "ZF_AI_GOLDEN", "OTEL_SDK_DISABLED")
env = {k: v for k, v in src.items() if k.startswith(keep)}
pw = secrets.token_urlsafe(12)
env.update(ZF_AUTH="password", ZF_PASSWORD=pw, ZF_STORE="sqlite", ZF_DATA=W + "/data.json", ZF_STATE=W + "/state", ZF_SQLITE=W + "/state/zf.sqlite", ZF_BIND="127.0.0.1", PORT="8099")
os.makedirs(W + "/state", exist_ok=True)
srv = subprocess.Popen([sys.executable, "-m", "zava_forward.api"], env=env, stdout=open(W + "/srv.log", "w"), stderr=subprocess.STDOUT)
B = "http://127.0.0.1:8099"
jar = http.cookiejar.CookieJar(); op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
def req(m, p, b=None):
    r = urllib.request.Request(B + p, data=None if b is None else json.dumps(b).encode(), method=m, headers={"Content-Type": "application/json"})
    try:
        with op.open(r, timeout=60) as x: return x.status, json.loads(x.read() or b"null")
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:300].decode(errors="replace")
out = {"rows": []}
try:
    for _ in range(40):
        try: urllib.request.urlopen(B + "/healthz", timeout=2); break
        except Exception: time.sleep(0.5)
    out["login"] = req("POST", "/api/login", {"email": USER["email"], "password": pw})[0]
    out["chat_status"] = {k: v for k, v in (req("GET", "/api/chat/status")[1] or {}).items() if k in ("activation", "storage_approved", "demo_activation")}
    for c in BUNDLE["cases"]:
        s, t = req("POST", "/api/chat/threads", {"case_id": case["id"]})
        if s != 200: out["rows"].append({"id": c["id"], "http": s, "err": str(t)[:200]}); continue
        s, a = req("POST", f"/api/chat/threads/{t['id']}/ask", {"content": c["q"]})
        out["rows"].append({"id": c["id"], "http": s, "answer": a})
        req("POST", f"/api/chat/threads/{t['id']}/delete", {})
finally:
    srv.terminate(); time.sleep(1)
    try: out["server_log_tail"] = open(W + "/srv.log").read()[-600:]
    except Exception: pass
    shutil.rmtree(W, ignore_errors=True)
    if os.path.exists("/tmp/r216.bundle"): os.remove("/tmp/r216.bundle")
print("RESULT216 " + base64.b64encode(json.dumps(out).encode()).decode() + " ENDRESULT216")
