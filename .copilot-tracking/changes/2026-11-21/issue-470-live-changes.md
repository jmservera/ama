# Changes: issue 470 gate scan count

Status: implemented. Tier: full (gate semantics); the coordinator owns the gate run.

## Source changes

* `tools/rpi-checks.py` `verify_results`: expected case journey scans 87 to 91. Strictness unchanged (exact count, no page errors, no serious or critical violations, zoom and axe identity).
* `tools/test_rpi_checks.py`: fixture `range(91)`; negative cases 90, 92 and 91 with a serious violation.

## Validation

* `python3 tools/test_rpi_checks.py`: 118 tests OK.
* `ruff check` on both files: 20 findings, identical before and after (pre-existing, not touched). `ruff format --isolated --line-length 100 --check`: clean. No type changes, so mypy was not re-run.
* Receipt `g2061/run10/case-journey-results.json` (read-only): 91 scans, 91 distinct states, 0 serious or critical, 0 scans with any violation, no page errors, no "skipped", axe 4.10.3, zoom correct.
* No other hard-coded scan totals found in `tools/`, `src/api/checks/` or the scenario manifest.

## Gate plan (coordinator)

`python3 tools/rpi-checks.py --all --base <current-origin-main-sha> --out <new-external-dir>`, then `--verify-receipt`. Not run here.

## Acceptance criteria, issue 470

| Criterion | Status | Evidence |
| --- | --- | --- |
| `--changed` selects groups, records scope | Proven (already ticked) | Ticked in issue; unchanged by this edit |
| `--verify-receipt` rejects partial receipt | Proven (already ticked) | Ticked; `test_rpi_checks.py` passes |
| `--jobs` parallel groups, single lock | Proven (already ticked) | Ticked; unchanged |
| Measured full-run time before and after recorded in the PR | Unproven | Needs a PR and full gate runs; this task may not open a PR or run `--all`. Run10 timings are adverse evidence from a failing gate and not a before/after pair |
| Tests for group selection and receipt scope | Proven (already ticked) | 118 tests OK |

No live Azure or browser proof applies: the change is gate tooling only.
