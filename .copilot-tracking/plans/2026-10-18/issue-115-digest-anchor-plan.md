---
title: Issue 115 digest anchor plan
description: Minimal fail-closed recognized remote-anchor evidence correction
ms.date: 2026-10-18
---
<!-- markdownlint-disable-file -->

## Task Metadata

* Task ID: 115
* Task slug: issue-115-digest-anchor
* Planning status: Correction TWO delivered, final permitted cycle; stopped for SAME reviewer; coordinator NOT ACCEPTED
* Plan date: 2026-10-18
* Phase details: .copilot-tracking/details/2026-10-18/issue-115-digest-anchor-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-18/issue-115-digest-anchor-plan-critique.md

## Executive Summary

The implemented correction prevents an unrelated JSON blob from making an
unanchored local ledger appear remotely verified. The absence guard inspects
recognized head and year collections, with an explicit missing-anchor problem. It keeps valid
head-only or sealed-year-only verification and create-only publication intact.
Coordinator complete exact-head assessment subsequently found one Medium
prefix/payload false green and returned NOT ACCEPTED. Authorized correction ONE
qualifies actual publisher names and required ledger fields, not prefixes alone.
Original critique/Review remain unchanged; no new Review or self-acceptance.
Correction ONE follow-up was also NOT ACCEPTED: suffix filtering hid reserved
non-JSON candidates. Correction TWO adds reserved-name enumeration and validates
names before any download, preserving unrelated listing compatibility.

### User Decisions and Requirements Highlights

Offline failing-first regression, one independent critique then implementation
and one original independent Review. Commit all task artifacts with source
delivery; publish a non-closing PR and stop for coordinator exact-head review.

### What You May Not Know

Remote publish/read-back already exists; issue body local-only status is stale.
An intact local chain is not itself remote evidence. An empty ledger with an
explicit remote zero-count GENESIS head currently succeeds; preserve that narrow
behavior without claiming pre-first-publish authenticity or full-year coverage.
Actual lock, retention authority, scheduling and monitoring acceptance remain open.

### Unresolved Decisions or Blockers

Coordinator acceptance is blocked by malformed prefixed remote evidence until
same-reviewer follow-up. Correction ONE is authorized; cloud/policy remain outside scope.
Original independent Review is Complete / Residual work, bounded source
Conformant with no implementation defects. RV-001 publication portion completed
on PR404; coordinator exact-final-head acceptance remains open. RV-002/003/004
are operational and first-publication trust follow-ups, not performed here.

## User Decisions and Requirements

* Use isolated fix/digest-anchor-evidence-115 at exact c803614e8ca7c604e509f1c088f8b8f90f3063ef.
* Correction ONE: reject malformed prefixed names and payloads using actual
  publisher/ledger invariants; preserve original assessments and stop for SAME
  coordinator after normal push/PR404 update. Maximum two correction cycles.
* Correction TWO is final permitted cycle: every case-sensitive digest-/year-
  candidate reaches qualification regardless suffix; invalid names rejected
  before fetch, unrelated objects ignored/not fetched. No third cycle authorized.
* No recognized head/year anchor means explicit unsuccessful missing-anchor
  report, LEDGER_DIGEST_ALERT and nonzero exit; never LEDGER_DIGEST_OK.
* First add a failing regression using existing FakeImmutableContainer with
  only unrelated.json, then implement the smallest evidence-backed correction.
* Preserve valid head OR sealed-year success and unrelated-blob neutrality,
  existing rewrite/truncation/year-mismatch/create-only tests and marker contract.
* No private inputs/support/.env, new mvp code, Azure/IAM/Graph, deployment,
  spending, retention choices/lock, issue boxes or board changes.
* One independent original critique and one independent original Review only;
  preserve original adverse evidence unchanged; at most two later source cycles.
* Push and open PR to main using Refs #115, no closing keywords; no merge,
  rebase or force-push. If main advances, report without unilateral integration.

## Goals

* Distinguish actual recognized remote anchors from arbitrary container content.
* Demonstrate negative and positive behavior at verifier and injected CLI boundary.
* Deliver persistent, ordered and independently assessed evidence without
  promoting local tests to operational acceptance.

## Scope and Non-Goals

In scope: digest_blob.py guard/problem text, test_digest_blob.py tests and narrow
existing orchestrator README clarification, dated task artifacts only.
Correction ONE includes existing publisher filename/essential payload qualification.
Non-goals: new digest format, timestamp-schema redesign, core ledger changes,
retention or identity changes, services, SQL/Docker/browser/cloud validation,
whole #115/#114 closure, KB inventory or other active workstreams.

## Functional Requirements

* FR1: both recognized collections empty => intact false, zero anchor counts,
  explicit digests-check problem stating no recognized remote anchor.
* FR2: CLI main with injected store/fake Blob returns1 and alert, not OK.
* FR3: qualifying head-only OR one completed-year-only anchor still returns
  intact true/exit0/OK; unrelated malformed JSON is ignored, not read.
* FR4: local digest files never substitute for remote evidence; empty ledger
  without remote anchors fails; explicit zero-count remote head retains behavior.
* FR5: broken chain or mismatching remote evidence remains unsuccessful even
  with unrelated blobs.
* FR6: malformed head/year candidate name or essential payload yields an explicit
  fixed-diagnostic unsuccessful report and CLI ALERT/exit1, even beside valid
  evidence, without echoing remote names/content or mutating blobs.

## Non-Functional Requirements

* Minimal surgical patch; no new dependencies or API/report-shape changes.
* All executed tests use constructed temporary fixtures and sanitized environment,
  BlobDigestStore(env={}, transport=existing fake); no inherited cloud credentials.
* Existing configured Ruff check/format and mypy must run; disclose pre-existing
  digest format exclusions and mypy ignore_errors rather than claim strict typing.
* Frozen original critique/Review receive SHA-256 receipts; no rewriting verdicts.

## Acceptance Criteria

* AC1: new only-unrelated regression fails against unchanged source (expected
  false versus actual true or expected1 versus actual0), then passes after guard.
* AC2: direct report + CLI marker/exit assertions cover absent anchors, local-only
  evidence and empty ledger. Successful controls exercise head/year separately,
  each with and without unrelated bytes and no unintended reads.
* AC3: truncation, rewrite, broken-chain, year mismatch, empty/unreachable and
  create-only/idempotent publication existing tests pass unchanged.
* AC4: targeted digest and coupled core recovery guards, full orchestrator
  discovery, configured Ruff/format/mypy and git diff --check have actual receipts.
* AC5: single critique and Review are retained; all task artifacts committed;
  PR reports exact base/candidate/head and unmet gates; stop for coordinator.
* AC6: correction malformed-name/empty/incomplete/wrong-type/invalid-JSON payload
  regression matrices fail before source change, pass after; valid historical
  head/year, empty GENESIS, unrelated neutrality and canonical large-count names
  remain compatible. No new original Review, coordinator acceptance pending.

## Implementation Context Record

| Item | Artifact |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-18/issue-115-digest-anchor-research.md (executed, Ready) |
| Plan | .copilot-tracking/plans/2026-10-18/issue-115-digest-anchor-plan.md |
| Details | .copilot-tracking/details/2026-10-18/issue-115-digest-anchor-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-18/issue-115-digest-anchor-plan-critique.md (Complete / Revise, PC-001 resolved in plan) |
| Changes | .copilot-tracking/changes/2026-10-18/issue-115-digest-anchor-changes.md (implementation-owned) |
| Continuation | Explicit automatic full-loop parent, no routine approval prompt |

## Sources

Research C1-C8, W1; existing src guides, pyproject and source CI; ADR 0002 audit
proposal/DH-007; user bounded criteria. No research readiness gap remains.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Establish failing-first regression and minimal correction

Dependency: single candidate critique disposition complete.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add and run bounded regression/control tests before source edit

Missing anchor, head/year neutrality, local-only and genuine empty ledger
controls in existing fake suite. Record actual failing-first command/output.
Details: P01-T01 in phase-details artifact.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Correct recognized-anchor absence guard and narrow guide

Change only absent-evidence predicate/problem wording and related README sentence.
Depends on P01-T01 failing evidence. Details: P01-T02.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate, reconcile and hand off for one original Review

Dependency: P01 complete.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run local checks and record exact evidence

Focused/coupled tests, full orchestrator discovery, configured Ruff/format/mypy,
diff check and hashes; reconcile task markers and changes. Details: P02-T01.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Freeze original independent Review and publish delivery

One original independent Review, immutable receipts, max two separate correction
cycles only if needed. Commit, push, open non-closing PR and reconcile publication.
Depends on P02-T01; source review cannot assess its own later receipt-only commit.
Coordinator must review exact final head independently. Details: P02-T02.

## Test Ownership and Locked Candidate

Canonical test owner: src/orchestrator/tests/test_digest_blob.py and existing
FakeImmutableContainer, not a new duplicate suite. Exact removals: none.
Original candidate maximum additions: eight methods, completed.
Correction ONE authorizes focused additional malformed name/payload and positive
compatibility methods under same existing fake owner, no removals.
Canonical production target: digest_blob.py; guide: orchestrator README ledger
section only. Generated targets: none. No new core tests or modifications.
Regression coverage: absence guard and CLI marker/exit. Semantic controls:
valid head/year separately, unrelated neutrality, local-only and empty states.
Validation evidence: sanitized env commands/output and actual source hashes
in changes; no proxy cloud or whole-issue acceptance claims.
Every sanitized test invocation must explicitly set TMPDIR to the pre-created
task-owned worktree directory `.digest-anchor-tmp` (absolute path), verify
`tempfile.gettempdir()` in a fresh process, and clean only task-owned scratch.

## Dependencies

No issue dependency; #114 hierarchy only. PR #403 is merged in pinned base and
its loadcheck paths remain untouched. Local packages/dev tools now installed
after actual chosen-command missing-dependency failure. No extra planner worker
needed for this bounded single trace; independent critique is mandatory.

## Critique Disposition

Exactly one independent critique executed by digest-plan-critique using
rpi-plan-critique. Original execution Complete, verdict Revise, one Medium PC-001.
Frozen SHA-256:
`d1add2a5642689cb9a615f3aaa989871a3b405f7f5cab076689fdcc0110314e0`.
No second critique.

| Finding | Owner and disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 task-owned TMPDIR | Planner-direct, applied | Test Ownership above and P01-T01/P02-T01 details bind every sanitized runner to absolute worktree .digest-anchor-tmp; implementation must record fresh-process root and actual commands |

The critique's claimed absolute runtime prohibition on system temp paths is not
an independently established repository rule here; the stricter task-owned
worktree TMPDIR is nevertheless compatible with user isolation and adopted.
Research baseline used automatically cleaned tempfile fixtures before critique;
subsequent failing-first and validation commands use the bound workspace root.

## Follow-Up Items

* Coordinator independent exact-head review on published PR404; outside this
  original Review and owned by coordinator. Publication portion of RV-001 is
  complete; this is not a second independent acceptance claim.
* Owner-controlled retention duration/irreversible lock and real scheduled
  verifier/alert/recovery acceptance; outside offline source correction.

## Handoff

Historical initial delivery P01/P02-T01: failing-first17/four failures,
passing focused21 and full orchestrator40, configured Ruff/format/mypy passed.
Single original Review executed Complete / Residual work; source Conformant,
zero source-correction cycles. P02-T02 complete: originals frozen and committed,
branch pushed and PR404 opened to unchanged pinned main with actual identity
readback; final evidence-only receipt records publication, not a new assessment.
Changes and delivery receipt own commands/hashes/publication facts.
Stopped per user instruction. Coordinator complete independent exact-final-head
review remains separate; no issue closure or operational acceptance.
Subsequent coordinator NOT ACCEPTED supersedes the historical candidate's
positive source judgment. Current correction ONE P03 has failing-first malformed
name/payload evidence and25/44 passing local checks; qualification is implemented,
not independently accepted. Source d0088301ba64cba8c632b6d0b4dcd80474580e41 committed/pushed; final receipt
reconciles actual publication. Stopped for SAME coordinator follow-up, no new Review.

## Correction ONE Active Checklist

<!-- rpi:phase id=P03 -->
### [x] P03: Qualify remote anchors after adverse coordinator finding

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Failing-first malformed-name/payload direct and CLI matrix

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Minimal publisher-contract qualification and accurate guide

Depends on P03-T01 expected behavioral failure, not setup error.

<!-- rpi:task id=P03-T03 -->
#### [x] P03-T03: Local gates, frozen parity, correction receipt and PR404 publication

Depends on P03-T02. No new/amended Review; stop for same coordinator.
Receipt: .copilot-tracking/changes/2026-10-18/issue-115-digest-anchor-correction-one.md.

## Correction TWO Checklist

<!-- rpi:phase id=P04 -->
### [x] P04: Close reserved-prefix enumeration and prefetch name gap

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Failing-first malformed suffix/name and unrelated controls

Both prefixes; .txt/.JSON/.json.bak/no extension, alone/valid head/valid year.
Direct and CLI report/markers/status, no download/leak/mutation. Test listing
compatibility and valid unrelated JSON/nonJSON/case-sensitive prefix controls.

<!-- rpi:task id=P04-T02 -->
#### [x] P04-T02: Minimal listing admission and canonical prefetch qualification

Depends on P04-T01 failure; same essential format, no new prefix/schema policy.

<!-- rpi:task id=P04-T03 -->
#### [x] P04-T03: Validate, preserve originals/correction ONE, publish and STOP

Depends on P04-T02; focused/full/configured gates and hashes. Correction TWO
receipt/logs separate. Same coordinator, no new Review, no third cycle.
Source aed065a014d6907dd0fda5399bb7983abf3c9784 normally committed/pushed;
final receipt-only commit reconciles delivery. Actual final hash in PR metadata.
STOPPED as explicitly instructed for SAME reviewer, NOT ACCEPTED pending follow-up.
