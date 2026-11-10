# Issue 81 forward preparation details, 2026-11-09

Plan: `.copilot-tracking/plans/2026-11-09/issue-81-forward-preparation-plan.md`.

## P1 merge

```bash
git merge --no-ff 9f9aacc8be6a1b0e9a10efd367d1ea8bd7520939
```

Expected conflict: `docs/architecture/cutover-evidence-pack.md` only. Resolution: keep main's added sections and this branch's added sections (append-only). Verification: `git diff <parent> -- <file>` for each parent shows additions only (no deleted lines from either side); no conflict markers. Commit message `Merge origin/main 9f9aacc8 into the issue 81 recovery branch` with the Copilot trailer, local author and committer `8036360+jmservera@users.noreply.github.com`.

## P2 selectors (once, scratch venv owned by this run, worktree-bound imports)

From `src/core/tests` with `python -m unittest`: `test_gates`, `test_resident_decisions` (SQL opt-in skips expected), `test_quality_procurement`, `test_hazard_referral`, `test_handoff_lifecycle`, plus the api auth/role and manual-path selectors present in `src/api/tests` that import the changed core modules. Also `ruff check`, `ruff format --check` and `mypy` on changed paths. No SQL, no `rpi-checks --all`.

## P3 prospective final #1292 integration (to execute only after #1292 is on main)

1. `git fetch origin`, confirm PR #1308 squash is an ancestor of `origin/main`.
2. `git merge --no-ff <exact origin/main SHA>`.
3. Expected conflicts: `src/core/src/zava_forward/core/store.py`, `src/core/tests/test_resident_decisions.py`, `src/core/README.md`. Reconcile preserving both intents (priority ordering, SQL index bootstrap serialisation, and this branch's resident-decision, gate and hold semantics); stop on any unresolved intent conflict.
4. Run owned disposable SQL Server (admission lock free) selectors: `test_resident_decisions`, `test_priority_order`, `test_sqlstore`, `test_sqlreads`, `test_sqlqueues`, `test_taskqueues`, ranking and quality SQL selectors, `ZF_RESIDENT_MSSQL=1 ZF_SQL_AUTH=password ZF_SQL_TRUST_CERT=1`.
5. Fresh independent exact-head review and hosted CI.
