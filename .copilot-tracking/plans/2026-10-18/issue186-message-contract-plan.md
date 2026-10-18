<!-- markdownlint-disable-file -->
# RPI Plan: Issue186 shared message contract and volume

## Task Metadata

* Task ID: issue186
* Task slug: issue186-message-contract
* Date: 2026-10-18
* Planning status: Ready; one critique complete, direct dispositions applied
* Phase details: .copilot-tracking/details/2026-10-18/issue186-message-contract-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-18/issue186-message-contract-plan-critique.md

## Executive Summary

Document the exact existing shared sensor observation contract and measure
three paired observation records/home/day at N=1 and fictional N=60,000.
Extend existing canonical documentation, not runtime or schemas. Preserve
stable reading IDs and existing replay/rejection behavior.

### What You May Not Know

Stock-mode sensor IDs are 73 characters with lowercase hex; the unchanged
consumer accepts uppercase IDs of at most20. Valid current fixtures therefore
prove the consumer contract only, not backfill/live producer compatibility.
No transport batching or live Hub sizing/billing decision follows from3N rows.
ADR0003 is already accepted with the Basic exercise amendment.

### Unresolved Decisions or Blockers

No blocker to documentation. Live and stock compatibility decisions remain
separate downstream187/188 work. Exact original Review may route findings;
no correction or second Review is authorized.

## User Decisions and Requirements

* Full ordered automatic RPI; one independent critique/direct dispositions,
  then implementation, then one original Review, then publish and stop.
* Exact branch/base fixed; no rebase, force-push, merge or issue criteria updates.
* Existing imported 13-field schema is authority; no duplicate schema or runtime
  edits, producer changes, ID remapping, validation weakening or third110 correction.
* Keep three paired observations/home/day; distinguish records, API batches,
  conditional wire messages and unmeasured Hub billing/throughput.
* Reuse public synthetic fixtures and serialization prior art; never private stock,
  .env, ZF_DATA or support. Report measured sample, not an upper bound.
* Explicit stock identity incompatibility and downstream decision; preserve
  accepted ADR and independent live/privacy/human/AI/Azure gates.
* Commit docs and all issue186 artifacts with safe author/committer and Copilot
  trailer; normal push and draft PRmain, body Refs #186 only, no closure language.

## Goals

Make the existing shared schema, replay semantics and bounded rate accounting
usable by later implementers without implying producer or service acceptance.

## Scope and Non-Goals

In scope: existing sensor synthesis, component READMEs, sensor addendum, KB
index/append-only log, synthetic measurement command and RPI evidence.
Non-goals: source/schema/store/test behavior changes, new services/tools, live
transport, cloud deployment, private datasets, product acceptance or approval.

## Functional Requirements

* FR1: Exact13 required string fields with source import authority, limits,
  UTC, units/version/provenance, rejection and envelope/observation distinction.
* FR2: Stable(sensor_id,reading_id) accepted replay versus conflict; bounded
  receipt/DQ and uncertain-prefix retry without invented identity.
* FR3: Three paired records/home/day,3N and3N/86400; declared N1/60000;
  explicit canonical synthetic bytes and reproducible command/results.
* FR4: Stock incompatibility, conditional packetizations only, no live claims;
  current ADR acceptance and all independent gates remain explicit.

## Non-Functional Requirements

* Zero changes outside approved documentation/tracking paths. Runtime/image
  unchanged; no app-image/UI/Azure reruns needed for docs-only delivery.
* Existing semantic checks, not test constant restatements or duplicated logic.
* Pin ZF_SENSOR_MSSQL=0 and session-local issue-owned TMPDIR for semantic
  suites; no ambient SQL connection probes or private setting reads.
* Measurement must verify shared field set/type, current consumer shape and
  actual admission/replay using existing fixture/tests, failing on drift.
* Reproduction is offline, deterministic and needs only installed src projects
  plus existing core test helper; no dataset/state path read.

## Acceptance Criteria

These are delivery evidence conditions, not GitHub issue checkbox updates.

* AC1: Source-linked descriptive table exactly matches current shared authority.
* AC2: Existing tests demonstrate stable replay/conflict, schema/unit/time refusal.
* AC3: N1=>3/day and1/28800 mean/s; N60000=>180000/day and25/12 mean/s.
  Sample-byte multiplication is executed and recorded, explicitly not a bound.
* AC4: No stock/live compatibility claim; sensor73/lowercase versus uppercase20
  is clear and downstream187/188 decision remains separately reviewed.
* AC5: One critique and one Review retained with actual commands/results;
  draft PR/frozen head/base inventory handed to coordinator without merge.

## Implementation Context Record

| Item | Artifact / status |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-18/issue186-message-contract-research.md; executed Ready |
| Plan | .copilot-tracking/plans/2026-10-18/issue186-message-contract-plan.md |
| Details | .copilot-tracking/details/2026-10-18/issue186-message-contract-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-18/issue186-message-contract-plan-critique.md; Complete, Revise, direct dispositions applied |
| Changes | .copilot-tracking/changes/2026-10-18/issue186-message-contract-changes.md; implementation owns creation |
| Review | .copilot-tracking/reviews/logs/2026-10-18/issue186-message-contract-review.md; one original run later |
| Execution | .copilot-tracking/rpi-sessions/2026-10-18/issue186-message-contract-execution.log |
| Continuation | Confirmed automatic parent, fixed base, stop after publication |

## Sources

Research C1-C11/W1-W5; live issue186 and owner bounded delivery request.
No demonstrated research gap; no additional research or planning worker needed.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Document and measure unchanged contract

Dependency: completed research and disposed independent critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Measure public current-contract example

Use observations()[0] unchanged and the exact existing sorted ASCII JSON
reference expression. Verify authority/shape and execute byte/count arithmetic.
Completed:366 bytes, SHA256efccea5eb698a3310aca7409837ad9b5ad3673b949ddb3c2395da21a8b01dc6c;
N1/60000 =>3/180000 rows and1098/65880000 sample-scaled bytes/day.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Integrate canonical documentation

Detailed contract/rate/example in existing sensor synthesis; concise links from
core/API READMEs and addendum; KB index update and append-only log.
Depends on P01-T01's actual measurement.
Completed: all six existing documentation targets updated; no new topic page,
runtime/schema/test change. P02 checks completed subsequently below.

<!-- rpi:phase id=P02 -->
### [x] P02: Verify and reconcile evidence

Depends on P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run focused checks and reconcile artifacts

Existing core consumer, API consumer and sensor_faults tests together; check
documentation fields/example/links/arithmetic and git diff. No test/source
changes planned, so configured lint/format/type runs are not required.
Completed:80 tests passed after temp-root refinement; initial80-test/16-error
output retained. Documented reproduction, exact table/example/bytes, links,
append-only log, clean diff and runtime/source parity verified. Scratch removed.

## Test Ownership and Change Lock

Canonical tests: src/core/tests/test_sensor_consumer.py,
src/api/tests/test_sensor_ingestion.py, src/core/tests/test_sensor_faults.py.
Exact removals: none. Maximum new test additions:0. Generated/runtime targets:
none. Canonical documentation targets: six existing Markdown files listed in
details. Semantic coverage is current replay/schema/unit/time behavior; regression
evidence is those unchanged suites plus reproducible doc measurement. No new
public schema API, runtime calculator or tooling.
If the unchanged contract cannot be represented honestly, stop rather than alter it.

## Dependencies

Contract dependency110 satisfied by merged411 at pinned base100ead1b.
Whole110/live gates remain open; parent184 does not impose ordering.
Local system Python lacks installed distributions; installing src/core and
src/api in a task-owned session venv is permitted after that observed failure.

## Critique Disposition

Exactly one critique executed, verdict Revise. Parent applied both compatible
execution safeguards directly; no repeat critique or user decision needed.

| Finding | Owner / disposition | Exact resolving evidence |
| --- | --- | --- |
| PC-001 High | Parent, resolved in plan | P02-T01 pins ZF_SENSOR_MSSQL=0; store_at's MSSQL branch requires1. No inherited SQL credentials inspected or connection probe allowed. Changes record must retain exact command/results. |
| PC-002 Medium | Parent, resolved with implementation-time refinement | Initial repository scratch caused16 generator errors because stock_fabric._destination forbids repository outputs. P02-T01 now uses issue-owned session scratch outside the repo and exact cleanup. Isolation intent retained; the critique's asserted blanket /tmp prohibition was not supplied by this caller and is not authority. Original failed run retained. |

Executive summary, phase details, scope and test lock remain synchronized.
Critique execution Complete and original Revise verdict remain immutable;
planning readiness now Ready based on these direct dispositions, not a second Pass.

## Follow-Up Items

* Downstream187/188 compatibility decision before producer/live work; outside
  unchanged-consumer documentation. Coordinator owns assignment/review.
* Hub identity/transport/cost/network/privacy/real AI/Azure/human gates remain
  distinct, not implementation tasks here.

## Handoff

Implementation complete for P01/P02; plan/details/changes/validation synchronized.
Ready for one original Review at the canonical path above. No active plan work
remains. Review and publication are lifecycle actions, not new feature work.
