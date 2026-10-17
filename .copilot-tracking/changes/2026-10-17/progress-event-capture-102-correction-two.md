<!-- markdownlint-disable-file -->
# Concrete Correction TWO: progress-event-capture-102

Date 2026-10-17. LAST authorized defect cycle. Same retained session.
Input: independent reviewer7ebc1f9d-17ae-4eb8-ac76-c66c89a0e10c, Revise,
one Medium on published7fda223a. Original RV-001/RV-002 and critique
dispositions independently verified closed; this receipt is not a new Review
or self-awarded final-head acceptance.

## Reproduction and Root Cause

Existing test_documents.StoreDocumentTests.
test_storage_outage_writes_no_metadata_and_is_audited failed: expected
upload_document_failed/upload_document_rejected, observed neither. The shared
controlled scope correctly rolled back failed state/success audit, but also
removed the upload's early failure entry. operation only caught validation/
authority/conflict exceptions, so DocumentStoreError left no replacement.

Failing-first command selected the unchanged document test and new actual
JSON/SQLite upload/storage-outage and scanner-error/recovery tests:

```bash
PYTHONPATH=src/core/tests .venv/bin/python -m unittest \
  test_documents.StoreDocumentTests.test_storage_outage_writes_no_metadata_and_is_audited \
  test_progress_event_capture.JsonCapture.test_upload_outage_preserves_prior_audit_and_truthful_failures_after_reload \
  test_progress_event_capture.SqliteCapture.test_upload_outage_preserves_prior_audit_and_truthful_failures_after_reload \
  test_progress_event_capture.JsonCapture.test_operational_rejection_preserves_original_error_and_no_success_on_recovery_failure \
  test_progress_event_capture.SqliteCapture.test_operational_rejection_preserves_original_error_and_no_success_on_recovery_failure -q
```

Five tests, six subtest failures and one error. Existing failure reproduced
without weakening its two-entry assertion. JSON recovery also replaced the
original operational error with a restoration RuntimeError.

## Bounded Implementation

Move storage-failure audit generation out of the rolled-back upload body into
operation's post-rollback exception handling. For the existing DocumentStoreError
and upload action, emit upload_document_failed then upload_document_rejected.
Generic operational exceptions retain rejection with the established safe
generic reason and exception class, never supplied filename/bytes/source/
transport diagnostic. Existing validation reasons remain unchanged.

No failed success audit is restored. SQL prior pending prefix survives recovery,
then only the truthful failure/rejection is queued. JSON audit tail rollback
still restores the prior signed prefix before new failure evidence.
CommittedOutcomeError is explicitly excluded from rejection, unchanged.

JSON restoration, failure-audit and orphan-object cleanup errors log explicitly
and annotate the original exception rather than replacing it. SQL lock-exit
already retains the original error and adds its existing diagnostic note.
No broad swallow or success-shaped fallback: all original operations still
raise and uncertainty remains explicit.

Four added semantic methods in the existing owned capture harness (18 methods
total, plus one existing HTTP test within the24-method bound):
actual storage outage with committed/pending prefix, zero metadata/history,
failure/rejection order, private diagnostic exclusion, durable reload and
ledger integrity; generic scanner failure with failed recovery and cleanup;
failed audit retains original storage error; actual SQL document COMMIT then
failed acknowledgement retains one document/history/success and no rejection/
cleanup. Existing ten-operation event COMMIT/retry/restart matrix retained.

Existing failed-recovery pending-queue expectation now explicitly includes the
truthful handoff_accepted_rejected on metadata-backed generic errors, while
retaining prior prefix and all no-success assertions. This is the requested
operational rejection contract restoration, not weakened error assertions.

## Executed Evidence on Sensor Main943febc2

Local document/provenance/JSON/SQLite first post-fix pass55 tests. An initial
local run correctly failed the old pending-only expectation after rejection
was restored; updated only that intentional contract assertion. Final static
checks core/API Ruff/check-format/mypy pass118/55 typed source files.

Full core:

```bash
cd src/core
../../.venv/bin/python -m unittest discover -s tests -q
```

Initial full run874 tests,819 pass,55 skips,244.299s. Final full run after the
last added document post-COMMIT test:876 tests,820 pass,56 explicit skips,
238.184s, exit0. No exit137, partial/full-pass conflation or omitted failure.

Actual own loopback MSSQL: verified SELECT1, ran private helper selector
test_progress_event_capture.MssqlCapture and
test_progress_report_api.MssqlProgressApi:29 passed,53.530s. Includes new
outage/recovery/audit-failure/document COMMIT tests plus existing exact-once
event/audit/retry/restart. Immediately stopped progress102-8f7a5abbc2.
No other container used. Private credentials/helper config not committed.

Final focused runtime command:

```bash
PYTHONPATH=src/api:src/core/tests:src/api/tests:src/agents/tests \
  .venv/bin/python -m unittest test_documents test_change_provenance \
  test_progress_event_capture.JsonCapture test_progress_event_capture.SqliteCapture \
  test_progress_report_api test_document_controls test_chat_isolation test_ai_tasks \
  test_sensor_privacy test_sensor_backfill test_sensor_stock test_sensor_faults -q
```

213 run,200 pass,13 explicit skips,106.012s. Includes sensor status/document/
chat/map pre-dispatch/current-generator admission and report/export boundaries.
Existing sensor fixture ResourceWarnings recorded, not failures.

## Corrected Installed-Source Image

Built progress-event-capture-102:correction2:
sha256:b89d7cf466d21f694ea0648f85fa2a9a9edfe39a473f5aee4d9b800705e766b4.
src/check-container.py passes hardened non-root controls/negative probes and
compatible loopback startup. Same image, read-only root, UID/GID10001, no
capabilities and no-new-privileges, mounted tests read-only:94 run,92 pass,
two explicit skips,13.668s, for documents/provenance/JSON/SQLite/progress API/
sensor privacy. Seven installed event/sensor core module SHA256 hashes match.

Initial image invocation forced ZF_AI=off and therefore two sensor tests
expecting mocked outbound calls failed (one failure/one error). Reran same
selection with workflow-only override unset; all transports remain existing
test mocks/offline.invalid, no paid/live AI. Corrected receipt above is actual,
not an assertion weakening. No image source patch needed.

## New Main Integration Required Before Publication

After final verification, remote main advanced to
bcb4871b19c2abd56e1ff536a77c15e52b544321, independently merged resident #392.
Owner already authorized own-topic rebase if main moved, exact old remote lease
7fda223a50fedfca16fcc2cb89dd01405862e829. Inspecting merged sources only, not
another worktree: resident writer validation/COMMIT markers overlap SqlStore
save, Store detail, workflows and docs. Preserve all upstream resident controls
and the correction; integrate after committing this retained correction.
Combined resident/event/document checks and justified actual SQL follow.
Evidence above is pre-integration, not prematurely claimed final-base proof.

Original adverse Review, critique and correction ONE remain byte-identical.
No third defect cycle, repeated Review, main write, merge or issue closure.

## Actual Resident-Main Integration and Final Validation

Committed correction first at0b2cd588, then performed the already-authorized
own-topic rebase onto bcb4871b19c2abd56e1ff536a77c15e52b544321.
Textual conflicts were append-only KB log and SqlStore's early-discard guard.
Retained BOTH resident_validation and change_validation exclusions; upstream
resident writer validation and resident mark_committed hook remain unchanged.
Store detail, commitment-preserving handoff and all resident response/remedy
independent clocks auto-merged. No third defect correction or invented approval.

All twelve owned src added/removed deltas exactly match before/after respective
bases, combined SHA256
264696a1d621868d06ecce3445fb0b0ee546d7a6226981a69b2c9f2ac18d5d1e.
All nonoverlap resident src exactly equal new main. Entire upstream KB index/
log byte prefixes preserved. Original Review, critique and correction ONE
byte-identical. Replayed correction/source headb0e2d02f6d981e83fa0c11cb3b3c38491bd89bbe.

Fresh combined selector:

```bash
PYTHONPATH=src/api:src/core/tests:src/api/tests:src/agents/tests \
  .venv/bin/python -m unittest test_documents test_change_provenance \
  test_progress_event_capture.JsonCapture test_progress_event_capture.SqliteCapture \
  test_resident_decisions test_handoff_lifecycle test_quality_procurement \
  test_hazard_referral test_progress_report_api test_resident_api \
  test_document_controls test_sensor_privacy -q
```

349 run,294 pass,55 explicit skips,126.002s. Core/API configured Ruff/
format/mypy pass118/55 source files, no weakened assertion or source rewrite.

Because shared SQL validation scopes now coexist, restarted only own SQL and
verified SELECT1. Actual MSSQL event/document/HTTP classes above plus six
resident writer/reassignment/concurrent/failure-recovery/post-COMMIT methods:
35 passed,80.162s. ZF_RESIDENT_MSSQL=1 selects the six existing explicit methods,
not a SQLite proxy. Own SQL stopped immediately and inspected Exited.

Rebuilt final integrated image
sha256:c1f989b49d4d12decadeb0084cb7c544d9344b23827caf69262027a1dadaf3f5.
Existing checker passes hardened non-root controls, negative probes and
compatible loopback startup. Same installed-source document/provenance/event/
HTTP/sensor selection:94 run,92 pass,two explicit skips,13.040s. No live model
endpoint/credentials or communications.

Full FINAL integrated core command above:942 run,847 pass,95 explicit skips,
237.990s, exit0. Includes upstream resident tests and unchanged original
document regression. SQL opt-ins intentionally disabled for full local run;
35 actual SQL cases are a separate executed selector, not skipped evidence.
Prior876 full-core and pre-integration SQL29/image results remain separately
labelled rather than promoted to the final base.

Final publication uses ONLY own-topic force-with-lease at exact expected remote
7fda223a50fedfca16fcc2cb89dd01405862e829 for the authorized rebase.
PR #394 body records correction TWO and final base/commands; issue #102 stays
open pending independent final gate. Final exact pushed head verified outside
this self-referential receipt and returned in handoff. No more defect cycles.
