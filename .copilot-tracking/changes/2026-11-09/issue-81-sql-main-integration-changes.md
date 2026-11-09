# Issue 81 SQL main integration changes, 2026-11-09

Refs #81 only. Plan: `.copilot-tracking/plans/2026-11-09/issue-81-sql-main-integration-plan.md`.

## Changes

* Merge commit `4b7349907f1f9aa6536f73b47977f9be8c04bd8c` (tree `3715d09347957fb31300871e67fb62e85a0794a7`): normal `--no-ff` merge of `origin/main` `8d6f029cac004506953f36606862168bbe9d9412` (#1308 squash) into `edc78a19e`. PR #1240 head `6ef6dc368` remains an ancestor. No rebase, reset or force.
* One conflict, `src/core/tests/test_resident_decisions.py`: kept this branch's `seed_extra_cases` helper and its dedicated test header, and made the helper call main's `reseed`, so the MSSQL class gets an owned database. The MSSQL `seed_extra_cases` override (merge_seed) is unchanged. `store.py` and core README auto-merged; main's order-unresolved view logic and this branch's resident-decision logic coexist.
* No other source edits. No defect found, so no correction cycle consumed or reset.

## Checks (owner demo-targeted tier; venv `/mnt/ama-gates/g81-sqlmain-AdOXBg/venv`, editable installs verified bound to this worktree; logs there; all exit 0)

* Non-SQL core: test_gates 20; test_resident_decisions 308 (110 skip); test_priority_order 142 (65 skip); test_quality_procurement 136; test_hazard_referral 41 (1 skip); test_handoff_lifecycle 20; test_grant_lifecycle_controls 44 (16 skip); test_sqlstore 18; test_sqlreads 15; test_sqlqueues 14; test_taskqueues 21.
* API: test_auth 41; role_matrix 13; hazard_api 4; handoff_api 7; grant_lifecycle_api 2 (1 skip); resident_api 20 (1 skip); entra_authoritative 36; role_endpoint_inventory 22; case_journey 31.
* ruff check, ruff format --check, mypy (276 files) clean.
* Real SQL: one `flock -n /tmp/ama-rpi-heavy.lock` admission (acquired first time), one owned loopback container `ama81-sqlmain-3001523-667` (labelled, port 38108, generated password, manifest guard accepted), SQL Server 2022 image `cf8f0ab2...`, removed on exit, no leftover databases. Results (`ZF_RESIDENT_MSSQL=1`): test_resident_decisions 308 (3 skip); test_priority_order 142 (0 skip); test_sqlstore 18; test_sqlreads 15; test_sqlqueues 14; test_taskqueues 21; test_ranking_publication 37; test_quality_procurement 136; test_grant_lifecycle_controls 44 (16 skip); test_hazard_referral 41 (1 skip); test_handoff_lifecycle 20. Every producer exit 0.
* Not run: `rpi-checks --all`, browser harness, hosted CI, deploy, model calls, live or private data.
