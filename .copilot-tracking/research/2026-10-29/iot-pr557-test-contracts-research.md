---
title: PR 557 IoT test contracts research
description: Focused evidence for the two remaining compiled-test findings
ms.date: 2026-10-29
---
<!-- markdownlint-disable-file -->

# Task Research: iot-pr557-test-contracts

## Research Brief

Research the missing live parameter compilation coverage and suffix-only
consumer-group assertion for PR #557. Audience: implementer and independent
reviewer. Output mode: convergence, preparing planning. Scope: infrastructure
tests and dated RPI evidence only. No production changes, Azure operations,
pushes, scorecard edits or unrelated review findings.

## Research Parameters

Focused posture, selected from the caller's two named findings. Internal
candidates: infra/tests/test_bicep_policy.py, infra/tests/test_iothub_module.py,
infra/iot-hub-live.bicepparam and its referenced template. External candidate:
PR #557 comments only. Evidence root: .copilot-tracking/. Research is read-only
outside its evidence and workflow state.

## Extension Registry and Provenance

Repository instructions and retention policy selected for evidence, branch
and validation boundaries. rpi-research selected for the research contract.
Research specialists skipped: the questions form one small continuous trace.
No web/UI, Azure or new regulatory research applies.

## User Participation and Direction Controls

The user explicitly requests the full Research, Plan, Implement, Review loop,
local commit, no push, no Azure and no scorecard edit. No clarification is
necessary or available. Run all four phases as explicitly directed, without
inferring consent to an ongoing automatic follow-up session.

## Scope and Success Criteria

* Compile the live bicepparam locally and assert its template and exact values.
* Evaluate and assert the complete live consumer-group name.
* Prove wrong-hub mutations fail; run requested unittest selectors and Ruff.
* Preserve original independent critique and Review evidence.

## Research Questions and Prior Knowledge Gate

Q1: Which existing build-params convention and output shape should be reused?
Q2: Which evaluator/fixture supplies the complete consumer-group name?
Both are straightforward, coupled questions investigated inline.
The supplied findings were verified against PR #557's current comments.
Required case-study, addendum, knowledge-base index, owner memory, infrastructure
guide and tracking retention policy were consulted. Existing historical RPI
evidence will not be overwritten.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

PR #557 is OPEN on feat/iot-hub-live-140 against main. The worktree was clean;
the first shell command ran git pull --rebase successfully, already up to date.
The live profile is a separate existing-hub template rather than a fourth main
environment. Existing parameter compilation is in test_bicep_policy.py.
Reflection: keep live coverage separate from main-profile assertions.

#### Wave 2: Deeper

Local `az bicep build-params --stdout` returns parametersJson and templateJson
strings. Compare the latter's parsed object to the existing independently
compiled self.live fixture, not a fragile source substring. The existing values
helper supplies hub name fixture; evaluate accepts format expressions and absent
variables via an empty dictionary. Ruff is missing from system Python.
Reflection: reuse existing subprocess, JSON and evaluator conventions.

#### Wave 3: Contrarian

A wrong hub with the same /events/api-consumer suffix passes the old assertion.
An equality against fixture/events/api-consumer rejects that case. Literal-source
checks do not prove build-params resolves the intended template; comparing the
emitted template does. Keep live profile separate from main environment loops
because it does not have workload/environmentName/main-profile parameters.
Reflection: add one positive build-params test, one full-name positive contract
and bounded wrong-hub/group mutation checks; no general helper refactor needed.

Parent synthesis: accept compiled-object comparison and exact evaluated names;
reject suffix-only and source-only alternatives. No further research cycle is
needed: both questions and relevant output shapes are directly verified.

## Evidence Log

| ID | Source | Evidence |
| --- | --- | --- |
| C1 | infra/iot-hub-live.bicepparam:1-9 | using iot-hub-live.bicep; name iot-cutover-test-rzsrg, location uksouth, SKU B1, unitCount 1 |
| C2 | infra/tests/test_iothub_module.py:85-86 | Current assertion only checks /events/api-consumer substring |
| C3 | infra/tests/test_bicep_policy.py:615-630 | Existing main-profile build-params coverage discovered |
| C4 | infra/tests/test_iothub_module.py:206-213 | values helper supplies fixture hub and template defaults |
| C5 | infra/tests/test_iothub_module.py:606-610 | Existing production exact evaluated full-name assertion |
| C6 | infra/tests/test_bicep_policy.py:118-155 | Existing evaluator handles strings and ARM format expressions |
| W1 | https://github.com/jmservera/ama/pull/557 | Retrieved 2026-10-29 through gh: two requested findings confirmed |

## Findings, Alternatives and Decision State

Q1 answered by C1/C3 and the successful local compiler probe: reuse build-params
and JSON decoding, assert emitted template equals self.live and parameters equal
the four approved entries. Q2 answered by C2/C4/C5/C6: evaluate with self.values
and compare to fixture/events/api-consumer. Use mutations to reject both wrong hub
and wrong group, preserving the existing mutation-test convention.
Selected approach is the smallest compiled-contract test change. No source
changes during research. No unresolved decision or research blocker.

## Planning Readiness

Ready. Research disposition: executed, complete. Evidence C1-C6 and W1 covers
both questions. Self-check: source pointers, caller boundaries, all three waves,
alternatives and readiness recorded. Parent proceeds to the explicitly requested
Plan phase; no ongoing automatic follow-up session is authorized.
