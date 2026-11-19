# Research: issue 114 live run 162131Z

Refs #114. Disposition: executed (re-run of tests, gap search). Planning Readiness: Ready.

* First unticked criterion: per-year audit and ledger digest verification proven by test before reliance.
* Prior evidence: docs/reference/research/issue-114-live-reverify-2026-11-18.md (62 tests OK).
* Gap search: `verify_ledger_before_reliance` is tested in `test_recovery.py`, `test_sqlstore.py` (including `MssqlStore` at line 338). Per-year, sealed-digest, tamper, drop, swap, corrupt and blob-anchor paths all have tests. No buildable code or test gap found.
* Remaining gap is deployment-only: the deployed API image predates `verify_ledger_before_reliance` and live data holds one year. An image roll and a `VIEW LEDGER CONTENT` identity are outside the owner decisions of 2026-11-18.
* Fresh run, from `src/core`, base 46920a0dd: `PYTHONPATH=src:tests python3 -m unittest test_recovery test_sqlstore test_ledger_digest_blob -q` gave 62 tests OK in 37.5 s.
* Critique (single pass, compatible): no source change warranted; record the result and stop. No Azure resource was created.
