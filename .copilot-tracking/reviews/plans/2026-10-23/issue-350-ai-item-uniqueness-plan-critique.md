---
title: Issue 350 AI item uniqueness plan critique
description: Single final-candidate assessment of the bounded second correction
ms.date: 2026-10-23
---

## Metadata

* Task ID: issue-350-ai-item-uniqueness.
* Critique date: 2026-10-23.
* Plan: .copilot-tracking/plans/2026-10-23/issue-350-ai-item-uniqueness-plan.md.
* Phase details: .copilot-tracking/details/2026-10-23/issue-350-ai-item-uniqueness-phase-details.md.
* Critique execution status: Complete.
* Original verdict: Revise.
* Execution count: one final-candidate critique; no lifecycle peer invoked.

## Inputs and Criterion Boundary

* Caller direction: ordered Research/Plan/Implement/Review; reject only duplicate
  captured AI case IDs on a01b36f86e36092cbe4d90a1b9db87a95a34531d. Preserve
  original artifacts, existing offline behavior and deferred PR #436 lineage.
* Research considered:
  .copilot-tracking/research/2026-10-23/issue-350-ai-item-uniqueness-research.md,
  including C1-C5, the reported actual 70-test baseline and duplicate reproduction.
* Implementation evidence inspected: tools/check-demo-feedback.py,
  tools/test_check_demo_feedback.py and
  src/core/src/zava_forward/core/ai_tasks.py.
* Gate evidence inspected: src/README.md and tools/rpi-checks.py, including the
  CLI, output-directory checks and shared-lock implementation.
* Repository context read: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. No new customer or regulatory claim is assessed.
* Decisions assessed: shape-guarded raw set cardinality; explicit duplicate
  diagnostic; no normalization, semantic membership/citation validation, count
  limits, checker IO, new dependency or runtime change.
* Locked tests: AiEvidence, no removals or generated targets, at most two added
  methods, duplicate and raw-distinct matrices, existing runtime-validator
  positive retained. This is regression coverage, not semantic validation.
* Delivery assessed: one original Review, reviewed evidence committed before
  exactly one complete gate, exact base
  140d8f494482c78e84d15f3d46b9223d3c487af0, lock timeout 86400, unique external
  output, official verifier/hash, then stop without publication.
* External logs and gate outputs are explicitly authorized for the parent.
  They are not restricted to this critic's single-file write boundary. The
  separate execution restriction on forbidden temporary paths nevertheless
  affects whether the supplied commands can be run.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1, C1-C2, P01-T02 | Covered | Existing item-shape predicate proves string IDs before the proposed elif hashes them; raw cardinality rejects adjacent and nonadjacent repetition. |
| FR2, C2-C3, P01-T01 | Covered | Raw-distinct positive matrix plus retained runtime-validator positive guards against normalization or validator reuse. |
| FR3, NFR1, C1-C3 | Covered | Existing malformed-item matrices include unhashable values; elif preserves structural failures and existing Verdict aggregation without new IO/imports. |
| NFR2, C3-C4, P01 | Partial | Installed-package and no-cache design is appropriate, but executable and fixture-scratch paths need correction: PC-001. |
| NFR3, P01-P03 | Covered | One critique, one original Review, one gate and no post-gate candidate writes are explicit. Findings must be disposed without another critique. |
| AC1-AC2, P01-T01/P01-T02 | Partial | Real red-first component assertions, full focused suite and targeted Ruff are specified; execution-path prerequisite remains PC-001. |
| AC3, FR3 | Covered | Component status, explicit duplicate reason and blocked/not-run/not-accepted positive residuals are explicitly required. |
| AC4, P02-T01 | Covered | Two source files and new dated artifacts only; old evidence, runtime and gate remain unchanged. |
| AC5, C4-C5, P02-T02/P03-T01 | Partial | Identity, commit order, fixed base, verifier and hash are explicit; the hard-coded shared-lock path prevents the claimed executable gate route under the supplied restrictions: PC-002. |
| P01 -> P02 -> P03 | Covered | Dependencies prevent source edits before critique disposition and prevent gating before reviewed clean committed head. |
| Publication and acceptance exclusions | Covered | No push, history rewrite, remote edits, independent approval or live/deployed/AI/SQL acceptance is inferred. |

## Verdict

* Verdict: Revise.
* Severity summary: zero Critical, one High, one Medium, zero Low.
* Rationale: the uniqueness algorithm and locked test plan are credible and
  appropriately narrow. Two execution-path issues require disposition before
  the plan can claim an executable validation sequence. PC-002 cannot be
  resolved merely by changing the external output directory.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Focused validation lacks a permitted interpreter and scratch route

* Related IDs: NFR2, AC1-AC2, C3-C4, P01-T01, P01-T02.
* Evidence:
  .copilot-tracking/details/2026-10-23/issue-350-ai-item-uniqueness-phase-details.md:45,
  :60-62 names an interpreter under /tmp. tools/test_check_demo_feedback.py:173-177
  uses tempfile.TemporaryDirectory in report_for; the proposed focused commands
  do not set a permitted scratch root.
* Concern: the commands cannot be followed as written under the supplied
  prohibition on /tmp file operations. Replacing the interpreter alone does
  not prevent the fixtures from choosing the default forbidden scratch root.
* Impact: the required red/green evidence may be blocked or produced through
  disallowed paths, despite correct source and test design.
* Smallest useful change: the planning parent should select and verify a
  permitted installed-package interpreter, specify a permitted external
  fixture-scratch location through TMPDIR, and route logs/caches outside the
  candidate. Use caller-authorized external locations addressed relative to
  the worktree; do not add task-created ignored candidate inputs or modify the
  locked tests to solve this environmental issue. Record a dependency blocker
  if no permitted interpreter exists rather than assuming an unverified one.
* Action owner: planning parent.
* Exact resolving evidence: corrected P01 command blocks naming the actual
  permitted interpreter and TMPDIR, with a recorded successful import/tool
  availability check through that interpreter before the planned red/green
  runs. The original research baseline remains historical, not rewritten.
* Decision route: directly applicable planner correction; no divergent user
  decision is needed. Parent authorization for external evidence is already
  sufficient and must not be narrowed to the critic's write boundary.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Gate execution has a fixed forbidden-path dependency

* Related IDs: AC5, C5, P03-T01, NFR3.
* Evidence:
  .copilot-tracking/details/2026-10-23/issue-350-ai-item-uniqueness-phase-details.md:107-109
  places gate output under /tmp. More importantly,
  tools/rpi-checks.py:1675-1678 hard-codes /tmp/ama-rpi-heavy.lock and opens it
  for creation/write. tools/rpi-checks.py:1721-1741 exposes --lock-timeout but no
  lock-path override and enters heavy_lock before running the matrix.
* Concern: moving --out to a permitted unique external directory does not make
  --all compliant: the existing runner still performs forbidden /tmp file
  operations. The candidate states no known blocker without recognizing this
  fixed dependency.
* Impact: successful exact-head gate/receipt acceptance cannot currently be
  promised under the supplied execution boundary. Starting the single gate
  while this is known would consume the authorized attempt on an incompatible
  route; removing or relocating the lock locally would violate the unchanged
  gate scope and shared-resource serialization requirement.
* Smallest useful change: replace the explicit output/receipt paths with a
  permitted unique external location, record the fixed-lock execution blocker
  in the plan/details and delivery evidence, and make P03 conditional on an
  independently established compliant execution route. If none exists, stop
  with the gate and AC5 explicitly Blocked/Not run. Do not invoke a knowingly
  forbidden command, bypass serialization, patch the gate, fabricate a receipt
  or claim a passing verifier/hash.
* Action owner: planning parent for blocker disposition; coordinator for any
  separately authorized future gate/environment change.
* Exact resolving evidence: updated P03/AC5 disposition explicitly naming the
  fixed-lock blocker and preserving the exact base, one-gate ceiling, original
  Review and no-publication stop. A future successful route would additionally
  require concrete evidence that the unchanged authorized runner can execute
  without forbidden file operations; none is established by the supplied CLI.
* Decision route: directly applicable blocker recording and safe stop. A gate
  source change is divergent, outside this correction and not authorized by
  this finding. No user response is required to record the blocker.

## Strengths and Residual Risk

* The shape-guarded elif avoids hashing malformed IDs and preserves existing
  field diagnostics. Raw equality matches the inspected runtime rule without
  importing the validator's excluded membership, citation or count behavior.
* Duplicate payload variants and nonadjacent repetition defeat simple
  adjacent-only or whole-object duplicate checks. The two-method bound and
  retained 70 methods avoid test-scope expansion.
* Focused tools tests are explicitly separate from the full gate, which does
  not automatically discover this suite.
* Review-before-commit and external post-commit evidence avoid receipt
  self-reference. Original adverse artifacts and deferred lineage remain
  unchanged.
* Actual SQL, AI, deployment, independent coordinator and human acceptance
  remain explicitly outside this correction. These accepted boundaries are
  not findings and must not be expanded to resolve this critique.

## Questions or Blocking Evidence Gaps

* No unresolved uniqueness or test-design question.
* PC-001 needs an actual permitted validation environment.
* PC-002 establishes a concrete gate execution blocker, not a request for
  further semantic research or another critique.

## Limitations

* This is a planning assessment, not implementation or RPI Review. No tests,
  checker probes, gate, verifier or hash command were executed by the critic.
* The reported 70-test baseline and reproduction were assessed as supplied
  research evidence, not independently rerun.
* Read-only Git inspection confirmed starting HEAD and branch
  test/deployed-feedback-harness-350 with its corresponding origin upstream.
  Only this task's new artifacts were untracked at inspection. No remote
  metadata, PR lineage or current main claim was independently re-established.
* This is the complete actionable finding set for the supplied boundary. No
  cosmetic or separately withheld follow-up findings are proposed.

## Recommended Next Action

* Highest-impact finding: PC-002.
* Action owner: planning parent.
* Smallest next action: dispose both findings directly, correct the permitted
  focused-test route and explicitly record the gate blocker before continuing
  the authorized ordered implementation/Review sequence.
* User response required: no for these direct corrections and honest blocker
  recording. No gate modification or restriction bypass is authorized.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-23/issue-350-ai-item-uniqueness-research.md](.copilot-tracking/research/2026-10-23/issue-350-ai-item-uniqueness-research.md) | Supplied completed research and baseline evidence |
| [.copilot-tracking/plans/2026-10-23/issue-350-ai-item-uniqueness-plan.md](.copilot-tracking/plans/2026-10-23/issue-350-ai-item-uniqueness-plan.md) | Assessed final-candidate plan, unchanged |
| [.copilot-tracking/details/2026-10-23/issue-350-ai-item-uniqueness-phase-details.md](.copilot-tracking/details/2026-10-23/issue-350-ai-item-uniqueness-phase-details.md) | Assessed task commands and dependencies, unchanged |
| [.copilot-tracking/reviews/plans/2026-10-23/issue-350-ai-item-uniqueness-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-23/issue-350-ai-item-uniqueness-plan-critique.md) | Original single-pass critique |

## Next Steps

The active planning parent owns dispositions and implementation. Address PC-001
and record PC-002 directly without rerunning critique or invoking a lifecycle
peer from this assessment. Preserve this original Revise verdict. No user action
is required for the identified corrections; gate success remains blocked unless
a compliant execution route is established.
