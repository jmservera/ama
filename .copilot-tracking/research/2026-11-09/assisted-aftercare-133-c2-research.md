# Research: assisted aftercare 133 corrective cycle C2 (Refs #133)

Activated 2026-11-09T23:03:42Z (`date -u`). Disposition: executed (new evidence: independent Functional findings). Parent task: `assisted-aftercare-133-stagea` at head `ad6deceb1`.

## Evidence read

* Coordinator findings `independent-133-aftercare-stagea-1109/functional-findings.json` (5b5b490f), metadata and read ledger: verdict approve_with_comments, four Medium, no tests executed by the reviewer, publication not authorised.
* Full web guidelines refreshed 2026-11-09 from the source URL: 8055 bytes, byte-identical to the coordinator copy `web-guidelines-132-133-review-1109.md`. The earlier 6000-character fetch qualification stays recorded for Stage A.
* Code re-read at the cited lines: `aftercare_intake.py` `record_concern`, `_assisted_errors`, `_date`, `add_sensor_context`, `FileStateStore.update`; `aftercare.py` `_context`, `_fraction`, `evaluator_view`; `aftercare.js` `aftercareSubmit`, `aftercareErrorMessage`, `aftercareEvaluatorView`; both test files.

## Findings confirmed against code (all four reproduce by reading)

1. F1 `aftercare.js`: network failure, empty reply, and 503 all read "Nothing was saved". A reply can be lost after the commit, and a 503 can also follow an unconfirmed write, so the claim is unsupported. The test asserts the phrase for network, server and empty.
2. F2 `aftercare.js`: `totals.concerns_unresolved` is `{count, denominator}` (`_fraction`), rendered through `acText` as `[object Object]`. The test fixture supplies scalar `1`.
3. F3 `aftercare_intake.py`: `_assisted_errors` applies `next_update >= today` before the idempotency lookup, so an exact retry after the date passes returns 400, not the stored receipt.
4. F4 `aftercare_intake.py`: `add_sensor_context` hands arbitrary keys and values to the register, whose `_context` only checks string type and the neutral-text phrases. No privacy guard or length cap, so an email or phone can persist.

## Design facts

* A raised `ValidationError` inside the `StateStore.update` mutator leaves the file untouched (write happens after the mutator returns), so time validation can move inside the transaction safely.
* The existing guard is `_redact` plus `_free_text` (cap plus flagged kinds; messages name the kind, never echo the value).
* `api` tests can import `zava_forward.core` (api depends on core), so node tests can use real service payloads produced in Python and passed to node.
* Hook contract (routes, statuses, store `update`, shared-file items) is unaffected: no route, status or shape change. `handle` 400 for refused sensor context already exists.

## Planning Readiness

Ready. No unresolved decision. Residual risk: the privacy guard is best effort and is not a privacy proof; stated in tests and docs.

## Not in scope

Shared hooks, `app.js` `api()` errors copy, served/browser/SQL checks, evaluator role, DPO basis, whole C1-C6.
