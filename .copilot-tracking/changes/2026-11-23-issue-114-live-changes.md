# Changes: issue 114 live re-verification (2026-11-23)

Status: complete. Refs #114. Tier: focused (test and documentation only, no src change; rpi-checks --all not run).

## Edits

* src/core/tests/test_recovery.py: added `test_unsealed_single_year_run_writes_no_digest_and_report_carries_no_entry_content`.
* docs/reference/research/issue-114-live-reverify-2026-11-23.md plus folder (probe.py, probe-job.log, local-tests.txt).
* docs/reference/README.md index row; docs/reference/log.md entry.

## Validation

* `tests.test_recovery tests.test_sqlstore tests.test_ledger_digest_blob` from src/core: 63 tests OK. `ruff check` on the test file passes.
* Live: throwaway job `job-114-reverify` Succeeded, deleted, no 114 job remains. Hosted CI not observed (nothing pushed).

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Per-year audit and ledger digest verification proven by test before reliance | Proven by tests and on live data (one year, 7,022 entries intact); gate absent from the orchestrator image, API image undetermined | local-tests.txt, probe-job.log |
| Measured load, latency and cost against PRD targets | Unproven in this run (not re-measured); earlier retained evidence stands | note, section Per-criterion status |
| Backup, restore and deletion re-application (DH-005) | Unproven in this run (drills not authorised); earlier evidence stands | note, section Per-criterion status |

No tick is changed; all three were already ticked and closure stays with the owner.
