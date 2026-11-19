# Changes: issue 1830 live r2

Status: complete, tier FOCUSED (tools and docs only; no `src/` change; no gate file edit).

## Files

* Added `tools/rpi-preflight.py`, `tools/rpi-gate-timing.py`, `tools/test_rpi_preflight.py`, `tools/test_rpi_gate_timing.py`, `docs/reference/method/rpi-gate-preflight.md` from `a2c27fda6` (two ISC004 lint fixes in the preflight test).
* Edited `docs/reference/README.md` (index) and appended `docs/reference/log.md`.
* Added `docs/reference/research/issue-1830-live-r2-tools-2026-11-18.md`.

## Validation

* `python3 -m unittest tools.test_rpi_preflight tools.test_rpi_gate_timing -q`: 54 tests OK.
* `ruff check` and `ruff format --isolated --line-length 100 --check` on the four Python files: pass.
* mypy: not applicable (not a `src/<project>`). rpi-checks.py not run. `/tmp/ama-rpi-heavy.lock` was free but the full gate is not required for this tier.
* Preflight refusal demonstrated live (rc 5); analyzer run on four retained receipts.

## Per-criterion table

| # | Criterion | State | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Measured wall time, queue wait, per-command and group timing and critical path from multiple comparable retained receipts; high-cost, repeated and redundant checks; mandatory versus optimizable | Partly proven | The analyzer now exists in this branch and reproduces wall, concurrency, critical chain, longest commands and setup cost for four retained full receipts. Not proven: queue (lock) wait is absent from receipts; no pair shares head and base, so none is comparable; the 16 November receipt is gone; no redundancy or mandatory-versus-candidate conclusion is evidenced |
| 2 | Change-specific preflight with exact selectors, rejects zero-test and invalid paths, keeps SQL and browser prerequisites, non-receipt label; catches #1297 320px regression; reruns #1828 map check | Unproven | The preflight carries the non-receipt label but refuses every selected unit, browser and SQL run (rc 5), so it cannot catch the 320px regression or rerun the map check. Needs an owner-chosen trust boundary and FULL-tier source work, not provable for the demo |
| 3 | Focused tests and documentation for the preflight; benchmark method with before/after when an optimization is implemented; no mandatory group removed or control loosened | Partly proven | 54 tests pass; the method page is restored; no gate file is touched. No optimization was implemented, so no before/after pair exists |
| 4 | Dated RPI research, plan, details, changes, original review on an isolated branch; impact classified; selected tier run; independent exact-head review; hosted CI | Partly proven | Dated artifacts exist in `.copilot-tracking/` of this isolated worktree; impact classified focused (tools and docs only); focused tier run. Independent exact-head review and hosted CI need a pull request, which was not opened |

No criterion can be ticked.
