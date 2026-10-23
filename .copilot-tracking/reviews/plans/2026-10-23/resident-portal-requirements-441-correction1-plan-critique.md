---
title: Resident proposal correction1 independent plan critique
description: Single bounded pre-implementation critique for issue 441
ms.date: 2026-10-23
---

## Metadata

* Task ID: jmservera/ama#441; resident-portal-requirements-441
* Native parent session: 59f31558-980b-475c-b2e2-3b8d68279ed9
* Critique date: 2026-10-23
* Plan: .copilot-tracking/plans/2026-10-23/resident-portal-requirements-441-correction1-plan.md
* Phase details: .copilot-tracking/details/2026-10-23/resident-portal-requirements-441-correction1-phase-details.md
* Critique execution status: Complete
* Observed local head: 81c405624608d704263676579730444394b043fb
* Observed origin/main: f1e2d830f17558efd868919de1973ea7244a8841
* Observed remote topic tracking ref: d8b416a3f13e3e4a5b018f0853285ced972c1c8a

## Inputs and Criterion Boundary

Read the complete correction1 research, plan and phase details, the supplied
validator, the historical Review's pin/outcome/artifact-table sections, and
the local commit/ref evidence. Read repository case-study and knowledge-base
entry context. The opening worktree contains precisely the parent's three
untracked correction1 research/plan/details files; they are not critic-owned.

The assessment covers P07-P09: local second-bot integration, scope and
baseline semantics, focused regression sufficiency, destination-only historical
navigation repair, provenance, independent correction Review and local commit
handoff. The criterion is credibility for this correction, not product
approval, rubric quality, publication readiness or a complete gate.

Owner decisions explicitly exclude product refinement, incomplete sibling
author output, score editing/regeneration, numbered ADR changes, heavy gate,
remote mutations and PR/issue status changes. Those decisions are constraints,
not missing implementation phases. The parent's permitted external pinned
Markdown CLI restoration is not restricted by this critic's write-only-output
boundary.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| P07-T01/T02; research C1-C6 | Covered | Actual failure and bounded research precede critique; pre-edit evidence commit and single disposition are explicit. |
| P08-T01; research C2 | Covered | Local d8b416a3 inspection confirms only .github/rubric/scores/latest.json changes; cherry-pick with source provenance, exact blob comparison and conflict stop preserve legitimate score history. |
| P08-T02; research C3 | Covered | Original reconstruction BASE remains fixed; independent merge-base scope, exact document/task/score allowlist, untracked checks and negative boundaries address the hosted assertion without broad exclusions. |
| P08-T02/T03; research C4 | Partial | True-absence and git-error semantics are specified, but the locked regression list does not explicitly exercise the affected fragment-link caller; PC-001. |
| P08-T02/T03; research C5 | Covered | Fourteen destination-only repairs, normalized-diff equality and separate provenance retain historical labels, prose, outcome and pins. |
| P08-T03; research C6 | Covered | One stdlib module, at most eight methods, actual validator execution, external fresh report, inherited diagnostics and 21/22 old output pins are explicit. |
| P09-T01/T02 | Covered | One correction Review, immutable historical evidence, local commit and clean identity handoff are bounded; no full gate or publication is planned. |
| Hosted Low 4364841399 / 4364841447 | Covered | Unsupported A5/B6 citation/rationale findings remain open; no paid scorer, workflow or manual generated-score repair is authorized. |
| Owner policy and product boundaries | Covered | Assisted continuity, current policy OFF, unsigned/live gates, unregistered id null, non-draft PR and requested mention are preserved rather than re-decided. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* Rationale: The correction is otherwise credible and appropriately narrow.
  One directly reproducible defect path needs explicit regression acceptance
  before implementation. This does not require broader research, a new
  critique, a ninth test method or a user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Exercise the new-file fragment baseline through the link checker

* Related IDs: research C4; P08-T02; P08-T03; focused-regression acceptance.
* Evidence: .copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/validate-integration.py, broken_links(), currently calls git_bytes(relative) directly for a present Markdown target with a fragment when baseline=True. The correction1 phase details explicitly identify that caller as needing the new absence semantics, while the locked test list names absent/existing bytes and invalid git command/ref without requiring a broken_links() invocation.
* Concern: A helper-only baseline test can pass while this independent caller still performs unconditional git show. Exercising the actual validator is valuable but does not specify a fixture that reaches this branch for a genuinely new fragment target. The supplied evidence does not establish that the current document links necessarily exercise it.
* Impact: The validator can still abort before its report on a valid new linked Markdown file despite passing all listed helper and scope tests. This leaves part of the researched baseline defect unprotected.
* Smallest useful change: Extend an already planned baseline test method with real git-fixture subcases invoking broken_links(..., baseline=True). A current Markdown target absent from BASE must produce the expected unresolved-baseline fragment result without a git-show exception; the corresponding current valid anchor must resolve. Include an existing baseline target/anchor and invalid baseline propagation through this caller. Reuse the existing absent/existing/error coverage rather than adding a framework or exceeding eight methods.
* Action owner: Planning parent, then implementing parent.
* Exact resolving evidence: Correction1 details explicitly require these caller-level subcases; the single adjacent stdlib module contains them against a real git fixture; focused unittest results demonstrate absent-target, existing-target and invalid-ref behavior through broken_links(), alongside the actual validator report.
* Decision route: Direct planner correction. No significant or divergent user decision is required.

## Strengths and Residual Risk

* Exact generated-score blob retention, conflict refusal and separate original
  BASE/current scope-base prevent a false score repair or custody rewrite.
* Scope rejection and untracked checks are explicit; this is not a blanket
  allowance for tracking, docs, code or generated rubric files.
* Destination-only repair and separate correction provenance preserve the
  historical Review rather than silently changing its judgement.
* A5/B6 remain accepted open limitations of this bounded correction, not
  supported score citations or completed rubric acceptance.
* Prior receipts become historical after changes. No current receipt,
  hosted approval, complete gate or publication readiness is inferred.
* The later author-package integration remains a separate dependency for a
  stable final publication candidate; it is not required in this local loop.

## Questions or Blocking Evidence Gaps

None requiring user response. PC-001 is a bounded regression-contract gap,
not a need to access sibling work or commission additional scoring.

## Limitations

This is one pre-implementation assessment of supplied inputs. No tests,
validator, dependency restoration, gate or implementation were run here.
Remote identities were read from existing local refs, not freshly fetched.
No incomplete sibling output or full product/scoring review was inspected.
The only critic-owned write is this critique artifact.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Disposition PC-001 once and make caller-level baseline
  subcases explicit within the existing eight-method regression contract.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-23/resident-portal-requirements-441-correction1-research.md](../../../research/2026-10-23/resident-portal-requirements-441-correction1-research.md) | Supplied bounded correction evidence |
| [.copilot-tracking/plans/2026-10-23/resident-portal-requirements-441-correction1-plan.md](../../../plans/2026-10-23/resident-portal-requirements-441-correction1-plan.md) | Assessed correction plan |
| [.copilot-tracking/details/2026-10-23/resident-portal-requirements-441-correction1-phase-details.md](../../../details/2026-10-23/resident-portal-requirements-441-correction1-phase-details.md) | Assessed implementation and test contract |
| [.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/validate-integration.py](../../../changes/2026-10-23/resident-portal-requirements-441/validate-integration.py) | Existing validator examined read-only |
| [.copilot-tracking/reviews/logs/2026-10-23/resident-portal-requirements-441-review.md](../../logs/2026-10-23/resident-portal-requirements-441-review.md) | Historical navigation and outcome boundary |

## Next Steps

Return to the active planning parent for one direct disposition and plan/details
finalization, then the authorized correction implementation and independent
correction Review. Do not run another plan critique. No user action is required.
Stop this critic here; no implementation, gate, push or PR/issue mutation.
