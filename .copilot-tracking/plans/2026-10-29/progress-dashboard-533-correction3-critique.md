---
title: Progress dashboard correction3 final-candidate plan critique
description: Independent assessment of malformed lifecycle coverage and local validation feasibility
ms.date: 2026-10-29
---

## Metadata

* Task ID: progress-dashboard-533-correction3
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction3-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/progress-dashboard-533-correction3-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique; no repeat.

## Inputs and Criterion Boundary

* Caller requirements: unknown lifecycle for non-dictionary history elements
  and non-string synthetic actions; bounded audit of history,
  home_case_closures and returns; JSON/SQLite persistence regressions for all
  malformed values; API/core mypy, Ruff lint/format and full units with
  nonblocking heavy-lock admission and the existing browser check.
* Locked decisions: canonical test owner, no removals, at most two additional
  inherited methods, unchanged acceptance criteria, no source outside src,
  no browser/asset implementation, no push, az or force push.
* Primary evidence: supplied correction3 plan, phase details and research C1-C6.
* Source evidence: src/api/src/zava_forward/api/progress.py,
  src/api/tests/test_progress_dashboard.py,
  src/core/src/zava_forward/core/store.py,
  src/core/src/zava_forward/core/sqlstore.py,
  src/api/checks/progress_browser_check.py, src/api/README.md,
  src/api/pyproject.toml and src/core/pyproject.toml.
* Supporting context: src/README.md commands and the supplied research's
  historical correction2 pointer, specifically
  .copilot-tracking/details/2026-10-29/progress-dashboard-533-correction2-phase-details.md.
  Required case-study, knowledge-base index and owner-memory context were read.
  Historical successful validation is not current-candidate evidence.
* Boundary: assess implementation readiness, complete JSON-shaped malformed
  value coverage, persistence feasibility, validation and local Review handoff.
  No implementation, tests, browser, installation, commit or remote operation
  was performed. No external research or wider UI/accessibility audit applies.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C2; P01-T02; unknown history elements/actions | Covered | Collection preflight and string guard before membership address both silent skipping and unhashable actions. |
| C4-C5; P01-T02; three-collection audit | Covered | Auxiliary dictionary guards already precede get calls; JSON tag equality, identity flags and observed timestamp validation require no additional schema restriction. |
| P01-T01; persisted closed/open cases | Partial | JSON save and reopened SQLite body writes are appropriate; history-container cases are not explicitly assigned a roundtrip. PC-001. |
| P01-T01; row/action matrix | Covered | Explicit synthetic admission, preserved valid transitions, before/after positions, all JSON element kinds and missing action are specified. |
| P01-T01; output assertions | Covered | Exact coverage, daily/weekly/episode totals, unknown archive dates and either-bound exclusion prevent false known evidence. |
| C5; positive controls | Covered | Unlabelled dictionary history, synthetic narratives, absent/empty auxiliary lists and ignored malformed auxiliary fields retain defined behavior. |
| Test ownership/removals/budget | Covered | One canonical inherited matrix, existing positive controls, no removals and at most two additional inherited methods suffice for the corrections below. |
| P02-T01; API/core static checks and imports | Partial | Both strict mypy configurations and required Ruff checks exist; worktree source/test precedence is specified, but the execution paths conflict with current filesystem constraints. PC-002. |
| P02-T01; full units/browser/lock | Partial | One nonblocking admission and honest busy-lock fallback are defined; existing pinned-axe real-server check is suitable. Path feasibility remains unresolved. PC-002. |
| P02-T02; independent Review and local stop | Covered | Candidate commit precedes one independent exact-source Review; original outcome is retained, no repeat Review or publication claim is authorized. |
| C6; documentation/pins/scope | Covered | API README is the appropriate contract location; no pinned target or browser source is in scope. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.
* Rationale: The parser correction is credible and bounded. Two direct
  planning corrections are needed: make history-container persistence
  coverage unambiguous and make validation executable, or explicitly blocked,
  without forbidden filesystem operations. Neither changes the locked
  acceptance criteria, test ownership or method budget.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Assign invalid history containers to the persisted matrix explicitly

* Related IDs: C3, P01-T01, JSON/SQLite acceptance criteria.
* Evidence: phase details lines 16-19 describe every malformed history as
  insertion of an invalid row into valid history. Plan lines 65-69 explicitly
  assign malformed containers to sibling collections but name history
  elements/actions instead. In src/api/tests/test_progress_dashboard.py,
  test_non_list_history_is_unknown_without_failing_either_read mutates ZF-4
  in memory; it neither saves nor reopens, and its malformed-container list
  omits floating-point values. The inherited persisted test currently handles
  only home_case_closures and returns.
* Concern: Expanding row/action coverage alone can satisfy the task prose
  while leaving invalid history containers without the owner-required
  JSON/SQLite roundtrip. The existing in-memory test is not that evidence.
* Impact: Container preservation and post-reopen read availability would be
  inferred rather than verified across both backends.
* Smallest useful change: In P01-T01, distinguish whole-container replacement
  from row insertion and synthetic-action mutation. Explicitly include invalid
  history containers: null, string, dictionary, boolean, integer and float.
  Apply the locked closed ZF-1/open ZF-2, explicit-admission, save/reopen and
  output assertions to these values. Preserve valid history around malformed
  rows/actions only; that instruction cannot apply to a non-list container.
  Extend the existing inherited persistence method, without removing tests or
  increasing the locked method budget.
* Action owner: Planning parent; implementation owner executes P01-T01.
* Exact resolving evidence: Revised P01-T01 explicitly enumerates the three
  mutation modes and history-container roundtrips. Implementation evidence
  later identifies passing inherited JSON and SQLite subtests for every
  listed container kind, both case states, exact coverage and either-bound
  archive exclusion.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Resolve validation paths before claiming an executable local gate

* Related IDs: P02-T01, required static/unit/browser validation.
* Evidence: phase details lines 46-53 require editable installation into
  /tmp/mv, optional browser tooling under /tmp/ama-533-venv and new logs/assets
  under /tmp. Plan lines 24-26 also prescribe /tmp tools and the shared lock.
  The current execution boundary disallows /tmp filesystem operations and
  requires newly created files to be workspace-relative. The existing test
  fixture at src/api/tests/test_progress_dashboard.py:106 uses
  tempfile.TemporaryDirectory, so changing only the output argument does not
  establish safe test scratch placement.
* Concern: P02-T01 currently prescribes operations unavailable in this
  execution context, while the details declare no blockers. The source and
  test plan can be implemented, but its validation recipe cannot be followed
  as written.
* Impact: Required checks may fail before exercising the candidate, or their
  execution could violate the filesystem boundary. Substituting a private
  lock would also fail to coordinate with the required shared heavy lock.
* Smallest useful change: Reconcile the validation recipe with the current
  execution boundary. Use permitted workspace-relative locations for newly
  written logs/assets, caches and test scratch where allowed, without editing
  test ownership or browser sources. Retain the requested toolchain and exact
  shared-lock requirements as requirements, not silently replaced equivalents.
  Explicitly mark any check requiring unavailable paths or lock access
  Blocked, preserve its reason, and run only permitted focused/static checks.
  Do not treat lock unavailability as acquired admission or report required
  browser/full-suite work as passed. If the parent executes in a different
  permitted context, record that actual context and its exact commands.
* Action owner: Planning parent; validation executor supplies actual evidence.
* Exact resolving evidence: Revised P02-T01 names permitted write locations
  and scratch/cache controls, identifies any remaining tool/shared-lock access
  blocker, and defines honest completion status. Later evidence records
  API/core mypy, Ruff lint/format, focused/full units and browser separately,
  with command, interpreter/import roots, lock outcome, result and blocker.
  A successful full/browser claim includes actual nonblocking admission to
  the required shared lock; otherwise those checks remain explicitly blocked.
* Decision route: Direct planner correction or explicit environment blocker;
  no user decision authorizing forbidden operations is requested.

## Strengths and Residual Risk

* Rejecting malformed history elements before provenance filtering prevents
  silent loss of evidence. Restricting action validation to explicitly
  synthetic dictionary rows preserves intentional narrative handling.
* The supplied function contains no further JSON element-type hazard in the
  three collection loops once the planned guards are applied. Auxiliary
  equality and identity checks do not require stricter arbitrary-field types.
* Raw constructed SQLite body injection is justified for retained malformed
  evidence; normal mutation validation is not the regression under test.
* Busy-lock targeted fallback is accepted by the plan but is not evidence that
  full suites or the browser passed. Human accessibility, hosted approval and
  publication gates remain outside this local correction.
* A later local closeout commit does not itself establish a fresh Review of
  that new head; preserve the reviewed source commit and original verdict.

## Questions or Blocking Evidence Gaps

* No unresolved user choice prevents the planning assessment. PC-002 records
  an execution feasibility gap; no current tool, lock or dependency
  availability was probed or assumed.

## Limitations

* This is a plan critique, not implementation acceptance. Source inspection
  supports the guard strategy; it does not substitute for red/green,
  persistence, full-suite, static or browser evidence.
* Branch/status inspection found feat/progress-dashboard-533 and the supplied
  untracked correction3 artifacts. Existing inputs were not moved or changed.

## Recommended Next Action

* Highest-impact finding: PC-002.
* Action owner: Planning parent.
* Smallest next action: Reconcile P02-T01 path feasibility and explicit blocked
  outcomes, then clarify the history-container matrix under PC-001.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction3-plan.md](.copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction3-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/progress-dashboard-533-correction3-phase-details.md](.copilot-tracking/details/2026-10-29/progress-dashboard-533-correction3-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-29/progress-dashboard-533-correction3-research.md](.copilot-tracking/research/2026-10-29/progress-dashboard-533-correction3-research.md) | Supplied C1-C6 evidence |
| [.copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction3-critique.md](.copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction3-critique.md) | Original single-pass critique |

## Next Steps

The active planning parent should resolve PC-001 and PC-002 directly and
finalize without another critique. Preserve locked acceptance, ownership,
removals and budget, then continue only within permitted local execution.
No user action, implementation by this critic or remote operation is required.
