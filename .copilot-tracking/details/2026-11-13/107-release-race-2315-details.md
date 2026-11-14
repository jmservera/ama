<!-- markdownlint-disable-file -->
# Details: Issue #107 release record, serving attestation, race tests

## P1 `src/core/.../rai_release.py`

* `missing_contract` also checks: `scope` equals the registry task `scope`; `evaluation_summary` is an object with `evaluation_version == EVALUATION_VERSION`, `decision == "Pass"`, a named `summary`, and `evidence_digest == digest(evidence)`; `consumption` has integer `max_calls` and `max_tokens` >= 1, `alert_threshold_percent` 1..100 and a named `alert_contact`.
* `changed_triggers`: a record `scope` that differs from the registry scope is an `intended_use` change.
* `attest_serving(record, returned)` returns `{expected, returned, outcome}`; outcome `matched`, `mismatch` or `unattested` (missing or unverified returned model).

## P2 `assistant_release.record`

* Copies `scope`, `evaluation_summary`, `consumption` from the body; validation by `missing_contract`.
* `src/core/README.md` documents the new fields and attestation wording.

## P3 `assistants.complete`

* Uses `attest_serving`; always stores `serving_attestation` (with `at`); non-match quarantines, suspends the release, emits a `serving-attestation` event and sets `fallback = {route: manual, release: suspended, reason}`.

## P4 Tests

* `src/core/tests/test_rai_release.py`: new field validation and `attest_serving`.
* `src/api/tests/test_assistant_release.py`: persisted binding round trip; matched attestation recorded; unattested model quarantines with fallback and event; in-flight concurrent revocation (second connection while the provider call is blocked), restart denial and re-enable only by a new human record; mismatch suspension survives restart and re-installing the old binding does not revive it.
