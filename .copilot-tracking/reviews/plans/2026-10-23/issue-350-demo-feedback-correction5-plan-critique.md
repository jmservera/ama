---
title: Issue 350 correction 5 independent final-candidate plan critique
description: Bounded assessment of exponent-overflow and schema-version correction planning
ms.date: 2026-10-23
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: issue-350-demo-feedback-correction5.
* Critique date: 2026-10-23.
* Critique execution status: Complete.
* Verdict: Revise.
* Severity summary: Critical 0; High 0; Medium 2; Low 0.
* Exactly one independent final-candidate critique was performed, activating rpi-plan-critique. No agents or additional critique passes were launched.
* Observed branch: test/deployed-feedback-harness-350.
* Observed input HEAD: e55bcd835c414cf55e57d2b49119cd24a30fff92.
* Caller-supplied base: 140d8f494482c78e84d15f3d46b9223d3c487af0. No fetch or base verification was performed.

## Inputs and Criterion Boundary

* Research: .copilot-tracking/research/2026-10-23/issue-350-demo-feedback-correction5-research.md, including C1-C5 and the selected parse_float alternative.
* Plan: .copilot-tracking/plans/2026-10-23/issue-350-demo-feedback-correction5-plan.md, including FR1-FR4, acceptance criteria, all phases and the validation lock.
* Details: .copilot-tracking/details/2026-10-23/issue-350-demo-feedback-correction5-phase-details.md, all tasks P01-T01 through P03-T02.
* Source evidence: tools/check-demo-feedback.py, particularly load_evidence, check_ai, run_check and build_report; tools/test_check_demo_feedback.py, particularly InputSafety, existing latency controls and fixture-file handling.
* Repository context: original case study and introductory excerpts of the addendum, reference index and owner memory. No regulatory, web or open-ended research was needed.
* Requirements: reject every non-finite decoded float before checks, including overflow in unchecked nested fields; require exact integer schema version excluding bool; prove the original failures with raw-exponent red-first regressions; preserve finite-value behavior and offline evidence limits.
* Candidate locks: primary owns tests; at most five added test methods using subtests; no removals; only the two named tool files and correction5 dated artifacts; cache-free existing environment and isolated Ruff; critique before source edits.
* Lifecycle boundary: the parent completes the ordered local RPI work and local commit, but performs no full gate or publication. This critique itself performs no implementation, tests, network operation, commit, gate or state update and writes only this artifact.
* Intake status showed four untracked correction5 research/plan/details/state artifacts and no tracked changes. They were not moved, staged or changed. Earlier receipt and plan outcomes remain historical, not new-head evidence.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1; C1; P01-T01/P01-T02 | Covered | Typed parse_float with float conversion and math.isfinite rejects overflow globally during decoding. Retaining parse_constant covers literal NaN/Infinity separately. Existing ValueError handling yields invalid-JSON BLOCKED. |
| Raw-exponent red-first requirement; C4 | Covered | Details explicitly specify valid JSON tokens 1e999, -1e999 and 1.0e999 across latency, unchecked rank and another nested payload; unique replacement and pre-source red evidence prevent an Infinity-serialization substitute. |
| FR2; C2-C3 | Covered | Exact type(value) is int plus supported-value comparison rejects true, false, 1.0 and 2 while retaining integer 1. Explicit schema diagnostics and supported-version controls are planned. |
| FR3; C5 | Covered | Fraction, large finite exponent, underflow and negative finite controls preserve unchecked-rank acceptance and latency-specific negative rejection without new rank rules. |
| FR4; evidence boundaries | Covered | Per-check BLOCKED reasons, an AssertionError runtime-loader sentinel, gaps NOT-RUN, offline_only and not-accepted assertions avoid relying on an already-BLOCKED aggregate. SQL durability, deployment, actual inference and whole-issue acceptance remain excluded. |
| P01 dependencies and ownership | Covered | Tests precede checker changes; ordinary controls are separate from red selection; five added methods with subtests can hold the bounded matrices without removals. |
| P02-T01; cache-free validation | Partial | Commands cover bytecode, Ruff and whitespace, but fixture scratch-file placement is not constrained: PC-002. |
| P03-T01/P03-T02; completion decision | Partial | Unconditional deferral of any residual Review findings can bypass resolution of these two defects before local closeout: PC-001. |
| Publication dependencies; historical receipt | Covered | Fresh gate and independent exact-head assessment belong to the coordinator after the local commit. Stale historical sequencing is disclosed, not reopened as new scope. |

## Verdict

* Verdict: Revise.
* The selected loader correction and test coverage are credible for both supplied P2 issues. No alternative architecture, extra field validation, new research or user decision is needed.
* Two direct execution-contract corrections are required: distinguish in-scope Review failures from accepted out-of-scope residuals, and make scratch-file placement explicit for the planned validation commands.
* This is one complete finding set for the supplied boundary; no additional discoverable findings are withheld for another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Blanket Review deferral can close an unresolved correction

* Related IDs: FR1-FR4; P03-T01; P03-T02.
* Evidence: .copilot-tracking/details/2026-10-23/issue-350-demo-feedback-correction5-phase-details.md:48-53 says to route any residual findings to later work without another implementation/review cycle. Lines 57-60 then direct a local commit after checks and Review without conditioning closeout on the Review outcome.
* Concern: The wording does not distinguish a known out-of-scope deployment limitation from a newly identified failure of overflow rejection, exact schema typing or required regression coverage. One critique and one planned Review do not authorize declaring an unresolved in-scope defect complete.
* Impact: A green but insufficient test suite or failed Review could still lead to a misleading completed local handoff for the two P2 corrections.
* Smallest useful change: Make local completion conditional on resolution of in-scope acceptance findings. Preserve the original Review outcome. Defer only explicitly classified out-of-scope residuals; if an in-scope finding cannot be resolved within the locks, mark the handoff blocked rather than complete. Do not mandate another critique or expand this task into publication checks.
* Action owner: Planning parent, with the primary implementer responsible for resolving any subsequent in-scope source/test finding.
* Exact resolving evidence: Matching correction5 plan/details disposition that states this conditional closeout rule; later Review/changes evidence maps each in-scope finding to its resolution or an explicit blocked completion status. Historical adverse Review evidence remains unchanged.
* Decision route: Direct planner correction. The caller already requires a working correction and local-only stop; no significant or divergent user decision is necessary.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Cache-free commands do not constrain fixture scratch writes

* Related IDs: P01-T01; P02-T01; validation lock.
* Evidence: tools/test_check_demo_feedback.py:798-802 and 842-845 use tempfile.TemporaryDirectory() without an explicit directory, as do other existing fixture paths. The plan's validation command at .copilot-tracking/plans/2026-10-23/issue-350-demo-feedback-correction5-plan.md:129-135 disables bytecode and Ruff caches but does not select a permitted scratch root. Details P02-T01 likewise omit that prerequisite.
* Concern: Disabling caches does not control tempfile placement. Unless the execution environment already provides a permitted scratch root, existing fixture helpers can write to the system default temporary directory, contrary to the supplied prohibition on /tmp and /var/tmp file operations. No current environment setting was verified in this critique.
* Impact: Required red/green validation can violate the execution boundary or be blocked for environmental reasons unrelated to the P2 regressions.
* Smallest useful change: Specify a project-relative scratch root and set TMPDIR to that permitted root before every selected or full unittest invocation. Keep the existing venv/Ruff selection and bytecode/cache flags. Clean only the exact newly created scratch directory before final status/commit inspection; do not alter existing helpers, ignore rules or other worktrees.
* Action owner: Planning parent for the command contract; primary implementer for environment setup and exact-owned cleanup.
* Exact resolving evidence: Correction5 plan/details include the same permitted scratch-root setup for red and green commands. Later changes evidence records the actual commands, scratch cleanup and final ignored/untracked inspection, with no forbidden temporary-directory fixture writes.
* Decision route: Direct planner correction under existing execution constraints, not a dependency/tooling change or significant/divergent user decision.

## Strengths and Residual Risk

* Decoder-level parse_float rejection covers unchecked fields without broadening component schemas or changing normal float types. A field-only rank or latency check would not satisfy FR1.
* The literal +1e999 wording in the plan is read as positive-overflow shorthand, not a proposed JSON token: the phase details explicitly use valid 1e999. The implementation must follow those details; a literal leading plus would test JSON syntax rejection instead of overflow.
* Exact int is appropriate for JSON decoder output and prevents both true == 1 and 1.0 == 1 bypasses. False remains a useful explicit control even though its rejection is not a new behavior.
* Existing in-memory latency defenses and huge-integer behavior need no unrelated rewrite. The proposed decoder hook leaves integer parsing and numeric strings unchanged.
* Existing synthetic-write caps and gaps mean aggregate BLOCKED alone cannot establish either regression. Planned per-check diagnostics and no-runtime sentinel address that risk.
* No evidence here establishes SQL durability, deployed behavior, actual AI execution, hosted/human approval or whole-issue acceptance. These remain outside the explicitly selected local outcome.
* The caller-supplied receipt at input HEAD becomes historical after changes; its prior success cannot certify a changed candidate. No fresh receipt is required within this local-only task.

## Questions or Blocking Evidence Gaps

* None requiring a user response. Both findings have direct corrections within the existing scope.
* Runtime scratch configuration is unverified, not asserted to be currently misconfigured. The missing explicit command prerequisite is the planning finding.

## Limitations

* This is a planning/source inspection, not implementation verification. No regression, lint, formatter, whitespace, gate or receipt verification command was run.
* Research reproduction claims were assessed against the named source, not re-executed. Dependencies, environment availability, external PR state and the supplied base/receipt were not independently checked.
* No source, plan, research, state, earlier review record or other worktree was edited. This artifact is the sole authored output.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Apply both direct planning corrections, record their disposition against PC-001/PC-002, then proceed to the existing raw-token red-first implementation sequence.
* User response required: No.
* Significant/divergent decision disposition: None. Confirmed user direction resolves scope, branch, local stop and later publication ownership. Do not request another critique.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-23/issue-350-demo-feedback-correction5-research.md](.copilot-tracking/research/2026-10-23/issue-350-demo-feedback-correction5-research.md) | Supplied focused research |
| [.copilot-tracking/plans/2026-10-23/issue-350-demo-feedback-correction5-plan.md](.copilot-tracking/plans/2026-10-23/issue-350-demo-feedback-correction5-plan.md) | Candidate plan requiring direct corrections |
| [.copilot-tracking/details/2026-10-23/issue-350-demo-feedback-correction5-phase-details.md](.copilot-tracking/details/2026-10-23/issue-350-demo-feedback-correction5-phase-details.md) | Candidate execution contract |
| [.copilot-tracking/reviews/plans/2026-10-23/issue-350-demo-feedback-correction5-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-23/issue-350-demo-feedback-correction5-plan-critique.md) | Complete independent critique |

## Next Steps

Planning parent: resolve PC-001 and PC-002 directly without another critique, then continue the ordered local RPI loop through source checks, outcome-aware Review and the authorized local commit. No user action is required. This critique stops here; no gate, network operation or publication is performed.
