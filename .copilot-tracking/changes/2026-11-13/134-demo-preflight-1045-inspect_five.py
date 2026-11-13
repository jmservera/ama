"""Read-only five-home preflight over the fictional seed 20260901 / as-of 2026-10-13."""
import importlib, json, re, sys, tempfile
from pathlib import Path
from unittest.mock import patch

REPO = Path("/home/azureuser/source/ama-demo-wt/child-134-demo-preflight-1045")
sys.path.insert(0, str(REPO / "src/core/tests"))
sys.path.insert(0, str(REPO / "support/synthetic-data/retrofit-flow/zava-forward-year-one/generator"))
import test_generated_dataset as tg
from zava_forward.core.store import Store

builder = tg.builder
homes = tg.runbook_five_homes((REPO / "docs/capstone/demo/runbook.md").read_text())
tmp = Path(tempfile.mkdtemp(prefix="pf1045-"))
seed = tmp / "seed.json"
with patch.object(builder, "load_register", return_value=tg.register()):
    with patch.object(sys, "argv", ["b", "--seed", "20260901", "--as-of", "2026-10-13", "--out", str(seed)]):
        builder.main()
store = Store(str(seed), live_path=str(tmp / "live.json"), audit_path=str(tmp / "audit.jsonl"))
user = next(s for s in store.data["staff"] if s["role"] == "Retrofit Programme Manager")


def find(obj, pat, path=""):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}"
            if re.search(pat, k, re.I):
                out.append((p, v if not isinstance(v, (dict, list)) else f"{type(v).__name__}[{len(v)}]"))
            out += find(v, pat, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:3]):
            out += find(v, pat, f"{path}[{i}]")
    return out


print("top-level data keys:", sorted(store.data))
print("sensor-like top-level keys:", [k for k in store.data if re.search("sensor|reading|backfill", k, re.I)])
for cid, ptype, stage in homes:
    c = store.cases[cid]
    d = store.detail(cid, user)
    try:
        hv = store.home_case_view(user, cid)
        hv_state = f"ok keys={sorted(hv)} building={'present' if hv.get('building') else 'absent'} version={hv.get('version_status')}"
    except Exception as e:
        hv_state = f"ERROR {type(e).__name__}: {e}"
    print("\n==", cid, ptype, stage)
    print("stage/closed/hazards:", c["stage"], c["closed"], len(c["hazards"]))
    print("building_id:", c.get("building_id"), "scheme_id:", c.get("scheme_id"))
    print("archetype/damp fields:", find(c, "arche|damp"))
    print("sensor fields:", find(c, "sensor|reading"))
    print("stock_reconciliation:", len(c.get("stock_reconciliation", [])), "conflict fields:", find(c, "conflict")[:4])
    print("gate:", d.get("gate"), "status:", d.get("status"))
    print("assistant proposal fields:", find(c, "proposal|assistant")[:4])
    print("home_case_view:", hv_state)
