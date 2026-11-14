<!-- markdownlint-disable-file -->
# Review: Epic 165 importer seed round-trip (2026-11-14)

Execution: executed once. Outcome: conformant with caveats. Boundary: the new test file only.

## Findings

* No blocking findings. The test asserts importer behaviour already present and adds no production code.
* Caveat (environmental, routed to a later task): `tests/test_version.py` errors unless `zava-forward-import` is pip-installed; unrelated to this change.
* Caveat: fixtures assert synthetic archetype fields only, not EPC or PAS 2035 compliance, consistent with the fabric label.
* Independent exact-head review, human approval and hosted CI remain outstanding; unchecked.

## Follow-ups

1. Install the importer in the dev environment so the full discovery runs clean.
2. Extend the round-trip to the refusal ledger (`submit_file`) for malformed synthetic workbooks.
