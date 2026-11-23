---
title: Issue 2245 demo AI override on the SQL store and live recheck (2026-11-23, 18:26Z run)
description: The owner-directed AI suspension override did not apply to the SQL store, plus a live probe of employee chat on revision 0000057
ms.date: 2026-11-23
ms.topic: reference
---

Scope: synthetic demo, desktop, resource group `ama`, API `ca-cutover-test-demo-api`, active revision `0000057` (created 2026-11-23T17:34Z). Sign-in values were read from the owner files at run time and never printed. Azure access was read-only (`az containerapp revision list`, `show` for variable names only, `logs show`). Probes and results sit in [issue-2245-override-sqlstore-2026-11-23/](./issue-2245-override-sqlstore-2026-11-23/).

## Findings

* Revision 0000057 sets `ZF_DEMO_AI_SUSPENSION_OVERRIDE` and `ZF_CHAT_DEMO_ACTIVATION` (names only read). The suspension `SYN-221-PROBE` is still open in `GET /api/continuity` ([probe-continuity-result.json](./issue-2245-override-sqlstore-2026-11-23/probe-continuity-result.json)).
* Source defect found: #2326 applied `continuity.demo_owner_override()` in `ContinuityMixin.continuity_suspension`, but `SqlStore.continuity_suspension` overrides that method and reads the persisted record, so the override never applied to the SQL store the demo runs on. Fixed in `src/core/src/zava_forward/core/sqlstore.py` (after the fail-closed `gate_hold`, so an integrity hold still wins). The new test `test_sql_store_hold_is_lifted_by_the_override_and_the_record_stays_open` fails without the fix and passes with it.
* Live probe: eight thread creations returned 200 (96 to 145 ms) and no thread-creation 500 occurred in this window. Two rules-first asks returned 200 with `model: workflow-only`. The first free-form ask returned 500 after 30.5 s and the probe stopped there ([probe-chat-result.json](./issue-2245-override-sqlstore-2026-11-23/probe-chat-result.json)). The cause is not readable (the console tail showed only health-check disconnects; Log Analytics is denied). It is consistent with a model call or lock wait exceeding the 30 s gateway window, but that is an inference.
* Not deployed: the fix is local. A new revision is an owner action; this run changed no Azure resource.

## Per-criterion table (the issue has no checkboxes; expectations taken from its text)

| Criterion | Status | Evidence |
| --- | --- | --- |
| Thread creation no longer returns a bare 500 on a busy SQL write lock | Proven locally; live not reproduced this window | `test_error_logging`/`test_chat_panel` (earlier runs); eight live creates returned 200 |
| Visible "Model calls: 1" for a model-answerable question | Unproven live | Defect found that blocks the override on SQL; fix local only; live free-form ask returned 500 |
| Banner states plainly when answers are rule-based | Proven earlier (2026-11-23 notes), not re-run | [issue-2245-recheck-2026-11-23.md](./issue-2245-recheck-2026-11-23.md) |
| Which skills and routes call the model and why none did | Proven | Open suspension plus the SQL-store override gap above |

## Owner actions

* Deploy a revision containing this fix, then repeat the free-form probe and expect "Model calls: 1".
* If the free-form ask still returns 500 after 30 s, read the replica log for the ask route (Log Analytics access needed).
