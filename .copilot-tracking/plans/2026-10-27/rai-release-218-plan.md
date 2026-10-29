<!-- markdownlint-disable-file -->

# Implementation Plan: rai-release-218

Task: #218; date: 2026-10-27; branch: feat/rai-release-218.
Status: bounded RPI loop complete; original critique Revise and Review Residual work preserved. Epic acceptance remains blocked.

## Executive Summary

Close the independently reproducible release-binding gap: a changed deterministic
ranking policy or quality checklist must require renewed release evidence before
fresh model dispatch, not merely stale an existing proposal. Prove proposal-only
behavior and scripted oversight mechanics; report the real human, cohort and
challenge-coverage gaps without claiming whole-issue acceptance.

## User Decisions and Requirements

* Full Research, Plan, Implement, Review loop and one PR to main for the listed children.
* New code stays in src, tests outside packages; no workflow renaming or Azure.
* Unknown OQ-017 holders remain unknown. No invented evaluations, approvals or fairness.
* #222 requires actual owner manifest approval before evaluator implementation (issue comments; open PR #421).
* Local tests only. No full gate; at most one locked scoped changed gate for large changes.
* Conventional commit plus required trailer; evidence-qualified PR uses Refs, not unsupported Closes.

## Sources

Research: .copilot-tracking/research/2026-10-27/rai-release-218-research.md,
C1-C10 and W1-W6. Requirements: PRD FR-051 to FR-054, AC-069 to AC-073,
OQ-017/018; BRD RULE-020/024; ADR 0002 control plane and ADR 0006 layout.

## Goals

Prevent policy changes escaping release admission. Preserve ordinary case work,
recipient permissions and history. Make acceptance limitations reviewable.

## Scope and Non-Goals

Existing core release bindings/capture, API regression harness and component
documentation only. No new evaluator, service, UI, role grant, ranking algorithm,
participants, deployment, actual restart, #224 work or #440 implementation.
Remaining assistant/form challenge coverage is not silently declared delivered.

## Functional Requirements

* Include actual current ranking content in stock and retained-priority release policy binding.
* Include quality checklist definitions and dispatch mapping in quality release policy binding.
* Resolve the current ranking policy explicitly during stock capture.
* Preserve unrelated capability bindings, stale history and ordinary human work.
* Exercise matching constructed releases, policy-change admission/claim/completion/review denial and scripted defect rejection.

## Non-Functional Requirements

Reuse canonical policy_hash/digest functions; no new dependencies. Deterministic
fingerprints, bounded records, existing SQL transactions and zero network/model
calls. Never treat scripted dispositions as competent human evidence.

## Acceptance Criteria

* Failing-first regressions prove actual policy-definition changes escaped admission.
* Changed ranking/checklist content blocks affected fresh and queued dispatch;
  in-flight output is quarantined and ready/verified reliance refused.
* Matching renewed constructed release permits proposals only and keeps old release history unusable.
* Unrelated task bindings and ordinary case data remain unchanged.
* Plausible wrong, unsupported, incomplete and stale scenarios exercise explicit
  source verification/reject/correct mechanics; an automation-bias negative
  control documents why syntactic checks do not prove human effectiveness.
* Each named child has an evidence/remaining-gap disposition. No issue ticks.

## Phase Checklist

<!-- phase: P01 -->
### P01: Release policy dependencies

* [x] P01-T01 Add failing-first policy-definition regressions.
* [x] P01-T02 Bind current ranking/quality definitions and fix current stock capture.

<!-- phase: P02 -->
### P02: Oversight and integrated evidence

* [x] P02-T01 Add scripted oversight mechanics/negative-control checks, retain sources/reasons and prove no controlled write.
* [x] P02-T02 Run focused release/assistant/incident/challenge tests and affected package suites/static checks.
* [x] P02-T03 Update component docs and detailed acceptance matrix with unresolved human decisions.

<!-- phase: P03 -->
### P03: Review and publication

* [x] P03-T01 Reconcile implementation evidence, run one independent post-implementation Review and route open findings.
* [x] P03-T02 Commit artifacts/source, push without force and create one Refs-only PR.

## Test Ownership and Locked Change Boundaries

Existing API unittest harness owns integration scenarios in
src/api/tests/test_assistant_release.py and src/api/tests/test_assistants.py.
Core pure contract tests stay unchanged unless failure requires them.
Exact removals: none. Maximum additions: twelve test methods across those two
existing files. No generated evaluator/report/golden labels. Semantic scenarios
are explicitly developer-authored, not held-out or human-study evidence.
Production targets: core assistants.py, ai_registry.py and quality.py (only if
a shared quality policy helper is needed). Canonical documentation:
src/core/README.md and src/agents/README.md as relevant.
Validation: failing-first reproduction, focused combined unittest selectors,
core/API suites, Ruff and mypy. No changed gate planned: small binding fix plus
regressions does not justify the heavy gate. Any unavailable check is recorded.

## Critique Disposition

Exactly one independent critique completed: Revise, PC-001 Medium.
Directly applied: independent mapping-only and order-sensitive quality-policy
mutations, with unchanged definitions and unchanged-case-source control, must
alter the policy binding and deny admission. Both phase details and tests own
this requirement. No human decision or second critique is required.
Artifact: .copilot-tracking/plans/2026-10-27/rai-release-218-critique.md.

## Follow-Up Items

1. Owner approves corrected versioned cohort manifest in #421 before #222 evaluator.
2. OQ-017 appointments and approved participant protocol before #223 effectiveness or #221 witnessed restart/drill acceptance.
3. #220 assistant/form challenge coverage beyond retained priority remains unproved.
4. #224 legal screening and #440 stabilization are required before #218 closure.

## Handoff

Details: .copilot-tracking/details/2026-10-27/rai-release-218-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-27/rai-release-218-changes.md.
Critique was dispositioned before implementation. One independent Review
completed with Residual work, no introduced code defect found. Draft PR #504
contains the source and original phase evidence; remaining human/coverage/
hosted gates are not accepted. Pinned main integration resolved only the
knowledge-index conflict, preserving all upstream evidence. Reviewed RAI source
and tests are unchanged; 35 post-integration focused tests passed.
