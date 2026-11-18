"""Local, offline exercise of the real simulator_admin start/stop/rate controls (no Azure)."""
import json, tempfile, os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from zava_forward.core import identity
from zava_forward.api import simulator_admin as sa, live_control
from zava_forward.api.live_simulator import Limits, check_capacity

class Store:
    def audit(self, *a): print("  audit:", a[0].split("@")[0][:0] + "<actor>", a[1:])
u = identity.principal("11111111-1111-1111-1111-111111111111", "22222222-2222-2222-2222-222222222222",
    identity.ADMIN_ROLE_NAME, name="Demo Admin", email="admin@example.invalid", roles=("ZavaForward.ApplicationAdmin",), app_admin=True, view_only=False)
now = datetime.now(UTC)
d = Path(tempfile.mkdtemp()); f = d / "control.json"; env = {sa.ENV: str(f)}
def call(label, method, path, body=None):
    code, out = sa.handle(Store(), u, method, path, body, env, now)
    print(f"{label}: HTTP {code} ->", json.dumps(out, sort_keys=True)[:420])
    return out
st = call("status-before", "GET", sa.PREFIX)
rev = st.get("revision", "absent")
exp = (now + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
homes = [f"HOME-{i:03d}" for i in range(5)]
good = dict(owner="demo owner", approval_reference="issue-189-demo", expires_at=exp, homes=homes, expected_revision=rev, confirm=True)
call("start-no-confirm", "POST", sa.PREFIX + "/start", {**good, "confirm": False})
call("start-blank-owner", "POST", sa.PREFIX + "/start", {**good, "owner": " "})
call("start-expiry-too-far", "POST", sa.PREFIX + "/start", {**good, "expires_at": (now + timedelta(days=15)).strftime("%Y-%m-%dT%H:%M:%SZ")})
call("start-rate-too-high-2000-homes", "POST", sa.PREFIX + "/start", {**good, "homes": [f"HOME-{i:04d}" for i in range(2000)]})
s = call("start-ok", "POST", sa.PREFIX + "/start", good)
call("start-again", "POST", sa.PREFIX + "/start", {**good, "expected_revision": s["status"].get("revision")})
call("stop-ok", "POST", sa.PREFIX + "/stop", {"expected_revision": s["status"].get("revision"), "confirm": True})
call("status-after", "GET", sa.PREFIX)
print("rate limits:", Limits())
for n in (1, 60, 1000, 5000):
    try: check_capacity(n, Limits()); print(f"capacity N={n}: ok")
    except Exception as e: print(f"capacity N={n}: refused {e}")
