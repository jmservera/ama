---
title: IoT Hub PR 557 fix cycle 1 research
description: Focused evidence for live scope guard regressions and bounded operator guidance
ms.date: 2026-10-29
---
<!-- markdownlint-disable-file -->

## Task Research

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher | RPI Agent, rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/iot-hub-live-140-pr557-fix-cycle-1-research.md |

## Research Brief

* Target: PR #557 fix cycle 1, issues #140/#184. Evaluate the live resource-group/requested-location/actual-location guard coverage and identify exact operator budget and cutoff wording.
* Purpose/audience: implementation and independent review of two supplied Copilot findings.
* Scope: infra live template, compiled evaluator/tests, publisher RunBudget and API operator documentation.
* Non-goals: Azure operations, secrets, runtime policy redesign, unrelated historical findings, score editing, publication or push.
* Criteria: positive and independently negative location/group cases, minLength assertions, bypass mutation rejection, precise two-message/one-per-second/60-second/cutoff instructions.
* Requested outputs: dated evidence, plan/critique, implementation and one Review, local commit.
* Output mode: convergence, preparing planning.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | Q1: How to exercise every live scope predicate and constraint? Q2: Which explicit RunBudget values and cutoff responsibility must operators observe? |
| Codebase scope | infra/iot-hub-live.bicep, infra/tests, src/api/README.md, IoT publisher/core stream contracts |
| External scope | None; supplied review findings and repository contracts |
| Initial internal candidate areas | Named files, prior IoT RPI artifacts, infra/API guides |
| Initial external candidate areas | None |
| Research posture | Focused |
| Posture provenance | Default for bounded caller-supplied failure evidence |
| Explicit limits | No Azure/secrets/push/score edits; /tmp/mv; caller-specified validation |
| Completion basis | Material questions answered with source evidence and in-scope counterexamples |
| Edits allowed | Evidence and state only during Research |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Match/provenance | Authority | Selection |
| --- | --- | --- | --- | --- |
| Instruction | Repository instructions | All input paths | Branch, evidence, validation and privacy constraints | Selected |
| Skill | rpi-research | Research phase | Three ordered evidence waves | Selected |
| Specialist | RPI Researcher | Available internal research specialist | Independent uncertainty only | Skipped: small tightly coupled source investigation, no separate lane needed |
| Skill | Web/design/security assessment | No UI changes or requested vulnerability audit | Not applicable | Skipped |

## User Participation and Research Decisions

| Checkpoint | Rationale | Answer | Decision |
| --- | --- | --- | --- |
| Intake | Precise supplied findings, scope, commands and local-only lifecycle; noninteractive execution | Explicit full-loop request | Execute all four authorized phases without inferring automatic mode |

## Scope and Success Criteria

Preserve production behavior unless evidence identifies a template defect. Verify compiled behavior, not source substrings alone. Preserve historical critique/Review evidence and distinguish local validation from live acceptance.

## Task Research Requests

Cover both review findings without changing the bounded runtime's general-purpose defaults.

## Direction Controls

| Control | Boundary | Source | Effect |
| --- | --- | --- | --- |
| Narrow | Two supplied Copilot findings | Owner 2026-10-29 | No unrelated fixes |
| Exclude | Azure operations, secrets, push, score edits | Owner 2026-10-29 | Local-only source and tests |

## Research Questions

| ID | Question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | Evaluate live group/location guards and constraints, rejecting bypasses | Depth | High | Answered |
| Q2 | Document explicit budget and cutoff boundary | Straightforward | High | Answered |

## Prior Knowledge Gate

Read original/addendum, reference index and owner memory. Prior task state remains manual Review/blocked with separate live/publication blockers; this child cycle does not overwrite that original outcome. Cross-session seven-day lookup returned no matching session. Starting HEAD is 3c04f84814052a7a552d4816a2fbd0834c1d3db8; PR #557 is open on the current branch.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline inspection identifies existing compiled scope/mutation helpers and the live profile's already-present combined requested/actual location check. API guidance explains activation but does not state the bounded exercise settings.

Reflection: prioritize evaluator context and independent negative cases; verify general RunBudget defaults before prescribing values. No external research or delegation needed.

#### Wave 2: Deeper

The existing evaluator accepts resourceGroup/reference contexts; use a synthetic actual hub with location independent of the requested parameter. Live guard parameter schemas carry minLength=1. Existing main/standalone scope assertions offer the local pattern: evaluate guard values, verify minLength, verify all child resources depend on the guard. RunBudget accepts 1..100000 messages and up to 3600 seconds/100 per second; its defaults are not this exercise's authority (C4-C7).

Reflection: isolate the three location states (requested westus/actual westus, requested uksouth/actual westus, requested westus/actual uksouth) so removing either conjunction clause or replacing AND with OR cannot survive. Add the separate non-ama group case and positive ama/uksouth/uksouth control.

#### Wave 3: Contrarian

Challenge: a wrong requested location combined only with a mismatching actual location would not prove the UK South clause. Use matching non-UK requested/actual locations as well. Constant-ok, removed parameters, weakened/missing minLength, dependency removal and individually bypassed location clauses should fail the same helper. Mutate compiled deep copies only, not source. The Bicep predicates are already correct; adding a redundant source guard or narrowing general-purpose runtime defaults would be unrelated behavior changes.

Reflection: documentation must distinguish monotonic per-run limits from calendar authorization. RunBudget/Pacer has no wall-clock cutoff. Explicitly require the operator to check UTC time and enough remaining window before each run and stop before 2026-11-01T00:00:00Z (through 31 October UTC), rather than imply code enforcement (C4-C8).

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Compiled live scope helper, independent cases and bypass mutations | C1-C2,C4 | Accepted | Tests the exact missing behavior without production drift |
| Explicit 2/1/60 budget plus operator cutoff responsibility | C3,C5-C8 | Accepted | Prevents mistaken use of permissive defaults |
| Change Bicep/runtime limits | C1,C5-C6 | Rejected | Existing template is correct; runtime supports broader separately approved uses |
| Live acceptance/publication repair | Prior parent state | Deferred | Outside two findings and prohibited Azure scope |

#### Cycle Re-entry Evaluation

No additional cycle needed: both material questions have source-backed answers, the contrarian cases strengthen isolation, and remaining sources would not change this bounded fix.

## Evidence Log

| ID | Claim | Location | Tool | Confidence |
| --- | --- | --- | --- | --- |
| C1 | Live guard already requires ama, requested uksouth and matching actual hub location | infra/iot-hub-live.bicep:12 | Read | High |
| C2 | Live tests evaluate SKU/units, while shared scope helper covers only main and standalone | infra/tests/test_iothub_module.py:60,511 | Read | High |
| C3 | Hub-only operator guidance lacks bounded budget settings | src/api/README.md:908 | Read | High |
| C4 | Evaluator supports injected resourceGroup/reference; dependency resolver is reusable | infra/tests/test_bicep_policy.py:123,181 | Read | High |
| C5 | RunBudget defaults to 100 messages/60 seconds/one per second and permits larger values | src/core/src/zava_forward/core/synthetic/sensor_stream.py:94 | Read | High |
| C6 | Pacer enforces monotonic deadline/rate, not calendar authority | src/core/src/zava_forward/core/synthetic/sensor_stream.py:235 | Read | High |
| C7 | Publisher validates budget and its supplied pacer; no date check | src/api/src/zava_forward/api/iot_stream.py:354 | Read | High |
| C8 | Prior accepted bounded plan requires at most two messages, 60 seconds and stop through October 31 | .copilot-tracking/plans/2026-10-29/iot-hub-live-140-plan.md:127 | Read; verified against supplied PR review comments | High |

## External Evidence

No external sources used.

## Findings, Alternatives and Decision State

Q1 selects a dedicated live-scope assertion reused by a positive/negative case test and a mutation test. Q2 selects concise operator prose adjacent to DeviceActivation, naming max_messages=2, max_per_second=1.0, max_seconds=60.0, required owner/cost/alert references and the UTC cutoff. No template or runtime change is necessary. No contradictions remain within these findings.

## Open Questions, Risks and Residual Uncertainty

Local tests cannot establish actual Hub deployment, transport, SQL delivery, resident gauges, credential authority or whole-issue acceptance. The parent task's adverse Review and publication blockers remain unchanged. No further research is necessary for this fix cycle.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready (C1-C8).

Self-check: both questions answered, three waves completed in order, stable evidence IDs resolve, alternatives and constraints recorded, no source changes or external/Azure requests, original artifacts preserved.

## Advisory Next Step

Active RPI parent proceeds to Plan under the owner's explicit full-loop request; this does not enter persistent automatic mode.
