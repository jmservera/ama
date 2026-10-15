---
title: Generator coverage baseline final-candidate plan critique
description: Independent bounded credibility assessment for issue 167
ms.date: 2026-10-15
---

## Metadata

* Task ID: #167, src-generator-coverage-167
* Critique date: 2026-10-15
* Plan: .copilot-tracking/plans/2026-10-15/src-generator-coverage-167-plan.md
* Phase details: .copilot-tracking/details/2026-10-15/src-generator-coverage-167-phase-details.md
* Critique execution status: Complete
* Critique count: one independent final-candidate assessment; no delegated agents.

## Inputs and Criterion Boundary

* Caller direction limits delivery to a metadata-only gap-routing and convention-declaration validator with deterministic stdout reporting in src/core. Existing generators are reused and inventory contents remain unchanged. Private data, owner approvals, SQL changes, deployment and inference changes are excluded.
* Supplied research: .copilot-tracking/research/2026-10-15/src-generator-coverage-167-research.md, including C1-C6 and W1-W4. External issue/PR summaries are supplied evidence, not independently reverified remote facts.
* Bounded corroboration: docs/reference/research/retrofit-synthetic-data/needs-inventory.json; src/core/tests/test_needs_inventory.py; src/README.md; docs/adrs/0006-src-layout-and-cutover.md. Required project context was consulted in docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md.
* Acceptance boundary: engineering routing validity, declaration presence, preserved pending items, regression evidence and honest local-check reporting. Neither this critique nor the proposed tool establishes output conformity, approved dataset scope, owner acceptance or full application acceptance.
* Delivery boundary: the parent completes the full RPI loop, records local commands/results and opens a main-target PR containing Refs #167. This critique only writes its designated review artifact.
* Constraints include ADR 0006 dependency direction; no new mvp code; no reads/writes of .env, .vscode or .copilot-tracking/github-issues; no use of system temporary directories.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Metadata-only scope; C1-C2; P01-T01 | Covered | Explicit path input, no implicit repository discovery, no data output writes, typed guards and semantic validation. Existing inventory remains canonical and unchanged. |
| Gap routes and declarations; P01-T01 | Covered | Unique IDs, supported closure/coverage values, positive nonduplicate issue references, nonblank notes, justified deferrals and delivered-only-covered rule address the supplied truthiness gap. Four declarations are named in C1 evidence. |
| Baseline acceptance | Covered | Inventory independently contains SN-01 through SN-13, with two covered, eleven partial and zero missing. These counts describe metadata coverage, not thirteen accepted generators or datasets. Existing test_needs_inventory.py owns inventory membership and binding checks. |
| Exact production/test budget | Covered | Exactly one new production module, src/core/src/zava_forward/core/synthetic/coverage.py, and one new test module, src/core/tests/test_generator_coverage.py. Removals: none. No extra fixtures, wrappers or generator modules are required. |
| Test ownership; C4-C5; P01-T01 | Covered | New module owns validator mutations, report shape/order and CLI success/errors. Existing inventory, generator and determinism tests retain their separate responsibilities. No duplicate dataset fixtures or replacement generator tests are proposed. |
| Deterministic stdout and failure semantics | Covered | Plan requires stable ordering, provenance fields, all rows, totals, conventions and pending items; invalid input produces a diagnostic/nonzero exit without a partial success report. Implementation tests should exercise these already-required boundaries. |
| Dependency rules; C3; ADR 0006 | Covered | Standard-library-only core module imports no workload. API-to-agents remains an existing temporary edge, not a proposed new dependency. |
| P01-T02; misleading acceptance claims | Covered | Documentation and report must distinguish routing/declaration checks from generated-record conformity. Research C6 explicitly identifies manifest labels versus per-record labels; the plan preserves that unresolved distinction. |
| P02-T01; scratch storage | Partial | Temporary metadata files and temporary ZF_DATA storage lack an explicit worktree-local location; PC-001 addresses the hard execution constraint. |
| P02-T01; local regression evidence | Covered | All five src suites, existing generator regressions, ruff/format/mypy, report CLI and an actual loopback API smoke are required. Docker permissions and unavailable live checks must be reported honestly, not treated as successful acceptance. |
| P02-T02; full loop and publication | Covered | One implementation review, changes evidence, explicit staging, authenticated privacy-safe identity, trailer, non-force push and main PR with Refs #167 are planned. Owner merge and CI remain separate. |
| Exclusions and owner dependencies | Covered | No inventory edits or invented deferrals. SN-01 regeneration, SN-03/08/09 scope, owner mapping, refresh approval, #103/#144 and output conformity remain outside active acceptance, not waived. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* Rationale: The engineering slice, test ownership and acceptance claims are credible and appropriately small. One planner-owned correction is needed to make temporary-file and smoke execution compatible with the explicit filesystem prohibition. No new product scope, dependency or owner decision is needed.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Make test and smoke scratch locations explicitly worktree-local

* Related IDs: P01-T01, P02-T01; caller execution constraints.
* Evidence: .copilot-tracking/details/2026-10-15/src-generator-coverage-167-phase-details.md calls for CLI tests with "temporary metadata files" and API smoke with "temporary ZF_DATA storage", but supplies no location. Only the virtual environment is explicitly worktree-local. The active execution instructions prohibit system temporary-directory file operations and require created files to be relative to the current worktree.
* Concern: The plan leaves standard temporary-file defaults available. Python temporary-directory helpers commonly select a system temporary directory unless explicitly directed otherwise. This is a missing execution safeguard, not evidence that any prohibited operation has already occurred.
* Impact: Otherwise valid CLI tests or smoke setup could violate the hard filesystem restriction or fail under enforcement, preventing the required local evidence from being collected.
* Smallest useful change: Specify a worktree-local ignored scratch parent for new test metadata and smoke data, explicitly pass that parent to temporary-file helpers, and set ZF_DATA to an isolated fictional-data child there. Require cleanup and prohibit system temporary-directory fallbacks. Keep the one-production/one-test-module budget and inventory unchanged; no new scratch-management framework is needed.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T01 and P02-T01 state the allowed scratch parent and explicit helper/storage configuration. Subsequent implementation evidence records the local scratch path, fictional dataset setup, smoke commands/results, exact process shutdown and cleanup; new tests use an explicit allowed directory rather than default temporary-directory selection.
* Decision route: Direct planner correction; current instructions already resolve location policy.
* Disposition eligibility: Eligible for addressed after the bounded plan/detail correction. Not eligible for risk acceptance that permits prohibited paths. No significant or divergent user decision is required.

## Strengths and Residual Risk

* A single module plus a single test module is proportionate to the demonstrated truthiness gap. Generic schema frameworks, new generators, extra dependency layers and remote GitHub-status reconciliation would be overengineering and are correctly excluded.
* Existing tests retain inventory membership, scenario binding and generator reproducibility ownership. The new module need not recreate those tests or read generated datasets to validate declarations.
* Declared is_synthetic wording is not proof that every historical generator record carries that field. The plan correctly preserves this research limitation rather than silently modifying records, inventory wording or acceptance status.
* Child issue references prove recorded routing only. They do not prove child delivery, owner scope ratification or accepted coverage. The proposed report must retain its already-required disclaimer and pending items.
* Full local regression testing and smoke are evidence collection requested by the caller, not justification for broad cleanup, SQL setup, model enablement or deployment changes. Unrelated baseline failures should be recorded and scoped, not repaired indiscriminately.

## Questions or Blocking Evidence Gaps

* None requiring user input. The scratch policy is already explicit.
* Owner-dependent dataset and application evidence remains intentionally unavailable and outside the metadata-only acceptance boundary.

## Limitations

* This is a plan critique, not an implementation or runtime review. No src tests, tools, API, Docker, inference or deployment commands were executed for this assessment.
* Research C4-C6 and external W1-W4 were assessed as supplied evidence; this critique did not repeat generator investigations or conduct external research.
* Existing untracked planning/research/session artifacts were observed on feat/src-generator-coverage-167 and left unchanged. No prohibited configuration, issue-export or private-data files were read or written.
* This is the complete actionable finding set for the supplied candidate and boundary. No cosmetic findings or additional critique pass are requested.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the worktree-local scratch constraint to P01-T01/P02-T01 and record its disposition, then finalize planning and continue the authorized loop.
* User response required: No.
* Stop boundary: This assessor writes only this critique and performs no implementation or further agent dispatch.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-15/src-generator-coverage-167-plan.md](.copilot-tracking/plans/2026-10-15/src-generator-coverage-167-plan.md) | Reviewed final-candidate plan |
| [.copilot-tracking/details/2026-10-15/src-generator-coverage-167-phase-details.md](.copilot-tracking/details/2026-10-15/src-generator-coverage-167-phase-details.md) | Reviewed task-level execution boundaries |
| [.copilot-tracking/research/2026-10-15/src-generator-coverage-167-research.md](.copilot-tracking/research/2026-10-15/src-generator-coverage-167-research.md) | Supplied evidence and residual uncertainty |
| [.copilot-tracking/reviews/2026-10-15/src-generator-coverage-167-plan-critique.md](.copilot-tracking/reviews/2026-10-15/src-generator-coverage-167-plan-critique.md) | Complete independent critique and PC-001 |

## Next Steps

The active planning parent should directly resolve PC-001, record the disposition and finalize without another critique. No user action is required. This assessor stops here.
