---
title: Issue 122 new bounded register and release remediation plan
description: Owner-authorized remediation of two independently reproduced findings
ms.date: 2026-10-18
---

## Task Metadata

Task ID and slug: issue-122-register-release-remediation. Automatic bounded loop,
2026-10-18. Branch fix/continuity-epoch-export-122, draft PR 398.

## Executive Summary

Withhold protected control narratives from register responses using the EXISTING
recorded-need policy, without removing permitted status access or modifying
canonical evidence. Check every retained release lifecycle, even when no proposal
references it. Require complete proof only when evidence supports it.

### What You May Not Know

The prior independent result is Not accepted. Its original Review, coordinator
messages and both correction receipts remain frozen. This is a new authorized
task with one critique and one original Review, not a third historical correction.
Bare test release fixtures have absent lifecycle evidence and must no longer be
misrepresented as full proof. Real task-local release construction replaces only
full-proof test setup; shared fixtures remain untouched.

## Sources

Research C1-C6 and exact coordinator messages:
.copilot-tracking/research/2026-10-18/issue-122-register-release-remediation-research.md
and adjacent coordinator-evidence.json.

## User Decisions and Requirements

* New full bounded RPI loop authorized for both findings; exactly one independent
  final-candidate critique and one original Review. At most two later corrections
  only after coordinator review; no such correction is pre-authorized here.
* Preserve all historical original assessments/correction receipts byte-for-byte.
* Before implementation rebase owned branch onto exact fetched
  9c648b2006e8b2e563823ea7d5aabdf7f1ac7096; stop unexpected head/source conflicts.
  Only additive documentation conflicts may be reconciled, preserving both.
* Publish ONLY this branch with exact force-with-lease old head
  1144647c8d539716e8ddddf9daa47407c9bd00ac; later corrections normal push.
* No private data, support, secrets, Azure/IAM/Graph/spend/model calls; pip only
  src packages. No web, server, queue or procurement production changes.
* Keep draft, use only Refs #122, verify no closing references, leave whole issue
  open, stop for full coordinator independent review.

## Goals

Close the reproduced raw-register disclosure and false retained-release proof.
Maintain permitted operation/status access, evidence fidelity and old safeguards.

## Scope and Non-Goals

Production: core continuity.py only. Test ownership: API continuity modules.
Documentation: additive API README and new dated task artifacts. No projection
policy, serving epoch, shared persistence/schema, domain projection or fixture
change. Integration retains upstream additions exactly.

## Functional Requirements

* Raw register and continuity mutation responses containing the same persisted
  control records use can_see_reason. Full readers retain exact canonical content;
  limited readers get closed status/identity/epoch summaries with held markers,
  not arbitrary nested text. Required IDs/status/communication-sent remain usable.
* Producer and offline verifier independently validate every retained release
  record's lifecycle counts, types, event IDs/time/association, legal kinds,
  initial record and current status; reference digest/version/task checks remain.
* Known-empty supported and explicit unsupported sources remain distinguishable
  from absent/unknown/unavailable/contradictory evidence. Malformed envelopes fail
  with explicit problems, not exceptions or success-shaped defaults.
* Full canonical heads/ledgers remain unchanged; limited bundles never assert
  full proof. No authenticity claim for consistent rewriting of unanchored history.

## Non-Functional Requirements

No new dependency or persistence change. Preserve epoch, in-flight charge/unknown,
late quarantine, local-only retry, atomicity and current domain projections.
Use installed packages, synthetic temporary stores and task-owned loopback SQL.
Any failure/skip is reported as such; local evidence is not Azure acceptance.

## Acceptance Criteria

* Exact prior raw-register role canaries and unreferenced event_limit=0
  reproduction fail first at the original head, pass after implementation.
* Actual HTTP allowed roles/denials and recorded-need override both directions;
  nested arbitrary narratives absent from limited reads/responses, exact full
  evidence preserved without persistent mutation.
* Unreferenced active/suspended/revoked complete positives, truncated/malformed/
  count/association/status negatives, recomputed digest and unchanged external
  head. Absent source and bare fixture evidence reject; explicit unsupported
  JSON and explicit limited export behave honestly.
* Existing focused continuity/export/epoch/legacy/role suites plus adjacent
  projection tests pass; adverse atomicity tests preserve their oracle.
* Actual local SQL inherited affected suites; hardened nonroot installed API image
  exact HTTP/full/limited/negative behavior; configured Ruff/format/mypy core/API/
  agents. No shared fixture edits to make checks green.
* Integration hash parity, append-only log prefix and all ten historical artifact
  hashes verified; new evidence committed in the same draft PR.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Exact-base integration and failing controls
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Integrate exact authorized base and preserve parity
<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add and execute task-owned adverse controls

<!-- rpi:phase id=P02 -->
### [x] P02: Bounded source remediation
<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Project control responses without altering policy/evidence
<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Validate every retained release and preserve reference checks

<!-- rpi:phase id=P03 -->
### [x] P03: Validate, reconcile and review once
<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Execute local, SQL, image and static checks; update guide
<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Reconcile evidence and obtain one original independent Review
<!-- rpi:task id=P03-T03 -->
#### [x] P03-T03: Commit/publish exact lease and stop for coordinator review

## Test Ownership Lock

Canonical tests: src/api/tests/test_continuity_epoch_export.py and
src/api/tests/test_continuity.py. Generated test targets: none.
Removals: none. Maximum additions: 12 semantic test methods, inherited MSSQL
executions do not create new semantic methods. New assertions are acceptance
oracles, not snapshots. Existing bare fixture tests keep absent-history negative
controls; full positives use task-local real release APIs. No shared fixture edits.
Exact commands/results retained in the changes record; failures preserved.

## Critique Disposition

Exactly one critique executed: Complete / Revise, five Medium findings,
zero High/Critical. Artifact:
.copilot-tracking/reviews/plans/2026-10-18/issue-122-register-release-remediation-plan-critique.md.
All five are compatible direct planner corrections, accepted below; no new owner
decision, scope expansion or second critique.

| Finding | Direct disposition and resolving implementation evidence |
| --- | --- |
| PC-001 | Validate raw producer inputs before coercion/defaulting and guard verifier traversals. Parameterized producer/verifier shapes matrix with unchanged external heads must reject without exceptions. |
| PC-002 | Explicit source decision table in details preserves actual unchanged JSON exporter, rejects missing SQL source without proposals and contradictory unsupported claims. |
| PC-003 | Timestamp-consistent possible lifecycle order, repeated suspension and ties explicitly specified. API-generated positive and impossible chronology negative controls required. |
| PC-004 | Field-level register/mutation contract in details preserves all operation IDs/enums/epochs/flags and removes arbitrary derived effective text; exercise all five mutation routes. |
| PC-005 | Test-local positive setup replaces ALL bare records before API construction; keep untouched shared-fixture negatives. Named consumers/method allocation specified in details. |

## Follow-Up Items

* New original Review Complete / Not accepted: RV-001 Medium, oversized integer
  timestamp OverflowError. Coordinator-selected later rpi-implement correction,
  not a second Review or self-correction in this task. Both original supplied
  reproductions are fixed in exercised normal paths; full contract not accepted.
* RV-002 Low: inherited malformed limited-metadata passthrough, separate
  conditional defensive hardening, not an ordinary HTTP disclosure finding.
* Control/platform owners: genuine authority, witnessed drill, external immutable
  Azure head, Azure SQL drill and enforceable legacy-image exclusion remain unmet.
* Coordinator: full exact published-head independent acceptance after this loop.

## Handoff

Details: .copilot-tracking/details/2026-10-18/issue-122-register-release-remediation-phase-details.md.
Changes target: .copilot-tracking/changes/2026-10-18/issue-122-register-release-remediation-changes.md.
Implementation ready after these direct dispositions. Executive summary and
scope unchanged; exact integration remains the first implementation prerequisite.
Current execution completed the one original Review, Complete / Not accepted,
and authorized exact-lease publication at 916c1b0800d2a9b8d092e5eded2f996d75a73b9b.
Final documentation-only receipt uses normal push; no source edits after Review.
Coordinator alone decides later corrections and acceptance. Owner-requested STOP,
not an automatically started child loop or a claim of source acceptance.
