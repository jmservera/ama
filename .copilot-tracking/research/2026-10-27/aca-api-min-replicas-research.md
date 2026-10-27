<!-- markdownlint-disable-file -->
---
title: API minimum replicas research
description: Focused evidence for cost-safe demo scaling
ms.date: 2026-10-27
---

# Task Research: aca-api-min-replicas

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-27/aca-api-min-replicas-research.md |

## Research Brief

* Target: API minimum replicas in `infra/modules/containerapps.bicep`, its callers, parameter files, documentation and offline tests.
* Purpose / audience: give the owner a demo-safe default of 0 with production opt-in to 2, preserving other infrastructure.
* Scope: existing Bicep scaling configuration and directly related validation.
* Non-goals: Azure deployment, secrets, full local gate, unrelated infrastructure.
* Criteria: default 0 reaches API scale; production 2 is configurable; other scale properties stay unchanged.
* Requested outputs: dated research, plan, changes and independent Review, committed on `fix/aca-api-min-replicas`, pushed with a main-targeting PR using Refs only.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | Which entry points need forwarding; which offline checks prove defaults and overrides? |
| Codebase scope | infra/, tools/rpi-checks.py and applicable repository instructions |
| External scope | None; no cloud calls needed |
| Initial internal candidate areas | containerapps.bicep, its callers, parameter files, infra README and tests |
| Initial external candidate areas | None |
| Research posture / provenance | focused / bounded caller task |
| Limits | Existing infra tests and az bicep build; no deployment or full gate; pip only if needed |
| Completion basis | Material questions answered with local evidence |
| Edits allowed | Research evidence and workflow state only |
| Evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Provenance / authority | Disposition |
| --- | --- | --- | --- |
| Instruction | Repository instructions | Supplied AMA guidance and .github/copilot-instructions.md | Selected: branch, privacy and component conventions |
| Skill | rpi-research | Active RPI phase | Selected: focused three-wave evidence |
| Specialist | hve-core-all:rpi-researcher | Host-registered independent research worker | Skipped: one tightly coupled, small trace |
| Skills | UI, regulatory and security assessments | No corresponding task surface | Skipped: infrastructure scaling only |

## User Participation and Research Decisions

The explicit full-loop request authorizes ordered phase progression and the named
commit/push/PR actions without routine prompts. Non-interactive execution is
required. The caller excludes the full gate. The repository publication
requirement still requires it for infrastructure changes, so local
implementation/commit may proceed but push/PR are blocked without that gate.

## Scope and Success Criteria

Verify the supplied hardcode against source. Preserve existing HTTP scaling,
maximum replicas, agent scale and jobs. Inspect only tracked configuration, never
private datasets or secrets. Initial worktree is clean, on the requested branch,
at `4bd06495651e58e9957ace590880006eedb8047a`, equal to fetched origin/main;
no existing PR was found.

## Task Research Requests

Implement a clearly described integer parameter defaulting to 0; forward every
relevant entry point; document production 2 and cold starts; update infra checks.

## Direction Controls

| Control | Source | Effect |
| --- | --- | --- |
| Narrow | Owner task | API minimum only; preserve everything else |
| Exclude | Owner task | No Azure deployment, full gate, secret reads or uv |
| Publish | Owner task | Topic branch only; PR to main with Refs wording |

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What is the complete module/parameter path? | depth | Answered |
| Q2 | What existing tests/builds cover it without cloud execution? | straightforward | Answered |
| Q3 | What bounds and production behavior preserve existing scale contracts? | depth | Answered |

## Prior Knowledge Gate

Read original case study, addendum, reference index and owner memory for context.
Owner's deployed-minimum claim is supplied direction, not independently verified
live evidence; no live inspection is needed. Verified API hardcode is 2 and
agents minimum is 0 in source.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline inspection found one module caller (`main.bicep`) and three committed
parameter examples. The separate resident demo does not call this module.
Reflection: forward the input through main; keep the standalone demo unchanged.

#### Wave 2: Deeper

Prioritized compiled-template policy tests and the resident-demo separation
test. Existing policy tests already assert the API hardcode and compile main.
The deployment wrapper passes parameter files through to ARM, requiring no new
wrapper option. Reflection: test the full compiled parameter chain and parameter
files rather than only matching source text.

#### Wave 3: Contrarian

Challenged automatic production minimum 2 and unbounded integer inputs.
Production security profile is independent of demo cost; setting a profile
must not silently raise minimum replicas. Accept 0 through the unchanged maximum
4, with explicit production 2 in a private parameter copy. Preserve committed
dev/test/pilot cost-safe values at 0. Found a stale resident-demo assertion and
README claim of a fixed two-replica main API; both need reconciliation.
The changed-path runner selects more than infra and requires clean committed
input/tool identity. Direct README infra commands give the requested bounded
validation without claiming a gate receipt. Reflection: local readiness is
Ready, while publication remains separately blocked by the full-gate conflict.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| apiMinReplicas int default 0, bounds 0..4, forward main | C1-C3 | Accepted | Meets owner cost direction without changing max |
| Explicit 0 in all committed examples; production 2 documented | C3-C4 | Accepted | Security profile must not imply warm replicas |
| Rewrite standalone resident deployment or wrapper | C2, C5 | Rejected | Neither needs new logic |
| Publish without complete gate | C8 | Rejected | Required infrastructure publication evidence absent |

#### Cycle Re-entry Evaluation

No further cycle required: all material code questions answered within scope;
no external research or live Azure checks necessary.

## Evidence Log

### Codebase Evidence

| ID | Claim | Location | Tool | Confidence |
| --- | --- | --- | --- | --- |
| C1 | API minimum is 2, maximum 4 and HTTP concurrency 50 | infra/modules/containerapps.bicep:179 | view | High |
| C2 | main is the only module caller, using an explicit params object | infra/main.bicep:318 | rg/view | High |
| C3 | Dev, test and pilot examples use main; production is a security profile | infra/main.bicepparam:1; infra/main.test.bicepparam:1; infra/main.pilot.example.bicepparam:1; infra/main.bicep:82 | view | High |
| C4 | README environment table documents all examples and production controls | infra/README.md:898 | view | High |
| C5 | Wrapper forwards parameter file and overrides; no scale-specific code | infra/scripts/deploy.py:180 | rg | High |
| C6 | Compiled policy test fixes minimum at 2; evaluate helper supports parameters | infra/tests/test_bicep_policy.py:121; infra/tests/test_bicep_policy.py:373 | view | High |
| C7 | Resident separation test and README assume main minimum 2 | infra/tests/test_resident_demo_deploy.py:135; infra/README.md:3171 | view | High |
| C8 | Infrastructure publication requires complete gate; scoped receipts are not full evidence | .github/copilot-instructions.md:71; src/README.md:46 | view | High |
| C9 | Existing offline infra checks compile/lint Bicep and run infra unittest discovery | infra/README.md:1101; tools/rpi-checks.py:662 | view | High |

### External Evidence

No external sources used.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence | Confidence |
| --- | --- | --- | --- |
| Q1 | main -> containerapps is the entire shared API input chain; three examples | C2-C5 | High |
| Q2 | Existing compiled ARM policy tests and full offline infra discovery; az build/lint | C6, C9 | High |
| Q3 | Bound minimum at 0..4; document explicit 2; preserve HTTP, agents and jobs | C1, C3, C7 | High |

## Alternatives and Decision State

Select `apiMinReplicas` with description, `@minValue(0)`, `@maxValue(4)`,
default 0 in both module and parent. Reject hardcoded 0 (not configurable),
profile-derived 2 (unexpected demo cost), and a new max parameter (unrelated).
Keep example minima at 0; production users can choose 2 in their private copy.

## Open Questions, Risks, and Residual Uncertainty

Cold-start behavior is expected when scaling to zero; runtime behavior will not
be measured because deployment is excluded.

## Current Decisions

Use the requested branch and owner-bounded offline validation.
No live what-if is needed or authorized. Existing offline what-if fake tests
will run; do not describe them as live deployment evidence.

## Potential Next Research

Only re-enter if a hidden caller or contradictory validation contract emerges.

## Planning Readiness

Ready for scoped implementation. Publication remains Blocked by C8: no full
gate is authorized by the caller, and it will not be run.

## Research Disposition and Continuation

Executed, complete. Active RPI parent owns continuation to Plan.
Self-check: three ordered inline waves, stable code evidence IDs, alternatives,
scope limits, residual cold-start uncertainty and readiness recorded.
