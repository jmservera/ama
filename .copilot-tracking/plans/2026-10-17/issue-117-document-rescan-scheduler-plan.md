<!-- markdownlint-disable-file -->
# RPI Plan: Bounded pending-document rescans

## Task Metadata

* Task ID: 117
* Task slug: issue-117-document-rescan-scheduler
* Plan date: 2026-10-17
* Planning status: Coordinator-authorized correction ONE active; original Review unchanged
* Phase details: .copilot-tracking/details/2026-10-17/issue-117-document-rescan-scheduler-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-17/issue-117-document-rescan-scheduler-plan-critique.md

## Executive Summary

Deliver an explicitly configured, one-shot orchestrator command that rescans
at most 100 pending/missing-scan documents through the current scan service.
Stable keyset pages prevent an always-pending first document starving later
documents. SQL CAS and rollback protect durable records/audit across races.
Malicious results remain unavailable, with bytes and legal hold retained:
this worker has no deletion or hold-release authority.

### What You May Not Know

The legacy unbounded helper has no executable scheduler and does not touch
clean/pending case rows for SQL persistence. A wrapper alone is insufficient.
The default synthetic local scanner must never implicitly replace Defender.
This delivers a schedulable offline mechanism, not a deployed recurring timer
or operational scanner approval.

### Unresolved Decisions or Blockers

No engineering decision blocker. Original Review execution Complete / outcome
Not accepted identified RV-001/RV-002 (Medium) at safe logging/malformed-result
boundaries. Coordinator authorized one coherent correction cycle on 2026-10-17;
both findings have targeted P03 implementation evidence. T01 complete and T02
validation complete; publication pending. No second critique/Review or self-Pass.
Actual Defender enablement, schedule owner/cadence and retention/deletion
delegations remain unmet human/service gates.

## User Decisions and Requirements

* Run Research, Plan with critique, Implement and one original Review in order.
* Implement only the missing bounded rescan job; preserve already delivered controls.
* Use current src distributions, orchestrator/configuration and scan service.
* Pending, unavailable, malformed or error results never imply availability.
* No worker deletion/hold-release authority; no automatic retention deletion.
* Use owned synthetic loopback SQL, actual offline command and hardened image.
* Preserve merged102 recovery, audit, resident and sensor controls.
* Commit/push authorized branch and main PR, using Refs #117; no merge/issue closure.
* Fresh main movement requires coordinator authorization; no silent integration.
* Coordinator authorizes correction ONE for RV-001/RV-002 on the same branch/
  draft PR395, with failing-first tests, actual SQL and hardened image receipts.
  Preserve original Review and critique byte-exact; keep draft pending independent
  coordinator acceptance. No second full Review.

## Goals

* Make bounded document rescan invocation durable, fair and externally schedulable.
* Demonstrate persisted safe retries, competing writers and truthful outcomes.

## Scope and Non-Goals

In scope: core scan-service extension, SQL page runner, orchestrator module CLI,
owned tests, directly related README and existing knowledge synthesis updates.
Out of scope: web, new frameworks, hosted timers/infra, scanner activation,
new retention policies, approvals, deletion or hold release.

## Functional Requirements

* FR1: Scan missing/pending non-generated records in stable `(case_id, doc_id)`
  order, limit integer 1..100, optional two-part exclusive cursor, next cursor
  only when more candidates exist, advancing through selected keys even when
  rechecks skip them. Start each new sweep with no cursor.
* FR2: Recheck eligibility under each existing store lock, touch the case, use
  the existing `_scan_stored` with a non-deleting bad-verdict mode.
* FR3: Only exact clean becomes available. Bad verdicts persist as blocked;
  invalid verdict is an explicit error, not removal or clean. Existing manual
  scan/removal behavior remains unchanged.
* FR4: CAS conflict/error rolls back failed success audit and preserves any
  prior pending prefix. Confirmed committed refresh error is separate, never
  a rejection. Use a thread-local own-operation COMMIT witness set immediately
  after SQL COMMIT, not snapshot comparison; competitor refresh is not own
  commit. Always restore prior prefix after rejected CAS. No unbounded retry.
* FR5: Report checked, clean, pending, blocked, skipped, failed and committed
  counts plus continuation. No filenames, bytes or exception diagnostics.
* FR6: CLI requires explicit `ZF_DATA`, SQL store and scanner. Synthetic local
  scanner requires explicit opt-in; Defender uses existing Blob configuration.
  Exit precedence: 1 failure/committed reconciliation, otherwise 2 pending or
  non-null continuation, otherwise 0. Pending earlier in a sweep still requires
  another cursor-free sweep. Close the owned store connection, including a
  reusable close-on-construction-failure guard before the factory returns.

## Non-Functional Requirements

* No more than requested document attempts in a single invocation.
* SQL independent-connection race yields at most one successful scan event
  per pending-to-clean transition; later sweeps skip resolved records.
* Retention, hold, resident, sensor, progress and upload paths retain behavior.
* Existing Ruff/format/mypy configurations apply; no new broad exemptions.
* Offline tests use only constructed local bytes and no paid/cloud services.

## Acceptance Criteria

* AC1: Real CLI invocation over a fresh synthetic SQL fixture persists clean,
  resumes bounded pages and reports nonzero incomplete/error runs.
* AC2: Pending/unknown/error/outage stay unavailable; infected/mismatch bytes
  survive with legal hold and no worker retention/deletion/hold-release call.
* AC3: Independent SQL connections prove CAS retry, fair paging, exactly-once
  successful transition audit, preserved prefix and no failed success audit,
  including commit-refresh and failed-recovery seams.
* AC4: Targeted core/orchestrator/API regressions and component lint/format/
  mypy succeed or actual limits/failures are plainly recorded.
* AC5: Existing Docker build and nonroot hardened startup run the changed job.
* AC6: Original critique/Review remain accurate; adverse findings route to
  separate follow-up, not a second Review or self-awarded coordinator Pass.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-17/issue-117-document-rescan-scheduler-research.md.
Changes (implementation-owned): .copilot-tracking/changes/2026-10-17/issue-117-document-rescan-scheduler-changes.md.
Automatic parent continues after the one critique gate.

## Sources

Research C1-C8 and W1-W2; ADR0002 decision2/open items; PRD DH-003.
Current source base ebc8dab87ae9bd6a33380b85e86f38be5ed9f213 includes merged102.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement bounded core and job

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Extend scan service and add safe SQL pages

Evidence C1,C4-C7; requires no new authority. Expected: non-deleting scan mode,
validated verdict and CAS/recovery page function.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Wire configured orchestrator command

Depends P01-T01. Evidence C2,C3,C8. Expected: explicit configuration and local
opt-in, bounded CLI, safe status, connection closure, no Azure timer.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and document delivery

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Exercise semantic and regression acceptance

Depends P01. New test ownership: core page/recovery tests and orchestrator CLI
tests only; at most two new test files, no test removals, no generated targets.
Canonical fixtures: existing `core/tests/dataset.py`, temporary synthetic bytes.
Semantic: fair paging, all verdicts, retry/race/outage and audit boundaries.
Regression: existing document controls, current progress capture/provenance,
resident and sensor selections. Actual owned loopback SQL and command required.
Use pip-installed distributions and existing tool versions.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Build image, update docs and reconcile evidence

Depends P02-T01. Existing Docker context src/; run `src/check-container.py`
plus actual job as UID10001/read-only/drop-all/NoNewPrivs. Update component
READMEs, existing synthetic evidence synthesis/index and append-only log.
Stop owned SQL and record exact commands/results. Original execution performed
no source correction after Review; the separately authorized P03 below now applies.

<!-- rpi:phase id=P03 -->
### [ ] P03: Coordinator-authorized correction ONE

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Reproduce and correct RV-001/RV-002 together

Add failing-first coverage within the two existing owned test files. Inspect
the entire actual CLI root log/stream, CAS winner/prior prefix/original conflict
and own-COMMIT boundary. Validate exact scanner tuple shape, arity, verdict and
string detail before unpack/mutation; do not stringify unknown objects.
Worker owns recovery under its active context, before nested traceback emission.
Preserve non-worker error/recovery semantics and manual valid scan behavior.

<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: Validate, reconcile and publish corrected candidate

Depends P03-T01. Actual SQL reruns all prior17 worker cases plus new malformed/
recovery tests; relevant progress102/resident88/sensor regressions, configured
core/orchestrator tools, rebuilt image/actual hardened job. Stop owned SQL.
Reconcile correction receipts/current state and PR395 body, fresh main/identity,
normal commit/push; retain draft and exact original Review/critique bytes.

## Dependencies

P01-T02 depends P01-T01; P02-T01 depends P01; P02-T02 depends P02-T01.
P03-T02 depends P03-T01 and separate coordinator correction authorization.
Local SQL driver/container and installed src packages are validation prerequisites.

## Critique Disposition

Original critique execution Complete; verdict Revise (one High, two Medium).
All are compatible direct planner corrections; original artifact unchanged.

| Finding | Disposition | Resolving plan evidence |
| --- | --- | --- |
| PC-001 | Applied | FR4/P01-T01 explicit post-COMMIT witness; rejected CAS always restores prior prefix; discriminating actual SQL race and failed-recovery test |
| PC-002 | Applied | FR1/FR6 selected-key advancement including skipped; exit1 precedence, exit2 for pending or continuation |
| PC-003 | Applied | FR6/P01-T02 reusable SqlStore construction cleanup; real-open failure/close test and sanitized CLI construction boundary |

## Follow-Up Items

* Defender account enablement and real Blob verification: owner/service gate.
* Hosted schedule ownership/cadence/monitoring: separate authorized delivery.
* DPO/Legal periods, holds and owner approvals: human gate, never worker authority.

## Handoff

Full P01/P02 implementation and validation executed, with actual limits/skips
in the changes record. The one original Review executed Complete / outcome
Not accepted, two Medium findings. Completion markers record execution, not
defect-free acceptance. Coordinator now authorizes correction ONE P03 for both
findings, without reopening or rewriting the original Review/critique.
Operational gates and independent coordinator acceptance remain separate.
