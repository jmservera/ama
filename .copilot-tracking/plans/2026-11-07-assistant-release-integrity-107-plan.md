# Plan: assistant release integrity regression (#107)

Task `assistant-release-integrity-107`. Research: [research](../research/2026-11-07-assistant-release-integrity-107-research.md). Details: [details](../details/2026-11-07-assistant-release-integrity-107-details.md). Critique: [critique](../plans/2026-11-07-assistant-release-integrity-107-critique.md).

## Decisions

* Do not redo merged admission, attestation-denial, revocation or metering code.
* Add only the missing combined regression for C10 (independent workers, revocation, restart, finite allowance).
* Never manufacture attestation, approval or real-platform evidence; SQLite is not SQL Server acceptance.
* No production change, push, PR, issue edit, provider call or heavy gate.

## Phases

* [x] Phase 1: add `test_racing_workers_and_restart_after_revocation_keep_allowance_and_make_no_call` to `src/api/tests/test_assistant_release.py`.
* [x] Phase 2: run focused API tests, ruff check, record evidence.
* [x] Phase 3: single critique, single review, freeze the candidate in a conforming commit.

## Gates

FULL tier is required for the release; it is NOT run here and publication is NOT READY until the coordinator admits the gate.
