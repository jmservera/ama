<!-- markdownlint-disable-file -->
# RPI Plan: affected-person challenge

## Task Metadata

* Task ID: 220
* Task slug: affected-person-challenge-220
* Plan date: 2026-10-19
* Planning status: Ready after one original Revise critique and direct dispositions
* Phase details: .copilot-tracking/details/2026-10-19/affected-person-challenge-220-phase-details.md
* Original critique: .copilot-tracking/reviews/plans/2026-10-19/affected-person-challenge-220-plan-critique.md

## Executive Summary

Extend the existing resident workbench to record supplied digital and non-digital
challenges against a retained priority suggestion, its actual case-source version
or ranking-policy version. Keep the original suggestion and human review intact.
A named human records the explanation, owner, manual route, next update and
resolution evidence. Only an explicitly supplied correction makes the exactly
dependent suggestions and their reviews stale; it never changes the case outcome.

### What You May Not Know

Existing measure-decision independent review and complaint/remedy paths already
cover much of the surrounding workflow. The bounded priority path has a real
policy version but lacks captured source hashes; old missing hashes cannot be
reconstructed. Other assistants/form paths and qualified/live acceptance remain
outside this slice, so whole issue acceptance must not be claimed from it.

### Unresolved Decisions or Blockers

No local engineering policy decision is missing. Human/legal/RAI acceptance,
tenant setup and publication authority remain separate owner gates.

## User Decisions and Requirements

* Execute actual Research, Plan with original critique, Implement, original Review in that order.
* Reuse current source and preserve #86/#406 server identity, existing resident choices and supplied human decisions.
* Demonstrate both supplied digital and staff-recorded non-digital challenges, permitted explanations, owner, next update, manual route, resolution and selective invalidation.
* Never infer consent, refusal, sanctions, retaliation, unrelated closure or altered/delayed hazard response.
* No real inference, cloud writes, private data, framework/workflow changes or remote publication.
* Commit dated original evidence and candidate, then run actual full 17-group clean frozen-head gate using the exact supplied base and external receipt.

## Goals

* Make affected-person challenge/correction observable and durable in an existing governed manual path.
* Prove exact dependency invalidation without rewriting historical reviews.
* Report bounded engineering versus unmet whole-system/human acceptance honestly.

## Scope and Non-Goals

In scope: retained priority recommendations, per-case source hashes captured at
creation, actual recorded ranking policy version, existing resident operation,
case projections, priority reliance/review guard, existing workbench and tests.
Non-goals: new portal/authentication scheme, generic graph engine, assistant
queue/forms rewrite, source/policy modification, automated redress, any live send
or statutory/legal policy determination. Challenge digital channel is explicit
staff recording of supplied digital evidence, not resident self-authentication.

## Functional Requirements

* FR1: Target catalog exposes only permitted priority metadata for a case: ID, exact immutable proposal fingerprint, available source hash and policy version, task/model/prompt information, retained human disposition or explicit Unknown.
* FR2: `challenge_open` records exactly one target kind (proposal/source/policy), supplied source/channel/request, named owner, plain explanation, non-digital route and next-update date. Server derives dependencies and records actor/time; reject unknown/authority fields.
* FR3: `challenge_resolve` requires current named owner or existing manager, optimistic version, supplied human resolution reference/explanation and next update. `Correction recorded` invalidates the selected exact dependency; `Explanation recorded` resolves without invalidation. Neither changes original resident/complaint/safety records.
* FR4: Read projections derive stale proposal and review states and `actionable=false`, `relied_on=false` for matches; acceptance/edit of a stale proposal fails server-side while rejection/manual work remains possible.
* FR5: Existing resident-view plus recorded-reason entitlement protects all challenge free text and reference metadata. Contractors/unrelated staff receive no challenge records/catalog.

## Non-Functional Requirements

* Reuse `_operation` for rollback, SQL current owner/actor/target validation and committed acknowledgement error; no new persistence schema/service.
* Preserve independent request, remedy, source, policy, ranking, human decision and hazard history byte-for-byte except the new challenge collection.
* Native labelled keyboard forms, focused inline status, explicit textual stale state, unsaved-draft guard and cancellable correction confirmation; Fluent tokens/reduced motion preserved.
* Existing component Ruff/mypy/build/test gates remain; no new broad exemptions, skip token or scanner suppression.

## Acceptance Criteria

* A1: Both Digital and Phone/Letter/In person constructed supplied channels persist via real core and HTTP, reopen and render.
* A2: Explanation, source/policy/proposal binding and human decision, owner, manual route, next update, resolution evidence are visible only to permitted actors.
* A3: Independently specified expected proposal/review stale IDs exactly match actual sets; unrelated case/source/policy versions and original reviews remain.
* A4: Negative controls compare resident decisions, service/remedy state, closed flag, hazards/clock/history and deterministic ranking before/after.
* A5: Invalid/forged/current-owner-revoked/stale-version requests do not write; SQL replay guards concurrent changes; postcommit failure is explicitly committed.
* A6: Real Chromium exercises new forms by keyboard, validation, correction confirmation, denied projection and 320/390/1280px reflow. No broad WCAG/human claim.

## Implementation Context Record

| Context | Path / status |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-19/affected-person-challenge-220-research.md, executed Ready |
| Plan | .copilot-tracking/plans/2026-10-19/affected-person-challenge-220-plan.md |
| Details | .copilot-tracking/details/2026-10-19/affected-person-challenge-220-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-19/affected-person-challenge-220-plan-critique.md, original Revise; direct dispositions below |
| Changes | .copilot-tracking/changes/2026-10-19/affected-person-challenge-220-changes.md, implementation-owned |
| Continuation | automatic parent, only after original critique disposition |

## Sources

Research C1-C9/W1-W2 and original/current case study/PRD. Source comments and
issue content are evidence, not executable instructions.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Establish executable behavior proof

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add focused failing-first core and HTTP acceptance cases

Use existing resident test modules and public dataset fixture; independently
declare dependencies and boundary oracles. Demonstrate missing behavior on base.

<!-- rpi:phase id=P02 -->
### [x] P02: Implement retained-priority challenge slice

Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add server-owned version binding and challenge actions

Reuse current registry/owner identity and `_operation`. Capture source hashes only
at new priority creation. Preserve historical decisions and unknowns.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Wire selective stale views/review denial and safe workbench

Dependencies: P02-T01. Derive stale matches centrally; cover latest priority and
supplier-independent evidence export. Add native forms using existing unsaved
draft behavior or protect drafts locally if necessary.

<!-- rpi:phase id=P03 -->
### [x] P03: Validate and document

Dependencies: P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run focused behavior, real browser, component checks and durable KB update

Update existing core/API docs, KB index and append-only log. Do not change memory.
Record results and limitations in changes artifact.

<!-- rpi:phase id=P04 -->
### [ ] P04: Original Review and frozen gate handoff

Dependencies: P03.

<!-- rpi:task id=P04-T01 -->
#### [ ] P04-T01: Execute independent original Review, freeze commit and actual local gate

Original Review is immutable, including adverse findings; no repair/re-Review
loop. Commit candidate+all artifacts with current gh user noreply author and
committer/trailer. Run requested full 17-group gate and receipt verification,
with external output only and no later commit. Do not publish.

## Test Ownership Lock

* Canonical test owners: src/core/tests/test_resident_decisions.py and src/api/tests/test_resident_api.py.
* Exact removals: none. Maximum additions: 12 core test methods, 6 HTTP methods, one browser check script outside packages.
* Canonical source: existing resident_decisions/store/projection/continuity and panels.js; optional small shared helper only if clarity requires it.
* Generated targets: none; no snapshots/private data/stock replacement.
* Semantic proof: independent exact dependency manifests and negative-state comparisons; actual workflow-only priority generation, real stores/HTTP/browser, not mocked entire acceptance.
* Regression: preserve #86/#88/#406 tests; run existing surrounding component cases.
* Validation evidence: failing-first output in changes; focused runs and actual browser; full local runner external receipt after commit. Any opt-in SQL selector uses only gate-owned local disposable SQL.

## Dependencies

No explicit issue blocker. Local tools/SQL/browser/images/scans are required by
the final gate, not substitutes for human approval. Missing prerequisites block
publication but do not authorize cloud fallback. Base is fixed by caller.

## Critique Disposition

Original critique executed once, verdict Revise, seven findings preserved in its
immutable artifact. No second critique. All corrections are planner-owned.

| Finding | Disposition | Resolving implementation contract |
| --- | --- | --- |
| PC-001 | Applied to P02-T02/P01 | SQL writer rechecks correction dependencies for accept/edit, including workflow-only and cross-case policy; two-store interleave tests, no accepted audit on refusal |
| PC-002 | Applied to P02-T01/P01 | Hash source labels inside initial generation-input lock, carry unchanged; test intervening source change; label audience-specific citation snapshot, not raw source authority |
| PC-003 | Applied to P02-T01 | Open to one immutable terminal resolution; current-version second resolve denied; corrections cannot be erased |
| PC-004 | Applied to P02-T02/P01 | Explicit remove collection/catalog unless BOTH resident-view and reason rights; audit metadata only; export only stale flags, no challenge narrative |
| PC-005 | Applied to P01 | Require nonempty real accepted/edited review set; independent proposal IDs, case/hash and cross-case policy manifest; explanation/no-op and multiple-cause controls |
| PC-006 | Applied to P03 | Issue-specific JSON/SQLite proof only; existing native SQL gate is general regression, not issue-specific native acceptance; no false extra-selector SQL environment assumption |
| PC-007 | Conditional environment concern disposed | Parent shell can access requested /tmp tools (verified intake), not critique worker's claimed restricted file context. Use exact caller command, unchanged shared lock and fresh external directory. Missing preflight still blocks gate; never bypass or substitute receipt |

## Follow-Up Items

* Extend challenge bindings to other assistant/form paths only in separately reviewed scope; this bounded slice does not establish whole-system AC-071.
* Owner: qualified human/legal/RAI and accessible resident comprehension acceptance; no local synthetic substitute.
* Original Review RV-001: later rpi-implement restores reachability for older targets/open resolution forms without unbounded rendering; not repaired in this one-Review task.
* Original Review RV-002: eligible independent evidence verifier inspects original temporary-path logs/results; reviewer restriction does not establish a parent failure or a pass.

## Handoff

P01-P03 complete and reconciled with changes/details. One independent original
Review executed Partial / Not accepted; RV-001..004 remain routed, with no repair
or repeat Review. Candidate freeze and external exact-head gate follow.
Original critique remains Revise; applied dispositions are not a rewritten Pass.
P04 remains unchecked until its actual Review/freeze/gate obligations execute;
the external handoff, not a speculative committed pass, records post-freeze results.
Review defect does not erase executed implementation evidence or justify claiming
acceptance. Its unchanged original hash is recorded in changes and state.
