<!-- markdownlint-disable-file -->

# Implementation Plan: demo-transport-blob-360

| Field | Value |
|---|---|
| Task ID / slug | demo-transport-blob-360 |
| Date | 2026-10-22 |
| Parent | demo-transport-plan-360-recovery (preserved) |
| Research | .copilot-tracking/research/2026-10-22/demo-transport-blob-360-research.md |
| Details | .copilot-tracking/details/2026-10-22/demo-transport-blob-360-phase-details.md |
| Changes | .copilot-tracking/changes/2026-10-22/demo-transport-blob-360-changes.md |

## Executive Summary

Replace the ARM-tag and console result paths for the in-VNet SQL staff job with a private Blob result: the worker writes AEAD-encrypted, paged, run-bound results to a dedicated private container with its managed identity; the controller reads and strictly validates them with Entra credentials from a private-connected host and refuses anything corrupt, incomplete, ambiguous, expired or unreachable. Everything is implemented and tested offline with fake clients. Nothing is deployed, granted or run. Live acceptance (private routing, role grants, a real run, Entra role acceptance, signed attestation, screen-reader acceptance) stays unproved and listed as prerequisites.

## User Decisions and Requirements

* DN1: private Blob with managed identity; no tags for results; keep backing services private; no public Blob, SAS or shared key.
* DN2: complete results; measure real size; bounded paging if needed; no silent truncation or reduction of housing stock.
* DN3: three old failures remain unknown historical transport failures; retire old demo code paths; validate Blob independently; production root-cause is follow-up; no Front Door or Azure resource deletion.
* DN4: production roles assigned manually via Entra Enterprise App; demo may match demo-tenant users to sensible roles from actual evidence, else random; admin-prefixed account stays ProgrammeManager; never directory-admin roles; never overwrite immutable bindings; app roles remain authorization source; assignment is not competence or real authority. Collect no names, UPNs or object IDs.
* DN5: controlled demo worker checks accepted; independent signed source/image attestation unverified and deferred.
* Offline implementation only; no Azure charges, deployment, tenant mutation or grants until the coordinator releases a verified plan. USD700 all-in October ceiling retained with 2026-10-25T16:02Z expiry; worker126 supplies costs.
* Reuse existing helpers and `src` packages; surface errors; keep manual paths; no parser relaxation or silent fallback to console or tags.
* Rebase run-owned branch on fresh main; lease push; update draft PR #423; leave #360 open without closing keywords; do not merge.
* Run the full `tools/rpi-checks.py --all` gate and verify the receipt before push.

## Goals

* G1 Private Blob result transport implemented offline with strict validation.
* G2 Old tag/console demo result code and tests retired.
* G3 Infra definitions (container, lifecycle, scoped role) as reviewable Bicep, not applied.
* G4 Design revision and precise live prerequisites documented.

## Scope and Non-Goals

* In scope: infra scripts, tests, Bicep, README design, evidence pack, KB log and index entry, tracking.
* Non-goals: deployment, role writes, web changes, deleting resources, reading private datasets, changing production role assignment code.

## Functional Requirements

* FR1 Worker publishes pages to `staff-results/<run>/page-NNN.json` through managed identity only.
* FR2 Controller reads exactly the named run, validates and returns a complete result or raises `StaffJobError`.
* FR3 Pages carry version, run, operation, input digest, image digest, schema, index, count, totals, created, not-after; AEAD associated data covers them.
* FR4 Page size bounded; page count bounded; total bytes recorded; refusal on any excess instead of truncation.
* FR5 Unreachable, corrupt, missing, extra, duplicate, expired or ambiguous Blob state is an explicit error; no fallback.
* FR6 Discovery verifies storage account is private, shared-key off, anonymous off, container exists and private.

## Non-Functional Requirements

* NFR1 No secrets, names, UPNs, object IDs or roster content in logs, tests or artifacts.
* NFR2 Python 3.12 style matches the repository; ruff passes.
* NFR3 Offline tests use fake clients only.

## Acceptance Criteria

* AC1 New and updated unit tests pass, including boundary, tamper, replay, expiry, extra-blob, missing-page, unreachable and size tests.
* AC2 `grep` finds no tag/console result code in `infra/scripts`.
* AC3 Bicep builds if `bicep` is available; otherwise recorded as NOT RUN with the existing text-contract tests passing.
* AC4 Full `tools/rpi-checks.py --all` gate and receipt verification pass or any failure is reported.
* AC5 PR #423 body lists implemented versus NOT RUN and live prerequisites.

## Phase Checklist

* [ ] P01 Blob transport module and worker/controller wiring
* [ ] P02 Bicep, tests and retirement of tag path
* [ ] P03 Design revision, evidence pack, KB entries
* [ ] P04 Validation, gate, push

## Critique Disposition

One critique executed (verdict Revise, 11 findings, all planner-applicable, no user decision): .copilot-tracking/reviews/plans/2026-10-22/demo-transport-blob-360-plan-critique.md. No second critique runs.

| ID | Disposition | Applied as |
|---|---|---|
| PC-001 | Accepted | Research corrected; controller preflights Blob list access before creating any job; unreachable read after run is "unverified, rerun" (P01-T02) |
| PC-002 | Accepted | P02-T04 adds `.dockerignore`, `rpi-checks.py` and CI lint list updates for the new module |
| PC-003 | Accepted | P01-T04 validates account URL `https://<name>.blob.core.windows.net`, name matches ARM-verified account, container fixed |
| PC-004 | Accepted | P01-T01 reader/writer rules: fixed `<run>/` prefix, name grammar and count bound, size checked from listing before download, read only after Succeeded, no-overwrite writes, explicit credential, no retries, skew-aware not-after |
| PC-005 | Accepted | Ceiling stated as fail-closed (64 pages); real size measurement is a live prerequisite |
| PC-006 | Accepted | `includeResultBlob` defaults false; operator Reader role and ARM read named as prerequisites; container-before-role ordering; residual account-wide Contributor overwrite risk documented |
| PC-007 | Accepted | New container appended after existing six; guard test on indexes; lifecycle deletes versions and blobs; soft-delete 30-day retention documented |
| PC-008 | Accepted | Retire `ZF_STAFF_RELAY`, `relay` payload field, `TAG_VERSION`, chunk codecs; AC2 grep pattern `tags_url|result_tags|ZFSTAFF|ZF_STAFF_RELAY|TAG_VERSION|Microsoft.Resources/tags` over `infra/scripts` and Bicep |
| PC-009 | Accepted | `StaffJobError` defined in `staff_blob`, re-exported by `staff_azure`; worker imports only `staff_blob`; import test |
| PC-010 | Accepted | AC1 test list extended: FR6 properties, failed job skips read, worker write failure prints no detail, run-prefix confusion |
| PC-011 | Accepted | P03-T01 cites existing role-assignment tests as the DN4 evidence; no code change |

## Follow-Up Items

* FU1 Production root-cause of the historical transport failures.
* FU2 Independent signed image/source attestation.
* FU3 Screen-reader acceptance of the demo.
* FU4 Live private-route test after coordinator release.
