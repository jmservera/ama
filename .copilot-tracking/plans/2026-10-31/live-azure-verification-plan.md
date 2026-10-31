<!-- markdownlint-disable-file -->
# RPI Plan: Live Azure verification

## Task Metadata

* Task ID: 3a44be57-db3a-46d1-b9e4-fe82bd7c74e7
* Task slug: live-azure-verification
* Plan date: 2026-10-31
* Planning status: Ready; one critique completed and disposed
* Phase details: .copilot-tracking/details/2026-10-31/live-azure-verification-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-31/live-azure-verification-plan-critique.md

## Executive Summary

Execute bounded real-browser checks on the two owner-named deployed apps,
reuse the employee acceptance adapter, and supplement it with fresh asset,
capacity, resident geometry and metering observations. Publish only sanitized
evidence; missing identity/financial authority blocks the affected test, not
unrelated checks. No application or Azure configuration changes are planned.

### What You May Not Know

The employee adapter requires independent immutable tenant/object expectations.
Resident check mains create local fixtures and cannot be used as live drivers.
Fresh browser assets do not prove every historic cache or a controlled cold
start. One advisory reply cannot prove billing reconciliation or metering joins.

### Unresolved Decisions or Blockers

Runtime directory attestation and full local gate availability must be measured.
No bypass, fixture identity substitution or cloud fallback is authorized.

## User Decisions and Requirements

* Run research, plan, implement and review with dated tracking artifacts.
* Live checks authorized using ~/.ama-test-user and ~/.ama-resident-test-user only inside automation; never print/log/commit credentials; at most two sign-ins per account.
* Check both supplied Azure apps, allowing scale-from-zero delay; no config, replica, job or deployment changes.
* Verify employee chat/tabbed first-load/assets, resident chat dock/resize, #523/#524 capacity/assets, #570 identity and #432 metering.
* Record observations in the existing evidence pack and issue comments. Tick only proven criteria; close only all-ticked issues; file reproducible new bugs.
* Use pip only. Commit with requested Copilot trailer, non-forced push and main-targeted Refs PR.

## Goals

* Establish precisely what this deployed release demonstrably supports.
* Preserve adverse evidence and leave unproven acceptance/human gates explicit.

## Scope and Non-Goals

* In scope: dated evidence, one supplemental capture-free live driver, issue updates, local gate and publication.
* Non-goals: source product fixes, Azure writes, load tests, controlled scaling, callback bookings, real-resident content, economic batches or cost estimates.

## Functional Requirements

* Warm health endpoints with bounded network timeouts; fresh ephemeral Chromium contexts, no trace/video/HAR/session saves or console bodies.
* Read credentials internally; resolve expected employee tenant/object from independent directory or independently supplied expectations, never /api/me; increment attempts before credential submission, never retry beyond two.
* Invoke checks.employee_acceptance_check.verify_employee only after strict identity admission.
* Observe first successful navigation assets before manual reload; hash public JS/CSS and compare local tracked sources. Do not cache-bust or route/mock live responses.
* Check capacity APIs and rendered data/empty state without writes; resident open/close/dock/resize without booking or consent changes.
* Read /api/ai/report and project coverage/cost/field-presence only, never raw case/model content.
* Record failures and blockers separately; update issue bodies conservatively, comment each target, create deduplicated reproduction bugs.

## Non-Functional Requirements

* Secrets and case text never leave automation memory. Fixed observations, paths, hashes, statuses, counts and geometry only.
* Fresh contexts; no persistent profile or historical session reuse. Maximum two sign-in attempts/account across all scripts in this task.
* Network and browser watchdogs; no hidden retries of credential submissions.
* Final clean exact-HEAD full gate, external receipt verification, independent exact-head assessment, normal hosted/human approvals.

## Acceptance Criteria

* Each requested surface has dated observed pass/fail/blocked evidence and a reproducible command.
* Existing acceptance logic is actually used, not replaced by weaker HTTP/selection predicates.
* Issue criteria retain source/live/financial distinctions and all original historical results.
* Full RPI artifacts, independent critique and one original Review are committed with documentation.
* Publication only after required full gate/receipt and independent assessment; main PR uses Refs, no closing keywords.

## Implementation Context Record

| Context | Record |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-31/live-azure-verification-research.md (executed, Ready) |
| Plan | .copilot-tracking/plans/2026-10-31/live-azure-verification-plan.md |
| Details | .copilot-tracking/details/2026-10-31/live-azure-verification-phase-details.md |
| Changes | .copilot-tracking/changes/2026-10-31/live-azure-verification-changes.md (implementation-owned) |
| Continuation | Explicit full-loop automatic parent |

## Sources

* Research C1-C5 and W1-W2; target issue bodies fetched 2026-10-31.
* src/api/README.md employee identity and resident live boundaries.
* src/README.md local-rpi-gate; repository final-candidate instruction takes precedence over partial-tier alternatives.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Execute live verification

* Intent: direct bounded observations.
* Dependencies: critique disposition; installed namespace projects and Chromium.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Prepare safe driver and run bounded checks

* Evidence: employee adapter C3, resident fixture boundary C4, manager routes C5.
* Expected: sanitized dated JSON and automation; every requested result explicit.

<!-- rpi:phase id=P02 -->
### [x] P02: Record and reconcile evidence

* Dependencies: P01 observations.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update documentation and GitHub issues

* Expected: evidence pack/index/log, four issue comments, only proven checkbox changes, deduplicated bug reports.

<!-- rpi:phase id=P03 -->
### [ ] P03: Review and publish

* Dependencies: P02, reconciled artifacts.

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Independent Review, commit, full gate and Refs PR

* Expected: original Review preserved; clean exact-HEAD gate, verified external receipt, independent exact-head assessment, normal push and main PR.

## Dependencies

* Independent identity: no expected-ID inference from admitted /api/me.
* Live financial data/authority: only inspect accessible report; no batch or spend assumption.
* Local prerequisites: install missing dependencies with pip; no npm/uv.

## Critique Disposition

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Rejected: unsupported runtime restriction | Critique asserted a /tmp/external-write prohibition absent from parent runtime instructions. Parent explicitly permits external scratch/venv/receipts; unchanged gate remains mandatory and actual failures will be recorded. No gate bypass or source patch. |
| PC-002 | Applied directly | Sole driver checkpoints pre-submit counters in its result JSON; exclusive lock, interrupted-run refusal and no reset |
| PC-003 | Applied directly | Exact origin table and recognized auth redirect boundary in details |
| PC-004 | Applied directly | Semantic observation matrix in details |

Critique execution Complete, original verdict Revise preserved. No second
critique. Compatible findings applied; the alleged PC-001 runtime blocker
is not supported by this parent's actual instructions.

## Test Ownership Lock

* Existing product tests: no edits/removals; exact removals none.
* Maximum additions: one dated live driver plus one sanitized result JSON; no product test files.
* Canonical targets: evidence pack, knowledge-base index/log, dated RPI artifacts.
* Generated targets: sanitized results only; no screenshots, HAR, cookies or identity claims.
* Semantic coverage: actual employee adapter, first-page assets, capacity UI/API, resident bounds, metering schema.
* Regression coverage: unchanged existing suites through full gate; this task fixes no source bugs.
* Validation: compile driver, actual bounded live execution, link/diff/privacy checks, independent original Review and final full gate.

## Follow-Up Items

* #570: independently attest expected employee tenant/object IDs, then execute
  actual chat/map/case/tabs/capacity/metering with a separately tracked finite
  driver/run; current task used zero employee slots but does not authorize
  unlimited reruns or historical-session reuse.
* #432: live billing/price/quality/batch evidence and owner decisions remain
  separate; no model calls or financial evidence collected.
* #608: post-Review full-gate persistent Chromium socket path failure. Local
  tooling follow-up for early path admission/owned short scratch; no source
  remediation or original Review repetition in this task.

## Handoff

* P01/P02 observations and records complete; ready for one original Review of
  that delivered boundary. P03 remains pending post-Review commit/full gate/
  independent exact-head publication assessment/push/PR. Employee live
  acceptance is blocked explicitly, not an implementation failure hidden by
  checked observation-recording tasks.
