---
title: Source monitor retry final-candidate plan critique
description: One bounded read-only credibility assessment for issue 332
ms.date: 2026-10-16
---

## Metadata

* Task ID: #332 / source-monitor-retry-332.
* Critique date: 2026-10-16.
* Plan: .copilot-tracking/plans/2026-10-16/source-monitor-retry-332-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/source-monitor-retry-332-phase-details.md
* Critique execution status: Complete.
* Assessment count: One final-candidate critique; no additional critique requested.

## Inputs and Criterion Boundary

* Caller requirements: fix failed-retrieval cadence, demonstrate a next-day
  retry, prove original due() fails the regression tests, retain portable SQL,
  keep application edits in src/ and tests outside packages, validate in a
  local pip venv with both component suites and Ruff/mypy, update component
  READMEs and the reference log, and deliver RPI evidence and a PR with
  Refs #332 only.
* Supplied research:
  .copilot-tracking/research/2026-10-16/source-monitor-retry-332-research.md.
  Its implementation pointers were read directly: core source_monitor.py,
  core tests/test_source_monitor.py and tests/source_monitor_fixture.py, and
  orchestrator source_monitor.py and tests/test_source_monitor.py.
* Supporting evidence: docs/adrs/0006-src-layout-and-cutover.md,
  src/core/pyproject.toml, src/orchestrator/pyproject.toml, component READMEs,
  and .github/workflows/src-ci.yml. Bounded reads of repository context and
  referenced component test helpers informed execution constraints.
* Fixed decisions: success-based cadence, latest-attempt clock guard, core
  ownership of due() semantics, orchestrator ownership of routing/reporting,
  no removed tests, at most three additional core tests and one additional
  job test, and in-memory mutation of due() only.
* Dependencies: P01-T01 implementation and regressions precede P01-T02
  validation; measured validation precedes P02-T01 implementation review and
  P02-T02 publication. Current topic branch is fix/source-monitor-retry-332.
* Assessment boundary: plan credibility against supplied evidence, not
  implementation acceptance. No tests, installations, network research,
  private-data reads, environment-file reads, Azure, Docker or uv execution
  were performed. Only this critique artifact is written. Runtime file
  operations must also avoid system temporary directories.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Failed-attempt cadence / P01-T01 | Covered | Descending observations retain source filtering; cadence uses the first successful observation rather than the newest attempt. |
| Latest-attempt clock guard / P01-T01 | Covered | Phase details explicitly check the newest attempt before scanning for success; failure-only history must not bypass that check. |
| Regression ownership and limits / P01-T01 | Covered | Core semantics and job reports have distinct owners; subtests can cover the stated matrix within the locked addition limits. |
| Failure then next day / P01-T01 | Covered | Replace the existing job assertion that incorrectly skips the day after failure; acceptance requires an actual checked retry and subsequent successful-cadence skip. |
| Original-behavior mutation / P01-T02 | Covered | Original due() is substituted only in memory in a separate interpreter; selected new core and job regressions must fail and restored behavior must pass. |
| Portable SQL and package layout / P01-T01 | Covered | Existing adapter query can select at and body, preserve source_id binding and descending id order, and decode JSON in Python; no schema or dialect extension is needed. |
| Pip venv, component suites and static checks / P01-T02 | Partial | Tooling and suite scope match component configuration, but fixture temporary-file placement is unspecified; PC-001. |
| READMEs and append-only reference log / P01-T01 | Covered | Both component READMEs are in scope, including the orchestrator's explicit faulty failure-cadence statement. |
| Implementation review and RPI evidence / P02-T01 | Covered | One implementation review, reconciled markers/changes/state, and separation of local from external acceptance are explicit. |
| Branch, identity, PR and issue boundaries / P02-T02 | Covered | Existing topic, authenticated privacy identity, trailer, normal push, main-based PR and Refs #332 only are explicit; no merge or issue disposition. |
| Excluded systems and data / all phases | Covered | Private data and forbidden paths/tools are excluded; fixture scratch placement needs the additional execution safeguard in PC-001. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* Rationale: The scheduling design and bounded regression strategy are credible.
  One planner-owned execution correction is required to prevent the planned
  validation from writing fixtures into a forbidden system temporary directory.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Make fixture and pip scratch placement repository-local

* Related IDs: P01-T02; local pip validation; filesystem execution constraint.
* Evidence: src/core/tests/source_monitor_fixture.py creates its SQLite
  database and blob fixture below tempfile.TemporaryDirectory() without a
  directory argument. src/orchestrator/tests/test_source_monitor.py inherits
  that fixture. src/core/tests/dataset.py and
  src/orchestrator/tests/test_digest_blob.py also use TemporaryDirectory().
  .github/workflows/src-ci.yml supplies no local scratch override. The
  P01-T02 details specify src/.venv-332 but no temporary-file override.
* Concern: Creating the venv inside src/ does not relocate Python tempfile
  or pip build scratch. Without a verified override, the prescribed suites
  and mutation tests can create fixture files under a system temporary
  directory, contrary to the active filesystem restriction.
* Impact: Otherwise-correct validation could violate the execution boundary
  or fail before producing acceptable regression and mutation evidence.
* Smallest useful change: Add an execution-only prerequisite to P01-T02:
  create scratch storage within the repository, set TMPDIR to its absolute
  path before pip and each suite/mutation interpreter starts, and verify
  tempfile.gettempdir() resolves inside the worktree. Keep generated scratch
  uncommitted and clean it after validation. Do not edit fixtures, increase
  test additions, add dependencies or create an environment file.
* Action owner: Planning parent, then implementation executor.
* Exact resolving evidence: Revised P01-T02 details state the project-local
  scratch override and preflight. Implementation evidence subsequently records
  the resolved tempfile directory and successful suite/mutation execution
  under that same override, with generated scratch absent from the PR.
* Decision route: Direct planner correction. No significant or divergent user
  decision is needed.

## Strengths and Residual Risk

* The latest-attempt and latest-success clocks remain deliberately separate.
  For a successful observation followed by a later failure, a clock between
  those dates must still raise; only after that check may due() compute the
  interval from the older success. The proposed ordering preserves this.
* No-success history remains due only after passing the latest-attempt guard.
  Successful recovery restores the configured interval and exact boundary.
* Stored successful observations include error: null, so "without an error"
  must mean a decoded non-error value, not absence of the error key.
  This is an implementation clarification of the stated design, not a
  separate missing requirement.
* Existing tests retain approval, append-only evidence and source-isolation
  checks. The proposed new semantic and job coverage fits the locked budget;
  no extra test class or generated test target is required.
* Retrieval success remains distinct from verified legal content and approval.
  No live SQL, hosted scheduling or external acceptance is claimed or needed
  for this bounded local correction.
* Scanning retained observations has history-dependent cost; the proposed
  query already retrieves all attempts in the current implementation.
  The supplied evidence does not establish a new performance blocker or
  justify expanding this issue into schema or indexing work.

## Questions or Blocking Evidence Gaps

* None requiring a user response. PC-001 is directly resolvable by the parent.

## Limitations

* Issue text and account/PR claims were assessed as supplied context, not
  independently fetched. Publication must verify them when executed.
* No implementation or validation was performed. Test assertions must reject
  the original scheduling behavior, not merely fail from import/setup errors.
* Source plans, details and research remain unchanged. No production edits
  or additional workers were used.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add repository-local scratch configuration and its
  preflight to P01-T02, then continue the authorized implementation without
  another plan critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/source-monitor-retry-332-plan.md](.copilot-tracking/plans/2026-10-16/source-monitor-retry-332-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-16/source-monitor-retry-332-phase-details.md](.copilot-tracking/details/2026-10-16/source-monitor-retry-332-phase-details.md) | Assessed task-level details |
| [.copilot-tracking/research/2026-10-16/source-monitor-retry-332-research.md](.copilot-tracking/research/2026-10-16/source-monitor-retry-332-research.md) | Supplied research and implementation pointers |
| [.copilot-tracking/reviews/plans/2026-10-16/source-monitor-retry-332-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-16/source-monitor-retry-332-plan-critique.md) | Complete one-pass critique |

## Next Steps

Planning parent: resolve PC-001 directly in the validation details, reconcile
the critique disposition, and proceed through the already authorized delivery
gates. No user action is required. This reviewer stops after this single
critique; no repeat critique or implementation is performed here.
