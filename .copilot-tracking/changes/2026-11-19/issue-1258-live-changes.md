# Changes: issue 1258 live (2026-11-19)

Source changes: none. Tier: not FULL (no src change). `rpi-checks.py --all` not run, per brief.

| Criterion | Status | Basis |
| --- | --- | --- |
| Pre-created archive or sync new ancestors before confirming | Proven (already ticked) | `_confirmed` in `ranking_publication.py` syncs held folder and parents |
| Post-link sync failure follows audited `committed_unconfirmed` | Proven (already ticked) | `test_ranking_publication.py`; 110 targeted tests OK |
| Syscall-order regression for missing nested ancestors | Proven (already ticked) | same test run; pre-fix failure not re-demonstrated here |
| Retry, private-stage, audit, 409/503, original-date behavior intact | Proven (already ticked) | same test run |
| Original RPI, FULL receipt, independent exact-head review, hosted checks | Unproven | FULL receipt barred by brief; independent review and hosted CI need a human and a push; mocks do not prove real crash durability |

Command: `cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_ranking_publication*.py" -q` gave `Ran 110 tests, OK`.

Outcome: every remaining criterion is production-only or needs a human; stop.
