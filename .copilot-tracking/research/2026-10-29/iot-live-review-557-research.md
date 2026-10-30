---
title: PR 557 live IoT review correction research
description: Focused evidence for compiled diagnostics targets and one-run exercise guidance
ms.date: 2026-10-29
---

## Research Brief

Correct the two owner-supplied Copilot findings on PR #557, Refs #140 #184.
Audience: implementer and independent reviewer. Output mode: convergence,
preparing planning. Scope: compiled live-profile hub/workspace assertions,
target-changing mutations, and documentation restricting the bounded publisher
exercise to one run without retries absent separate owner approval.
Non-goals: deployment, transport changes, cumulative publisher accounting,
rubric-score edits, push or live Azure activity.

## Research Parameters

Focused posture, selected because the owner names both defects and prior art.
Initial questions: what compiled expressions identify the diagnostic scope and
workspace; how existing mutation assertions work; whether documentation alone
can safely restrict publisher calls. Internal candidates: infra live profile,
IoT test modules, API README and publisher implementation. External candidates:
none needed for these local contracts.

## Direction Controls and Extensions

Repository instructions and RPI phase skills apply. Research is inline because
the evidence is tightly coupled and bounded. No research specialist is needed.
Web/design, regulatory and Azure skills are not applicable to this test/docs
correction. Interaction is unnecessary: scope and acceptance are explicit.
Prior-knowledge gate: supplied findings remain claims to verify against source;
recent branch history search returned no session results.

## Research Cycle Log

Cycle 1 completed inline, in order:

1. Wider: inspected the live Bicep, existing shared IoT compiled tests and API
   exercise guidance. The live profile is already correctly wired; the missing
   protection is in tests, not infrastructure (C1-C3).
2. Deeper: locally compiled the profile and inspected the exact ARM expressions;
   read the publisher's fresh-pacer construction and the existing diagnostic
   mutation helper pattern (C1-C4). Baseline discovery passed 18 tests with no
   skips. Ruff is missing from PATH and `python3 -m ruff`.
3. Contrarian: checked whether restricting calls alone would leave replay
   advice contradicting the boundary. The same section explicitly recommends
   rerunning uncertain deliveries (C5), so both paragraphs need correction.
   The receiver's retained-history/SQL replay is a distinct mechanism and must
   remain intact. A supplied pacer is not evidence of cumulative message
   accounting and is not offered as a workaround. Existing historical RPI
   state has a failed full publication gate; it is not current passing evidence.

## Evidence Log

Opening source: clean HEAD `27f7b2d0c6b3b13a59dbb886379a5b615566d394`,
local origin/main `7fb58c4b7fe425408731537e3f213c97a7317937`.
`git pull --rebase` reported already up to date; PR #557 is open on the requested
branch. No source changes have been made.

* C1: `infra/iot-hub-live.bicep:21-45` names existing workspace
  `log-cutover-test` and hub parameter `name`. Local compilation returns scope
  `[resourceId('Microsoft.Devices/IotHubs', parameters('name'))]` and workspace
  `[resourceId('Microsoft.OperationalInsights/workspaces', 'log-cutover-test')]`.
* C2: `infra/tests/test_iothub_module.py:62-84` checks live categories but neither
  target. `:40-46` already pins the allowed hub name.
* C3: `infra/tests/test_iothub_module.py:488-525` provides a reusable style:
  helper assertions, a positive test and deepcopy/subTest mutations expecting
  AssertionError. `infra/tests/test_bicep_policy.py:92-102` compiles locally
  through `az bicep build`; this performs no Azure operation.
* C4: `src/api/src/zava_forward/api/iot_stream.py:354-376` validates the budget
  then constructs `pacer or Pacer(...)` per call. Runtime changes are unnecessary
  for an explicitly single-call, operator-controlled exercise.
* C5: `src/api/README.md:913-922,979-985` says "Before each run" and recommends
  rerunning identical frames after uncertain delivery. Both contradict one
  approved two-message allowance across the entire bounded exercise.

## Findings Mapped to Questions and Evidence

Q1 answered by C1-C3: assert the complete compiled diagnostic scope and
workspace expressions using the intended hub parameter and exact workspace.
Mutations must separately change scope and workspace with other fields intact.
Q2 answered by C4-C5: explicitly authorize ONE `HubPublisher.run()` call total,
no repeated/concurrent calls (including another instance/process), and no retry
after uncertain delivery without separate owner approval and accounting.
Preserve the cutoff, rate, duration and all wider approval boundaries.

## Alternatives and Decision State

Prefer the requested docs-only exercise restriction over publisher changes if
the source confirms per-call pacing. Accepted: it does (C4). Reject a new shared
runtime accounting layer as unnecessary scope. Preserve production module tests
and receiver recovery documentation; they are not this finding.

## Risks and Residual Uncertainty

These are local test/documentation corrections, not enforcement of a cross-call
runtime quota, authorization to send or proof of live acceptance. Full-gate
eligibility and inherited live blockers remain separate from requested tests.
No new knowledge-base fact requires an index/log update: durable implementation
guidance belongs in the existing API README.

## Planning Readiness

Ready. Research disposition: executed, Complete. No unanswered material
question warrants another focused cycle. Self-check: questions answered,
source IDs and exact expressions captured, all three waves and alternatives
recorded, no source changes or external calls made.
