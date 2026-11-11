<!-- markdownlint-disable-file -->
# Plan: aftercare blank stored state (issue 1402, C1 of 3)

Research: [research](../../research/2026-11-11/aftercare-blank-state-1402-1111-research.md). Details: [details](../../details/2026-11-11/aftercare-blank-state-1402-1111-details.md). Prospective plan, committed before implementation.

## Scope

* Source: `src/core/src/zava_forward/core/aftercare_intake.py`, `_parse` only.
* Tests: `src/core/tests/test_aftercare_intake.py` only.
* Out: numeric ordering and its tests, adapters, SQL, API, docs, formatting of other code.

## Phases

* [ ] Phase 1: failing regression tests (RED), raw output retained under `.copilot-tracking/evidence/2026-11-11/aftercare-blank-state-1402-1111/`.
* [ ] Phase 2: one-line `_parse` fix (GREEN) and affected validation.
* [ ] Phase 3: changes record, one critique, one review, state, handoff.

## Validation (focused, owner demo policy)

* `test_aftercare_intake.py` and `src/api` `test_aftercare_screen.py` (no SQL). Per critique CK-01, `test_aftercare_store.py` and `test_aftercare_served.py` reference SQL stores, the adapter path cannot reach the changed branch, and SQL is not admitted, so they are not run: N/A, recorded.
* Each blank-state path (read, write, HTTP, restart) is an independent test method with a bytes assertion (CK-02).
* Ruff check and format check, mypy for the two changed files with existing project configs.
* No blanket gate, no SQL, no cloud, no installs.
