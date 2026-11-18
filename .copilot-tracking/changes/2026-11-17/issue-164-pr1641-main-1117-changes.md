# Changes: #164 / PR #1641 merge with main f1df574bb

* Merge commit 9d2fdfb2e (made before the implement-start witness call, which required the changes file; recorded honestly): origin/main f1df574bb merged without rebase. 27 conflicted paths; 26 replayed from rerere and verified against the prior reviewed tree and main; docs/reference/README.md resolved by hand (both sides' index rows kept, ms.date 2026-11-17). docs/reference/log.md auto-merged with both sides' entries.
* Alignment (from 69367b4f1, 3-way applied): main chat widget markup restored, safeguarding owner projection removed from staff case detail, AC-071 traceability retargeted, PR tests for dropped behaviour removed.
* Correction found by tests: first targeted run failed (27 errors: circular import store -> quality -> aftercare -> ai_registry -> assistants -> store, caused by PR quality.py `aftercare.neutral_violations` hook that the prior reviewed reconcile had already dropped because main's aftercare owns neutral text; then 12 failures from main's `complete_work_order` order vs the #81 exercise gate). Decision: take the prior reviewed tree (3ec8444c0) for every file that differs from it and was not touched by main since 7546c3105: quality.py, procurement.py, store.py, taskqueues.py, rai_control_plane.py, chat web files, API/core tests for dropped behaviour, infra reproducibility_check.py and test_environment_quota_parameters.py, and the formatter-only join e2d4691b1. Files main did move (54) were verified as prior + main delta by a 3-way merge-file comparison (aftercare, README, agent md, latest.json, map checks all identical). Settled review findings were not reopened; dropped PR behaviours remain the routed follow-ups of the prior review.

## Validation observed locally (tier FULL expected; focused checks only)

* Core targeted (31 modules matching chat, consent, safeguard, hazard, taskqueue, resident_decisions, aftercare, store, workflows, governance, gates, rai_control, provenance): 1123 tests OK, 193 skipped.
* API targeted (43 modules matching chat, consent, safeguard, hazard, origin, provenance, accessibility_baseline, content_standard, role_endpoint, aftercare_served, continuity): 753 tests OK, 40 skipped.
* mypy: src/core, src/api (PYTHONPATH core+agents), src/agents all no issues.
* ruff format --isolated --line-length 100 --check on 25 changed infra files and the 215 stabilization test: pass. ruff check on infra: 27 findings, equal to the prior recorded baseline (35 on main), none added by this merge.
* test_scenario_manifest and test_needs_inventory: 19 OK.

## Not run (remaining, FULL tier)

* `rpi-checks.py --all` and receipt verification (coordinator, heavy lock); full core and API suites; employee-chat browser harness and the other browser/MSSQL groups (prerequisites); agents and infra test suites; hosted CI; independent review.
