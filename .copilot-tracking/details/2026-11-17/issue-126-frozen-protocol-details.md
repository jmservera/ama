---
title: Issue 126 plan details
ms.date: 2026-11-17
---

# Details

* P1 test goes in `src/core/tests/test_governance.py` next to `test_paused_scope_blocks_case_workflows_but_not_hazards`. It appends a synthetic work order (`case_id`, `package`, `state`) to `store.data["procurement"]["work_orders"]`, records a breach with `scope_kind="work package"`, asserts `log_call` raises "paused", asserts a case with no order in the package is unaffected, then restarts and asserts `log_call` succeeds.
* P2 reads `self.data.get("procurement", {})` read-only (no setdefault, so no data mutation) and uses the ACTIVE states from `procurement`; import lazily if a cycle appears.
* Workstream: no case mapping exists; documented limitation, no new model.
* Tier FOCUSED: no SQL, security-control change or deployment. The change tightens an existing pause, in-process only.
