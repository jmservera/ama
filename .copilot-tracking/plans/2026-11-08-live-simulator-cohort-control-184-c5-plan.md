---
title: "#184 C5 plan: enforce the 14-day maximum in the shared reader decision"
ms.date: 2026-11-08
---

Details: [details](../details/2026-11-08-live-simulator-cohort-control-184-c5-details.md).

* [ ] 1. Commit research and plan/details before any source or test edit.
* [ ] 2. Red: add tests to src/api/tests/test_live_control.py, run them against the unchanged source, keep the raw failing output and exit.
* [ ] 3. Green: change only `decide` in live_control.py (INVALID outcome); update the live_control docstring and src/api/README.md sentence if they describe reader behaviour.
* [ ] 4. Re-run the relevant unit tests, Ruff lint and format, and mypy with --cache-dir=/tmp/mypy-184, each with separate output and exit files.
* [ ] 5. Write changes and one original Review; commit only issue files.
* [ ] 6. Return frozen HEAD/tree and source hashes; full gate stays pending for the coordinator.
