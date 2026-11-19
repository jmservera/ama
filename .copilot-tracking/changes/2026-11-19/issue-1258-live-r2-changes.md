# Changes r2: issue 1258 (2026-11-19)

Source changes: none. Tier: not FULL; `rpi-checks.py --all` not run.

| Criterion | Status | Basis |
| --- | --- | --- |
| Pre-created archive or sync new ancestors before confirming | Proven (already ticked) | ranking publication tests, 110 OK |
| Post-link sync failure follows audited `committed_unconfirmed` | Proven (already ticked) | same run |
| Syscall-order regression for missing nested ancestors | Proven (already ticked) | same run; pre-fix failure not re-demonstrated |
| Retry, private-stage, audit, 409/503, original-date behavior intact | Proven (already ticked) | same run |
| Original RPI, FULL receipt, independent exact-head review, hosted checks | Unproven | FULL receipt barred; review and hosted CI need a human and a push; mocks do not prove real crash durability |

Commands (from `src/core`):

* `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_ranking_publication*.py" -q`: Ran 110 tests, OK.
* `python3 -m mypy`: 22 errors in 3 files; `ruff format --isolated --line-length 100 --check src`: 35 files would be reformatted. No source file changed here, so these are pre-existing and not attributable to this candidate; not investigated.

Outcome: every remaining criterion is production-only or needs a human; stop.
