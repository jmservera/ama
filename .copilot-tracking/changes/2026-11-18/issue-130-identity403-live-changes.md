# Changes: issue 130 identity 403 (2026-11-18)

Refs #130. Tier FULL (src security control); `rpi-checks.py --all` not run by instruction; not pushed; not deployed.

## Process note (adverse, preserved)

Source and test edits and the validation runs happened before the plan, details, critique and this changes file were persisted, and before the `implement-start` witness call. The `plan-done` witness was recorded after the plan files existed but after the source edit; `implement-start` is therefore recorded late. A first artifact write also overwrote the brief-mandated state file path; the earlier content is in Git at `HEAD` for `issue-130-live`.

## Files

* `src/core/src/zava_forward/core/resident_decisions.py`: `_same_signed_in_person` replaces the whole-dict comparison in `_operation`.
* `src/core/tests/test_resident_decisions.py`: helper `roster_bound_principal` and three tests (accepted, forged refused, differing roster person refused); imports `identity`.
* `docs/reference/research/issue-130-identity-403-live-2026-11-18.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

| Command | Result |
| --- | --- |
| `PYTHONPATH=src:tests python3 -m unittest tests.test_resident_decisions -q` (src/core) | 458 tests OK, 162 skipped (SQL Server only) |
| Before the fix: new positive test, JSON and SQLite | Failed with the 403 PermissionError (bug reproduced) |
| Mutation: comparison disabled (`if False and ...`), then restored | 2 refusal-test failures; restored code passes |
| Mutation on the original code (bare `_person` call) | 449 tests still passed, showing the check was untested |
| `python3 -m mypy` in src/core / src/api (`PYTHONPATH=../core/src:../agents/src`) | No issues (396 / 347 files) |
| `ruff check` and `ruff format --isolated --line-length 100 --check` on touched Python | Clean |
| `python3 -m unittest discover -s tests -p "test_*nomin*.py"` (src/api) | 14 OK |
| Not run | `rpi-checks.py --all`, hosted CI, SQL Server tests, browser checks (no web files changed), live redeploy |

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Original account, source, channel kept | Ticked, unchanged | Existing tests; resident suite passes |
| Acknowledged route and named owner before review | Ticked, unchanged | Resident suite passes |
| Challenge or correction with evidence, reviewer, outcome | Ticked, unchanged | Resident suite passes |
| Correction re-reviews dependents | Ticked, unchanged | Resident suite passes |
| Hazard routes to #85 | Ticked, unchanged | Hazard test in resident suite passes |
| Non-response never lowers priority; unknown not none | Ticked, unchanged | Resident suite passes |
| Tests cover wrong identity, limited representative authority, manual route | Strengthened | New identity tests; the identity check was previously untested (mutation probe) |
| RAI items except the last two | Ticked, unchanged | Not re-proven live; the fix is not deployed |
| Representative participation and comprehension need authorized human evidence | Unproven | Synthetic demo; owner excluded person-run testing and DPO/Legal approval; constructed checks cannot pass this gate |

Live Entra 403 re-probe was not repeated: the same revision and image were probed in earlier runs, no fix is deployable under this task, so the live outcome after the fix is unproven.
