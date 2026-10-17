<!-- markdownlint-disable-file -->
# RPI Changes: controlled-bulk-preview-78

Task 78, 2026-10-17. Scope: full corrected plan P01/P02.
Plan: .copilot-tracking/plans/2026-10-17/controlled-bulk-preview-78-plan.md.
Details: .copilot-tracking/details/2026-10-17/controlled-bulk-preview-78-phase-details.md.
Critique: one execution, Revise, six direct dispositions applied.

## P01-T01: Core implementation

Complete. Added bulk_edits.py with strict closed-field request validation,
server-owned previews, exact ordered changes/failures/outcomes, current
creator/registered staff/OID and owner/note rights, source/version/reason,
whole-case SHA-256 and SQL rowversion snapshots. Canonical issuance digest and
consumption anchored independently in immutable audit. Returned response is
deep-copied; mutable request/document and ABA/replay corruption tests pass.

Two thin Store wrappers call module functions rather than adding a new mixin;
this is local implementation judgment, not a field/authority change. SQL adds
one checked document and a commit-time validation hook inside existing save,
including current governance snapshot. All-case writes/history, audit and
terminal result commit together. Bulk-scoped exception recovery restores cases,
pending success events and all shared docs, including absence. Faults exercise
first-row, document, queue, audit, before-commit and lost-acknowledgement paths.

New tests contain deterministic two-store interleavings for competing applies
(including all-no-op), role revocation between preparation and transactional
validation, guardrail change, stale/ABA, reopen, immutable provenance equality
and every controlled category. Source/version/time/reason and monotonic case
edit history are retained; redaction explicitly removes nested history text
for viewers without existing need. Ownership/decisions remain unchanged.

## P02: API and delivery

Complete after P01. Added exact preview/apply routes, existing authentication
and CSRF, role-inventory entries, metadata-only rejected role/malformed input
audit and explicit storage-failure 503 with uncertain-outcome recovery wording.
Actual loopback HTTP tests check responsive health, exact shape, zero preapply
mutation, batch blocking, source history, replay, controlled fields, creator,
cached password/proxy revocation, OID rebinding and authenticated claim limits.

Updated component docs, existing UX synthesis, index and append-only KB log.
Full FR-005 acceptance remains partial for preexisting evidence-upload and
handoff-transfer operations outside the new bounded edit path; no closure
claim. No UI/source assets changed and no browser/conformance claim.

PR #377 remains open (head observed 7e1dbdd95f5b7abb0124cba0bee8b9a27146475a).
Actual overlap: shared DOCS tuple, thin Store wrappers, projection history
redaction, server routes, route inventory, component guides/pyproject and KB.
Changes are additive and forms.py/routes remain untouched; no dependency,
merge, rebase or nested delivery assumed.

## Validation

System Python could not import zava_forward. Created own .venv and installed
editable core/agents/api and declared dev extras. No private datasets/cloud.

* Fail-before core: 25 tests, 2 failures/91 subtest errors, missing bulk methods
  and missing rejection audit; expected nonzero verified before implementation.
* Fail-before API: 5 tests failed with missing routes; health helper initially
  used wrong path/JSON assumption, corrected to actual text `/healthz`.
* New core/API contracts: 37 tests passed before final additional HTTP case.
  Final new core count 32; final API count 6, all passed in focused selections.
* Broader targeted selection: 172 attempted, 171 passed and one loader error
  (`tests.test_mvp` namespace missing in invocation of test_mssqlstore).
  Corrected PYTHONPATH to include src/api and reran only that module:
  51 tests, 3 passed/48 opt-in live SQL Server skipped, no live connection.
* Final new contracts + sqlqueues/handoff HTTP: 54 passed. Existing handoff
  fixture emits expected unavailable-law-store diagnostics; no rule approval
  or passed rule-engine claim is inferred.
* Final API and complete role inventory after malformed/storage-failure case:
  25 passed (6 new HTTP plus 19 role inventory checks).
* Existing core `ruff check .`, `ruff format --check .`, `mypy`: pass,
  51 formatted and 104 typechecked source files. API equivalent: pass,
  18 formatted and 48 typechecked files. Typed new modules/tests retain strict
  checking; narrowly scoped untyped-call overrides match existing Store boundary.
* `git diff --check`: pass. Added documentation links reviewed against exact
  paths/heading anchors. KB log only appended; memory/original untouched.
* No full test suite, cloud/Azure/paid model/Docker/private dataset used.

## Criterion Evidence

| Criterion | Evidence | Boundary |
| --- | --- | --- |
| Edits retain source/version/actor/time/reason | test_exact_preview_before_apply_and_provenance_reopens, exact hash-chain event/history equality, monotonic versions and projected history | New closed-field path; broader preexisting FR-005 remains partial |
| Targets/change/failure/outcome before apply | mixed missing/foreign/valid, no-op/mixed-no-op, closed/inactive and actual HTTP exact-shape tests | Backend API only, no new UI acceptance |
| No controlled approvals | All controlled categories and unknown/nested keys rejected, ownership/decisions/commitments unchanged, actor/OID/guardrail concurrency checks | Fictional local exercise, not operational approval |

## Review Handoff

Ready. Full plan markers and details synchronized, critique executed once and
six direct dispositions complete, no implementation blockers. Perform exactly
one post-implementation Review. Route any findings forward; do not repeat
implementation/Review in this task. Then privacy-safe commit, push and main PR
with Refs #78, exact criterion evidence and explicit outstanding boundaries.
