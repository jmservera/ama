# Changes: issue 1840 live2 (rebase and self-test fix)

Refs #1840. Base origin/main e91b6fa81. Focused validation; `rpi-checks.py --all` not run (owner brief).

## Changes

* Cherry-picked 2d4538e69 onto origin/main; conflicts resolved keeping both sides (see research). Candidate tracking files are `issue-1840-live-run2-*`; main's earlier `issue-1840-live-*` files are unchanged except the state file, which carries this run's state because the witness path is fixed by the brief.
* `src/api/checks/old_image_sql_probe.py`: `ISOLATED_LAUNCHER` and `SubprocessEngine.run` now start the worker as `python -I -B -c <launcher> <paths> <worker> <spec>`, so `-I` isolation stays while the parent's import path is passed explicitly. Note: this src edit was made before the `implement-start` witness call (the changes file did not yet exist); the witness is observational and the order is recorded here honestly.
* Docs: README index and log entries kept; note `docs/reference/research/old-image-incomplete-completion-1840.md` updated.

## Validation

* Before fix (rebased tree): `unittest tests.test_old_image_sql_probe` 41 tests, 1 failure (SelfTest, `ModuleNotFoundError` under `-I`).
* After fix: 41 tests OK, 0 skips; self-test ACCEPTED (lower fidelity).
* `PYTHONPATH=../core/src:../agents/src python3 -m mypy` from `src/api`: no issues in 351 files.
* `ruff format --isolated --line-length 100 --check` and `ruff check` on the three files: pass.
* Full `src/api` discover run hit the 590 s cap with no summary (inconclusive, not a pass); not repeated. Scenario manifest SHA unchanged: no browser check touched.
* FULL tier (src changed, security-sensitive diagnostic) not satisfied: no external full receipt.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Failing-first regressions | Proven (fixture) | Six subcases failed before the candidate fix, pass now. |
| Incomplete completion yields INSUFFICIENT | Proven (fixture) | `test_incomplete_mismatch_completion_with_an_active_mutated_row_is_insufficient`. |
| Preserve positive control, late restoration, active-MUTATED, identities, adverse precedence | Proven (fixture) | All 41 tests pass. |
| Affected tests, strict typing, counts and skips recorded | Proven | See validation; 0 skips. |
| Independent exact-head review, justified tier | Unproven | Own review only; external review and full receipt remain. |

Azure: not used (offline judge; demo apps do not run it). No throwaway resource. No screenshots (not applicable).
