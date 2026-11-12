# Issue 115 scheduler trace plan (2026-11-12, 1112)

Research: [.copilot-tracking/research/2026-11-12/issue-115-scheduler-trace-1112-research.md](../research/2026-11-12/issue-115-scheduler-trace-1112-research.md). Details: [.copilot-tracking/details/2026-11-12/issue-115-scheduler-trace-1112-details.md](../details/2026-11-12/issue-115-scheduler-trace-1112-details.md). Refs #115 only; no closing keyword.

## Phases

* [ ] Phase 1: failing-first tests. Add to `src/orchestrator/tests/test_digest_blob.py` cases where `open_store` fails and where the store read raises a non-`DocumentStoreError`; each expects exit 1, `ALERT_MARKER`, no `OK_MARKER`, and no exception text beyond the type name. Add one marker-binding case that reads the `LEDGER_DIGEST_*` strings in the compiled `infra/main.bicep` ledger alert queries (static test in `infra/tests/test_bicep_policy.py`).
* [ ] Phase 2: smallest fix in `digest_blob.main()`: wrap store open, publish and verify so any `Exception` prints `ALERT_MARKER` with the exception type name only and returns 1. `SystemExit` and `KeyboardInterrupt` pass through. Existing exit codes and markers unchanged.
* [ ] Phase 3: update `src/orchestrator/README.md` ledger section by one sentence; run focused tests, ruff and mypy as configured; changes record; original Review.

## Boundaries

No Bicep, workflow, retention, lock, hosted or acceptance claims. Focused validation tier.
