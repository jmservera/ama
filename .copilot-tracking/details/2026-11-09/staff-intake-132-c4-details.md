<!-- markdownlint-disable-file -->
# Details C4: intake integrity corrections (#132)

## C4-P1 Red tests (`src/api/tests/test_staff_intake_api.py`, `test_staff_intake_browser.py`)

* Add a `digest()` helper and pass the explicit digest in all capture calls.
* `test_independent_qa_accepts_and_contributors_denied`: capture (sam), correct, acknowledge (pam); then `accept_quality` as `quil` succeeds with ZF-3 synthetic resident acceptance, scope and design; sam, pam and a worker-name actor are denied through the real path (`PermissionError` or `ValueError` from `_independent`, not the resident gate). Record `resident_binding == dict(measure, context_revision=1)`.
* `test_replacement_after_acceptance`: after acceptance a new capture with a new ref and current digest supersedes the accepted record.
* `test_unbound_or_changed_scope_rejected`: remove the binding revision or bump scope revision, capture returns 409 with nothing written.
* `test_correction_updates_current_quality_item`: after correct, `rec.items` evidence for the label equals the latest correction, `original_notes` unchanged, two corrections keep history, latest wins, restart readback, other items untouched. Failure injection after the item mutation leaves neither item nor correction changed.
* `test_digest_required_and_validated`: missing, empty, non-string and malformed digests return 400 with no record; a valid replay with a missing digest after a recorded capture still returns duplicate; offline capture with an old digest after a design or scope change returns 409.
* Browser `test_lost_response_retry_reconciles`: route the first capture response to abort after the server commits, click submit again on the same form, expect a status message, the receipt, the acknowledgement button, one record, no error text.

## C4-P2 `staff_intake.py`

* `DIGEST = re.compile(r"[0-9a-f]{64}")`.
* `capture`: build `probe` receipt with the current digest only for validation and replay matching; replay returns duplicate. For new evidence require `body["pack_digest"]` to be a string matching `DIGEST` (ValueError, 400), then stale compare to the current pack (409), then `pack["ready"]`, then `_binding(c, w, measure)`, then `submit_quality(..., context_revision=rev, field_receipt=dict(probe, pack_digest=supplied))`.
* `_binding(c, w, measure)`: read `w["versions"][-1]["resident_bindings"]`, find the measure, compare to `resident_decisions.current_context(c, measure)["revision"]`; missing or unequal raises `IntakeError(409, ...)` naming the contract manager as next step. No waiver.
* `correct`: after validating, set the matching `rec["items"]` entry evidence to the note in the same operation before `store.save()`.

## C4-P3 `staff-intake.js`

* Module `let intakeNotice = ""`; capture task sets it on duplicate and clears it otherwise; `intakeOrder` renders `h("p", { role: "status", "aria-live": "polite" })` when set, and the render clears it after painting. No throw on duplicate. Keep native controls and textual status.

## C4-P4 Validation commands

Run from `src/api/tests` with the venv and `PYTHONPATH=../../core/tests:../../agents/tests`. Impacted set: `test_staff_intake_api`, `test_role_endpoint_inventory`, `test_content_standard`, `test_procurement_api`, `test_procurement_screens`, `test_role_screens`, `test_role_screens_conformance`; core `test_job_pack`, `test_quality_procurement`. Then SQLite (default), MSSQL via `/tmp/zf132-mssql-run.sh`, browser via `flock -n` after holder inspection.

## C4-P5 Docs and handoff

Update the core and API README staff-intake sections, the C4 changes record, one Review, the C4 state file, a local commit, and the external handoff `handoff-132-c4-intake-integrity-1109.md`. Counter 4 of 5.

## Critique dispositions applied (see critique)

* Replay matches the stored receipt first (its own measure, labels, worker, notes) before current-pack validation.
* `_binding` returns 409 when `current_context` is None or the revision differs.
* Unbound receipts show an explicit review blocker in the view.
* Independence tests: one fresh Submitted record per contributor (pam recorder, quil corrector, pam acknowledger) asserting the independence message, then separate acceptance by an independent quality identity and a replacement.
* JS notice keyed by order with an always-present `role="status"` region filled after paint.
