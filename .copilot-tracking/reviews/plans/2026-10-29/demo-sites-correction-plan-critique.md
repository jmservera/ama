---
title: Demo sites correction plan critique
description: One independent final-candidate assessment of the bounded local evidence plan
ms.date: 2026-10-29
---

## Metadata

* Task ID: eb7ee1f8-42fd-48a8-9c24-a1cbebb99513.
* Task slug: demo-sites-correction.
* Critique date: 2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/demo-sites-correction-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/demo-sites-correction-phase-details.md.
* Critique execution status: Complete.
* Assessment count: exactly one independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: complete the bounded local RPI loop and evidence commits on the existing branch; no push, az, gh, alternate cloud SDK/REST execution, secrets, .env, private data, networking or RBAC changes. This critique runs no tests and edits only its designated output.
* Supplied research: .copilot-tracking/research/2026-10-29/demo-sites-correction-research.md, including C1-C8 and its recorded inspection of #543 and unmerged #521.
* Decisions and dependencies: earlier live approvals remain recorded, but the later no-az instruction controls. SQL projection precedes resident verification, employee deployment and separately gated authority work. A single resident forward revision cannot silently absorb unmerged authority changes.
* Acceptance boundary: all five plan acceptance criteria, P01-P03 and their six tasks, unchanged test ownership, zero test additions/removals, no source changes or generated-pin effects.
* Assessment boundary: credibility of proposed local actions and the blocked-live coordinator handoff, not independent verification of cloud state or supplied historical research. No additional research or source inspection was performed.
* Read-only git inspection confirmed branch ops/sites-redeploy-20261029b and the four existing untracked task artifacts. None was moved, committed or changed by this assessment.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Current execution restrictions; acceptance criterion 2 | Partial | Live execution and prohibited tools are excluded, but local validation paths conflict with the active no-temporary-directory instruction; PC-001. |
| C1-C5; P01-T01 | Covered | SQL-first sequence, exact preservation, target-revision readiness, retained rollback and unknown fresh state are explicit. Historical observations are not presented as current evidence. |
| C3-C4; P01-T02 | Covered | Unmerged source, exact-version credential operation, individually approved row renewal, expiry boundary and revision-budget incompatibility are parked explicitly. |
| C6; acceptance criteria 3 and 5 | Covered | Requested component results do not replace the complete publication gate. Both-sites and January authority acceptance remain unmet. |
| C7-C8; P02-T01 | Partial | Existing checks, nonblocking admission and SQL/browser prerequisite boundaries are identified. Private-data isolation and deterministic busy-lock fallback need correction; PC-002. |
| P02-T02 | Covered | Anonymous status/body hashes cannot establish configuration or new-revision health. Command outcomes and skipped checks must be reconciled. |
| Acceptance criterion 1; P03-T01 | Covered | One original independent Review, original finding preservation and explicit execution/outcome are required. No serial Review loop is planned. |
| Acceptance criterion 4; P03-T02 | Covered | Prior identity provenance is disclosed without forbidden gh lookup; local-only scoped commit, trailer and clean-worktree verification are specified. |
| Locked test ownership and source boundary | Covered | No source/test changes, generated pins or separate #521 worktree mutation are proposed. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0; High 1; Medium 1; Low 0.
* Rationale: the evidence-only delivery boundary and blocked-live handoff are credible. Two directly correctable local-execution safeguards remain unresolved. Neither requires live access or a new user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Local validation requires prohibited temporary-directory operations

* Related IDs: non-functional requirements; acceptance criteria 2-3; P02-T01; research C6.
* Evidence: .copilot-tracking/plans/2026-10-29/demo-sites-correction-plan.md, Non-Functional Requirements, requires /tmp/mv. .copilot-tracking/details/2026-10-29/demo-sites-correction-phase-details.md, P02-T01, requires flock -n /tmp/ama-rpi-heavy.lock and editable installation into /tmp/mv. Active execution instructions prohibit all file operations in /tmp or temporary directories.
* Concern: the proposed admission and editable setup cannot be executed as written within the current restrictions. A lock-open is itself a file operation; being nonblocking does not remove this conflict.
* Impact: execution could violate the active boundary before running any requested checks, or claim admission/results from an impermissible setup.
* Smallest useful change: remove these operations from eligible local execution. Use an already established compliant shared-admission mechanism and compliant environment only if available within the permitted boundary; otherwise record full suites/browser/setup as blocked and use only safe focused checks. Do not invent a separate lock that bypasses shared admission, relocate shared coordination unilaterally or modify the prohibited environment.
* Action owner: planning parent, followed by local executor.
* Exact resolving evidence: corrected P02-T01 and non-functional requirements with either an identified compliant shared admission/environment or an explicit blocked prerequisite; the changes record must distinguish permitted focused results from unexecuted heavy suites and contain no prohibited temporary-path operations.
* Decision route: direct planner correction. The existing prohibition resolves the choice; no user permission request or cloud fallback is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Test isolation and the busy-lock fallback are not executable safeguards

* Related IDs: private-data restriction; acceptance criteria 2-3; P02-T01; research C7-C8.
* Evidence: .copilot-tracking/details/2026-10-29/demo-sites-correction-phase-details.md, P02-T01, says to clear inherited ZF_ settings so no private default is selected and, when admission is busy, run focused checks without naming their selectors. Repository instructions identify the default working dataset as ~/.zava-forward/data/zavaforward.json.
* Concern: removing overrides does not itself prevent fallback to the private default. Explicit source/fixture import paths select code, not necessarily its data. The unspecified focused fallback also leaves the executor to choose checks without a documented isolation boundary.
* Impact: requested validation could access a forbidden default dataset, or use a fallback whose data safety and coverage cannot be reconciled from its recorded result.
* Smallest useful change: specify the existing synthetic harness/fixture entrypoints and focused selectors eligible without heavy admission, with an explicit data-path isolation mechanism that prevents default private-data access before application import or startup. Use only permitted project-relative synthetic inputs; do not inspect private defaults to verify isolation. If an existing check cannot be demonstrated safe from the supplied fixture contract, record its prerequisite as blocked instead of running it.
* Action owner: planning parent for the invocation boundary; local executor for the actual safe command and outcome record.
* Exact resolving evidence: P02-T01 identifies safe invocations/selectors, synthetic data-path handling and blocked fallback behavior; subsequent command summaries show those invocations and their actual exits without private values or data. No new tests or source edits are required.
* Decision route: direct planner correction. No new user decision, secret read or private-data inspection is required.

## Strengths and Residual Risk

* The plan correctly rejects SDK/REST bypasses, silent #521 integration, extra resident revisions and unsupported deployment-success claims.
* Fresh configuration, revisions, digests, SQL shape, credential metadata, cost headroom and live readiness remain unknown. This is an explicitly accepted delivery blocker, not a critique prerequisite to obtain prohibited evidence.
* The coordinator handoff preserves backup, exact-template handling, Manual jobs, protected images, rollback, private SQL routing, narrow rights and owner-performed authenticated verification.
* No source edits, test removals/additions or generated-pin changes are needed for this evidence-only candidate.
* The complete publication gate and exact-head assessment remain separately gated. Local evidence commits do not imply publication, hosted approval or live acceptance.

## Questions or Blocking Evidence Gaps

* No user question is required. Current restrictions already determine the disposition of unavailable admission, environment, SQL, browser and cloud prerequisites.
* Whether a compliant local shared-admission/environment and safe focused invocations exist remains an execution prerequisite. Record a precise blocker if they cannot be established within the permitted boundary.

## Limitations

* No tests, browser checks, anonymous HTTP probes, cloud actions, secret/private/runtime-file reads, source edits or nested agents were performed.
* Supplied C1-C8 and historical deployment/identity statements were assessed as supplied evidence, not freshly reverified.
* This artifact is the sole output of the one critique. Plan, details, research and state remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: directly correct P02-T01 and its related requirements for permitted admission/environment and synthetic-data isolation; preserve this original Revise verdict.
* User response required: no.
* Do not request another plan critique. Continue only eligible local execution and the single original Review after corrections, recording unavailable checks and all live delivery as blocked.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/demo-sites-correction-plan.md](.copilot-tracking/plans/2026-10-29/demo-sites-correction-plan.md) | Assessed local evidence plan |
| [.copilot-tracking/details/2026-10-29/demo-sites-correction-phase-details.md](.copilot-tracking/details/2026-10-29/demo-sites-correction-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-29/demo-sites-correction-research.md](.copilot-tracking/research/2026-10-29/demo-sites-correction-research.md) | Supplied evidence and provenance |
| [.copilot-tracking/reviews/plans/2026-10-29/demo-sites-correction-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/demo-sites-correction-plan-critique.md) | Original independent critique |

## Next Steps

Planning parent: resolve PC-001 and PC-002 directly without another critique, preserve this original outcome and retain the blocked-live handoff. No user action is required. This reviewer stops here.
