<!-- markdownlint-disable-file -->
---
title: Finance 510 refresh final-candidate plan critique
description: Single independent integration and validation readiness assessment
ms.date: 2026-10-29
---

## Metadata

* Task ID: finance-510-refresh-2221.
* Critique date: 2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/finance-510-refresh-2221-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/finance-510-refresh-2221-phase-details.md.
* Critique execution status: Complete.
* Original verdict: Revise. Preserve this outcome after parent corrections; no second critique requested.

## Inputs and Criterion Boundary

* Assessed the three canonical plan/details/research artifacts supplied by the caller, FR1-FR4, NFR1-NFR4, AC1-AC6, both phases and their dependencies.
* Caller constraints: rebase PR #510's docs/finance-96 onto immutable main 129808b3d0a2a5ab88bdcf631d2722362de9e857; preserve both sides, authoritative main rubric/manifest and historical evidence; canonical src source/external tests; no removals, zero planned additions; existing environment and heavy-lock admission; no Azure or push; attributed Conventional Commit, references only.
* Read the supplied C1-C8 evidence pointers: src/README.md; .github/workflows/src-ci.yml; core/API pyproject.toml; scenario-manifest.json; prior main-sync changes and source-guards Review. Read required case-study/index/memory context.
* Read-only Git inspection confirmed HEAD 6a0a6d95231e7e0a5548259b81aa3929089e9b47, origin/main at the immutable target and upstream 011f6a6e0460b9d271e97128756c48a80d40de6b. Upstream changes only .github/rubric/scores/latest.json. Inspected both sides' store diffs and selected external test fixture construction.
* Boundary: integration/validation safety and readiness, not finance redesign, implementation acceptance, full publication qualification or live financial/resident approval.

## Coverage Assessment

| Requirement, research, phase or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1; P01-T01; Q1 | Covered | Known upstream score-only commit, fast-forward before rebase, immutable-main identity check. |
| FR2-FR3; AC1-AC2; P01-T02; Q2 | Covered | Both-sided composition, main log prefix/index retention, byte-identical historical evidence, protected equality, ancestry and manifest pins. |
| NFR1; NFR4; AC6 | Covered | No cloud/private data/push, explicit staging and local authenticated noreply identity. Current author/committer identities are already noreply. |
| NFR2; AC3-AC4; P02-T01 | Partial | Appropriate static scopes/selectors/import assertions; fixture output placement is unspecified: PC-002. |
| AC5; C2-C3 | Covered | Full API is optional and requires nonblocking admission held throughout; busy is not passing evidence. |
| NFR3; FR4; AC6; P02-T02; Q3 | Partial | Single independent Review is planned, but blanket routing of findings lacks an adverse-outcome readiness stop: PC-001. |
| Test ownership lock | Covered | Source in owning src packages, tests external, no removal/assertion weakening, zero planned additions. |
| Publication and human acceptance | Covered | Explicit coordinator follow-up; no hosted/full-gate/financial approval claim. No push is authorized. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0; High 0; Medium 2; Low 0.
* Rationale: the integration approach is credible, but completion must fail closed on material Review findings, and selected tests need explicit workspace-local fixture placement.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Adverse Review findings need an explicit readiness stop

* Related IDs: G1-G2, FR4, AC6, P02-T02.
* Evidence: .copilot-tracking/details/2026-10-29/finance-510-refresh-2221-phase-details.md, P02-T02, says "Route findings to later work, no repeat Review" and proceeds to commit. The plan has no severity/disposition condition distinguishing an adverse Review from accepted residual publication limits.
* Concern: this blanket route could defer a newly discovered lost main/finance behavior, failed preservation proof or invalid validation evidence while still presenting the task as locally ready. One Review is a frequency constraint, not permission to accept its defects.
* Impact: a clean attributed commit and completed lifecycle could be mistaken for successful integration despite an adverse independent result.
* Smallest useful change: state that material integration/validation findings prevent an accepted/ready handoff. Preserve the single original Review and its outcome. Record each finding's disposition; correct in-scope defects with targeted revalidation where authorized, or hand off explicitly Not accepted/Blocked with owned follow-up. Do not silently convert the original Review to acceptance or invoke another Review.
* Action owner: planning parent; implementation parent executes the disposition.
* Exact resolving evidence: P02-T02 and completion criteria contain the adverse-outcome stop; final changes/handoff records the actual Review outcome, every finding and its resolution or explicit outstanding blocker. No readiness claim while a material blocker remains.
* Decision route: Direct planner correction. No user decision required; existing one-Review/no-push constraints remain unchanged.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Selected tests leave synthetic fixture writes to the process default

* Related IDs: NFR1-NFR2, P02-T01, AC4.
* Evidence: .copilot-tracking/details/2026-10-29/finance-510-refresh-2221-phase-details.md specifies PYTHONPATH, bytecode and cache controls, but no fixture root. src/core/tests/test_form_review.py:23, src/core/tests/test_form_review_pack.py:23, src/core/tests/test_form_staging.py:79, src/api/tests/test_form_staging_api.py:26, src/api/tests/test_finance_match_api.py:23 and src/api/tests/test_resident_api.py:24 construct tempfile.TemporaryDirectory() without an explicit directory. Both selected test_dependency_rule modules do likewise. Supplied C7's prior changes record explicitly set TMPDIR to the project cwd.
* Concern: no planned command ensures that these tests' synthetic file writes stay under the current workspace rather than the interpreter's default scratch location.
* Impact: otherwise passing focused tests can violate the execution environment's file-placement restriction or leave fixture placement unproven.
* Smallest useful change: set TMPDIR="$PWD" in each owning project cwd before starting the test interpreter; assert its selected tempfile root resolves there. Keep existing self-cleaning fixture behavior. This concerns generated fixture writes only, not a recommendation to relocate the caller-selected existing interpreter or heavy-lock path.
* Action owner: planning parent; validation executor applies the environment.
* Exact resolving evidence: P02-T01 documents the fixture setting and root assertion; changes records those actual commands/results and confirms no fixture residue. No test/source additions or assertion changes are needed.
* Decision route: Direct planner correction. No user decision required.

## Strengths and Residual Risk

* Both store edits are additive in the inspected overlap: main strips resident intake fields for unauthorized views; finance strips form review/hold internals. Keeping both hooks is more credible than restoring an entire old source tree.
* Complete configured core/API static checks, explicit current-worktree source/test paths and import-origin assertions directly address sibling editable-install contamination.
* Existing finance/source-freshness/scenario tests plus inherited resident tests provide appropriate bounded regression scope without expanding the feature.
* Prior research's free-lock observation is not treated as actual admission. Full API remains optional; no API discovery or heavy work was executed in this critique.
* Hosted checks, complete publication receipts, SQL/browser coverage and Finance/Board acceptance remain separate and unverified. Their declared deferral is not a finding for this no-push task.

## Questions or Blocking Evidence Gaps

* No unresolved user choice or research gap prevents this assessment.
* Both findings are planner-owned corrections, not requests for broader feature work or a second critique.

## Limitations

* No rebase, test, source edit, plan/state edit, Git mutation, remote operation, nested agent or Azure operation was performed.
* Actual conflict resolution, final preservation proofs and validation results do not yet exist for this candidate; this is a plan credibility assessment.
* Historical C7/C8 results were inspected as context, not reused as current candidate passes. Live GitHub metadata was not refreshed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: add the adverse-Review completion stop and workspace fixture environment to the canonical details, recording disposition without overwriting this original Revise verdict.
* User response required: No.

## Artifacts

| Workspace-relative path | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-29/finance-510-refresh-2221-plan.md | Canonical assessed plan. |
| .copilot-tracking/details/2026-10-29/finance-510-refresh-2221-phase-details.md | Canonical assessed task details. |
| .copilot-tracking/research/2026-10-29/finance-510-refresh-2221-research.md | Supplied evidence and decisions. |
| .copilot-tracking/reviews/plans/2026-10-29/finance-510-refresh-2221-plan-critique.md | Single original critique and complete actionable finding set. |

## Next Steps

Active parent resolves PC-001 and PC-002 directly, preserves this original outcome and continues the authorized local RPI loop. No repeat critique or user action is required.
