# Plan: #360 correction1 (Blob credential binding and operation budget)

* Task ID: demo-transport-blob-360-correction1; parent task demo-transport-blob-360
* Date: 2026-10-22. Research: `.copilot-tracking/research/2026-10-22/demo-transport-blob-360-correction1-research.md`

## Executive Summary

Two blocking review findings on head 829890010f69 are corrected offline. The Blob client will authenticate with the same selected operator profile as ARM (including the isolated fallback profile) instead of an ambient credential chain, and every Blob list/download will run under explicit socket/retry limits plus a bounded overall budget so a stall cannot prevent job and roster-secret cleanup. Nothing live is run; all live acceptance remains unverified.

## User Decisions and Requirements

* Blob must use the same explicit operator context as ARM; no ambient chain (review finding 1; earlier PC-004).
* Explicit connection/read/retry limits and a bounded total operation budget; preserve bounded cleanup (finding 2).
* Test real client construction incl. fallback profile, slow/failing operations and cleanup; never print tokens.
* Keep complete results, fail-closed integrity, private Blob MI, no truncation, no PII logs, no invented attestation.
* No Azure/tenant action, no role change, no merge, no closing keywords; no edits while a gate runs; one uniquely named gate; preserve prior outputs.

## Goals

* Close both findings with tested code and updated docs/evidence.

## Scope and Non-Goals

* In: `infra/scripts/staff_azure.py`, `infra/scripts/staff_blob.py`, `infra/tests/test_staff_azure.py`, `infra/README.md` note, evidence/log entries, tracking.
* Out: worker changes, Bicep/RBAC, live runs, web files, gate-hash changes unless drift appears.

## Functional Requirements

* FR1 `default_container(url, cli)` builds `ContainerClient` with a credential that obtains tokens only via `cli.call` (selected profile environment).
* FR2 Client sets explicit `connection_timeout`, `read_timeout`, `retry_total`.
* FR3 `preflight` and `read_result` accept a monotonic deadline and enforce it for the whole operation (list plus all downloads); expiry raises `StaffJobError` with unverified wording.
* FR4 Execute passes a preflight budget (before job creation) and a read budget bounded by the job deadline; cleanup still runs.

## Non-Functional Requirements

* No token or secret in output, errors or tests; generic errors; daemon worker threads; read-only operations.

## Acceptance Criteria

* AC1 Test constructs the real client via the real `Azure` fallback profile (patched subprocess) and asserts AZURE_CONFIG_DIR is the selected profile and the credential is the profile adapter, not DefaultAzureCredential.
* AC2 Tests: stalled list in preflight, stalled download in read, failing token acquisition, all raise `StaffJobError` within the budget and, for the read case, job delete/cleanup still completes.
* AC3 Full infra tests, ruff, mypy pass; full gate with unique output dir; receipt verified; pushed to PR #423.

## Phase Checklist

* [x] P01 Credential binding
* [x] P02 Operation budget
* [x] P03 Tests, docs, validation, gate

## Critique Disposition

Critique: `.copilot-tracking/reviews/plans/2026-10-22/demo-transport-blob-360-correction1-plan-critique.md`, verdict Revise, executed once; all findings applied directly, none needed a user decision.

* PC-001 applied: token is primed eagerly under a temporary bounded `cli.deadline` before preflight and cached; the adapter never mutates `cli.deadline`; later refresh runs in the bounded call.
* PC-002 applied: preflight timeout keeps the "no job was created" wording; read timeout uses "outcome is unverified".
* PC-003 applied: accept `expires_on` int or naive-local `expiresOn`; anything else fails closed with a generic error raised `from None`.
* PC-004 applied: the `default_container` patch becomes `lambda url, cli`; budgets are module constants read at call time; fake-clock tests keep working because the deadline is checked against `time.monotonic` once before the call; stall tests release threads with an Event.
* PC-005 applied: tests call `get_token` through the real `Azure` fallback profile (patched `subprocess.run`), assert `AZURE_CONFIG_DIR`, assert `DefaultAzureCredential` is never constructed, and assert `execute` passes the transport.
* PC-006 applied: budget is `min(job deadline, now+budget)`; no remaining budget raises immediately; a read timeout is terminal (no retry loop) and cleanup runs.

## Follow-Up Items

* Live token acquisition for storage data plane from the operator profile, real size, live data actions: unchanged live prerequisites.
