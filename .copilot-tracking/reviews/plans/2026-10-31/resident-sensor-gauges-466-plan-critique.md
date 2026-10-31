---
title: Resident issue 466 final-candidate plan critique
description: One independent bounded assessment of the 2026-10-31 candidate
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: 466; resident-sensor-gauges-466.
* Critique date: 2026-10-31.
* Plan: .copilot-tracking/plans/2026-10-31/resident-sensor-gauges-466-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/resident-sensor-gauges-466-phase-details.md
* Critique execution status: Complete.
* Execution count: exactly one independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requires ordered full RPI, reuse of merged runtime, own-home synthetic
  gauges/history, isolated advisory AI and standing IoT priority. Deployed AI
  stays off behind existing settings. Local API discovery, Ruff and Playwright
  remain mandatory, with pip only and no Azure, credentials, private data,
  main/other-worktree or mvp edits. Publication is conditional on the full gate
  and independent exact-head eligibility; use Refs #466.
* Supplied research:
  .copilot-tracking/research/2026-10-31/resident-sensor-gauges-466-research.md,
  Q1-Q3, C1-C8 and W1-W4. Its provenance records reading the issue body first.
  This critique also read the current issue body; its unchecked decisions do
  not supersede the explicit current caller direction or merged decision.
* Bounded evidence read: docs/architecture/resident-assistant-prototype.md,
  src/api/README.md:1200-1330, and
  .copilot-tracking/reviews/logs/2026-10-30/resident-sensor-gauges-466-review.md:125-200.
  Necessary lock evidence: tools/rpi-checks.py:2273-2288 and
  src/README.md:109-125. Repository context was read from the original case
  study, bounded addendum/index sections and owner memory.
* Assessed all seven ACs, P01-P03, their tasks, dependency order, zero new or
  removed tests, unchanged runtime, accepted AT/actual-model limits and
  conditional publication. Earlier 2026-10-30 outcomes remain historical.
* Boundary: credibility of the documentation-only candidate and its executable
  validation/publication instructions. No fresh test result, live setting,
  billing, actual-model quality or human acceptance is inferred.
* Branch inspected: feat/resident-sensor-gauges-466; HEAD and recorded
  origin/main both 5666bd33e1827670e5c07e3e3063bbbe989b59d3. Existing untracked
  caller RPI inputs were neither moved nor edited. No fetch or publication
  eligibility assessment was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1-Q3; C1-C8; W1-W4 | Covered | Supplied convergence supports reuse, current decision reconciliation and retained acceptance limits. |
| AC1; P01-T01 | Covered | Explicit current direction supplies scope/priority; old unproven wording needs prospective correction, not historical outcome replacement. |
| AC2; AC4 | Covered | Existing sensor/isolation suites and browser checks are designated for fresh synthetic-only exercise. |
| AC3 | Covered | Current API guide distinguishes typed generated prose, protected document facts, own-case authorization and advisory limits. |
| AC5 | Covered | Existing native/text/keyboard/reflow checks retained; manual AT and incomplete-rule acceptance are explicitly separate. |
| AC6 | Covered | Dated merged decision records regional mini, permanent USD20 inside USD30 and managed identity; activation/expiry unchanged. |
| AC7; P02-T01 | Partial | Exact caller discovery invocation is not written out; prohibited lock location makes heavy-check instructions unsafe. PC-001, PC-002. |
| P02-T02 | Covered | One independent Review, preserved findings, no repeated Review or acceptance by proxy. |
| P03-T01 | Partial | Correct clean-commit/receipt/exact-head sequence, but mandatory runner creates a prohibited lock. PC-001. |
| Scope; dependencies; test ownership | Covered | Four documentation targets, index/log maintenance, ordered prerequisites, no runtime/UI/infra changes or test additions/removals. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0; High 1; Medium 1; Low 0.
* Rationale: Documentation-only delivery is supported and does not need new
  runtime or a replacement model decision. However, the candidate presently
  directs prohibited filesystem operations and calls validation implementation
  ready without a compatible mandatory gate. Exact required discovery should
  also be made executable without relying on an implicit caller reference.
  Both concerns can be dispositioned directly by the planning parent; neither
  justifies activating AI or changing historical acceptance outcomes.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Mandatory heavy-check and publication instructions conflict with the no-temporary-directory boundary

* Related IDs: AC7; P02-T01; P03-T01; readiness and publication dependencies.
* Evidence: The phase details explicitly prescribe
  /tmp/ama-rpi-heavy.lock for P02. tools/rpi-checks.py:2273-2276 hardcodes that
  same path and opens it with O_CREAT for the mandatory full gate. The caller
  environment prohibits all /tmp and temporary-directory file operations.
  src/README.md:109-125 requires the same shared lock for heavy checks; simply
  choosing another task-local lock would not preserve shared serialization.
* Concern: External output alone does not remove the runner's prohibited
  write. The documentation-only scope excludes the tooling change needed to
  make that runner compatible. Current readiness statements acknowledge
  generic gate failures but not this known prerequisite incompatibility.
* Impact: The parent cannot safely execute the prescribed heavy checks or
  obtain the required publication receipt as written. A successful browser
  check or alternative lock cannot authorize a push in place of that gate.
* Smallest useful change: Remove instructions to use the prohibited path,
  explicitly record the known validation/publication blocker in the plan and
  details, and make P02 heavy execution and P03 dependent on a compliant
  shared-lock/full-gate capability. Keep documentation-only scope, original
  evidence and publication prohibitions intact. Do not patch tooling, bypass
  locking or claim receipt eligibility inside this bounded task.
* Action owner: Planning parent for the direct disposition; separately
  authorized tooling owner for any later shared-runner remediation.
* Exact resolving evidence: Revised plan/details name the incompatible
  hardcoded lock and keep affected execution/publication blocked. Unblocking
  later requires a reviewed compliant runner/shared coordination mechanism
  with no forbidden writes, followed by the actual full-gate receipt and
  fresh exact-head assessment; a changed output directory is insufficient.
* Decision route: Direct planner correction to record the blocker; no user
  response is needed for that correction. A source/tooling scope expansion
  is a separate significant decision and is not authorized by this critique.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The required exact API discovery command remains implicit

* Related IDs: AC7; P02-T01.
* Evidence: The plan says "caller API discovery"; phase details say "run
  exactly caller PYTHONPATH discovery" without the full value or invocation.
  Caller requires PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests.
  src/api/README.md contains several different focused command variants;
  none should silently replace the requested full discovery.
* Concern: The phase-details artifact does not independently specify the
  exact required command, although AC7 depends on its recorded execution.
* Impact: A runner can execute a focused resident selector or omit the
  caller-required path entries and still mistakenly mark AC7 complete.
* Smallest useful change: Write the exact invocation, with working directory
  src/api, in P02-T01:
  `PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q`.
  Keep `ruff check .` and `ruff format --check .` explicit and retain
  exit/count/skip/failure reporting. Do not execute until PC-001 is cleared
  for the affected heavy validation.
* Action owner: Planning parent.
* Exact resolving evidence: Phase details contain the complete discovery
  command and working directory; eventual engineering evidence records that
  invocation's real exit status, discovery counts and skips, not a focused
  selector or historical log.
* Decision route: Direct planner correction; no significant or divergent
  user decision and no new tests are required.

## Strengths and Residual Risk

* Existing runtime plus explicit current direction makes documentation
  reconciliation preferable to duplicate sensor/AI implementation.
* The plan preserves model/cap/identity decisions, deployment-off settings,
  tariff expiry, synthetic-only data and no submission/consent authority.
* Historical sentence-selection wording is preserved while a dated current
  section can explain eligible generated questions and protected facts.
* Manual accessibility/AT, actual-model relevance, live service and renewed
  authority remain expressly outside this task. These accepted boundaries
  are not new PC findings or a basis for a closing keyword.
* One original independent Review and a separate final exact-head assessment
  are appropriate distinct gates; neither substitutes for the full receipt.

## Questions or Blocking Evidence Gaps

* No missing scope/model decision requires asking the owner again.
* PC-001 is a confirmed tooling/constraint incompatibility, not an unverified
  hypothesis. Publication remains blocked until compatible capability exists.

## Limitations

* No application/static/browser validation, Azure operation, credential lookup,
  private-data access, tool modification or publication was performed.
* Runtime coverage is assessed from supplied source-backed research and
  bounded guide/original-review evidence, not independently re-established
  by a whole-project investigation.
* Only this critique artifact was written. Plan, details, research, source and
  earlier 2026-10-30 records remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Record the known lock incompatibility and blocked
  heavy-validation/publication dependency, then make the PC-002 command
  explicit. Finalize dispositions without another critique.
* User response required: No for these direct planner dispositions.

| .copilot-tracking/research/2026-10-31/resident-sensor-gauges-466-research.md | Supplied current-main research and decision evidence. |
| .copilot-tracking/plans/2026-10-31/resident-sensor-gauges-466-plan.md | Candidate requiring direct dispositions. |
| .copilot-tracking/details/2026-10-31/resident-sensor-gauges-466-phase-details.md | Execution instructions requiring correction. |
| .copilot-tracking/reviews/plans/2026-10-31/resident-sensor-gauges-466-plan-critique.md | This single independent critique. |
| .copilot-tracking/reviews/logs/2026-10-30/resident-sensor-gauges-466-review.md | Preserved historical outcomes and acceptance limits. |

## Next Steps

Planning parent directly dispositions PC-001 and PC-002, retains blocked gates,
and finalizes planning without a second critique. No user action is required
for those dispositions. Stop this critique here; no peer stage is invoked.
