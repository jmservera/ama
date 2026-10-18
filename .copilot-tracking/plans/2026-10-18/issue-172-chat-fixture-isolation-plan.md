<!-- markdownlint-disable-file -->
# RPI Plan: issue-172-chat-fixture-isolation

## Task Metadata

* Task ID: 172
* Task slug: issue-172-chat-fixture-isolation
* Plan date: 2026-10-18
* Planning status: Ready; single independent critique executed, original Pass
* Phase details: .copilot-tracking/details/2026-10-18/issue-172-chat-fixture-isolation-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-18/issue-172-chat-fixture-isolation-plan-critique.md

## Executive Summary

Make the existing synthetic fixture coverage resource-specific, and add explicit
denial expectations for both contractors reading, listing and searching a valid
eligible staff owner's active thread. No runtime authority or eligibility changes.

### User Decisions and Requirements Highlights

Preserve public-only synthetic data and all lifecycle/privacy controls. Run one
independent critique before implementation and one original independent Review
afterwards, preserving adverse verdicts and routing later defects.

### What You May Not Know

The baseline passes 11 focused tests. The claimed contradiction is not a failure:
the eleven-perspective assertion includes memory. Actual eligible thread owners
cover seven perspectives (14 users); other staff roles as well as contractors
lack assistant tasks. One contractor already has an incidental read denial.

### Unresolved Decisions or Blockers

No bounded engineering blocker. SN-08 scope/volume and OD-45 to OD-49 remain
unverified/open, outside this plan. #172 remains open.

## User Decisions and Requirements

* Execute actual ordered Research, Plan with exactly one critique, Implement and
  exactly one original Review; commit all dated artifacts in the same PR.
* Work on caller branch from supplied base; Refs #172 only, no closure or AC edits.
* Preserve 22 personas, eleven perspectives and existing app-role/task mappings;
  no contractor-owned threads or contractor eligible chat.
* Derive owner coverage from eligible personas; add explicit contractor actor
  read/list/search denials with real targets and mutation-sensitive coverage.
* Preserve deterministic seeds, nine synthetic payloads, null deleted content,
  opt-in/withdrawal semantics and metadata-only retained ledger.
* Never read private inputs, modify runtime/UI/mvp, approve policy/volume, resume
  #122/draft #398, or run paid rubric/inference/cloud operations.
* Original adverse Review blocks publication and routes coordinator corrections
  (maximum two); do not repeat Review or self-certify acceptance.

## Goals

Make missing fixture denial coverage detectable without conflating persona
representation, eligible thread ownership and declarative runtime expectations.

## Scope and Non-Goals

In scope: `src/agents/tests/chat_fixture.py`, `test_chat_fixture.py`, necessary
existing provenance/role regressions only if coupled, data dictionary, component
README, KB index/log and RPI artifacts. Non-goals: runtime, mapping changes,
new payload families, stored snapshot refresh, whole-issue acceptance.

## Functional Requirements

* Existing same-role thread probes cover every eligible user and no ineligible
  user as owner; preserve separate existing memory perspective coverage.
* Add `contractor_access_denied` cases for both contractor personas, each with
  read/list/search expected deny against a real active eligible staff thread.
* Assert actor/owner differ, actor is contractor, owner/task are eligible, target
  ID resolves to the declared owner, and no contractor owns a thread.

## Non-Functional Requirements

* Same seed yields identical manifest/all payload bytes; changed seed changes data.
* Keep schema and role/task mapping stable, no new dependencies or runtime access.
* Fresh temporary generation only; hash generated outputs with existing `write()`.
  No tracked chat source hash exists; unrelated frozen hashes/reports stay intact.

## Acceptance Criteria

* Focused fixture/provenance/roles tests pass, including a failing-first coverage
  test and a mutation test that removes each required contractor action and fails
  the shared coverage assertion.
* Exact eligible-owner sets and legitimate targets checked independently of probe
  construction, with active target to avoid denial passing merely due to expiry.
* Existing nine-payload rehashed label/email mutations and lifecycle tests pass.
* Agents discovery and existing Ruff lint/format/mypy gates pass using current
  migration exclusions; report exclusions rather than claiming new strict typing.
* Public provenance/scenario metadata regressions pass without rewriting snapshots.
* Original Review independently records actual execution and verdict.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-18/issue-172-chat-fixture-isolation-research.md
Changes (created in Implement): .copilot-tracking/changes/2026-10-18/issue-172-chat-fixture-isolation-changes.md
Review: .copilot-tracking/reviews/logs/2026-10-18/issue-172-chat-fixture-isolation-review.md
Continuation: explicitly caller-authorized automatic parent loop.

## Sources

Research C1-C5 and W1-W5; current helper/tests; source CI and agents README.
Baseline command from root:
`PYTHONPATH="$PWD/src/core/tests:$PWD/src/agents/tests:$PWD/src/api/tests" .venv/bin/python -m unittest test_chat_fixture test_chat_provenance test_chat_fixture_roles -q`.
It passed 11 tests after missing-package recovery via editable pip in `.venv`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Strengthen fixture contracts

Dependency: Research Ready and exactly one critique disposed.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Establish resource-specific and contractor coverage tests

Split existing isolation coverage without removing existing assertions. Add exact
eligible thread-owner checks and shared contractor assertion used by a production-
fixture test and removal/invalid-target mutation tests. Record pre-fix failure.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Generate explicit contractor denials

Depends on P01-T01. Select a deterministic active thread with eligible owner from
existing generated threads; emit three denial actions per contractor, no owner
or eligibility fabrication. Absence of a legitimate target must raise an explicit
error, not silently skip probes. Preserve existing payload content/lifecycle.

<!-- rpi:phase id=P02 -->
### [x] P02: Document and validate bounded evidence

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update directly related evidence and run local checks

Depends on P01. Document seven eligible perspectives versus eleven personas,
declarative denial limits, SN-08 partial and approval boundaries. Run focused
tests, agents discovery, agents lint/format/mypy, relevant public core tests and
`python3 tools/rename-zava-tests.py` if applicable to source metadata. No live
SQL/Azure/model/browser tests apply to fixture-only changes.

<!-- rpi:phase id=P03 -->
### [ ] P03: Original independent Review and publication gate

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Run one original Review

Depends on P02. Fresh independent worker activates rpi-review and writes only the
single original Review artifact. If Not accepted, freeze local evidence and stop
for coordinator; no correction/re-review here. If accepted, commit own files and
all artifacts, normal push, main PR with Refs #172 and explicit partial limits.

## Locked Test Ownership and Targets

Parent owns helper and existing test file. Removals: none. Maximum additions:
six test methods in `test_chat_fixture.py`; reuse existing test class/assertion
helpers, not new test files or frameworks. Canonical source targets listed above.
Generated targets: nine JSONL payloads + ephemeral manifest in temporary dirs;
never tracked. Semantic coverage: owner eligibility and contractor action/target
matrix. Regression coverage: lifecycle, seed, synthetic labels/pattern canaries,
role equality and public provenance. Commands/results recorded in changes.

## Dependencies

#158 closed/ADR 0004 accepted as written October 15 in merged #279.
#167 hierarchy only. OD-45 to OD-49 and SN-08 approval not assumed satisfied.

## Critique Disposition

Independent final-candidate critique executed once by
`issue172-independent-critique`: original Pass, zero findings. No dispositions
or significant decisions remain open. Preserve the critique as written.
Per-actor/action removal mutations and all-payload byte comparisons remain
explicit implementation obligations, not evidence of already completed work.

## Follow-Up Items

* SN-08 approved scope/volume remains an owner/coordinator decision, not engineering.
* Runtime enforcement and human privacy/retention approval remain separate evidence.

## Handoff

P01/P02 implementation and validation complete; ready for parent P03-T01 original
independent Review. No source changes were made during planning. Original
independent critique is complete and requires no corrections or second critique.
No implementation amendment or divergence occurred.
