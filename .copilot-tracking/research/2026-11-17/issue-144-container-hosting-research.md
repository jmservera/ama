---
title: Issue 144 container hosting assessment against main (research)
ms.date: 2026-11-17
---

## Scope

Assess issue #144 against `origin/main` eb51af5c9ab0b1353ac380fc8960ee8dd96d17c4. Evidence only, demo-first,
desktop-only, focused tier. Research disposition: executed. Status: opened; findings follow below.

## Findings (measured on main eb51af5c9, 2026-11-17)

Planning Readiness: Ready.

* Targeted tests pass sequentially on main: `infra.tests.test_container_hosting_completeness` (16), `test_container_contract` plus `test_bicep_containerapp_demo_wiring` (28), `src/agents` `test_worker.py` (19), `src/api` `test_scale_fixture_load_and_restart.py` (4), `test_restart_audit.py` (1), `test_scale_load.py` (7). Run with the worktree `src` directories on `PYTHONPATH`, because the installed editable distributions point at the main checkout.
* Recorded main evidence: `docs/architecture/scale-load-2026-11-01.json` and `scale-restart-2026-11-13.json`. Both state `meets_declared_workload: false` (53,821 of 600,000 events; 126 s and 62 s of the declared 1,800 s) and every route p95 exceeds the NFR-002 thresholds (1 s, 1 s, 3 s). Neither is production, Azure or autoscaling evidence.
* Drift: issue comments cite `scale-load-2026-11-15.json`, `scale-restart-2026-11-15.json`, `test_container_load_and_restart_144.py` and the hardening inspection (`inspect_runtime_container_hardening`, PR #1788 and #1809). None exists on main; they sit on the stacked branch of PR #1641, which is OPEN (not merged). The two ticked criteria remain supported on main by the 2026-11-01 and 2026-11-13 records and the tests above. The hardening code is not on main.
* Unmet on main and in the issue: real versioned worker and job images deployed through the pipeline (the infra README records the agents `serve` loop gated by `ZF_AGENT_RESULT_ROUTE`, which Bicep omits) and deployed hardening (Bicep exposes no `readOnlyRootFilesystem` or capability-drop setting; recorded in `infra/README.md`). Both need live Azure, so they are out of scope here (no Azure actions, infrastructure edits excluded).
* Gap found: no test ties the recorded JSON reports to the README claims "not at declared scale" and "no production claim".
