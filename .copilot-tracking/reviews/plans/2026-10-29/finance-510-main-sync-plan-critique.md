<!-- markdownlint-disable-file -->
---
title: Finance PR 510 main synchronization plan critique
description: Single independent final-candidate credibility assessment
ms.date: 2026-10-29
---

## Metadata

* Task ID: finance-510-main-sync.
* Critique date: 2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/finance-510-main-sync-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/finance-510-main-sync-phase-details.md.
* Critique execution status: Complete.
* Assessment count: exactly one independent assessment of the supplied final candidate; no delegated assessment.

## Inputs and Criterion Boundary

* Caller requirements: authorized local rebase of docs/finance-96 for PR #510, preserving both branches' intent, append-only log, README index, all eight finance commits' substantive changes and immutable adverse evidence. Main owns .github/rubric and the scenario manifest. Existing tests only, maximum additions zero, removals none; canonical core/API tests remain outside packages. Use the existing /tmp/mv tools with local/sibling src and tests import precedence, configured Ruff/format/mypy and focused unittests. No full API discovery without the specified nonblocking admission, no Azure, no push, no issue-closing keywords.
* Environment boundary: tool execution may read the requested /tmp/mv executables but must not write fixtures or scratch outputs under /tmp or other forbidden temporary locations.
* Research considered: .copilot-tracking/research/2026-10-29/finance-510-main-sync-research.md, C1-C6, including the distinction between historical adverse outcomes and later corrective outcomes.
* Supporting supplied evidence read: .github/workflows/src-ci.yml; src/core/pyproject.toml; src/api/pyproject.toml; docs/reference/research/retrofit-synthetic-data/scenario-manifest.json; src/core/tests/test_scenario_manifest.py; .copilot-tracking/reviews/logs/2026-10-29/finance-510-source-guards-review.md; .copilot-tracking/changes/2026-10-29/finance-96-main-rebase-changes.md. Direct test context included src/core/tests/test_form_review.py, src/core/tests/test_form_review_pack.py and src/api/tests/test_form_staging_api.py.
* Repository context: required case-study and knowledge-base introductory material, docs/reference/memory.md and src/README.md. Memory was treated as context, not evidence.
* Decisions and dependencies: finalized critique precedes P01; P01 precedes validation; validated integration precedes the single Review and local commit. The user already selected rebase, main-owned generated files, bounded tests, no push and coordinator-owned publication. None requires reconsideration.
* Acceptance boundary: FR1-FR4, NFR1-NFR4 and AC1-AC6, including preservation, pinned provenance, tool/import identity, evidence reconciliation, local attribution and honest hosted/publication limitations.
* Intake verification: HEAD bafcb2415991a15eb3a16b781649a2ce7c749fcf; origin/main 8ee1b77f8983ddf39216da07ae60c63ef66431d6; branch docs/finance-96. Status showed only the four caller-owned untracked current-task artifacts. Git inspection confirmed eight unique finance commits and the monitoring-side index/log/rubric overlap.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1; C1; P01-T01; AC1 | Partial | Assessed base is recorded, but executable rebase and comparison policy does not enforce it against a moving origin/main; PC-002. |
| FR2; C1/C5; P01-T01; AC2 | Covered | Main log byte-prefix plus finance append; single-date README with both navigation entries; range-diff and original-source comparison protect finance fixes. |
| FR3; C2/C4; AC2/AC4 | Covered subject to PC-002 | Exact main-owned rubric/manifest copies and unconditional selected test_scenario_manifest protect existing source hashes without regenerating them. |
| FR4; C5; AC2/AC5 | Covered | Byte comparison to starting HEAD preserves original adverse research/critique/Review alongside later corrective outcomes. |
| NFR1/NFR3; C3; P02-T01 | Covered | Zero new tests, no removals/exemptions or package-internal tests; existing finance, staging, role, provenance, dependency and manifest modules selected. |
| NFR2; C6; AC3/AC4 | Partial | Explicit local/sibling PYTHONPATH and import assertions address foreign editables; fixture output location remains unspecified; PC-001. |
| NFR4; AC6; P02-T01 | Covered | Full API discovery is not selected; no lock admission, SQL, browser, hosted CI or complete publication success is claimed. |
| P02-T02; AC5/AC6 | Covered | One independent Review, retained findings, privacy-safe local attribution, Conventional Commit/Copilot trailer, references only, no push or Azure. |
| Decisions, dependencies and residuals | Covered | Existing owner choices resolve integration strategy; coordinator publication and human finance authority remain separate, not waived. |

## Verdict

* Verdict: Revise.
* Rationale: The preservation and focused validation strategy is credible, but execution needs an explicit allowed fixture directory and an enforced assessed-base identity. Both are direct planning corrections within the already authorized scope.
* Severity summary: Critical 0; High 1; Medium 1; Low 0.
* Complete actionable finding set: PC-001 and PC-002. No additional findings are withheld for another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Selected test commands do not enforce the permitted fixture-output boundary

* Related IDs: NFR2; P02-T01; AC4; caller execution boundary.
* Evidence: .copilot-tracking/details/2026-10-29/finance-510-main-sync-phase-details.md, P02-T01, specifies PYTHONPATH and cache/bytecode guidance but no TMPDIR or equivalent preflight. src/core/tests/test_form_review.py, FormReview.setUp, and src/api/tests/test_form_staging_api.py, FormApi.setUp, call tempfile.TemporaryDirectory() without an explicit directory. The supplied .copilot-tracking/reviews/logs/2026-10-29/finance-510-source-guards-review.md explicitly records TMPDIR under src/core for its existing self-cleaning synthetic fixtures.
* Concern: The proposed commands depend on an unspecified inherited temporary-directory setting. If it is unset or points outside the worktree, these existing tests can create fixtures under /tmp or another disallowed location. PYTHONPATH and cache controls do not redirect tempfile.
* Impact: Otherwise correct regression execution can violate the task's hard file-operation boundary before producing acceptance evidence.
* Smallest useful change: In P02-T01, require an absolute project-local TMPDIR for each test process before Python starts, for example TMPDIR="$PWD" from the stated src/core or src/api working directory. Retain the existing tests unchanged. Make bytecode/cache output handling explicit where necessary, and constrain cleanup to artifacts created by this invocation.
* Action owner: Planning parent.
* Exact resolving evidence: Revised phase details specify the working directory, absolute allowed TMPDIR and environment inheritance for each selected test command; the changes record subsequently captures those actual environments and existing fixture cleanup. No test additions or implementation changes are required.
* Decision route: Direct planner correction. The current execution boundary already resolves the choice; no significant or divergent user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The assessed main SHA is documented but not enforced during replay and preservation checks

* Related IDs: C1/C2/C4; FR1/FR3; P01-T01; AC1/AC2.
* Evidence: .copilot-tracking/details/2026-10-29/finance-510-main-sync-phase-details.md records main 8ee1b77f8983ddf39216da07ae60c63ef66431d6, then instructs git rebase origin/main and retention of main's copies without an explicit equality preflight or stop/reconciliation rule. .copilot-tracking/research/2026-10-29/finance-510-main-sync-research.md explicitly identifies main moving after assessment as a risk. At critique time origin/main still matched the assessed SHA.
* Concern: A later fetch or shared-ref update can change origin/main between assessment, rebase and protected-path comparison. The executor could replay on an unassessed base or compare protected paths against a different base while the evidence continues to name the original SHA.
* Impact: Ancestry, main-owned rubric/manifest preservation and range-diff evidence can refer to inconsistent integration boundaries; new source or pin changes might then be treated as already assessed.
* Smallest useful change: Require a pre-rebase origin/main equality assertion against the assessed SHA, use the captured immutable base for replay and preservation comparisons, and record the original merge-base/start range for range-diff. If the requested latest main differs, stop automatic replay and reconcile the changed base's affected scope before continuing; do not silently reuse the old assessment. Keep the coordinator's later fresh-main publication verification separate.
* Action owner: Planning parent.
* Exact resolving evidence: Revised plan/details define the expected SHA, equality preflight, immutable comparison base and changed-base route. Implementation evidence records actual start/base SHAs, rebase target, range-diff ranges, ancestry and protected-path comparisons against that same base.
* Decision route: Direct planner correction. No user response is needed merely to enforce the assessed boundary; genuinely divergent newly discovered work would be routed separately if it occurs.

## Strengths and Residual Risk

* The log resolution preserves main as a byte-prefix rather than selecting one whole conflict side, while the README retains both finance and monitoring entries and main's corrected date.
* Later finance source guards and their Conformant Review remain distinguishable from the unchanged original adverse Review. No historical outcome is rewritten as current acceptance.
* Main's scenario manifest has four public source hashes; the selected existing manifest regression checks their integrity even though research found no source delta. No new pin or generated score is proposed.
* Local source precedence, configured package-wide static scopes and bounded external regression modules directly address the shared editable-install hazard.
* Hosted Source CI/rubric action_required with no executed jobs, the non-draft PR state, absent finance/Board authority and coordinator-owned full publication gates are accurately qualified. This critique grants none of those approvals.
* Rebase conflict discovery remains implementation work. An unexpected conflict requires inspection and evidence, not permission to discard finance/source commits or historical artifacts.

## Questions or Blocking Evidence Gaps

* No unresolved user choice prevents these two planner corrections.
* No decision-critical evidence gap blocks completion of this critique. Implementation and hosted outcomes do not yet exist for this candidate and are not inferred.

## Limitations

* Read-only assessment of the supplied plan, details, research and directly relevant supplied evidence. No external research, GitHub refresh, test execution, rebase, commit, push, Azure operation or nested delegation.
* Source preservation is a proposed acceptance contract, not an already demonstrated post-rebase result.
* No complete local publication receipt, exact committed-head independent assessment, hosted CI success or whole-finance acceptance is asserted.
* Only this critique artifact was written. Plan, details, research, state, source, tests and original evidence were not edited.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the explicit worktree-local fixture environment and the assessed-base preflight/comparison policy to the existing plan/details; disposition both PC IDs while preserving this original Revise verdict.
* User response required: No.
* Return to the active parent for direct revisions and continuation after its gates; do not request another same-candidate critique.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/finance-510-main-sync-plan.md](.copilot-tracking/plans/2026-10-29/finance-510-main-sync-plan.md) | Assessed final-candidate plan. |
| [.copilot-tracking/details/2026-10-29/finance-510-main-sync-phase-details.md](.copilot-tracking/details/2026-10-29/finance-510-main-sync-phase-details.md) | Assessed replay and validation details. |
| [.copilot-tracking/research/2026-10-29/finance-510-main-sync-research.md](.copilot-tracking/research/2026-10-29/finance-510-main-sync-research.md) | C1-C6 research and base identity. |
| [.copilot-tracking/reviews/plans/2026-10-29/finance-510-main-sync-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/finance-510-main-sync-plan-critique.md) | This single independent Complete / Revise critique. |

## Next Steps

The active planning parent should directly resolve PC-001 and PC-002, record their dispositions and finalize planning before implementation. No user action is required. This reviewer stops after writing this artifact.
