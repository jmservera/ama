---
title: Resident startup final-candidate plan critique
description: Independent assessment of the local-only SQL startup prerequisite plan
ms.date: 2026-10-29
---

## Metadata

* Task ID: f568fbf4-e1b7-45d5-ae08-d7034d24a85b
* Task slug: resident-startup
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/resident-startup-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/resident-startup-phase-details.md
* Critique execution status: Complete
* Candidate context: fix/resident-startup, supplied origin/main base d70ee60a
* Execution: exactly one independent assessment; no tests, builds or cloud commands executed.

## Inputs and Criterion Boundary

* Caller requirements: ordered local-only RPI for failed revision res-main-20261029-072628; Docker reproduction with constructed settings; no az, Azure access/mutation, live SQL, .env, secrets, private datasets or push. Preserve user authority over activation and publication.
* Supplied evidence: .copilot-tracking/research/2026-10-29/resident-startup-research.md, especially C5-C9 and its distinction between an observed sufficient local failure and unverified historical Azure causality.
* Scoped source: src/api/src/zava_forward/api/resident_demo/__main__.py, src/core/src/zava_forward/core/resident_showcase_sql.py, src/core/tests/test_resident_showcase_sql.py, infra/sql/resident-showcase.sql, infra/scripts/resident_showcase_sql.py, src/api/checks/resident_demo_image_check.py, src/api/README.md and src/README.md.
* Decisions: document the SQL-before-image prerequisite; add at most one regression in the existing SQL harness; no runtime changes, removals, generated targets, wider grants or invented document facts.
* Acceptance boundary: relevant static/unit checks, opted-in real local SQL and existing image checks; retain one critique and one independent Review; local commit only. Full gate, receipt, exact-head publication assessment and cloud diagnosis remain outside this authorization.
* Project context: docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md were consulted. No regulatory or new product claims are introduced.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Local-only diagnosis and research C5-C9 | Covered | Startup selects SQL before binding; fixed reader columns include documents_json. The supplied same-image comparison isolates a local prerequisite without establishing Azure causality. |
| No new mandatory agenda/model setting | Covered | P01-T01 matches optional agenda construction and supplied C8; the plan does not propose configuration or runtime invention. |
| P01-T01 documentation | Covered | Existing src/api/README.md already identifies the separately authorized column update near line 514. Adding discoverable startup/deployment guidance is a scoped clarification, not a new migration authorization. |
| P01-T02 regression and change budget | Covered | SqlBoundaryTests owns a unique database, synthetic fixture, query helpers and restricted-principal execution. Removing only the projection, asserting driver failure and restoring rendered batches in finally is implementable without new fixtures or production edits. |
| Unknown document facts and restricted access | Covered | Existing tests distinguish unknown from empty and exercise document projection. Planned restoration and restricted SELECT complement existing denial checks without broadening rights. |
| P02-T01 static/unit/SQL/image validation | Partial | Appropriate existing tools and harnesses are selected, with genuine SQL execution and skips/blockers recorded. Shared-lock feasibility needs explicit disposition: PC-001. |
| Same-image old/current view acceptance | Covered | Research C9 supplies the already completed comparison. The existing image check supplements configuration/session/Host checks; it does not itself recreate the old-view comparison or require port 8089. Keep those evidence roles distinct. |
| P02-T02 Review and local commit | Covered | Independent original Review is preserved, later findings routed rather than hidden by a second Review. Privacy-safe local identity, mandated trailer and no push are explicit. |
| Full gate and publication limits | Covered | No full-gate success, cloud diagnosis, deployment readiness or owner approval is inferred from scoped checks or a local commit. |
| Dependencies, cleanup and shared environment | Partial | Owned loopback SQL, clean lifecycle and noninterference are explicit; the shared admission mechanism must also fit the allowed filesystem boundary: PC-001. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 0 High, 1 Medium, 0 Low.
* Rationale: the technical scope and evidence interpretation are credible. One execution-feasibility correction is needed before treating heavy validation as unconditionally runnable. No source investigation, additional critique or significant user decision is necessary to make that correction.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Resolve shared-lock admission against the allowed filesystem boundary

* Related IDs: P02-T01; plan Dependencies and Publication Boundary; heavy-validation acceptance criteria.
* Evidence: .copilot-tracking/details/2026-10-29/resident-startup-phase-details.md requires the shared heavy lock nonblocking. src/README.md, Local RPI gate, and existing src/api/README.md heavy-check guidance identify the shared lock as /tmp/ama-rpi-heavy.lock. This execution context does not permit file operations in /tmp or other temporary directories. The plan does not identify a permitted shared admission mechanism or explicitly handle that conflict.
* Concern: following the repository's normal lock command would violate the permitted filesystem boundary. Inventing a task-local replacement would not serialize against other users of the actual shared lock. Neither is a valid implicit implementation choice.
* Impact: heavy SQL/image validation could be attempted without effective shared admission, or completion could be reported against a validation step that cannot be executed as written.
* Smallest useful change: add an explicit precondition to P02-T01: use only an already established, permitted mechanism coordinating with the actual shared admission lock. If none is available, mark heavy validation blocked and retain the incomplete acceptance status; do not touch the forbidden path, invent an independent lock or bypass admission. Keep lightweight checks and the existing C9 research evidence separately identified.
* Action owner: planning parent.
* Exact resolving evidence: matching plan/details wording naming a verified permitted shared admission mechanism, or explicitly recording this prerequisite as blocked and prohibiting heavy execution and a complete-validation claim until resolved. Any subsequent implementation evidence must record actual admission and results, or the blocker, rather than a substituted lock.
* Decision route: direct planner correction. Current constraints already determine the safe fallback; no significant or divergent user decision is needed. Changing filesystem permissions, shared coordination policy or authorization is not part of this recommendation.

## Strengths and Residual Risk

* The plan correctly avoids a speculative runtime fix: the unchanged main image already worked after changing only the local SQL view.
* Missing projection is not equated with empty documents. Restoring the current template in finally protects subsequent tests while preserving the explicit refusal contract.
* The planned documentation should extend or cross-reference the existing prerequisite statement, retaining separate authorization for any real application.
* Cloud schema, identity authentication, expiry, secret resolution and connectivity remain unverified. Local password-mode SQL and offline dummy MSI configuration do not resolve those uncertainties.
* The earlier external probe's harness port error remains historical evidence, not causal proof. No cleanup or rewriting of that evidence is authorized.
* A preserved adverse Review or blocked validation must remain adverse or blocked. A local commit is not acceptance, publication or permission to retry the revision.

## Questions or Blocking Evidence Gaps

* No decision-critical gap prevents this critique or the scoped documentation/regression design.
* Heavy-check admission has the concrete feasibility gap in PC-001. It can be represented honestly as blocked without seeking broader user authorization.

## Limitations

* The parent-supplied Docker reproduction and C9 outcomes were assessed as supplied evidence; external probe files and historical cloud artifacts were not independently rerun or retrieved.
* No current cloud cause, byte identity with the failed deployed image, fresh test pass, full local gate or production readiness is established here.
* Read-only inspection covered supplied artifacts and the directly relevant source. No plan, details, research, state or source file was changed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: dispose PC-001 directly in plan/details, preserving this original verdict; finalize the plan without another critique, and keep heavy execution conditional on permitted shared admission.
* User response required: no.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/resident-startup-plan.md](.copilot-tracking/plans/2026-10-29/resident-startup-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/resident-startup-phase-details.md](.copilot-tracking/details/2026-10-29/resident-startup-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-29/resident-startup-research.md](.copilot-tracking/research/2026-10-29/resident-startup-research.md) | Local diagnosis and uncertainty boundary |
| [.copilot-tracking/reviews/plans/2026-10-29/resident-startup-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/resident-startup-plan-critique.md) | Original independent critique |

## Next Steps

The active planning parent should resolve PC-001 directly and retain this Complete / Revise outcome. No user action or second critique is required. This reviewer stops after delivering this artifact.
