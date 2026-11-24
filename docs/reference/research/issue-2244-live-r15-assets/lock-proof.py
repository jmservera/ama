"""Issue 2244 proof: open MssqlStore on a throwaway copy of the demo database while another connection holds the write lock.

Run inside the API image with the API managed identity (ZF_SQL_AUTH=msi). Never point it at the live database."""
import logging
import os
import sys
import threading
import time

os.environ["ZF_SQL_DATABASE"] = os.environ.get("PROOF_DB", "tmp-2244-lockproof")
assert os.environ["ZF_SQL_DATABASE"] != "retrofit"
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stdout)

import base64  # noqa: E402
import gzip  # noqa: E402
import hashlib  # noqa: E402
import importlib.util  # noqa: E402

import shutil  # noqa: E402

pkg = importlib.util.find_spec("zava_forward.core").submodule_search_locations[0]
if os.environ.get("OVERLAY_sqlstore"):
    # the installed package is read-only: copy it to a scratch path that comes first on sys.path
    shutil.copytree(pkg, "/tmp/ovl/zava_forward/core")
    sys.path.insert(0, "/tmp/ovl")
    for mod in [k for k in sys.modules if k == "zava_forward" or k.startswith("zava_forward.")]:
        del sys.modules[mod]
    pkg = "/tmp/ovl/zava_forward/core"
for name in ("sqlstore", "mssqlstore", "continuity"):
    path = os.path.join(pkg, name + ".py")
    print(f"IMAGE {name}.py sha256 {hashlib.sha256(open(path, 'rb').read()).hexdigest()[:12]}", flush=True)
    payload = os.environ.get("OVERLAY_" + name)
    if payload:
        open(path, "wb").write(gzip.decompress(base64.b64decode(payload)))
        print(f"OVERLAY {name}.py written, sha256 {hashlib.sha256(open(path, 'rb').read()).hexdigest()[:12]}", flush=True)

import mssql_python  # noqa: E402

from zava_forward.core import mssqlstore as m  # noqa: E402

cs = m.connection_string(dict(os.environ))


def hold(seconds):
    conn = mssql_python.connect(cs, autocommit=True)
    cur = conn.cursor()
    cur.execute(m.BEGIN)
    print(f"HOLDER took the write lock, releases in {seconds} s", flush=True)

    def release():
        time.sleep(seconds)
        conn.cursor().execute("IF @@TRANCOUNT > 0 ROLLBACK TRAN")
        conn.close()
        print("HOLDER released the write lock", flush=True)

    t = threading.Thread(target=release)
    t.start()
    return t


def open_store(label, force_locked_path):
    if force_locked_path:
        m.MssqlStore._schema_current = lambda self: False
    t0 = time.time()
    try:
        store = m.MssqlStore("/tmp/zf.json", env=dict(os.environ), state_dir="/tmp/zf-state")
        print(f"RESULT {label}: opened in {time.time() - t0:.1f} s", flush=True)
        store.db.close()
        return True
    except BaseException as e:
        print(f"RESULT {label}: FAILED after {time.time() - t0:.1f} s: {type(e).__name__}: {str(e)[:160]}", flush=True)
        return False


_orig_begin = m._Conn._begin


def _traced_begin(self):
    print("BEGIN requested by " + " < ".join(sys._getframe(i).f_code.co_name for i in range(2, 6)), flush=True)
    return _orig_begin(self)


m._Conn._begin = _traced_begin
scenario = os.environ["PROOF_SCENARIO"]
if scenario == "current":
    t = hold(45)
    ok = open_store("schema current, lock held 45 s", False)
elif scenario == "long":
    t = hold(300)
    ok = open_store("schema current, lock held 300 s (longer than the retry budget of about 211 s)", False)
elif scenario == "retry":
    t = hold(40)
    ok = open_store("locked path forced, lock held 40 s (15 s lock timeout)", True)
else:
    ok = open_store("no holder baseline", False)
    t = None
if t:
    t.join()
sys.exit(0 if ok else 1)
