<!-- markdownlint-disable-file -->
---
title: Resident chat 520 proposal expiry follow-up research
description: Bounded research for PR 525 proposal expiry review feedback
ms.date: 2026-10-28
---

# Task Research: resident-chat-520-expiry-followup

| Field | Value |
| --- | --- |
| Date | 2026-10-28 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-28/resident-chat-520-expiry-followup-research.md |

## Research Brief

* What to research: the proposal-expiry race in Agenda.book and a deterministic regression.
* Why it matters: expired resident callback proposals must not become committed bookings.
* Audience or intended use: implementation and independent review of PR #525.
* Scope: agenda backend, resident-demo unit/API tests, local validation and review thread.
* Non-goals: new chat features, UI changes, real appointments, deployments and whole-issue acceptance.
* Criteria: minimal fix, one fresh final instant for both deadlines, transactional rollback,
  no sleeping, preserved idempotency and authorization behavior.
* Requested outputs: dated RPI artifacts, tested fix, normal push and review-thread resolution.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Which deadlines must be selected and rechecked; how to prove rollback? |
| Codebase scope | src/api resident_demo agenda and tests; component validation guides |
| External scope | PR #525 and issue #520 metadata only |
| Initial internal candidate areas | agenda.py, resident-demo tests, previous 520 artifacts |
| Initial external candidate areas | PRRT_kwDOUU8JX86xTMcu |
| Research posture | focused |
| Posture provenance | Default for named code target and supplied failure evidence |
| Explicit limits / deadline | Heavy steps hold /tmp/ama-rpi-heavy.lock, nonblocking retries every 60s up to 40min; no az |
| Posture-specific completion basis | Focused scope, verified transaction and test coverage |
| Edits allowed during research? | Research artifacts and lifecycle state only |
| Resolved evidence root | .copilot-tracking/ |
| Known constraints / excluded sources | No secrets, .env, private data, merge, deploy, force push |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selection |
| --- | --- | --- | --- | --- |
| Instruction | Repository instructions | Supplied, all files | Branch, evidence, validation and privacy rules | Selected |
| Skill | rpi-research | RPI lifecycle | Three-wave evidence synthesis | Selected |
| Skill | Web design skills | Backend-only task | No web edits planned | Skipped |
| Research specialist | RPI Researcher | Registered host agent | Independent research lane | Skipped: single tightly coupled trace |

## User Participation and Research Decisions

The owner explicitly requests the full loop and gives the exact defect, branch, PR,
publication action and restrictions. No scope or phase question is needed; no interaction
is available. Initial worktree is clean and PR #525 is open on the requested branch.

## Scope and Success Criteria

Prove that a proposal valid when confirmation starts is rejected if authorization crosses
its expiry, even while the slot remains in the future. Verify rollback and existing
resident-demo behavior; keep the unavailable full gate separate from scoped checks.

## Task Research Requests

Fix, regression, resident-demo unit/API tests, ruff at 100 columns, mypy, dated RPI evidence,
fetch and reconcile any remote bot commit, Conventional Commit, normal push, then reply
and resolve only the specified thread.

## Direction Controls

Only the proposal-expiry follow-up is in scope. Existing issue #520 implementation and
historical RPI outcomes remain unchanged. The full gate is blocked by the explicit az bar.

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | How does booking revalidation interact with rollback and authorization? | straightforward | H | Answered |
| Q2 | Which existing tests and commands cover this race without sleep? | straightforward | H | Answered |

## Prior Knowledge Gate

Supplied head and review thread verified using git and gh. Prior 520 artifacts are
starting evidence to inspect, not fresh validation.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Read component/source validation guides, owning agenda/API tests and prior correction
research/changes. The caller-supplied head and unresolved thread match actual git/gh.
Reflection: scope is a backend booking fix, not a new resident-chat feature; the existing
unit fixture owns a disposable SQLite agenda and already injects a two-instant clock.

#### Wave 2: Deeper

Traced Agenda.book and the API call site. The initial query filters expires and starts,
but selects only slot fields. After INSERT and authorization, the second clock checks only
starts. The context manager rolls back raised exceptions. HTTP passes app.now as a callable.
Reflection: select o.expires and reuse one fresh final instant for both comparisons;
add a unit test crossing expiry during authorization while starts remains future.

#### Wave 3: Contrarian

Checked the prior-booking path and existing expiry/slot-start tests. Existing bookings
must remain idempotent even after proposal expiry, and static datetime callers must
remain supported. Existing tests cover exact expiry at initial lookup, exact slot start
at final check, owner isolation, double booking and authorization rollback, but not
expiry crossing during confirmation.
Reflection: do not modify idempotency or require an API/clock signature change.
Reject rechecking only the initial instant (stale) or checking before authorization
(retains the race). A fresh read before return is the established transaction boundary.

#### Parent Synthesis and Disposition

Accept C1-C4/W1: select expiry and compare both deadlines against one final instant.
Accept C5: use existing project lint/type configuration and synthetic test selectors.
Reject sleep-based reproduction and broad refactoring; neither improves correctness.
No independent research lanes: the work is one continuous trace.

#### Cycle Re-entry Evaluation

No further cycle required: focused questions answered, existing patterns verified,
contrarian checks reveal no design uncertainty. Validation is still pending, not passed.

## Evidence Log

### Codebase Evidence

| ID | Claim / finding | Location | Tool | Confidence |
| --- | --- | --- | --- | --- |
| C1 | Final booking check only rechecks slot start | src/api/src/zava_forward/api/resident_demo/agenda.py:199 | read | High |
| C2 | Transaction rolls back exceptions, including final conflict | src/api/src/zava_forward/api/resident_demo/agenda.py:38 | read | High |
| C3 | Existing test injects clock across slot start | src/api/tests/test_resident_chat_agenda.py:107 | read | High |
| C4 | API supplies fresh callable clock and maps conflicts to 409 | src/api/src/zava_forward/api/resident_demo/app.py:519 | read | High |
| C5 | Ruff100 and strict package mypy are configured | src/api/pyproject.toml:35 | read | High |
| C6 | Source guide distinguishes focused checks from complete gate | src/README.md:66 | read | High |

### External Evidence

| ID | Claim / finding | Source | URL | Retrieved | Confidence |
| --- | --- | --- | --- | --- | --- |
| W1 | Unresolved review requests fresh expiry and slot checks | PR #525 thread | https://github.com/jmservera/ama/pull/525#discussion_r4405500634 | 2026-10-28 | High |

## Planning Readiness

Ready. Research disposition: executed. Q1: C1/C2/C4; Q2: C3/C5/C6.
Select the smallest query/final-check edit and a deterministic authorization-driven clock
regression covering just-before, exact and after expiry, including persisted rollback
and slot availability. Preserve static-clock support and committed-booking idempotency.

## Alternatives and Decision State

Selected: existing callable clock, o.expires selection, one final timestamp and <= checks.
Rejected: wall-clock sleeps (flaky), schema change (unnecessary), final query outside the
transaction (breaks atomicity), global clock replacement (existing injection suffices).
Confirmed owner constraints supersede older nonqueued-lock and no-publication handoffs
for this bounded fix only; no historical outcome is rewritten.

## Open Questions, Risks, and Residual Uncertainty

No implementation-blocking uncertainty. Tools ruff/mypy are missing from the current
Python environment; restore manifest-pinned dev dependencies in an isolated external
environment after these actual missing-tool results. The full gate remains blocked
because az is barred; no receipt or whole-feature acceptance may be claimed.

## Current Decisions

Use the requested active topic branch; keep backend scope, held heavy lock with 60-second
nonblocking retries and 40-minute admission limit. Publish scoped-tested narrow fix,
then reply and resolve W1. No browser-facing code planned, so no browser harness.

## Unresolved Decisions and Potential Next Research

None for this fix. Complete full gate only under later authorization permitting its
prerequisites. Human/AT and hosted acceptance remain separate existing gates.

## Closeout Record and Advisory Next Step

Research Complete; Wider, Deeper and Contrarian executed inline; disposition executed;
Planning Readiness Ready. Automatic parent continues to Plan after persisting transition.
Artifact self-check passed: evidence, alternatives, constraints, uncertainty and
continuation recorded. Research wrote only evidence/state and ran no implementation.

## Sources

* W1: https://github.com/jmservera/ama/pull/525#discussion_r4405500634
* C1-C6: workspace-relative paths in the Codebase Evidence table.
