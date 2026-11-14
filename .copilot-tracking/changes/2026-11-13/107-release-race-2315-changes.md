<!-- markdownlint-disable-file -->
# Changes: Issue #107 release record, serving attestation, race tests

* Plan: [107-release-race-2315-plan.md](../../plans/2026-11-13/107-release-race-2315-plan.md)
* Base: `origin/main` `3033dc9c21e57c7f86eca3882fffaf7e9a025033`

## Modified

* `src/core/src/zava_forward/core/rai_release.py`: `scope`, `frozen_evaluation`, `valid_consumption` checks in `missing_contract`; scope joins the `intended_use` trigger; new `attest_serving`.
* `src/core/src/zava_forward/core/assistant_release.py`: `record` persists `scope`, `evaluation_summary`, `consumption`.
* `src/core/src/zava_forward/core/assistants.py`: `complete` always stores `serving_attestation` (expected, returned, outcome, `at`); a non-match quarantines, suspends the release, writes a `serving-attestation` event on the release and the task, and sets `fallback`.
* `src/core/README.md`: documents the extended record and attestation behaviour.
* `src/core/tests/release_support.py`, `src/core/tests/test_rai_release.py`: fixtures and unit tests for the new fields and `attest_serving`.
* `src/api/tests/test_assistant_release.py`: persisted-binding round trip with revocation, refusal of unfrozen/unbounded records, matched attestation, unattested quarantine with fallback surviving restart and re-enabled only by a new record, revocation by a second connection while generation is blocked, then restart and new-record re-enable.

## Divergences and amendments

* The request names `src/core` and `src/agents`; the assistant service tests live in `src/api/tests`, so the race tests were added there. `src/agents` is unchanged and its suite was run unchanged.
* Older stored records lacking the new fields now fail closed (intended; documented).
* Not touched: `infra/`, `monitoring_coverage.py`, `ranking_publish.py`. No #107 criterion is ticked; live Azure acceptance, a named approver and independent control-plane attestation remain unmet.
