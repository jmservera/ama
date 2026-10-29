---
title: Issue 96 PR 510 fix cycle 1 plan critique
description: Independent final-candidate assessment of report-local freshness reuse
ms.date: 2026-10-29
---

## Metadata

* Task ID: issue-96-pr-510-fix-cycle-1
* References: #96 and PR #510.
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/issue-96-pr-510-fix-cycle-1-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/issue-96-pr-510-fix-cycle-1-phase-details.md
* Critique execution status: Complete.
* Assessment count: one independent final-candidate critique.

## Inputs and Criterion Boundary

* Assessed the supplied plan, phase details and research C1-C4 against the
  caller's exact per-report freshness identity and lifetime, regression,
  source/test placement, validation and local-only constraints.
* Read the named implementation and test evidence:
  src/core/src/zava_forward/core/form_review.py,
  src/core/src/zava_forward/core/forms.py,
  src/core/src/zava_forward/core/doc_controls.py,
  src/core/tests/test_form_review.py,
  src/core/tests/test_form_staging.py,
  src/core/pyproject.toml and src/core/README.md.
* Read the required project specification, knowledge-base index and owner
  memory for context; they do not establish financial approval.
* Canonical targets, no generated targets, exact removals of none, maximum
  three test methods plus one helper, core test ownership and required
  validation are treated as locked decisions, not opportunities for expansion.
* Assessed planning credibility, not implementation acceptance, executed
  performance, whole-issue delivery or publication readiness.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Exact identity; C1/C3; P01-T01 | Covered | `_current` compares version/hash/kind after resolving source ID. The planned typed tuple includes all four, not field locators or ID alone. |
| Per-report lifetime; C2; P01-T01 | Covered | Dictionary allocation inside `_report` prevents sharing between drafts, requests or candidate verification. No store/module state or lock change is planned. |
| False-result reuse; P01-T01 | Covered | Membership testing before `_current` preserves cached false values. Planned negative-result invocation counts distinguish reuse from metadata short-circuiting. |
| Schema and visibility preservation; C1-C3 | Covered | Details retain the schema-current guard; `_visible` remains independent and `_current` exceptions are not converted to false. Existing schema/source and disclosure-denial tests remain active. |
| Meaningful read regression; C4; P01-T01 | Covered | Actual registration/upload/staging/review creates shared evidence; patching reads only after preparation excludes setup and candidate verification. Both JSON/SQLite and view/diagnose are included. |
| Later recheck; P01-T01 | Covered | Returning changed bytes on a later report without changing metadata defeats cross-report positive caching; both bound fields must become stale. |
| Key separation; P01-T01 | Covered | Copied-draft checks vary ID/version/hash/kind and spy on `_current`, preventing an ID-only cache or metadata early return from masquerading as exact-key reuse. |
| Bounded test structure; P01-T01 | Covered | One public-path shared-source test, one parameterized key-separation test and one negative-reuse test fit the three-method/one-helper ceiling. No installed-package tests or removals are needed. |
| Required checks; P01-T02 | Covered | Ruff check/format, core mypy and all seven named unittest modules are specified with the requested interpreter and test PYTHONPATH. All seven modules exist. |
| Documentation and handoff; P01-T02 | Covered | Core README update documents identity/lifetime; dated changes and independent Review follow actual validation. Local commit belongs to the enclosing task; this critique changes only its own output. |
| Scope and approval boundaries | Covered | No dependency, Azure, manual latest.json change, push or issue closure is planned. Later publication remains separately gated. |

## Verdict

* Verdict: Pass.
* Rationale: The proposed implementation is a simple local memoization of the
  existing boolean decision, not a second freshness policy. Its miss-only
  evaluation, exact key and allocation location directly meet the requested
  behavior. The regression plan measures duplicate byte reads rather than
  timing noise, checks semantic stale output, and requires original-code
  failure as well as fixed-code success.
* Severity counts: Critical 0; High 0; Medium 0; Low 0.

## Findings

The complete actionable PC-xxx finding set is empty. No evidence-backed
substantive correction or unresolved user decision was identified within the
supplied boundary. No findings are withheld for a later critique.

## Strengths and Residual Risk

* The existing schema permits both fields to use EPC evidence, and staging
  validates exact source spans. An explicit numeric correction makes the
  shared-source fixture feasible without bypassing the real review path.
* Candidate verification reads bytes separately before `_report`; excluding
  preparation from the read spy avoids an incorrect one-read assertion across
  an entire review action.
* Metadata-stale sources may require zero byte reads. Measuring `_current`
  invocations separately is the correct way to prove false-result reuse.
* The locked plan intentionally makes no whole-finance, live-system or
  publication claim. Tests and the independent post-implementation Review
  still have to establish that the implementation follows this plan.

## Questions or Blocking Evidence Gaps

* None for the bounded planning decision.

## Limitations

* No implementation, tests, validation environment or red/green experiment was
  executed during this read-only assessment. Planned checks are not passing
  results.
* GitHub lifecycle statements were considered as supplied research provenance,
  not independently refreshed. Local inspection confirmed docs/finance-96
  tracks origin/docs/finance-96; existing untracked planning inputs were
  preserved.
* The critique does not authorize committing other uncommitted inputs, changing
  locked targets or bypassing any later review/publication gate.

## Recommended Next Action

* Highest-impact finding: none.
* Action owner: planning parent.
* Smallest next action: record the passing critique disposition and continue
  the authorized P01 implementation and validation within the locked scope.
* Resolving evidence: not applicable; no actionable finding.
* Decision route: no direct correction or significant/divergent user decision.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/issue-96-pr-510-fix-cycle-1-plan.md](.copilot-tracking/plans/2026-10-29/issue-96-pr-510-fix-cycle-1-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/issue-96-pr-510-fix-cycle-1-phase-details.md](.copilot-tracking/details/2026-10-29/issue-96-pr-510-fix-cycle-1-phase-details.md) | Assessed implementation and validation details |
| [.copilot-tracking/research/2026-10-29/issue-96-pr-510-fix-cycle-1-research.md](.copilot-tracking/research/2026-10-29/issue-96-pr-510-fix-cycle-1-research.md) | Supplied C1-C4 research evidence |

## Next Steps

No user action is required. Return Complete / Pass to the planning parent for
disposition and the authorized next phase. This critique stops here; it does
not invoke implementation, Review, commit or publication.
