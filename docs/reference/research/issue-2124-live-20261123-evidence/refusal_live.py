"""Zero-model-call live refusal check of the demo case chat for the refuse-expected prompts.

Run from the eval-gates-live-216-2026-11-18/scripts folder after login.py staff <base> wrote
/tmp/state-staff.json. Only prompts that the rule layer must refuse are sent (R01-R07, A03, A04, A10).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
from pg import call, open_page  # noqa: E402

spec = json.loads(Path(sys.argv[2]).read_text())
case = spec["case_id"]
pw, ctx, pg = open_page()
rows, threads = [], []
try:
    for c in spec["cases"]:
        if c["expect"] != "refused":
            continue
        _, t = call(pg, "POST", "/api/chat/threads", {"case_id": case})
        threads.append(t["id"])
        st, a = call(pg, "POST", f"/api/chat/threads/{t['id']}/ask", {"content": c["q"]})
        cons = a.get("consumption") or {} if isinstance(a, dict) else {}
        rows.append(
            {
                "id": c["id"],
                "set": c["set"],
                "http": st,
                "kind": a.get("kind") if isinstance(a, dict) else None,
                "model_calls": cons.get("model_calls"),
                "cited": len(a.get("citations", [])) if isinstance(a, dict) else None,
            }
        )
finally:
    deleted = [call(pg, "POST", f"/api/chat/threads/{tid}/delete", {})[0] for tid in threads]
left = [x for x in call(pg, "GET", "/api/chat/threads")[1] if x["id"] in threads]
ok = [r for r in rows if r["kind"] == "refused" and r["model_calls"] == 0]
print(
    json.dumps(
        {
            "n": len(rows),
            "refused_with_zero_model_calls": len(ok),
            "delete_statuses": sorted(set(deleted)),
            "threads_left": len(left),
            "rows": rows,
        },
        indent=1,
    )
)
