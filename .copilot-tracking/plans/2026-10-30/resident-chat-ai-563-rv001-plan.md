---
title: Resident chat RV-001 implementation plan
description: Bounded follow-up to the original issue 563 review
ms.date: 2026-10-30
---

## Scope and Decisions

Task: issue-563-rv001, resident-chat-ai-563-rv001. Parent: issue-563,
resident-chat-ai-563. User explicitly selected RV-001 and requested Implement
then one independent Review, local commit, Refs #563 only, no push or Azure.
Reuse the clean active feat/resident-chat-ai-563 branch (no remote branch/PR).
Original parent critique and adverse Review remain immutable evidence.

Research is reused from the original Review RV-001 and current routing/HTTP
contracts. No new planning critique or product decision is needed for this
accepted bounded follow-up. No UI, model, accounting, consent or expiry changes.

Require positive household repair context, rather than a repair word alone.
Reject off-topic/instruction and report/contact-action requests before generated
dispatch. Preserve existing safety/legal/consent/appointment routes and the
enabled dead-rat observation. Informational repair-reporting questions may
explain how the resident can ask for help, but chat must not perform an action.
Ambiguous/unrecognised text keeps the deterministic unknown/human route.

Approved writes: chat.py, external tests in src/api/tests, directly related API
README wording and dated child RPI artifacts. No private data or cloud use.

## Implementation Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct host admission and prove the dispatch boundary
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Narrow repair routing and external regressions

Added negative direct-route and real loopback HTTP coverage for original RV-001
examples, household-context off-topic/instruction/action variants and protected
topics. Assert exact host responses and no advisor methods, reservation, token
or transport. Retain generated positive repair cases and disabled fallback.

Completion: 22 chat tests pass, including 30 exact host-route examples and ten
enabled generated repair examples. Existing disabled dead-rat fallback retained.
Admission is deliberately conservative: one household-linked observation or
informational clause; mixed requests and unrecognised wording remain host-owned.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and reconcile implementation evidence
<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Resident discovery, API Ruff/format and full mypy

Depends on P01-T01. Use installed source distributions with the README test
paths; preserve logs externally, including initial failures and existing skips.
No browser rerun required for this backend-only routing correction.

Completion: resident discovery 149 run, 142 passed, six existing opt-in SQL
skips and one existing opt-in browser skip; API Ruff lint/format (59 files) and
full mypy (113 files) pass. Diff whitespace passes. External logs are listed
in the changes record.

<!-- rpi:phase id=P03 -->
### [ ] P03: Independent Review and local persistence
<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Review once, preserve outcome and commit locally

Depends on P02-T01. Review this follow-up's exact diff and evidence, not the
parent Review again. Preserve findings without a same-task correction loop.
Resolve GitHub noreply identity, use required Copilot trailer and Refs #563.
Attempt the repository full local gate after committing, with external output;
record blockers honestly. No push, merge, rebase or Azure.

## Follow-Up Items

Parent RV-002 actual-model/live activation and RV-003 human/content/AT approval
remain outside scope. Publication requires a fresh complete local receipt and
hosted/human approval. The parent's original advanced-main ancestry failure is
historical; fresh fetch shows origin/main f7482602 is already an ancestor of
this branch. This does not establish a passing current full gate.

## Review Handoff

P01/P02 complete with bounded local evidence. No implementation blocker or
material product decision. Original critique Pass and parent Review Not accepted
remain unchanged. P03 Review/local persistence remains unchecked until executed.
No actual-model, Azure, live browser or human/AT acceptance is claimed.

## Executed Review and Routed Implementation

Independent Review executed once: Complete / Not accepted, resident-chat-ai-563-rv001-review.md.
It found comma/then continuations escaping partial matching. Preserve that
outcome; no repeat Review. Routed RV-001 is implemented separately by
resident-chat-ai-563-complete-admission, within the original user direction.
This plan describes the reviewed intermediate candidate, not final-source
acceptance. P03 local persistence and subsequent gate attempt remain pending.
