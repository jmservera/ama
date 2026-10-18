---
title: Issue 120 DPIA reference plan critique
description: Sole independent final-candidate assessment of the bounded implementation plan
ms.date: 2026-10-18
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: issue-120
* Task slug: issue-120-dpia-reference
* Critique date: 2026-10-18
* Plan: .copilot-tracking/plans/2026-10-18/issue-120-dpia-reference-plan.md
* Phase details: .copilot-tracking/details/2026-10-18/issue-120-dpia-reference-phase-details.md
* Required and observed source HEAD: a86282c4badebc58eabbf9e441410d930a201ac2
* Required and observed branch: fix/time-capture-dpia-reference-120
* Critique execution status: Complete
* Review identity: One independent final-candidate plan critique; no additional critique or review agents invoked.

## Inputs and Criterion Boundary

* Caller requirements: Refuse absent/blank and trimmed case-insensitive yes,
  true, on and 1; expose false dpia_recorded/enabled and a plain reference
  reason; refuse all four writers without a fresh fallback database or new
  rows; retain literal-seeded invalid history across restart on fallback and
  shared SQLite; disable immediately after a valid-to-flag switch; require a
  renewed request and activation for a different valid reference.
* Preservation boundary: D1, trimmed DPIA-2026-007 and other non-prefix
  references; manager separation; notice acknowledgement/version; audit;
  aggregate minimum groups; own entries; shared SQL behavior. No arbitrary
  format, approval service, server, schema, shared fixture or web changes.
* Test ownership: Existing src/api/tests/test_timecapture.py only, no removals,
  at most seven added methods and two small helpers. Task evidence is not a
  replacement test suite.
* Supplied research: .copilot-tracking/research/2026-10-18/issue-120-dpia-reference-research.md,
  C1-C12 and selected/discarded alternatives.
* Retained experiments:
  .copilot-tracking/research/2026-10-18/issue-120-dpia-reference-baseline-probe.log
  and .copilot-tracking/research/2026-10-18/issue-120-dpia-reference-contrarian.log.
  The caller's shortened log names resolve to these existing prefixed files.
* Relevant repository evidence: Current timecapture.py, test_timecapture.py,
  the narrow time-capture README section, API tooling configuration,
  Dockerfile, existing HTTP time-write handlers and the cited historical
  2026-10-15 review. The retained probe was read to assess its execution needs.
  Required project context was read from the original case study, addendum
  opening, reference index and owner memory.
* Dependencies and decisions: P01 follows critique disposition; P02 follows
  retained failing-first tests; P03 follows implementation. Exactly one later
  original Review and at most two later correction cycles remain separate
  gates. Human governance and coordinator acceptance are not implementation
  results.
* Assessment boundary: Plan credibility and executable verification design,
  not an implementation review, current legal assessment, authenticity check
  or approval. Only this critique artifact is written.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1 / AC1 / C1-C4 / P02-T01 | Covered | One derived predicate controls both the reason and dpia_recorded; the matrix includes missing, blank, mixed case and outer whitespace. Flag-off reason precedence is preserved. |
| FR2 / AC2 / P01-T01 | Covered | Four direct writer denials, absent fresh fallback file and parent, unchanged four-table contents, plus authenticated existing-handler HTTP denials and no time audit events. |
| FR3 / AC3 / P01-T01 | Covered | Literal DDL/INSERT historical controls and acknowledgement, distinct managers, matching references/current notice, row comparisons and restart on fallback and shared SQLite are explicit. These are planned tests, not existing passing evidence. |
| FR4 / AC4 / P01-T01 | Covered | Same-instance valid-to-flag mutation and denied writes, followed by D2 requiring both renewed steps, are specified. |
| FR5 / AC5 / C5-C6 / P01-T01 | Covered | D1, padded DPIA-2026-007 and non-prefix strings with stored trimming; unchanged existing manager, notice, audit, aggregate, own-entry and shared-store tests. |
| AC6 / P02-T01 | Covered | Narrow README/module explanation rejects flags without inventing formats or representing presence as authenticity/legal approval. |
| Test ownership / P01-T01 | Covered | Existing test file, zero removals, seven-method/two-helper ceiling and one HTTP regression are locked. No separate module, server or shared fixture edit is needed. |
| SQL/runtime boundary / C10-C12 / P03-T01 | Covered | Exact-base AST comparison outside status/module prose, explicit DDL/statements/storage/import preservation and original hashes are required. SQL/runtime expansion requires authorization. Historical engine claims are not promoted to current results. |
| Compliant local execution / P01-T01 / P03-T01 | Partial | PC-001: Default temporary-directory use is not redirected to a repository-local scratch root in the validation instructions. |
| Review and delivery gates | Covered | Sole critique, one later original Review, retained adverse evidence, maximum two later corrections and coordinator/human gates remain separate. |

## Verdict

* Verdict: Revise
* Severity summary: Critical 0; High 0; Medium 1; Low 0.
* Rationale: The bounded implementation and semantic verification strategy are
  credible. One execution prerequisite must be made explicit so the planned
  tests and probe can run without violating the supplied filesystem boundary.
  This is a direct planner correction, not a significant user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Constrain validation scratch storage before running existing tempfile-based tests

* Related IDs: P01-T01, P03-T01, AC2, AC3; supplied no-/tmp filesystem constraint.
* Evidence: .copilot-tracking/details/2026-10-18/issue-120-dpia-reference-phase-details.md:47-49
  calls for synthetic HTTP data in a temp directory; lines 79-88 require the
  existing suite, retained probe and practical image execution without a
  repository-local scratch setup.
  src/api/tests/test_timecapture.py uses tempfile.TemporaryDirectory() in
  TimeTests.setUp and SharedStoreTests.
  .copilot-tracking/research/2026-10-18/issue-120-dpia-reference-probe.py uses
  default tempfile.TemporaryDirectory() in both probes.
  .copilot-tracking/research/2026-10-18/issue-120-dpia-reference-baseline-probe.log
  records a historical local-store path under /tmp.
* Concern: No planned command establishes a permitted scratch root before
  those Python processes start. Running the listed commands unchanged can
  therefore repeat default system-temporary-directory writes, which the
  current execution instructions explicitly forbid. The historical path is
  evidence of the risk, not authorization to reproduce it.
* Impact: Failing-first and post-change verification lack a compliant execution
  prerequisite. The implementer must either improvise that prerequisite or
  execute outside the permitted filesystem boundary.
* Smallest useful change: Add one shared validation precondition to the plan
  and phase details: create a task-owned scratch directory beneath this
  worktree, set TMPDIR to its absolute path before launching every test/probe
  Python process, and keep generated logs and fixtures within task-owned
  repository paths. For any attempted image probe, supply an equivalent
  writable task-owned repository mount and scratch environment without
  changing the Dockerfile or runtime source. Clean up generated scratch
  contents after evidence capture. Do not alter the retained adverse log or
  existing shared fixtures, and do not spend a test helper/method on this
  command-level setup.
* Action owner: Planning parent; implementing agent executes the finalized
  command-level precondition.
* Exact resolving evidence: Plan and phase-details instructions explicitly
  establish the repository-local scratch root and environment for P01/P03;
  implementation logs later record the actual commands and
  tempfile.gettempdir() resolving beneath the task worktree in the launched
  process. Any attempted container probe records its repository-backed
  writable scratch mapping, or its blocker. The original adverse baseline
  remains unchanged.
* Decision route: Direct planner correction. Current instructions already
  resolve the filesystem choice; no significant or divergent user decision
  and no user response are required.

## Strengths and Residual Risk

* Both _ready_to_enable and _require consume status in the exact-base source.
  The proposed local predicate therefore covers request, activation,
  acknowledgement and recording without a persistence redesign.
* Literal-seeded historical controls avoid a circular regression test that
  depends on the newly guarded writers creating the invalid state.
* The supplied baseline log actually records two failing tests and four HTTP
  200 results; the contrarian log records accepted short/padded/non-prefix
  references and restart behavior. Neither proves the future fix.
* Existing tests directly cover separation of duties, versioned/per-person
  acknowledgement, audit, aggregate suppression, own entries and shared
  SQLite persistence. Rerunning them is appropriately narrower than adding an
  unrelated role suite or repeating destructive engine fixtures.
* The plan explicitly discloses formatter/mypy exclusions. Configured tooling
  success must not be described as full static checking of these legacy files.
* Historical SQL Server review evidence remains historical. Unchanged-source
  comparison and current synthetic SQLite tests can support a bounded
  non-change claim, not a fresh SQL Server execution claim.
* Reference presence does not verify an approval's authenticity or complete
  the DPIA, consultation, notice ratification or issue acceptance.

## Questions or Blocking Evidence Gaps

* No unresolved significant user decision or decision-critical research gap.
* PC-001 is resolvable entirely by the planning parent before implementation.

## Limitations

* No tests, probe, Docker build, engine fixture or model call were executed
  during this critique. Baseline and contrarian outcomes are retained
  historical observations, not new executions.
* Git read-only inspection verified the requested branch/HEAD and no tracked
  changes in the three proposed implementation paths against the exact base.
  Existing untracked planning/research/session artifacts were left untouched.
* No private .env, ZF_DATA, support material, Azure/IAM/Graph/spend resources or
  unrelated issue discovery was accessed. No live governance approval or
  legal-currentness assertion is made.
* The full supplied criterion boundary was assessed once. This is the complete
  actionable finding set; no discoverable findings are withheld for another
  critique cycle.

## Recommended Next Action

* Highest-impact finding: PC-001, Medium.
* Action owner: Planning parent.
* Smallest next action: Finalize the repository-local scratch precondition in
  the plan/details and record this critique's disposition, then proceed to P01.
* User response required: No.
* Do not run another plan critique. Preserve this original and perform the one
  original implementation Review only at its later gate; at most two later
  correction cycles remain permitted.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-18/issue-120-dpia-reference-plan.md](.copilot-tracking/plans/2026-10-18/issue-120-dpia-reference-plan.md) | Assessed final-candidate plan; unchanged |
| [.copilot-tracking/details/2026-10-18/issue-120-dpia-reference-phase-details.md](.copilot-tracking/details/2026-10-18/issue-120-dpia-reference-phase-details.md) | Assessed phase details; unchanged |
| [.copilot-tracking/research/2026-10-18/issue-120-dpia-reference-research.md](.copilot-tracking/research/2026-10-18/issue-120-dpia-reference-research.md) | Supplied bounded research |
| [.copilot-tracking/research/2026-10-18/issue-120-dpia-reference-baseline-probe.log](.copilot-tracking/research/2026-10-18/issue-120-dpia-reference-baseline-probe.log) | Retained adverse original |
| [.copilot-tracking/research/2026-10-18/issue-120-dpia-reference-contrarian.log](.copilot-tracking/research/2026-10-18/issue-120-dpia-reference-contrarian.log) | Retained valid-reference observations |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-120-dpia-reference-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-120-dpia-reference-plan-critique.md) | Sole independent critique and complete finding set |

## Next Steps

Planning parent addresses PC-001 directly and finalizes without another
critique. No user action is required. This critique execution stops here; no
implementation, plan edit, commit or original implementation Review is performed.
