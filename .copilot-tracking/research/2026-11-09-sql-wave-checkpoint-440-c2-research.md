---
title: SQL feature-recovery wave checkpoint 440 C2 qualification research
ms.date: 2026-11-09
task_id: 440-sql-wave-checkpoint-1109-c2
---

## Task identity and scope

* Task `440-sql-wave-checkpoint-1109-c2`, slug `sql-wave-checkpoint-440-c2`, parent task `440-sql-wave-checkpoint-1109`. State: `.copilot-tracking/rpi-sessions/2026-11-09/sql-wave-checkpoint-440-c2-state.json`.
* Worktree `/home/azureuser/source/ama-demo-wt/issue-440-sql-checkpoint`, branch `docs/demo-sql-checkpoint-440-1109`, clean at start. Prior candidate head `06f408dd7d46e9cdd521a17b10579552ffadd598`, tree `c07ee46b056acff4fef81e2c040a518872f602ab`; comparison source `8d6f029cac004506953f36606862168bbe9d9412` (merged PR 1308).
* Objective: one scoped review-correction cycle (C2) for the independent PARTIAL Readiness findings. Documentation only; no source, test, workflow, infrastructure or policy change. `Refs #440` only.
* Allowance: C1 (the historical `b270` qualification) is spent; C2 is explicitly authorized by the coordinator within five total correction cycles, leaving three after this one. Research disposition: `executed`; Planning Readiness: Ready.
* Provenance: coordinator brief `brief-440-c2-facts.md`, `demo-rpi-common.md` and the exact Readiness file `independent-440-sql-wave/readiness-findings.json`. The normalized `approve_with_comments` is not full publication clearance; the assessment is PARTIAL.

## Evidence read in this task

* Finding 1 (Medium). The pack table row at `docs/architecture/cutover-evidence-pack.md` line 5388 says "Committed or uncertain creation maps to HTTP 409 `outcome=committed`". Source read at this tree:
  * `src/api/src/zava_forward/api/server.py:1242-1246` maps only `CommittedReloadError` from `ai_priority` to HTTP 409 with `outcome: "committed"`; `1265-1268` does the same for the resolve route (including `ResidentCommittedError`).
  * `src/core/src/zava_forward/core/sqlstore.py:156-159` defines `CommittedReloadError` as a write that committed whose reload did not settle (`committed = True`).
  * `src/api/src/zava_forward/api/web/app.js:38-40` `mutationNeedsHistory(error)` is true for `outcome` committed, `outcome` uncertain, or an error without `status` (transport failure); `724-730` latches `checkHistory` for any such error, so the repeat control stays hidden and history must be reconciled.
  * Conclusion: a `CommittedReloadError` (a write that committed whose reload failed) returns 409 `committed`, while a successful creation returns 200; the UI latch applies to the current panel instance. An uncertain or transport failure does not prove a commit or any HTTP status. The existing row conflates them. Rendered browser behavior was not observed in the checkpoint and is not claimed.
* Finding 2 (Low). The original authored Review (`.copilot-tracking/reviews/2026-11-09-sql-wave-checkpoint-440-review.md`) R3 says one occurrence in four runs. The retained records show five executions of the affected test: the first failing Core selection (exit 1, 421 tests, one "database is locked" failure), three passing isolated runs, and the passing serial Core selection (exit 0, 421 tests). The pack F2 already says "four times" later passes. The failed assertion is the errors-list assertion at `test_priority_order.py:734`, not the elapsed-time assertion at 735. Cause is UNKNOWN; no waiver.
* New diagnosis, #1292 startup-lock diagnostic, read from its coordinator handoff `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/handoff-1292-startup-diagnostic.md`: frozen head `59accfa1ca9be77f2e98faf5ef862deba76cf941`, tree `93e1bf9f2bf563e22ed4c34c1eb84c46f2fd1085`, base `origin/main` `ef28d4da42d83b111d48f14df9b70e3c4932a477`; it ran the exact test six times (three plain, three observer-instrumented) with 0 of 6 reproductions, all OK in about 15 to 16 seconds. Its observational timing hypothesis H1 (a lock hold of about 3.05 to 3.25 s against a 5.0 s wait, margin about 1.6x) is consistent but NOT proven or reproduced; cause remains UNKNOWN. No source correction is indicated by that evidence, and it does not diagnose, fix or classify the earlier failure. Raw logs are outside this repository in `/home/azureuser/source/ama-demo-wt/logs-1292-startup-diagnostic/`. They were not re-read in this task; the handoff is the cited source (coordinator-reported).

## Main reconciliation

* Pinned main `ef28d4da42d83b111d48f14df9b70e3c4932a477` differs from merge base `8d6f029ca` only by `.github/rubric/scores/latest.json` (generated rubric advance). The planned merge preserves both sides and changes no source or policy.
* A later fetch shows `origin/main` `1464b4d850a89aaaf835ba8a9ad98d38aeb1fdd6` (#1312: `tools/rpi-checks.py`, `tools/test_rpi_checks.py` and tracking records, 17 files). It exceeds the rubric-only condition and is not merged in this task; reported to the coordinator.

## Planning Readiness

Ready. Facts are single-sourced to cited lines; no fresh test, SQL, browser or hosted run is needed or planned for a pure documentation correction.
