---
title: AI item shape final-candidate plan critique
description: One bounded credibility assessment for issue 350 and draft PR 436
ms.date: 2026-10-23
---

## Metadata

* Task ID: issue-350-ai-item-shape
* Critique date: 2026-10-23
* Plan: .copilot-tracking/plans/2026-10-23/issue-350-ai-item-shape-plan.md
* Phase details: .copilot-tracking/details/2026-10-23/issue-350-ai-item-shape-phase-details.md
* Critique execution status: Complete
* Assessment count: One final-candidate critique; no repeat requested or performed.

## Inputs and Criterion Boundary

* Caller requirements: correct the reproduced malformed captured-item false
  PASS in check_ai; test missing/wrong case_id/reason types and empty/non-string
  citations; retain runtime-shaped synthetic positives. No semantic citation
  validation, arbitrary limits, cloud/AI/private data or whole-issue acceptance.
* Exact research: .copilot-tracking/research/2026-10-23/issue-350-ai-item-shape-research.md,
  especially C1-C8 and their runtime, checker, tests and delivery pointers.
* Authority checked: ai_tasks.priority_items, Store.ai_priority/_rec_view and
  POST /api/ai/priority; src/README.md local RPI gate requirements.
* Decisions assessed: existing branch test/deployed-feedback-harness-350;
  preserve prior evidence; canonical tools/test_check_demo_feedback.py;
  no removals and at most six new methods; one original Review; candidate and
  original evidence committed before exactly one complete gate with base
  140d8f494482c78e84d15f3d46b9223d3c487af0 and lock-timeout 86400;
  external unique receipt, verification, normal push and draft PR #436 update.
* Boundary: FR1-FR4, NFR1-NFR3, AC1-AC5 and every P01-P03 task, dependency,
  decision and residual risk. This assesses planning credibility, not an
  implemented correction, executed gate, remote PR state or live acceptance.
* Only the specified critique artifact is written. Existing untracked planning
  inputs are caller-owned and are not moved, staged or changed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1-FR2; C1-C2/C7 | Covered | Existing guarded all predicate plus nonempty_str addresses published item shape without coercion or source resolution. |
| FR3; AC4; C4/C7-C8 | Covered | Runtime-validator synthetic positive and retained enriched fixture cover required fields and allowed display fields. |
| FR4; NFR1; AC2 | Covered | Existing unrelated guards and explicit acceptance boundaries remain unchanged; direct component assertions avoid aggregate blocked false assurance. |
| AC1/AC3; P01-T01 | Covered | Missing keys, wrong scalar/container types, whitespace, mixed citation elements and repros are required; subtests can fit the six-method ceiling. |
| NFR2; P01-T01/P01-T02/P03-T01 | Partial | PC-001: executable paths and default test scratch are not reconciled with the execution-environment restriction. |
| P01-T02 | Covered | Bounded guard/module documentation, full focused module, targeted Ruff and diff checks are appropriate. |
| NFR3; P02-T01/P02-T02; AC5 | Partial | PC-002: preserve one original Review, but define an outcome-dependent stop before gate/publication. |
| P02-T02 | Covered | GitHub-resolved privacy identity, author/committer, trailer and candidate/evidence commit are explicit. |
| P03-T01/P03-T02; AC5 | Partial | Exact base, one run, lock wait, external receipt, fresh fetch/verification and normal push are defined; PC-001 still prevents literal execution. |
| Scope, dependencies, decisions and residual risks | Covered | No new coding decision; full gate remains pending; independent coordinator and live acceptance remain separate. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.
* Rationale: The structural correction and regression boundary are credible.
  Two operational corrections are required before the parent can safely execute
  the authorized single-pass delivery sequence. Neither expands product scope
  nor requires another critique or a new user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Planned validation paths violate the execution restriction

* Related IDs: NFR2, AC1-AC2/AC5, P01-T01, P01-T02, P03-T01.
* Evidence: .copilot-tracking/details/2026-10-23/issue-350-ai-item-shape-phase-details.md:43-45
  selects a venv under a prohibited temporary root; :93-100 selects the full
  gate output under that root. Caller-supplied execution instructions prohibit
  those file operations. tools/test_check_demo_feedback.py:167-168 also uses
  tempfile.TemporaryDirectory through report_for; changing only the displayed
  venv path does not establish compliant test scratch placement.
* Concern: Literal execution cannot satisfy both these commands and the active
  environment restriction. Research reports successful prior probes but does
  not establish a compliant execution layout for this candidate.
* Impact: Red/green evidence and the single authorized gate/publication sequence
  could be blocked by a predictable path failure or executed contrary to the
  restriction. A failed full run cannot simply be retried under this authority.
* Smallest useful change: Before implementation validation, reconcile the venv,
  test scratch/logs, and unique external gate/receipt locations with the active
  restriction. Specify permitted paths and supported scratch configuration;
  ensure scratch is cleaned before the exact-head clean-input check. Establish
  that existing gate prerequisites and owned scratch can operate compliantly
  before consuming the one full run. If not, stop and report that blocker;
  do not bypass the restriction, change the gate, or silently rerun it.
* Action owner: Planning parent, then implementation executor.
* Exact resolving evidence: Revised P01/P03 details identify compliant execution
  and scratch locations, a new external receipt destination verified absent,
  and the supported prerequisite/setup basis. Commands retain the exact
  authorized base, --all, --lock-timeout 86400 and one-run limit. Alternatively,
  an explicit pre-execution blocker prevents gate/push until compliant.
* Decision route: Direct planner correction. Existing user authority settles
  delivery scope; this finding does not request an alternate gate or permission
  to access another session.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Review completion is not a sufficient delivery prerequisite

* Related IDs: AC5, NFR3, P02-T01/P02-T02, P03-T01/P03-T02.
* Evidence: .copilot-tracking/details/2026-10-23/issue-350-ai-item-shape-phase-details.md:67-71
  says to route any finding to later work; :76-81 proceeds to candidate commit.
  .copilot-tracking/plans/2026-10-23/issue-350-ai-item-shape-plan.md,
  Dependencies, requires Review completion rather than disposition of any
  blocking Review findings. Its gate/push dependencies specify focused and
  gate success, not this separate prerequisite.
* Concern: The plan does not distinguish accepted out-of-scope residuals from
  a newly discovered in-scope defect or missing evidence that blocks delivery.
  Recording the single Review as Complete does not establish its acceptability.
* Impact: The literal sequence could defer a correction-specific blocking
  finding and still spend the one full gate or push a known-defective candidate.
  Local gate success cannot substitute for that finding's disposition.
* Smallest useful change: Make entry to the final-candidate gate/publication
  conditional on no unresolved blocking in-scope Review finding. Preserve the
  original Review and the one-Review limit. Known excluded live/coordinator
  residuals may remain explicit; a new blocker stops delivery for a separately
  authorized follow-up rather than triggering another Review or gate.
* Action owner: Planning parent.
* Exact resolving evidence: P02-T01 and the P03 prerequisites explicitly
  distinguish Review execution from outcome, name the blocking-finding stop,
  and retain original adverse evidence, one Review and one full gate.
* Decision route: Direct planner correction. No significant or divergent user
  decision is needed to avoid publishing unresolved in-scope blockers.

## Strengths and Residual Risk

* Runtime output, not model-input coercion, is the right structural authority.
  String/nonempty checks do not introduce citation semantics, length caps,
  exact key sets or display-field requirements.
* The retained enriched fixture and genuine runtime-validator synthetic output
  are complementary positives, not evidence that a model or deployment ran.
* Existing guards and the six-method/no-removal lock are preserved.
* The commit-before-gate sequence, external authoritative receipt and ban on
  post-gate evidence commits avoid receipt self-reference.
* Shape PASS cannot prove source truth. case_write_reload remains blocked,
  spend_bound/admin_account not-run, and overall acceptance not-accepted.
  Independent coordinator, hosted/human and whole-issue acceptance remain open.

## Questions or Blocking Evidence Gaps

* No unresolved product or semantic-validation decision requires user input.
* PC-001 requires a compliant operational setup or an explicit stop before
  execution. No gate attempt was made to investigate it.

## Limitations

* Research's prior probe/count claims are supplied evidence, not rerun results.
* No tests, gate, identity query, remote access, source edit, commit or push was
  performed. No private data or another worktree/session was accessed.
* Existing prior artifacts are historical; this critique does not replace,
  amend or claim to resolve their outcomes.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Correct operational paths/setup and add PC-002's
  blocking-Review stop, recording dispositions without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-23/issue-350-ai-item-shape-plan.md](.copilot-tracking/plans/2026-10-23/issue-350-ai-item-shape-plan.md) | Assessed final-candidate plan. |
| [.copilot-tracking/details/2026-10-23/issue-350-ai-item-shape-phase-details.md](.copilot-tracking/details/2026-10-23/issue-350-ai-item-shape-phase-details.md) | Assessed execution details. |
| [.copilot-tracking/research/2026-10-23/issue-350-ai-item-shape-research.md](.copilot-tracking/research/2026-10-23/issue-350-ai-item-shape-research.md) | Supplied C1-C8 evidence. |
| [.copilot-tracking/reviews/plans/2026-10-23/issue-350-ai-item-shape-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-23/issue-350-ai-item-shape-plan-critique.md) | This complete, single critique. |

## Next Steps

No user action is required. Return to the active planning parent for direct
disposition of PC-001 and PC-002, without repeating critique. This reviewer
stops after writing this artifact; implementation, Review, gate and delivery
remain the parent's separately controlled actions.
