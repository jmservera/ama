---
title: Rubric src cut-over final-candidate plan critique
description: Single bounded credibility assessment for issue 198
ms.date: 2026-10-27
---

## Metadata

* Task ID: 198
* Task slug: rubric-src-198
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/rubric-src-198-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/rubric-src-198-phase-details.md
* Critique execution status: Complete
* Assessment count: One final-candidate critique; no nested agents.

## Inputs and Criterion Boundary

* Caller requirements: ordered Research, Plan, Implement and independent Review;
  local-only validation; no full --all gate, cloud, private data, workflow/check
  renaming or rubric_version bump; eventual draft PR with Refs #198.
* Research considered:
  .copilot-tracking/research/2026-10-27/rubric-src-198-research.md,
  C1-C8/W1-W3 and its explicit evidence limitations.
* Named sources inspected: .github/rubric/artifacts.json,
  .github/rubric/rubric.json through source references,
  .github/rubric/scores/latest.json,
  .github/rubric/README.md:344-404,
  .github/rubric/scripts/test_gate.py,
  .github/rubric/scripts/test_prepare.py,
  .github/rubric/scripts/test_safe_output_runtime.py and
  .github/rubric/scripts/prepare.py and gate.py.
* Workflow YAML was parsed read-only to check the current trigger matrix.
  Relevant ADR 0006 layout/counting sections and the original/later cut-over
  evidence sections were read. Repository context included the case-study
  original/addendum and knowledge-base index/memory; memory is not evidence.
* Decisions and dependencies: production registry changes are already delivered;
  P02 follows P01; at most two new test functions; existing tests are repaired
  in place; one unrelated deck failure and unavailable historical scorecards
  remain disclosed rather than repaired or invented.
* Boundary: assess implementation credibility, test shapes, fixture stability,
  evidence truthfulness and scope constraints, not score quality, issue closure,
  application acceptance, live authority or publication approval.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C3; src includes/excludes | Covered | Registry already includes src/**/*, excludes vendor/data/build outputs and maps seven solution criteria; existing tests cover representative source paths and exclusions. |
| C4; P01-T01 fixture stability | Partial | Fixed gate scores are appropriate, but the prepare deletion assertion remains semantically coupled to a mutable A2 grade; PC-001. |
| C5; P01-T01 workflow contracts | Partial | Current YAML can be tested without workflow changes; source CI also has manual dispatch, omitted by the detail's PR-only description; PC-003. |
| P01-T02 retired-path refusal | Covered | Parameterized real-Git cases are bounded to retired module/test/web/Dockerfile/README/prototype-deploy evidence, with empty change/criterion expectations. |
| P01-T02 trusted-base transition | Partial | Correct trust boundary is selected, but the historical solution-code fingerprint prerequisite is unspecified; PC-002. |
| C6-C7/W2-W3; P02-T01 ledger | Covered | Carried 47-point snapshots, real retirement comparison, sequence deviations and missing fresh historical scores are separated; no migration gain is attributed. |
| P02-T01 documentation preservation | Covered | Existing README and cut-over pack are updated; historical rows and append-only log bytes remain preserved; index/log updates are included. |
| P02-T02 local validation | Partial | Full rubric suite plus selectors, links/diff and byte invariants are appropriate; scratch location must be made explicit; PC-004. |
| RPI order and publication | Covered | One later independent Review, retained original outcomes, privacy-safe identity and draft Refs PR are planned; no approval or merge is inferred. |
| Accepted residual failures/skips | Covered | Seventeen migration-related failures are targeted; unrelated deck-selection failure remains visible; runtime skips are reported, not represented as passes. |
| No full gate/cloud/private data/version bump | Covered | Explicit caller restrictions override contrary critique advice; no broader gate, live scorer, production registry change or application work is requested. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 0 High, 4 Medium, 0 Low.
* Rationale: scope and evidence handling are credible, but fixture prerequisites
  and the exact local execution contract need direct planner corrections before
  implementation. None requires new research, another critique or a user choice.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Baseline-relative totals do not stabilize the prepare deletion test

* Related IDs: C4, P01-T01, fixture-stability requirement.
* Evidence:
  .copilot-tracking/details/2026-10-27/rubric-src-198-phase-details.md:30-33;
  .github/rubric/scripts/test_prepare.py:27-49,415-433;
  .github/rubric/scripts/gate.py:190-195,218-226.
* Concern: the detail fixes the expected total but does not replace the live
  baseline/proposed-score relationship. The existing test submits A2=3 from
  a fixture derived from latest.json. If a later legitimate score is 3, this
  is no drop and passed becomes true; below 3, removed evidence cannot justify
  the increase. A baseline-relative expected total alone still fails for
  unrelated score movement.
* Impact: a repair can pass against today's A2=5 while preserving the mutable
  fixture failure mode this task is intended to remove.
* Smallest useful change: explicitly give this existing test a synthetic
  workflow baseline with A2 above 3, deriving all proposed scores from that
  baseline and recomputing its total/sections consistently. Keep its expected
  total relative to the constructed baseline. Do not edit the recorded score.
* Action owner: Planning parent; implementation owner executes the fixture edit.
* Exact resolving evidence: P01-T01 specifies the synthetic prepare baseline,
  fixed A2 relationship and metadata recomputation; the existing deletion test
  checks valid=true, passed=false, drops containing A2, the removed path and
  the calculated total. Its score/drop setup no longer reads a mutable A2
  value from latest.json. Preserve the two-new-function ceiling.
* Decision route: Direct planner correction; no human decision required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Trusted-registry deletion needs a pre-deletion fingerprint baseline

* Related IDs: C3, P01-T02, trusted-base transition acceptance criterion.
* Evidence:
  .copilot-tracking/details/2026-10-27/rubric-src-198-phase-details.md:42-49;
  .github/rubric/scripts/test_prepare.py:27-49;
  .github/rubric/scripts/prepare.py:245-255,278-287.
* Concern: committing an old registry and then deleting its evidence is not
  sufficient. compute_state classifies removals only for changed artifacts,
  whose membership is determined by comparison with recorded fingerprints.
  The existing make_repo helper records only a brd fingerprint. If the only
  legacy solution file is then deleted, its current fingerprint and absent
  previous fingerprint both resolve to None, so solution-code is not changed
  and the removed legacy path cannot be observed. An instrument change alone
  opens criteria but does not supply that missing changed artifact.
* Impact: the new regression can fail for fixture construction rather than
  trust semantics, or be weakened into an instrument-change-only assertion
  that does not prove old-registry deletion detection.
* Smallest useful change: specify committing the legacy evidence first, then
  recording a synthetic workflow baseline fingerprint under the old registry
  on main before branching. Preserve the intended registry edit and deletion
  on feature; use the merged registry for the post-merge observation.
* Action owner: Planning parent; implementation owner constructs the baseline.
* Exact resolving evidence: P01-T02 explicitly requires a nonempty pre-delete
  solution-code fingerprint and bootstrap=false. PR assertions include
  solution-code in changed_artifacts, the exact old path in removed_files and
  changed_files, and instrument_changed=true with all 20 criteria open.
  Post-merge assertions prove the legacy path is outside the merged registry
  and absent from its artifact files/removal set. Do not require should_score
  to be false merely because the legacy path is excluded: comparison with
  the old recorded fingerprint may still require scoring.
* Decision route: Direct planner correction; no human decision required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Exact workflow contract must retain source CI manual dispatch

* Related IDs: C5, P01-T01, workflow/check preservation requirement.
* Evidence:
  .copilot-tracking/details/2026-10-27/rubric-src-198-phase-details.md:33-35
  calls source CI PR-only; .github/workflows/src-ci.yml:3-6 declares both
  pull_request and workflow_dispatch. The existing test in
  .github/rubric/scripts/test_safe_output_runtime.py:156-174 assumes every
  workflow has direct PR/push triggers.
* Concern: the promised exact matrix is underspecified by a PR-only label
  that omits an actual supported entry point. Copying that label into event
  set assertions would fail against unchanged YAML or miss manual-path drift.
* Impact: migration repair could replace one inaccurate trigger assumption
  with another, despite the plan's requirement to test current contracts.
* Smallest useful change: write the full expected event-key sets:
  src-ci={pull_request, workflow_dispatch};
  mvp-ci/mvp-validation/src-deploy={workflow_dispatch};
  infra-plan={workflow_run};
  rubric-score.lock={pull_request, push, workflow_dispatch}.
  Preserve the source path checks only for applicable direct events and the
  infra workflow_run dependency on Source projects CI/completed.
* Action owner: Planning parent; implementation owner updates the existing test.
* Exact resolving evidence: corrected P01-T01 matrix and existing parameterized
  test asserting each parsed real YAML event set, including source manual
  dispatch and absence of source push. Workflow files/names remain unchanged.
* Decision route: Direct planner correction; no human decision required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: The local pytest command leaves scratch writes outside the workspace

* Related IDs: P01-T02, P02-T02, workspace-local file-operation boundary.
* Evidence:
  .copilot-tracking/details/2026-10-27/rubric-src-198-phase-details.md:73
  gives python3 -m pytest .github/rubric/scripts -q -ra without a scratch
  override. Existing Git/runtime tests use pytest tmp_path fixtures throughout
  .github/rubric/scripts/test_prepare.py,
  .github/rubric/scripts/test_record_workflow.py and
  .github/rubric/scripts/test_safe_output_runtime.py.
* Concern: the prescribed command does not ensure workspace-local tmp_path
  allocation. The normal pytest temporary root can be under /tmp, which is
  not an eligible file-operation location for this execution.
* Impact: the planned validation can violate the execution boundary before
  reaching its assertions, or become blocked despite requiring no cloud.
* Smallest useful change: specify unique, previously nonexistent project-local
  scratch directories and explicit pytest --basetemp for both the suite and
  targeted selectors; set workspace-local temporary environment variables
  for subprocesses as needed. Do not point --basetemp at evidence or an
  existing directory, because pytest clears that directory. Preserve the
  retention policy and avoid unapproved cleanup of historical files.
* Action owner: Planning parent; implementation owner selects fresh run paths.
* Exact resolving evidence: P02-T02 contains executable workspace-local scratch
  setup and commands with explicit --basetemp, including targeted runs;
  the later changes record identifies the actual paths and unmodified test
  results. No /tmp or /var/tmp file writes are needed.
* Decision route: Direct planner correction; no human decision required.

## Strengths and Residual Risk

* No redundant registry edits are proposed. Current src tests exercise real
  prepare calls; retired-path cases and the transition fit the two-function
  addition boundary once their setup is made explicit.
* The supplied baseline is 18 failed/355 passed/7 skipped, not the historical
  19. Seventeen failures are in scope; the deck-selection mismatch is an
  explicitly accepted separate concern, not justification for skipping it.
  A local suite retaining that failure must be reported as failing, not green.
* The current latest.json inspected at 09099ecd is a 77-point workflow score
  for scored commit f1be9b1d, run 40569657958. A repository snapshot SHA is
  distinct from the scored commit. The proposed ledger should retain both
  identities, dates and provenance rather than call snapshots fresh scores.
* The research distinguishes missing migration scorecards from existing carried
  assessments and real #499 evidence. A 47-to-77 difference is not established
  migration causality. Refs #198 and uncompleted acceptance remain appropriate.
* Historical ADR sequencing cannot be retroactively achieved. Documenting
  actual #295/#300/#302 timing is credible; replaying the changes or changing
  rubric_version would not resolve the historical acceptance gap.
* No full gate is requested or recommended. Local tests, absent runtime checks,
  later independent Review, hosted checks and owner approval remain separate
  forms of evidence. A draft PR is not release or whole-issue acceptance.

## Questions or Blocking Evidence Gaps

* No user question blocks the scoped repairs. All findings are direct planner
  corrections within the selected approach.
* Missing fresh historical migration scorecards continue to block any claim of
  complete historical scoring acceptance, not this draft-PR workstream.

## Limitations

* This critique did not run tests, a full gate, deployments or a scorer, and
  does not claim implementation success. Baseline counts are supplied research
  evidence, not newly reproduced results.
* GitHub history/run claims were assessed from the supplied research; no new
  historical scorecard recovery or open-ended research was performed.
* Only the caller-specified critique artifact was written. Existing untracked
  plan/details/research/state inputs were left intact. No application, plan,
  detail, research or prior review record was edited.

## Recommended Next Action

* Highest-impact finding: PC-002, because the required new deletion regression
  depends on an otherwise absent baseline state.
* Action owner: Planning parent.
* Smallest next action: directly revise the existing task details for PC-001
  through PC-004, record their dispositions, then continue the ordered RPI.
* User response required: No.
* This is the complete actionable finding set for the supplied boundary.
  Do not commission a second critique for these direct corrections.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/rubric-src-198-plan.md](.copilot-tracking/plans/2026-10-27/rubric-src-198-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-27/rubric-src-198-phase-details.md](.copilot-tracking/details/2026-10-27/rubric-src-198-phase-details.md) | Task details requiring direct corrections |
| [.copilot-tracking/research/2026-10-27/rubric-src-198-research.md](.copilot-tracking/research/2026-10-27/rubric-src-198-research.md) | Supplied evidence and accepted limitations |
| [.copilot-tracking/reviews/plans/2026-10-27/rubric-src-198-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/rubric-src-198-plan-critique.md) | This single critique and full finding set |

## Next Steps

Planning parent: disposition the four direct corrections and finalize planning
without another critique, then continue implementation and the single independent
Review under the existing authorization. No user action is required. This
critique execution stops here.
