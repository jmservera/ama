---
title: Employee acceptance gate bootstrap plan critique
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: 570-gate-bootstrap
* Task slug: employee-identity-check-570-gate-bootstrap
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/employee-identity-check-570-gate-bootstrap-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/employee-identity-check-570-gate-bootstrap-phase-details.md
* Critique execution status: Complete
* Candidate assessment: One final-candidate critique of this child task.

## Inputs and Criterion Boundary

* Caller requirements: Resolve the directly coupled fresh-browser publication/bootstrap defect under the complete-gate request. Permit only the existing approved missing-executable discovery qualification; require exactly three tests and zero skips for mandatory CLI success. Preserve integration execution, original correction outcomes and authority boundaries.
* Research: .copilot-tracking/research/2026-10-31/employee-identity-check-570-gate-bootstrap-research.md, C1-C6.
* Supporting sources: src/api/tests/test_browser_asset_urls.py:53-60; src/api/tests/test_employee_acceptance_check.py:223-249; src/api/checks/employee_acceptance_check.py:466-478; src/api/README.md:47-95; tools/rpi-checks.py:80, 335-343, 1027-1052, 1144, 1596-1610, 1902-1940.
* Project context: docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md, docs/reference/memory.md and docs/reference/research/sector/housing-association-primer.md. No customer, legal or live-identity claim is added by this assessment.
* Decisions and dependencies: The caller authorizes this narrow bootstrap correction, not browser installation, gate/environment changes or another assessment of completed RV002/RV001 work. P01-T02 follows P01-T01. Independent child Review, a new committed clean complete gate, current-base receipt verification and exact-head assessment remain prerequisites to publication.
* Acceptance boundary: Assess discovery versus mandatory execution, absent/present/non-missing-error validation, locked test ownership and truthful evidence/authority. No new methods, removals, observer/BINDING edits, matrix/CI edits, credentials, Azure operations or implementation are authorized here.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C2; fresh-browser ordering | Covered | The isolated browser path is set before discovery. Browser depends on project-api; the shared API execution chain places browser installation before extras. The planned fix addresses early discovery without altering that chain. |
| C3; P01-T01 narrow qualification | Covered | Existing browser-asset coverage catches only Playwright launch errors containing "Executable doesn't exist", records the exact approved reason, and reraises other errors. The plan reuses that condition only around launch in the shared helper. |
| C4; P01-T01 CLI reduction | Covered | Current CLI selects three methods but relies only on wasSuccessful. Planned success requires wasSuccessful, testsRun equal to three and an empty skipped collection, preventing skipped, empty or incomplete suites from passing. |
| C6; required integration | Covered | Existing check_skips integration mode rejects this discovery skip; extra selectors use integration=True. The plan explicitly retains all three Chromium extra selectors and does not change the allowlist or gate. |
| C5; P01-T02 absent-browser evidence | Covered | Caller and research report three actual missing-executable launch errors. Planned post-fix evidence distinguishes three enumerated discovery skips from CLI exit one, with a fresh absent PLAYWRIGHT_BROWSERS_PATH. |
| P01-T02 present/error validation | Covered | Actual installed-browser module and CLI execution must show three browser methods with zero skips. Injected non-missing BrowserError must propagate rather than become a skip. Whole-module regression and existing static/tool checks are retained. |
| Locked ownership and unchanged semantics | Covered | Only the helper launch handling, runner reduction, owning guide and child evidence change. Maximum method additions zero; removals none. Admission, map and observer bodies remain unchanged. |
| Publication and evidence authority | Covered | Historical aa531930 attempt and original correction outcomes stay historical. A fresh clean complete gate and independent child Review are required; synthetic checks do not establish live identity acceptance, hosted approval or owner approval. |

## Verdict

* Verdict: Pass
* Rationale: The candidate makes a narrowly evidenced discovery correction while strengthening the maintained CLI's execution requirement. Existing mandatory integration rejection remains intact. Validation covers the three decision-critical browser states without expanding test methods, runtime semantics or publication authority.

## Findings

No actionable PC findings within the supplied boundary.

* Severity counts: Critical 0; High 0; Medium 0; Low 0.
* Direct dispositions: Preserve the existing exact skip reason and missing-executable condition; enforce all three CLI result predicates; retain required integration selectors and no-skip enforcement; capture absent/present/non-missing-error outcomes as specified. These are already explicit plan requirements, not additional revisions or user decisions.

## Strengths and Residual Risk

* The research identifies the actual sequencing defect rather than prescribing browser preinstallation or a gate bypass.
* The shared launch helper is the smallest useful correction location. Only missing-executable launch errors are eligible; driver startup, context creation and unrelated launch failures remain failures.
* Missing-browser discovery is explicitly recorded, not represented as executed acceptance. The CLI and required extras cannot inherit unittest's success-shaped skip result.
* The owner-required full gate, independent review and exact-head/current-base checks remain necessary after any source commit. This critique grants no publication permission.
* The plan preserves the accepted synthetic-versus-live distinction. Independent identity resolution and live employee criteria remain unmet; local Chromium execution does not resolve them.

## Questions or Blocking Evidence Gaps

None for this bounded planning decision. Current caller direction resolves the discovery qualification and mandatory execution choices; no significant or divergent user decision is needed.

## Limitations

* This is plan assessment, not implementation Review or an observed passing gate. No tests, browser installation, gate or live operations were performed during the critique.
* The external chromium-bootstrap-reproduction.log was not independently reopened. The three-error reproduction is supplied by both caller and research; supporting source confirms the unconditional launch and fresh-path ordering. This does not justify claiming independently reproduced execution here.
* Zero/incomplete CLI execution rejection is explicit in the proposed predicate. Its implementation must still be verified by child Review; this artifact does not certify unimplemented code.
* Completed correction findings and Reviews are not reopened, superseded or regraded. Source artifacts remain unchanged; only this requested critique artifact is written.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent.
* Smallest next action: Record this Pass disposition, finalize the child plan and implement P01-T01/P01-T02 within locked scope. Obtain the specified independent child Review and new complete publication evidence afterward.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-31/employee-identity-check-570-gate-bootstrap-research.md](.copilot-tracking/research/2026-10-31/employee-identity-check-570-gate-bootstrap-research.md) | Bootstrap evidence and decisions |
| [.copilot-tracking/plans/2026-10-31/employee-identity-check-570-gate-bootstrap-plan.md](.copilot-tracking/plans/2026-10-31/employee-identity-check-570-gate-bootstrap-plan.md) | Assessed final candidate |
| [.copilot-tracking/details/2026-10-31/employee-identity-check-570-gate-bootstrap-phase-details.md](.copilot-tracking/details/2026-10-31/employee-identity-check-570-gate-bootstrap-phase-details.md) | Assessed phase details |
| [.copilot-tracking/reviews/plans/2026-10-31/employee-identity-check-570-gate-bootstrap-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/employee-identity-check-570-gate-bootstrap-plan-critique.md) | Canonical complete Pass critique |

## Next Steps

No user action is required. Return Complete / Pass to the active planning parent for direct disposition and finalization without another critique. Implementation, independent child Review and fresh full-gate publication checks remain subsequent parent responsibilities; this critique performs none of them.
