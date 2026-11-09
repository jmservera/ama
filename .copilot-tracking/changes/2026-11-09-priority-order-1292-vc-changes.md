<!-- markdownlint-disable-file -->
# Changes: issue 1292 validation correction (2026-11-09)

Plan: [plan](../plans/2026-11-09-priority-order-1292-vc-plan.md). Research: [research](../research/2026-11-09-priority-order-1292-vc-research.md). Critique: [critique](../plans/2026-11-09-priority-order-1292-vc-critique.md). Cycle 5 of 5 (default budget; C1-C4 used on 2026-11-08; the 2026-11-09 recovery made no source change; the owner's additional grant was not invoked).

## Identities

* Frozen start `f4d7b3d5d8c8137c765b6b823b936bcd2860a819` (tree `2885028de9c57c4911e8cbbc7d063a7e8ebb3157`).
* Fresh main named by the coordinator `9814cf6b236be1f2e86c4401973b8e834be927bc`; fetched `origin/main` `76db469b1` differs only by the rubric score file. Local merge commit `ba8c3a51cecba0123aa47f3b02964d4368fbc5ad` (tree `0258ec36c8410fedc09fe84f41509e4a80a022c2`) is the tested base of the source edits; `src/core` and `src/agents` are byte-identical between the frozen start and it. All control and corrected runs are against these identities, not a rebase.

## Source changes (test fixtures only, three files)

* `src/core/tests/test_resident_decisions.py`: `JsonResidentDecisions.reseed(data, name)`; `MssqlResidentControls.create_owned_database()` (UUID database, name bound per closure, cleanup registered before `CREATE DATABASE` and guarded by `DB_ID`) and a `reseed` override creating a fresh owned database; the one test calls `reseed`. No assertion, expected value, skip or production file changed.
* `src/core/tests/test_priority_order.py`: `# type: ignore[assignment]` on the fake-adapter `conn.driver` assignment (found by the pinned whole-package `mypy`, which the recovery had not run).
* `src/core/README.md`: one sentence recording that a test supplying its own seed gets a second owned database.
* Environment only: `.venv` gained the API dev extra (`playwright==1.64.0`, `ruff==0.17.1`, `mypy==2.4.0`) via `pip install -e "src/api[dev]"`; no uv, global install or application edit.

Process disclosure: the fix was first drafted during reproduction (kept at `evidence-1292-vc/draft-fix.patch` in the session files), reverted before the research, plan, details and critique were written, then re-applied from the critiqued plan with the critique's two cleanup changes. Nothing else was reverted.

## Evidence (outputs preserved outside the repo in the coordinator session `files/evidence-1292-vc/`)

Owned SQL Server 2022 (`16.0.4305.5`, image `sha256:cf8f0ab2ebe6...`), labelled `zf.task=1292-sql-disposable`, loopback only, random port, manifest written by `sqlguard.write_manifest` and admitted by the real `docker inspect` path. Nonqueued `flock -n /tmp/ama-rpi-heavy.lock` was refused while a foreign session held it (PID 2565848, confirmed in `/proc/locks`; not interrupted or inspected); a later fresh attempt was admitted. Container removed on exit; leftover `zf_resident88_*`/`zf_priority1292_*` databases: none; the foreign `zf-1288-e1-sql` container was not touched.

| Check | Result |
| --- | --- |
| Control, selector `MssqlResidentControls.test_challenge_edited_in_case_outside_generation_candidates`, `9814cf6` source and tests | exit 1, `AssertionError: 4 != 40` |
| Same, frozen-start-equivalent source (`ba8c3a51` archive, identical `src/core`) | exit 1, `4 != 40` |
| Same selector, corrected tree, 10 fresh runs | 10/10 exit 0, 1 test each, 0 skips |
| `test_resident_decisions.MssqlResidentControls` (whole class, corrected) | 91 run, OK, 1 skipped (`JSON file rollback only`; structurally inapplicable to SQL, executes in `JsonResidentDecisions`) |
| `test_priority_order` on SQL Server (`ZF_RESIDENT_MSSQL=1`) | 93 run, OK, 0 skipped (199 s) |
| Original two resident selectors (`..._source_exact_dependency_manifest_and_original_reviews`, `..._failed_priority_accept_edit_remove_disposition_and_audit`) x10 | 20/20 exit 0 |
| `test_priority_order` + `test_resident_decisions`, no SQL Server | 349 run, OK, 112 skipped (the opt-in `Mssql*` classes, covered by the rows above, plus the one JSON-only skip) |
| `src/api` discover (README command), after restoring the dev extra | 2031 run, OK, 363 skipped, 0 errors (frozen-head run: 1994 run, 7 errors, 365 skips; all 7 were `No module named 'playwright'`) |
| The 7 formerly failing API modules (`PYTHONPATH=tests:../core/tests:../agents/tests`) | 44 run, OK |
| Impacted API modules (ai_tasks, coordinator_api, resident_api, continuity, continuity_epoch_export, ranking_policy, case_journey), verbose | 248 run, OK, 47 skipped, all opt-in (44 owned-MSSQL classes in `test_continuity_epoch_export` and `test_coordinator_api`, 3 Chromium journey/browser); not selected, not run on SQL Server here, therefore unproven on SQL |
| ruff 0.17.1 `check .` and `format --check .` (core, api) | clean (218 and 121 files) |
| mypy 2.4.0 `mypy` whole package, core | clean, 271 source files (one error before the type-ignore) |
| Import provenance | `sqlstore`, `mssqlstore`, `resident_decisions`, `test_resident_decisions` import from this worktree `src/core` (editable install); control runs print their archive paths and SHA-256 in `*.imports.txt` |

Scope classification: selected and required to pass with 0 skips on SQL: `test_priority_order` (93) and the corrected resident selector plus the two original selectors; the whole resident MSSQL class has one structural JSON-only skip, disclosed. API broad-suite skips (363) are opt-in browser, live or MSSQL classes not selected for this tier and are reported, not waived.
