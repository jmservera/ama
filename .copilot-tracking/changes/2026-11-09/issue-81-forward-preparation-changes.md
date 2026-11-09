# Issue 81 forward preparation changes, 2026-11-09

Refs #81 only. Plan: `.copilot-tracking/plans/2026-11-09/issue-81-forward-preparation-plan.md`.

## Changes

* Commit `397d6fefc`: research, plan, details and critique, committed before any change.
* Commit `b18141b19`: normal merge of `origin/main` `9f9aacc8be6a1b0e9a10efd367d1ea8bd7520939` into `05ec1a7e`. Only `docs/architecture/cutover-evidence-pack.md` conflicted (single append hunk); both appended sections kept, main's newer `ms.date` retained. This branch's source is unchanged versus the previous merge; main's sensor and live files arrive unmodified. No #1292 (PR #1308) content imported.
* Ancestry after merge: `6ef6dc36` (PR #1240 head), `05ec1a7e` and `origin/main` are all ancestors of the merge. Publication would be a fast-forward of `feat/controlled-lifecycle-integration-81` (coordinator only; not done).

## Owner demo-targeted checks

Scratch venv `/mnt/ama-gates/g81-fwdprep-5oFR1J/venv` (owned, mktemp; logs in the same directory); editable installs verified bound to this worktree's `src/` paths.

| Command (from `src/core/tests`: `python -m unittest <module>`) | Result |
| --- | --- |
| test_gates | 20 OK |
| test_resident_decisions | 308 run, 110 skipped (SQL opt-in), OK |
| test_quality_procurement | 136 OK |
| test_hazard_referral | 41 run, 1 skip, OK |
| test_handoff_lifecycle | 20 OK |
| test_grant_lifecycle_controls | 44 run, 16 skips, OK |

From `src/api` with `PYTHONPATH=../core/tests:../agents/tests` (discover `-p <module>.py`): test_auth 41 OK; test_role_matrix 13 OK; test_hazard_api 4 OK; test_handoff_api 7 OK; test_grant_lifecycle_api 2 run 1 skip; test_resident_api 20 run 1 skip; test_entra_authoritative 36 OK; test_role_endpoint_inventory 22 OK. All exit 0. `ruff check` clean, `ruff format --check src/core` 221 files clean, `mypy src` (core) 131 files clean.

The earlier `/mnt/ama-gates/g81-recovery-1109/venv` holds stale non-editable copies and was not used.

## Not run (deferred, not green)

Owned SQL (resident decisions, ranking, quality, priority order), browser, hosted CI, `rpi-checks --all`, deploy, model calls. #1292 is not on main.
