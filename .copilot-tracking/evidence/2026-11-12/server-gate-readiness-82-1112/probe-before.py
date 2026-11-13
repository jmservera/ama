import json, tempfile, copy, sys
from pathlib import Path
sys.path.insert(0, ".")
from dataset import DATA
from test_quality_procurement import STAFF
from zava_forward.core import store as S
for mode in ("absent", "none", "yes", "false"):
    d = copy.deepcopy(DATA); d["staff"] = STAFF
    c = next(x for x in d["cases"] if x["id"] == "ZF-3")
    if mode == "absent": del c["funding_ok"]
    elif mode == "none": c["funding_ok"] = None
    elif mode == "yes": c["funding_ok"] = "yes"
    else: c["funding_ok"] = False
    with tempfile.TemporaryDirectory() as t:
        p = Path(t)/"z.json"; p.write_text(json.dumps(d))
        st = S.Store(str(p))
        u = next(s for s in STAFF if s["role"] == "Resident Liaison Officer")
        user = dict(name=u["name"], email=u["email"], role=u["role"], code=u["code"])
        try:
            st.advance(user, "ZF-3"); print(mode, "advanced")
        except Exception as e:
            print(mode, type(e).__name__, repr(getattr(e, "reasons", e))[:200])
        try:
            print("  gate_reasons", S.Store.gate_reasons(st._case("ZF-3"))[:1])
        except Exception as e: print("  gate_reasons", type(e).__name__, e)
