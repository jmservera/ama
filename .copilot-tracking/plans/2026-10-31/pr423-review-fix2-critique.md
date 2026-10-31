---
title: PR 423 review fix2 independent plan critique
description: Single final-candidate assessment of preservation and offline review corrections
ms.date: 2026-10-31
---

## Metadata

* Task ID: pr423-review-fix2
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/pr423-review-fix2-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/pr423-review-fix2-phase-details.md
* Critique execution status: Complete
* Assessment count: Exactly one final-candidate independent critique.
* Observed branch/head: docs/demo-transport-plan-360-fix2 / 7eba611664c12d09270c5765575a57d1aea1a936.

## Inputs and Criterion Boundary

* Caller direction controls the assessment: full ordered RPI; merge pinned
  origin/main without rebase; retain both intents and append ranges; select
  main's latest.json; address the four supplied review concerns; pip only;
  offline unittest and available Bicep; serialized heavy work; privacy-safe
  local commit with Copilot trailer; no Azure, secrets, push or PR body edits.
* Research: .copilot-tracking/research/2026-10-31/pr423-review-fix2-research.md,
  Q1-Q5 and C1-C9. The supplied plan and details were read in full.
* Relevant source inspected: infra/scripts/staff_blob.py,
  infra/tests/test_staff_azure.py, infra/staff-initializer-rbac.bicep,
  infra/README.md and
  .copilot-tracking/changes/2026-10-30/pr423-merge-rubric-changes.md.
* Repository context considered: docs/case_study_48_original.md and the
  opening current proposal/context sections of docs/case_study_48_addendum.md,
  docs/reference/README.md and docs/reference/memory.md.
* Decisions and dependencies: P01-T01 precedes source/runbook corrections;
  P02-T01 follows corrections; P02-T02 follows validation. AC1-AC6 and the
  canonical test owner, no-removal budget and maximum two added tests were
  assessed together.
* Boundary: credibility of the proposed local integration and corrections,
  not implementation completion, a fresh operational approval, issue
  acceptance or an integrated successful exact-head receipt.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC1; Q1; C9; P01-T01 | Covered | Two explicit parent SHAs, merge rather than rebase, main rubric selection, append preservation, no unintended deletions and imported main source equality are required. Read-only parent comparison supports the bounded integration scope. |
| AC2; Q2; C1/C3; P01-T02 | Covered | Retains download offset/range and separately specifies read(MAX_BLOB+1); fake must enforce explicit size and record returned bytes, prohibit readall, and exercise replacement refusal plus owned job/secret cleanup. |
| AC3; Q3; C2/C4; P01-T02 | Covered | Preserves the existing all-pages serialized check; strengthens the exact requested counterexample at write_result/no-upload; keeps complete multi-page, head, exact boundary, Unicode and page-count controls. |
| AC4; Q4; C5/C6/C8; P01-T03 | Covered | Keeps already correct active default-off/opt-in examples; clarifies historical parameter scope and non-revoking incremental deployments without rewriting performed commands. |
| AC5; Q5; C7; P01-T03 | Covered | Requires current-candidate qualification of historical provenance, preserves original adverse outcomes and disclaims successful integrated receipt; owner-only PR body correction is separate. |
| AC6; P02-T01/P02-T02 | Covered | Missing installed namespace has an observed prerequisite failure; pip restoration, focused unittest, available offline Bicep, actual result retention, one independent Review and local commit are specified. |
| Test ownership and change budget | Covered | infra/tests/test_staff_azure.py owns the targeted tests; existing replacements/controls are strengthened, removals are zero, additions are capped at two and generated compilation targets stay external. |
| Non-functional requirements and non-goals | Covered | Shared finite heavy lock, no cloud/private data/secrets, no publication and no UI changes; complete exact-head gate and hosted/human acceptance remain separate unmet follow-ups. |

## Verdict

* Verdict: Pass
* Rationale: The candidate targets actual remaining assurance gaps rather than
  reimplementing safeguards already present. Its sequence, preservation checks,
  regression budget and historical/current evidence distinctions are credible.
  No meaningful correctness, coverage or preservation flaw requiring a plan
  revision was identified within the supplied boundary.

## Findings

No actionable PC-xxx findings. Severity counts: Critical 0, High 0, Medium 0,
Low 0. There is no significant unresolved decision requiring owner input.

## Strengths and Residual Risk

* Explicit consumer read hardening complements, rather than replaces, the
  existing ranged request. The fake's explicit-size enforcement and readall
  prohibition are essential implementation requirements, not optional polish.
* Existing source rejects overflow/list-size mismatch before decoding. Planned
  within/outside-bound replacement coverage and valid complete round trips
  preserve both refusal and successful behavior.
* The wrapper counterexample already exists; moving its assertion through
  write_result with no upload is a useful assurance improvement, not a request
  to change the correct all-page validation or broaden the algorithm.
* Main-side changes identified by the read-only comparison are resident-chat
  source/tests and dated tracking. The plan imports them intact without a
  separate UI review or unrelated edits.
* Live SDK/private-route/managed-identity behavior remains unverified, as
  explicitly recorded in research. Offline fake tests and Bicep compilation
  cannot establish operational transport acceptance.
* A successful integrated receipt remains absent. The explicit no-push local
  task does not authorize publication or promotion of historical receipts.
* Implementation must obey the existing commit-time authenticated-account
  lookup and repository-local author/committer configuration; the address in
  phase details is the supplied expected identity, not permission to bypass
  that lookup.

## Questions or Blocking Evidence Gaps

* None for this plan assessment. No additional phase prompt, cloud exercise,
  UI work or historical receipt rewrite is needed to finalize planning.

## Limitations

* No implementation, dependency restoration, unittest, Bicep, heavy command,
  merge, commit or remote write was executed by this critique.
* GitHub thread contents and tool availability were assessed from the supplied
  research/caller context, not independently retrieved or exercised.
* Passing this plan is not a fresh Review of implemented changes, completion
  of AC1-AC6 or confirmation of a successful publication gate.
* Only this critique artifact was written; existing untracked RPI inputs and
  all source, research, plan, details and historical outcomes were preserved.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent.
* Smallest next action: Record this Pass disposition and finalize the supplied
  plan, then continue its authorized implementation and one independent Review.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/pr423-review-fix2-plan.md](.copilot-tracking/plans/2026-10-31/pr423-review-fix2-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-31/pr423-review-fix2-phase-details.md](.copilot-tracking/details/2026-10-31/pr423-review-fix2-phase-details.md) | Assessed implementation and validation details |
| [.copilot-tracking/research/2026-10-31/pr423-review-fix2-research.md](.copilot-tracking/research/2026-10-31/pr423-review-fix2-research.md) | Supplied research and evidence boundary |
| [.copilot-tracking/plans/2026-10-31/pr423-review-fix2-critique.md](.copilot-tracking/plans/2026-10-31/pr423-review-fix2-critique.md) | This single independent critique |

## Next Steps

The active planning parent may finalize directly and continue the ordered RPI
loop under the existing owner direction. No repeat critique or user action is
required. Preserve the no-push, offline-only and honest receipt boundaries.
