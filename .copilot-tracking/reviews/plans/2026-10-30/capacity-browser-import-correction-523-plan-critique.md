---
title: Capacity browser import correction plan critique
description: Independent final-candidate critique for task 523-correction-1
ms.date: 2026-10-30
---

## Metadata

* Task ID: 523-correction-1.
* Critique date: 2026-10-30.
* Plan: .copilot-tracking/plans/2026-10-30/capacity-browser-import-correction-523-plan.md.
* Phase details: .copilot-tracking/details/2026-10-30/capacity-browser-import-correction-523-phase-details.md.
* Critique execution status: Complete.
* Assessment count: One independent final-candidate critique.
* Branch observed: fix/capacity-work-orders-page-523.
* PR context: PR #577, Refs #523 only.

## Inputs and Criterion Boundary

The assessment covers the supplied plan, phase details and
.copilot-tracking/research/2026-10-30/capacity-browser-import-correction-523-research.md,
against the caller's correction-cycle requirements. Named implementation
evidence inspected:

* src/api/checks/capacity_browser_check.py.
* src/api/tests/test_capacity_browser_check.py.
* src/api/tests/test_regulatory_ux_check.py.
* src/api/pyproject.toml.
* src/api/README.md, local engineering checks.

Repository context was consulted in docs/case_study_48_original.md,
docs/case_study_48_addendum.md, docs/reference/README.md and
docs/reference/memory.md. This is a bounded plan assessment, not a new
reproduction, implementation review, publication gate or accessibility audit.
The supplied reproduction is accepted as reported evidence; no new test run
or remote inspection was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC1; research C1-C2; P01-T01 | Covered | Research records the fresh-process loader failure; implementation must separately preserve the new regression's baseline failure before editing the harness. |
| AC2; P01-T01; test ownership lock | Covered | Exactly four named existing scanner/pin tests run under denied Playwright imports; count and no-skip assertions prevent empty success. Explicit selection avoids recursive subprocess tests. |
| AC3; P01-T01-T02 | Covered | Local imports at the beginning of check precede the current store.staff access and server construction. check(None) under the blocker detects incorrect placement. |
| Lazy imports and annotations; research C6-C7 | Covered | Postponed annotations plus TYPE_CHECKING cover Page, Request, Response and Route; expect and sync_playwright remain real execution-time imports. |
| Browser-independent mocks; existing assertions | Covered | Two evaluate-only mock substitutions preserve scanner JSON, violations, WCAG tag, app-root and pin assertions. No test removals or dependency changes are planned. |
| AC4; P02-T01 | Partial | Exact caller PYTHONPATH and four required checks are retained, but the specified lock cannot be used in the active execution environment; PC-001. |
| P01-T03 | Covered | Existing README promises runtime-only unit discovery and explicit browser failure, making a capacity clarification directly relevant. |
| AC5; P02-T02-T03 | Covered | One independent critique and Review, preservation of adverse evidence, privacy-safe local identity, trailer and local-only commit are explicit. |
| Branch, PR, issue and scope boundaries | Covered | Existing branch is explicit; PR #577 and Refs #523 remain bounded. No cloud, sign-in, secrets, uv, push or issue-completion claim is authorized. |
| Dependencies and inherited gates | Covered | Existing pinned tools and current-worktree source paths are required; full publication and live acceptance remain unmet and coordinator-owned. |

## Verdict

* Verdict: Revise.
* Severity summary: Critical 0, High 1, Medium 0, Low 0.
* Rationale: The implementation and regression design is credible. The
  heavy-validation locking requirement has an unresolved execution constraint,
  so AC4 cannot currently be completed as planned.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Resolve the unavailable mandatory lock location before heavy validation

* Related IDs: AC4; P02-T01; User Decisions and Requirements.
* Evidence: The caller and
  .copilot-tracking/details/2026-10-30/capacity-browser-import-correction-523-phase-details.md,
  P02-T01, require flock -w 600 /tmp/ama-rpi-heavy.lock. The active execution
  environment prohibits file operations in /tmp and other temporary directories.
* Concern: Opening the required lock is itself a prohibited file operation.
  The plan supplies neither a permitted shared-lock agreement nor an explicit
  blocked disposition for this conflict.
* Impact: Heavy validation cannot follow the prescribed serialization command.
  Running unlocked or silently choosing a private worktree lock would not
  establish coordination with other heavy-check participants; claiming AC4
  would therefore be unsupported.
* Smallest useful change: Record P02-T01 as blocked pending an agreed permitted
  shared lock location or a compliant execution environment. Do not silently
  substitute a lock, omit serialization or mark validation successful.
* Action owner: Planning parent coordinates resolution with the execution owner.
* Exact resolving evidence: An explicit approved execution arrangement in the
  plan/details that is permitted by the runtime and preserves a common lock
  across competing heavy checks, followed by recorded acquisition with the
  600-second wait and the exact required validation commands and outcomes.
  Until then, preserve a blocked validation status.
* Decision route: Direct planner correction to record the blocker. Changing the
  caller's specified lock protocol requires an execution-owner/user decision;
  this critique does not authorize that change.

## Strengths and Residual Risk

* The baseline defect is grounded in actual module-level imports, not inferred
  solely from whether Playwright happens to be installed.
* Executing the existing scanner tests under the import blocker is stronger
  than import-only coverage and preserves the locked maximum of two additions.
* TYPE_CHECKING imports and deferred annotations preserve strict typing without
  turning a dev dependency into a runtime requirement.
* No broader source changes, tests, skips, exclusions or dependency additions
  are needed from the supplied evidence.
* Passing local correction checks would not establish full issue acceptance,
  publication readiness, hosted approval or live human verification.

## Questions or Blocking Evidence Gaps

* PC-001 requires a permitted shared-lock execution arrangement before heavy
  validation. No further research trace or additional critique is requested.

## Limitations

* The assessment verifies planning credibility, not implementation correctness.
  Environment executables, full discovery and tool outcomes remain to be
  demonstrated during implementation.
* Existing untracked correction artifacts were observed and left unchanged.
  Only this critique artifact was written; no source, plan, phase details,
  research, workflow state or historical review record was edited.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Record the locking blocker and resolve a compliant
  shared-lock arrangement before scheduling P02-T01.
* User response required: Yes for a change to the mandated locking protocol,
  unless the execution owner can provide a compliant environment retaining it.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/capacity-browser-import-correction-523-plan.md](.copilot-tracking/plans/2026-10-30/capacity-browser-import-correction-523-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/capacity-browser-import-correction-523-phase-details.md](.copilot-tracking/details/2026-10-30/capacity-browser-import-correction-523-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-30/capacity-browser-import-correction-523-research.md](.copilot-tracking/research/2026-10-30/capacity-browser-import-correction-523-research.md) | Supplied reproduction and source evidence |
| [.copilot-tracking/reviews/plans/2026-10-30/capacity-browser-import-correction-523-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/capacity-browser-import-correction-523-plan-critique.md) | Complete independent critique |

## Next Steps

Return to the active planning parent for direct disposition of PC-001. Preserve
this original verdict, resolve the execution constraint, and finalize the plan
without another critique. Do not run blocked heavy checks, publish or push.
