---
title: Issue 74 criterion 2 populated-building probe changes and raw evidence
description: Runner source, hashes, commands, exits, in-process origins and raw output for the populated building rows two-home probe; no repository source or test change
ms.date: 2026-11-13
---

## Changes

Evidence Markdown only. No source or test edit.

## Runs (both executed after the acceptable critique)

* Setup: temp venv, `pip install --no-deps -e src/core -e src/agents -e src/api` from this worktree, exit 0; `ZF_DATA` set to a temp path in the same temp directory; fixtures only.
* Command: `cd /tmp && ZF_DATA=<temp>/zf.json <temp>/v/bin/python /tmp/c2b_runner.py` (direct, no pipe).
* Run 1, runner sha256 `495a58df...ef76ed`: producer exit 1, AssertionError on ZF-2 documents. Cause (diagnosed with a one-off print): `open_store` adds `SYN-COMMITMENT` to each home's documents via the contract fixture, so my expected list was wrong. This is a runner expectation error, not a reproduced product defect. Retained as an adverse first outcome.
* Run 2, runner sha256 `86495834...55d7d9` (only change: the documents assertion ignores `SYN-COMMITMENT`): producer exit 0, stderr empty.

Raw stdout of run 2 (origins asserted inside the same process to be under this worktree `src/core`):

```text
origin building_fixture /home/azureuser/source/ama-demo-wt/demo-home-building-c2-74-1012/src/core/tests/building_fixture.py
origin zava_forward.core.store /home/azureuser/source/ama-demo-wt/demo-home-building-c2-74-1012/src/core/src/zava_forward/core/store.py
origin zava_forward.core.sqlstore /home/azureuser/source/ama-demo-wt/demo-home-building-c2-74-1012/src/core/src/zava_forward/core/sqlstore.py
origin zava_forward.core.home_case /home/azureuser/source/ama-demo-wt/demo-home-building-c2-74-1012/src/core/src/zava_forward/core/home_case.py
origin zava_forward.core.buildings /home/azureuser/source/ama-demo-wt/demo-home-building-c2-74-1012/src/core/src/zava_forward/core/buildings.py
OK sql=False
OK sql=True
ALL OK
```

## Runner source (sha256 86495834a4710b30df4729c6e191702cbc75f0744ddd6e6728629fc80e55d7d9)

```python
import sys, os, tempfile, json
from copy import deepcopy
W = "/home/azureuser/source/ama-demo-wt/demo-home-building-c2-74-1012"
sys.path.insert(0, W + "/src/core/tests")
import building_fixture as bf
import zava_forward.core.store as st, zava_forward.core.sqlstore as sq, zava_forward.core.home_case as hc, zava_forward.core.buildings as bl
for m in (bf, st, sq, hc, bl):
    print("origin", m.__name__, m.__file__)
    assert os.path.realpath(m.__file__).startswith(W + "/src/core"), m.__file__
d = bf.fixture()
b = d["buildings"][0]
b["dependencies"] = [{"id": "DEP-1", "label": "Shared roof access", "status": "Open", "owner": "Syn owner", "source": "SYN-DEP", "case_ids": ["ZF-2", "ZF-3"], "package_ids": ["PKG-SHARED"]}]
b["holds"] = [bf.hold()]
b["works"].append({"id": "WORK-2", "label": "Shared drainage", "status": "Proposed", "owner": "Syn owner", "source": "SYN-SCOPE", "case_ids": ["ZF-3"], "package_ids": ["PKG-OTHER"]})
b["costs"].append({"id": "COST-2", "work_id": "WORK-2", "amount_gbp": "7000.00", "source": "SYN-EST2"})
z2, z3 = d["cases"]
z2["decision"]["status"] = "Accepted"; z3["decision"]["status"] = "Waiting"
z2["funding_ok"] = True; z3["funding_ok"] = False
z2["cost_allocation"] = [{"shared_cost_id": "COST-1", "amount_gbp": "6000.00", "source": "SYN-ALLOC-2"}]
z3["cost_allocation"] = [{"shared_cost_id": "COST-2", "amount_gbp": "3500.00", "source": "SYN-ALLOC-3"}]
z3["stage"] = "Survey"; z2["stage"] = "Design"
exp = {
 "ZF-2": dict(status="Accepted", funding=True, alloc=["6000.00"], docs=[x["id"] for x in z2["documents"]], stage="Design"),
 "ZF-3": dict(status="Waiting", funding=False, alloc=["3500.00"], docs=[x["id"] for x in z3["documents"]], stage="Survey"),
}
assert exp["ZF-2"]["docs"] != exp["ZF-3"]["docs"]
for sql in (False, True):
    with tempfile.TemporaryDirectory() as f:
        s = bf.open_store(f, sql, deepcopy(d))
        try:
            pam = s.data["staff"][1]
            v = {c: s.home_case_view(pam, c) for c in exp}
            for c, e in exp.items():
                h = v[c]["home"]
                assert h["decision"]["status"] == e["status"], (sql, c, "decision")
                assert h["funding_confirmed"] is e["funding"], (sql, c, "funding")
                assert [a["amount_gbp"] for a in h["cost_allocation"]] == e["alloc"], (sql, c, "alloc")
                assert [x["id"] for x in h["documents"] if x["id"] != "SYN-COMMITMENT"] == e["docs"], (sql, c, "docs")
                assert h["stage"] == e["stage"], (sql, c, "stage")
                bld = v[c]["building"]
                assert bld.get("status") != "Unknown" and "homes" not in bld
                assert [r["id"] for r in bld["dependencies"]] == ["DEP-1"]
                assert [r["id"] for r in bld["holds"]] == ["HOLD-1"]
                assert [r["id"] for r in bld["works"]] == ["WORK-1", "WORK-2"]
                assert [r["id"] for r in bld["costs"]] == ["COST-1", "COST-2"]
                blob = json.dumps(bld)
                for sentinel in ("SYN-ALLOC-2", "SYN-ALLOC-3", "SIBLING-EVIDENCE", "3500.00", "6000.00", "Waiting"):
                    assert sentinel not in blob, (sql, c, sentinel)
            assert v["ZF-2"]["building"] == v["ZF-3"]["building"], "building differs between homes"
            assert v["ZF-2"]["home"] != v["ZF-3"]["home"]
            print("OK sql=%s" % sql)
        finally:
            if sql: s.db.close()
print("ALL OK")
```

## Coverage

In-memory Store and SqlStore (temp SQLite) through `home_case_view` as a finance-capable staff user: populated dependency, hold, two works and two costs equal for both homes, with no home allocation, evidence or Waiting sentinel; each home keeps distinct decision status, funding, allocation, documents and stage; swap would fail. Outcome adequacy of stage/closed/quality is not decided.

## Limits

No API HTTP, browser, real SQL, Docker, cloud, accessibility or conformance run. No repository test added. Criterion 2 not ticked; no human approval is claimed or invented. Source-correction history: UNKNOWN.
