# Research: issue 1258 criterion triage (2026-11-19)

Task: issue-1258-live. Refs #1258. Mode automatic. Source changes: none.

## Findings

* Issue #1258 has four ticked criteria and one unticked: complete original RPI, current FULL receipt/verification, independent exact-head review and hosted checks.
* Code check: `src/core/src/zava_forward/core/ranking_publication.py` `_confirmed` (lines 342-355) syncs the held archive folder and parent folders; `_publish_held` calls it after the link. Regression tests exist in `src/core/tests/test_ranking_publication.py`.
* Local run, `src/core`: `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_ranking_publication*.py" -q` gave `Ran 110 tests ... OK`.
* The unticked criterion has no buildable code or test part. FULL receipt is forbidden by the owner brief (`rpi-checks.py --all` not to be run); independent exact-head review and hosted checks need a human and a push. No live Azure proof applies (filesystem durability, no demo resource involved).

## Planning readiness

Ready: record the per-criterion table and stop.
