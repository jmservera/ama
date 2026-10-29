---
title: Masked chat question length plan
description: Bounded correction for issue 157 and PR 503
ms.date: 2026-10-29
---

# RPI Plan: chat-masked-length-157

## Task Metadata

* Task ID: 157-chat-masked-length-2026-10-29
* Task slug: chat-masked-length-157
* Planning status: Executed; independent critique Complete / Pass, Review Complete / Conformant
* Plan date: 2026-10-29
* Phase details: .copilot-tracking/details/2026-10-29/chat-masked-length-157-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/chat-masked-length-157-plan-critique.md

## Executive Summary

Reject questions whose redacted text exceeds the existing 1,000-character cap
instead of silently truncating them for dispatch. Extend the existing guard;
retain raw-length checking, refusal precedence and recorded fallback turns.
Add a regression and inclusive-boundary test, run focused chat suites and
project Ruff checks, obtain one independent Review and commit locally.

### What You May Not Know

The existing fallback persists both the masked question and workflow reply.
This fix preserves that behavior, and neither focused tests nor a local
commit establish a complete publication gate or live/hosted approval.
No implementation blockers or unresolved choices.

## User Decisions and Requirements

* Fix the masked-length finding in core chat_panel for #157 / #503.
* Add a below-limit raw input whose redaction exceeds 1,000 characters.
* Validate focused chat tests, ruff check and ruff format --check.
* Reuse feat/agent-chat-157; commit locally with Conventional Commit/trailer rules.
* Do not push, use az or hand-edit .github/rubric/scores/latest.json.
* Execute Research, Plan, Implement and Review with dated tracking artifacts.

## Goals

* Prevent model dispatch of a silently truncated redacted current question.
* Preserve accepted inputs and existing workflow-only fallback semantics.

## Scope and Non-Goals

In scope: core chat-panel guard, owning tests, directly related documentation
if an existing limit description needs clarification, dated RPI artifacts.
No cap, redaction, storage schema, UI, API contract or model-policy changes.
No publication, Azure, rubric score, SQL or unrelated fixes.

## Functional Requirements

* Either raw or masked length above MAX_QUESTION_CHARS returns LIMIT_REACHED.
* Return kind fallback, workflow-only model, empty citations and zero model calls.
* Keep existing refusal precedence, stored turns and audit metadata.
* Masked text at exactly the cap remains dispatchable in full.

## Non-Functional Requirements

* Reuse the current condition and fallback; no new dependencies or abstractions.
* Use existing installed editable src distributions and synthetic test fixtures.
* Preserve human/resident authority and existing privacy boundaries.

## Acceptance Criteria

* The 977 raw / 2,297 masked postcode fixture fails regression before the fix.
* After the fix, overflow never reaches the injected model in legacy case,
  general and all five advisory modes.
* A 989 raw / 1,000 masked question dispatches its complete masked text.
* Focused core/API chat tests and core Ruff lint/format checks pass.
* Independent critique and Review each execute once; original results retained.
* Candidate and evidence committed locally; no push or cloud actions.

## Implementation Context Record

| Item | Record |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-29/chat-masked-length-157-research.md; executed / Ready, C1-C5 |
| Plan/details | Metadata paths above |
| Critique | Complete / Pass, no findings; metadata critique path |
| Changes record | .copilot-tracking/changes/2026-10-29/chat-masked-length-157-changes.md, implementation owned |
| Continuation | Explicit full-loop request; manual mode, no automatic session |

## Sources

* Research C1-C5: raw-only admission, expanding redaction and truncating neutralisation.
* Existing StoredQuestionTests and API chat panel/isolation tests: owning fixtures.
* src/README.md: focused-first validation; full gate required before publication.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct question admission

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add regression and inclusive-boundary coverage

Add no more than two methods to StoredQuestionTests in
src/core/tests/test_chat_panel.py. Use a fresh case-bound thread per mode.
Observe actual raw/masked lengths, returned fallback and injected model calls.
Run the new overflow selector before production changes to preserve red evidence.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Extend the existing length guard

Add masked-length strict greater-than test beside the original condition in
src/core/src/zava_forward/core/chat_panel.py, before neutralise/model dispatch.
Clarify an existing limit description only if needed.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and preserve local delivery evidence

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run focused validation and reconcile evidence

Run focused core chat modules and API chat panel/isolation modules using their
existing test paths. Run core-wide `ruff check .` and `ruff format --check .`.
Record exact results and original red evidence in the changes artifact.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Independent Review and local commit

Obtain one independent rpi-review after implementation reconciliation.
Record execution, outcome and any routed findings. Commit the bounded fix and
all original dated evidence with authenticated privacy-safe identity and
Copilot co-author trailer. Do not push or claim a full publication gate.

## Dependencies

P01-T02 follows regression red run. P02-T01 follows both P01 tasks.
P02-T02 follows validation and reconciliation. Existing .venv provides Python
3.12.3, editable core and Ruff 0.17.1; no new dependencies.

## Test Ownership and Coverage Lock

* Owner: src/core/tests/test_chat_panel.py, StoredQuestionTests.
* Exact removals: none. Maximum additions: two test methods, subtests per mode.
* Canonical targets: chat_panel.py and owning tests; existing limit guide only.
* Generated targets: none; rubric latest.json remains untouched.
* Regression: actual 977/2,297 expansion with trailing semantic question.
* Semantic: inclusive 1,000 masked boundary retains full dispatched question.
* Validation: core test_chat_panel/test_chatthreads/test_chat_privacy/test_chat_memory;
  API test_chat_panel/test_chat_isolation; core-wide Ruff lint and format.

## Critique Disposition

Single independent final-candidate critique execution Complete, verdict Pass.
No findings or required decisions; candidate retained without changes.
Artifact: .copilot-tracking/reviews/plans/2026-10-29/chat-masked-length-157-plan-critique.md.
No repeat critique.

## Follow-Up Items

* Existing publication/hosted/human/activation gates remain outside this
  local-only task; no new follow-up implementation is authorized.

## Handoff

All implementation/validation complete: core chat 85/85, API chat 70 run with
one browser opt-in skip, core Ruff check/format and mypy pass. Single independent
Review Complete / Conformant, no findings; original record preserved.
P02-T02 delivery is persisted by the local commit containing this final record;
the parent verifies that commit and clean worktree immediately afterward.
No implementation blockers, material divergence or additional decisions.
No push, complete publication gate or hosted/human approval is claimed.
