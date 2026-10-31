---
title: RPI Plan Critique - Versioned asset cache headers
description: Single final-candidate implementation-readiness assessment for RV-001
ms.date: 2026-10-31
---

## Metadata

* Task ID: 12a8273a-1cfb-42aa-ae85-97f032ffafbd.
* Task slug: versioned-asset-cache-headers.
* Critique date: 2026-10-31.
* Plan: .copilot-tracking/plans/2026-10-31/versioned-asset-cache-headers-plan.md.
* Phase details: .copilot-tracking/details/2026-10-31/versioned-asset-cache-headers-phase-details.md.
* Critique execution status: Complete.
* Assessment count: exactly one final-candidate critique; no delegated assessment.

## Inputs and Criterion Boundary

* Caller direction: full research, plan, implement and review for original PR #596 RV-001 High; current versioned non-HTML responses must use exactly `public, max-age=31536000, immutable`, HTML must remain no-store, and bare assets must remain no-cache.
* Canonical evidence: .copilot-tracking/research/2026-10-31/versioned-asset-cache-headers-research.md, C1-C9, Q1-Q3 and its accepted/rejected alternatives; the supplied plan and phase details.
* Direct source evidence: src/api/src/zava_forward/api/static_assets.py; static response branches in src/api/src/zava_forward/api/server.py, src/api/src/zava_forward/api/resident_demo/app.py and src/api/src/zava_forward/api/resident_preview/app.py; src/api/tests/test_static_assets.py; src/api/checks/asset_cache_browser_check.py; the local-context and final Leaflet HTTP assertions in src/api/checks/workspace_scripts_browser_check.py; src/api/README.md release-safe-assets section.
* Project context: docs/case_study_48_original.md, introductory scope in docs/case_study_48_addendum.md and docs/reference/README.md, and docs/reference/memory.md. No business, legal, visual or accessibility acceptance is assessed.
* Decisions assessed: exact single decoded current `v`, HTML precedence, current-byte compatibility for obsolete URLs, retained byte ETags and GET/HEAD/304 behavior, one immutable release snapshot per handler, and no historical asset store.
* Dependencies assessed: Research Ready and critique disposition before P01; P01 before P02; reconciled validation before P03; existing Python/Ruff/Playwright prerequisites and missing-dependency-only restoration.
* Ownership and budget: existing test_static_assets.py only, no removals, at most three added test methods, no new test files/tooling; extend the two named browser checks and leave chat_submit_browser_check unchanged.
* Execution boundary: write only this critique; do not edit source/plan, execute tests/browser/cloud, spawn agents or commit. The planned local Refs #568 commit is assessed as a later parent action, not performed here. No push, workflows, Azure or secrets.
* Publication boundary: a later full local publication gate, exact-head approval and live acceptance are outside this no-push assessment; none is established or requested as a condition of this critique.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| RV-001, FR1, AC1, Q1/C1/C6 | Covered | Snapshot version is centralized; query-aware Asset.headers can select the exact immutable value for current non-HTML assets. |
| FR2, AC2, C1/C7 | Covered | Existing HTML headers and not_modified short-circuit independently; planned version/wildcard requests preserve no-store and prevent HTML 304. |
| FR3, AC2/AC3, Q1/C6/C7 | Covered | Blank values retained and exact one-value equality reject absent, old and duplicate versions while retaining current bytes and validators. |
| FR4, AC1/AC2, Q2/C3-C5, P01-T01 | Covered | All three consumers and both successful/conditional branches identified; resident route selection and guards explicitly remain unchanged. |
| AC3, P01-T02, test budget | Covered | Shared real-handler helper and release-identity test support the matrix without exceeding three new methods or moving tests into packages. |
| AC4, Q3/C8/C9, P01-T02 | Covered | Normal same-context cache reuse is distinguished from explicit conditional HTTP; legacy turnover, failure recovery, bare Leaflet and unchanged chat checks retained. |
| AC5, P02-T01 | Partial | Exact required API commands specified, but the prescribed lock and default scratch locations violate the execution environment; PC-001. |
| P02-T02, AC6 | Covered | Actual exits/results, deviations, preserved adverse outcomes and source-versus-publication boundaries must be reconciled before Review. |
| P03-T01 | Covered | One independent Review has a full source/evidence boundary and separate execution/outcome; findings remain visible and routed rather than silently repaired or re-reviewed. |
| P03-T02, AC6 | Covered | Later local-only commit uses privacy-safe local identity, Refs-only linkage, required trailer, narrow staging and metadata verification. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 0 High, 1 Medium, 0 Low actionable findings.
* Rationale: the header/query design, route integration, regression budget and browser observation strategy are credible. One direct correction to validation paths is required before execution can comply with this environment. No unresolved product or user decision is needed.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Validation prescribes forbidden temporary-file locations

* Related IDs: AC5, P02-T01, P01-T02 documentation completion.
* Evidence: .copilot-tracking/details/2026-10-31/versioned-asset-cache-headers-phase-details.md, P02-T01 prescribes `/tmp/ama-rpi-heavy.lock`. src/api/tests/test_static_assets.py uses tempfile.TemporaryDirectory() without a directory; src/api/checks/asset_cache_browser_check.py likewise uses tempfile.TemporaryDirectory(prefix="asset-release-") without a directory. src/api/README.md release-safe-assets examples repeat the `/tmp` lock. The current execution instructions prohibit file operations in `/tmp` and `/var/tmp` and require scratch creation relative to the working project.
* Concern: external result-output selection does not relocate the lock or Python's default scratch files. Following the details literally therefore conflicts with the environment before the required local validation can complete.
* Impact: the parent could fail the requested validation for environmental reasons or violate the execution boundary while claiming a compliant run.
* Smallest useful change: revise P02-T01 to create an owned project-relative scratch directory, set TMPDIR before Python/browser processes so existing tempfile consumers use that directory, and use an allowed lock path with explicit heavy-run coordination. Retain the exact three requested command bodies and existing test/check ownership. Update only the directly related README command examples when implementing the planned documentation task. Record owned scratch cleanup without deleting historical evidence or other workers' files.
* Action owner: planning parent; implementation parent applies the revised execution setup.
* Exact resolving evidence: plan/details name the allowed scratch/lock setup, TMPDIR export and owned cleanup; the related README examples no longer instruct this task to open a `/tmp` lock. Later P02 evidence records the effective scratch/lock paths, unchanged required command bodies and actual exit results. Resolving this critique requires the plan correction, not premature test execution.
* Decision route: direct planner correction. Current environment restrictions already settle the choice; no significant or divergent user decision and no user response are required.

## Strengths and Residual Risk

* Shared classification avoids divergent per-handler cache policies. Passing the raw query to both 200 and 304 headers preserves the existing validator and HEAD framing paths.
* The proposed parse_qs(..., keep_blank_values=True) value-list comparison is concrete: a single decoded current `v` qualifies; duplicate current values and current-plus-blank/old values do not. A different parameter alone does not qualify. Additional non-`v` parameters do not invalidate a single current `v` under this selected rule, consistently with FR1; the rule is not full-query-string equality.
* The immutable guard addresses the material snapshot hazard: an obsolete URL on a new handler still serves current bytes but cannot acquire a new immutable promise. Existing old-snapshot bytes remain stable, while a changed release invalidates the previous version classification.
* The shared actual-handler test helper can exercise positive and negative query shapes, validators and conditional HEAD across all three apps without duplicating test owners. HTML version/wildcard coverage should use that same helper.
* Browser validation is sound as planned: establish successful release-B loads and recovery, compare per-asset origin counts across normal navigation in the same context, and assert explicit ETag 304/policy separately. An aggregate historical 304 or a reload alone is not the planned proof of fresh reuse.
* src/api/checks/asset_cache_browser_check.py currently has no Playwright routing interception. Preserve enabled browser caching there. The routed workspace check is useful for recovery and HTTP header assertions, not independent evidence of browser cache reuse.
* Release turnover, ordinary failure recovery and the bare Leaflet assertions remain required; the new versioned Leaflet assertion supplements rather than replaces them. Chat submission remains an unchanged executed regression target.
* Process restart after packaged changes, already-open-page behavior, live deployed headers and authenticated operational acceptance remain explicitly deferred or unverified as stated in the supplied artifacts.

## Questions or Blocking Evidence Gaps

* None requiring a user decision or additional research within the supplied boundary.
* Original PR #596 Review attribution was supplied through the research C2 pointer and caller context; the original remote record was not independently reread or modified.

## Limitations

* This is implementation-readiness assessment, not implementation or validation. No tests, Ruff, browser, cloud, commits or publication gates were executed.
* Dependency availability and future command success are not inferred from the research baseline or plan.
* Only the supplied task artifacts and named source evidence were assessed; no open-ended repository audit or new external research was performed.
* Existing source, research, plan, details and review records were left unchanged. Existing untracked parent artifacts were not staged, moved or cleaned.

## Recommended Next Action

* Highest-impact finding: PC-001, Medium.
* Action owner: planning parent.
* Smallest next action: correct the P02 execution setup and reconcile its disposition in plan/details, retaining this original critique outcome.
* User response required: no.
* Parent may finalize after addressing this complete finding set without another critique. Continue into P01 only after recording the disposition; do not treat this Revise verdict as a validation pass.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-31/versioned-asset-cache-headers-research.md](.copilot-tracking/research/2026-10-31/versioned-asset-cache-headers-research.md) | Supplied source evidence and selected cache semantics |
| [.copilot-tracking/plans/2026-10-31/versioned-asset-cache-headers-plan.md](.copilot-tracking/plans/2026-10-31/versioned-asset-cache-headers-plan.md) | Final-candidate plan requiring one correction |
| [.copilot-tracking/details/2026-10-31/versioned-asset-cache-headers-phase-details.md](.copilot-tracking/details/2026-10-31/versioned-asset-cache-headers-phase-details.md) | Implementation and validation task details |
| [.copilot-tracking/reviews/plans/2026-10-31/versioned-asset-cache-headers-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/versioned-asset-cache-headers-plan-critique.md) | Complete single critique and original Revise verdict |

## Next Steps

The active planning parent resolves PC-001 directly, records its disposition and finalizes the plan without repeating critique. No user action is required. This critic stops after returning the artifact; implementation, validation, independent Review and local persistence remain parent-owned, with publication/full-gate acceptance outside the current scope.
