<!-- markdownlint-disable-file -->
---
title: Case view review fixes 552 plan critique
description: One independent final-candidate assessment of the two PR 554 fixes
ms.date: 2026-10-29
---

## Metadata

* Task ID: 552-pr554-review-fixes.
* Task slug: case-view-review-fixes-552.
* Critique date: 2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/case-view-review-fixes-552-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/case-view-review-fixes-552-phase-details.md.
* Critique execution status: Complete.
* Original verdict: Revise.
* Execution count: one independent final-candidate assessment; no second critique.

## Inputs and Criterion Boundary

* Caller requirements: fix exactly the direct-child summary selector and missing
  API wheel PNG package data on feat/case-view-ux-552 / PR #554. Preserve the
  absorbed rubric commit, prohibit push, az, rubric edits and unrelated fixes.
* Assessed research:
  .copilot-tracking/research/2026-10-29/case-view-review-fixes-552-research.md,
  including C1-C8 and its recorded pre-fix browser and wheel failures.
* Assessed plan and phase details: the exact paths in Metadata, including
  AC1-AC5, P01-T01, P01-T02 and P02-T01.
* Confirmed decisions: exactly one added manifest regression in the existing
  test_case_journey.py using tomllib/fnmatch against six known PNG paths; no
  removed tests, production JavaScript/CSS changes or dependency changes.
* Dependencies: existing interpreter/tooling, synthetic owned loopback browser,
  pinned axe, actual wheel build, one independent Review and local-only commit.
* Boundary: assess credibility of this bounded candidate from supplied evidence,
  not issue-wide acceptance, redesign, live deployment or publication readiness.
  Mandatory project context was read; no additional research or source audit
  was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Selector requirement; C1-C2; AC1 | Covered | Exact .case-summary > dl > div > dt selector preserves nested semantics and exercises the existing six-term browser assertion. |
| Packaging requirement; C3-C5; AC2 | Covered | Explicit nested PNG glob fixes the wheel boundary; fresh ZIP member and source-byte comparisons distinguish packaging proof from source serving. |
| Test budget; C6; P01-T01 | Covered | One manifest method, six known paths, existing source-file and deck-byte provenance retained, no removals or new framework. |
| Focused checks; AC3; P01-T02 | Covered | Five named modules, supplied PYTHONPATH, targeted ruff lint/format and both relevant JavaScript syntax checks are specified. |
| Browser checks; C7; AC4 | Covered | Full journey and compact checks, synthetic loopback ownership, desktop/narrow evidence and honest later failures are explicitly retained. |
| Evidence output dependencies; P01-T02; P02-T01 | Partial | PC-001: specified generated-output locations cannot be used in the current execution environment. |
| RPI reconciliation; AC5; P02-T01 | Covered | Independent Review follows reconciliation; local privacy-safe identity, Conventional Commit, trailer and task-owned staging are explicit. |
| Prior outcomes; C8; scope constraints | Covered | Original Partial/RV-001 preserved; no push, cloud operation, rubric edit or publication claim is authorized. |

## Verdict

* Verdict: Revise.
* Rationale: the technical corrections, proof strategy and locked test budget are
  credible. One direct execution-path correction is required before the planned
  validation can run within this environment. No technical scope expansion or
  additional test is needed.
* Severity summary: Critical 0; High 0; Medium 1; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Use permitted persistent locations for generated validation evidence

* Related IDs: P01-T02, P02-T01, AC2, AC4.
* Evidence: .copilot-tracking/details/2026-10-29/case-view-review-fixes-552-phase-details.md
  directs new browser output, wheel output and an optional target installation
  into /tmp locations. The plan also requires external generated evidence.
  Those generated-output locations are unavailable under this executor's
  filesystem constraints.
* Concern: the validation commands are not executable as written in the current
  environment. A permitted evidence location must be established before wheel
  creation, browser output or an optional target install.
* Impact: otherwise AC2 and AC4 can be blocked by output-location restrictions
  rather than by either requested fix, and the independent reviewer cannot be
  supplied the intended persistent evidence.
* Smallest useful change: planning parent should replace generated-output
  destinations with explicit persistent project-relative paths outside the
  task's commit set, and update the review handoff accordingly. For example,
  use .local-evidence/case-view-review-fixes-552/ from the repository root and
  ../../.local-evidence/case-view-review-fixes-552/ from src/api. Account for
  build/browser scratch output as necessary using permitted locations. Preserve
  the supplied PYTHONPATH, existing test/tool choices, test budget and exact
  path/byte and browser assertions; do not install dependencies or alter
  production code merely to relocate evidence.
* Action owner: planning parent.
* Exact resolving evidence: a direct disposition in the plan/details names
  permitted generated-output and scratch paths consistently from each working
  directory; subsequent changes evidence records the actual wheel and browser
  artifact locations and outcomes; the review handoff grants read access to
  those artifacts; the local commit excludes generated output. Preserve this
  original Revise verdict. No second critique is required.
* Decision route: direct planner correction to execution paths, not a
  significant or divergent user decision.

## Strengths and Residual Risk

* Both defects have recorded actual reproductions, not merely inferred causes.
* The existing browser owns six-term semantic coverage; the single new manifest
  test prevents accidental configuration loss without duplicating deck-byte
  provenance or pretending to prove a wheel build.
* Exact wheel paths and bytes are stronger packaging evidence than successful
  source HTTP responses. The optional target install is not necessary to AC2.
* Existing production JavaScript/CSS and Docker behavior remain unchanged.
* Full browser failures must remain visible even if AC1 independently passes.
  Prior RV-001, deployed-container behavior, hosted/publication gates and human
  acceptance are explicitly outside this bounded local acceptance.

## Questions or Blocking Evidence Gaps

* No unresolved user decision or decision-critical research gap.
* PC-001 requires a direct operational correction, not new research.

## Limitations

* Supplied C1-C8 and baseline outcomes were assessed as recorded evidence, not
  independently rerun. This is a plan critique, not implementation acceptance.
* No source changes, validation runs, remote operations or further critique were
  performed. Existing uncommitted parent artifacts were left untouched.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: directly disposition PC-001 with permitted evidence
  paths, then proceed to P01 under the existing full-loop authorization.
* User response required: no.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/case-view-review-fixes-552-research.md](.copilot-tracking/research/2026-10-29/case-view-review-fixes-552-research.md) | Supplied reproductions and bounded research. |
| [.copilot-tracking/plans/2026-10-29/case-view-review-fixes-552-plan.md](.copilot-tracking/plans/2026-10-29/case-view-review-fixes-552-plan.md) | Assessed final candidate. |
| [.copilot-tracking/details/2026-10-29/case-view-review-fixes-552-phase-details.md](.copilot-tracking/details/2026-10-29/case-view-review-fixes-552-phase-details.md) | Assessed tasks and commands. |
| [.copilot-tracking/reviews/plans/2026-10-29/case-view-review-fixes-552-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/case-view-review-fixes-552-plan-critique.md) | Original independent critique and complete finding set. |

## Next Steps

Planning parent directly corrects the PC-001 execution paths and records its
disposition, preserving this original verdict. Continue implementation and the
single independent Review without another critique. No user action is required.
