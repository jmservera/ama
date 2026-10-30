<!-- markdownlint-disable-file -->
---
title: IoT Hub test strength research for PR 557
description: Focused evidence for resource-reference and diagnostic-identity mutation coverage
ms.date: 2026-10-29
---

## Research Brief

Investigate the two supplied test-strength findings in
`infra/tests/test_iothub_module.py` for maintainers of PR #557. Output mode:
convergence, preparing the explicitly requested Plan/Implement/Review phases.
Scope is test-only resource identity and diagnostic setting identity.
No production changes, Azure operations, push, rubric score edits, new
infrastructure or unrelated findings. Success means valid fixtures still pass
and mutations to each hub reference or the diagnostic name fail.

## Research Parameters

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Status | Complete |
| Posture | Focused, inferred from caller's named file and two findings |
| Internal candidates | IoT tests, shared ARM evaluator, live Bicep source, infra guide |
| External scope | None; GitHub PR metadata is lifecycle context only |
| Evidence root | .copilot-tracking/research/2026-10-29/ |
| Questions | Q1: How to bind both reference fixtures to the correct hub? Q2: How to pin and mutation-test the live diagnostic name? |
| Completion basis | All three focused waves, sufficient local evidence, no material unresolved question |

## Extension Registry and Provenance

| Extension | Selection and authority |
| --- | --- |
| Repository instructions | Selected: branch safeguards, test-only scope, dated evidence and local-only publication boundary |
| rpi-research | Selected: focused wider/deeper/contrarian cycle and evidence handoff |
| Domain skills | No web, accessibility, regulatory or security assessment needed for these test-only assertions |
| Research specialists | Skipped: a single continuous, small local trace is more appropriate inline |

## User Participation and Research Decisions

No clarification needed: caller supplies exact paths, expected identities,
mutation requirements, validation commands and exclusions. All four phase
advancements are explicitly requested, without starting an ongoing automatic
follow-up session.

## Direction Controls

* Preserve production templates and existing behavior.
* Run requested unittest selector from infra and Ruff on touched Python.
* Commit locally; never push, deploy, access Azure, or edit rubric scores.

## Prior Knowledge Gate

Read original/addendum, reference index and owner memory. Recent seven-day
session lookup returned no matching prior sessions. The user-supplied findings
are starting evidence to verify against current source, not assumed results.
The branch is clean and matches open PR #557 after the required initial pull.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Read the live and production diagnostic tests and live source. Both reported
gaps are present: fixtures accept arbitrary reference arguments, while only
the production diagnostic helper pins the setting name.
Reflection: focus the deeper wave on evaluator arguments and reusable test helpers.

#### Wave 2: Deeper

C4 confirms the evaluator passes the resource ID as the first positional
argument to the reference fixture. C6 provides existing local precedent for
a named reference function asserting its identifier before returning synthetic
properties. Extract the existing SKU/unit body into a template-taking assertion
helper, preserving its matrix and consumer-group coverage.
Reflection: direct fixture assertions suffice; no shared evaluator change needed.

#### Wave 3: Contrarian

Challenge: a mutation can fail for a removed clause rather than a wrong hub.
Keep each guard expression intact except for its resourceId hub-name argument;
assert the replacement changed the expression. Mutate SKU, units and location
independently, and match the expected/actual hub identifiers in the assertion
failure so unrelated errors cannot satisfy the regression. Pin the diagnostic
name in the existing helper and mutate only that field.
Reflection: valid fixtures plus isolated wrong-target mutations address both
false positives without widening production scope.

#### Parent Synthesis and Disposition

Accept named fixture functions with exact ID assertions (C1/C2/C4/C6).
Accept the live diagnostic name pin and name-only mutation (C3/C5).
Reject string-only reference-shape checks: they cannot prove the evaluated ID.
Reject shared evaluator changes: context fixtures own the contract and already
have a local precedent. No further research cycle needed: both questions have
specific implementation and validation evidence; remaining research is redundant.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | SKU/unit fixture ignores all reference arguments | infra/tests/test_iothub_module.py:92-118 | High |
| C2 | Location helper also ignores reference arguments | infra/tests/test_iothub_module.py:176-205 | High |
| C3 | Live diagnostics lack name assertion; production helper has one | infra/tests/test_iothub_module.py:135-174 and :573-592 | High |
| C4 | resourceId evaluator synthesizes /fixture/type/name and passes context reference calls | infra/tests/test_bicep_policy.py:123-176 | High |
| C5 | Live hub is existing and diagnostic name is to-log-analytics | infra/iot-hub-live.bicep:25-45 | High |
| C6 | Existing reference function asserts ID before returning properties | infra/tests/test_iothub_module.py:348-354 | High |

No external sources used. No contradictory source claims.

## Findings, Alternatives and Decision State

Q1 answered by C1/C2/C4/C6: assert
`/fixture/Microsoft.Devices/IotHubs/fixture` in each reference fixture before
returning its properties. Reuse a template-taking SKU/unit assertion helper.
Q2 answered by C3/C5: assert `to-log-analytics`, and extend existing live
diagnostic mutation coverage to a name-only mutation.

Selected recommendation: minimal changes to the named test file and dated RPI
evidence. Preserve existing mismatch matrices and existing-hub/consumer-group
coverage. All findings have high confidence from current local source.

## Risks and Validation Constraints

The test class requires local Azure CLI/Bicep compilation. This is offline
template compilation, not an Azure service operation. No login, deployment,
what-if or cloud request is authorized. Ruff is absent from PATH and the system
Python module; restore the repository-pinned version in an external isolated
environment before lint/format checks. No runtime/project installation is
necessary for these infrastructure-only standard-library tests.

## Current Decisions and Self-check

No unresolved implementation decisions. No delegated research or external
sources. Required three waves and alternatives are recorded, findings resolve
to stable local evidence IDs, and production writes remain excluded.

## Planning Readiness

Ready. Research disposition: executed, complete. Handoff: C1-C6, focused test-only
recommendation, no design blockers; next explicitly requested phase is Plan.
