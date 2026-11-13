<!-- markdownlint-disable-file -->
# Plan: #74 criterion 2 building separation verification (issue-74-building-separation-0400)

Date 2026-11-13. Research: [research](../../research/2026-11-13/issue-74-building-separation-0400-research.md). Details: [details](../../details/2026-11-13/issue-74-building-separation-0400-details.md). Prospective, planning-only. Nothing below has been run or implemented. Review boundary for this task: planning records only.

## Objective

Establish whether current main already shows building dependencies, holds, works and costs apart from each home's evidence, decision, cost allocation and outcome, and obtain current-head execution evidence without changing product behavior. Criterion 2 is not ticked, narrowed or closed by this plan.

## Decision from research

Source already delivers the separation. No missing behavior is established for the literal criterion, so no implementation increment is ready. The single established display omission (G5, applicability not shown in the home panel) and any outcome-field addition are decision-gated and excluded by the 2026-11-12 admission.

## Phases

* [ ] Phase V1 (supported, verification only, future task, needs no new source grant): on a clean worktree at the then-current origin/main, run the two touched Python test files and the home-case browser check, and record exact head, tree, counts and hashes. No source edit.
* [ ] Phase V2 (supported, documentary): append a dated record to the #74 evidence chain mapping each maintained assertion to the criterion terms, qualifying the "home 24" figure as author-reported unless V1 reproduces it, preserving 1406 and 1409 artifacts unchanged.
* [ ] Phase G5 (NOT READY, blocked on decision): render `case_ids` and `package_ids` (or Unknown) per shared item in the home-case building panel. Requires an explicit admission that covers a product `app.js` change and a decision on whether the criterion requires it. Do not start from this plan.
* [ ] Phase O (NOT READY, owner or human authority): approve an outcome definition (handover evidence, intended versus measured performance, Not measured) before any field or UI change.

## Resume point

Next eligible action: V1 once a future task is started with run permission. Unresolved decisions: G5 admission and outcome definition; PR #82 dependency named in the 2300 follow-up is unresolvable (no such PR number in this repository), so the follow-up must be re-expressed against the current head rather than inferred.

## Validation plan (targeted, not full)

| Impacted surface | Check | Tier |
| --- | --- | --- |
| `home_case.py`, `view` | `src/core/tests/test_home_case.py` | unit |
| `/api/cases/<id>/home-case` | `src/api/tests/test_home_case_api.py` (run with `PYTHONPATH=../core/tests:../agents/tests`) | unit |
| `app.js` `homeCaseView` | `python -m checks.home_case_browser_check` from `src/api`, with pinned axe via `ZF_AXE_JS` (opens home-case routes only; synthetic dataset on a local loopback server) | browser |
| `app.js` `buildingView` | Source-inspected only; no check in this plan opens `#/building/<id>`. Execution proof would need a separate existing check, to be identified in V1, not assumed | unobserved |
| Static | configured Ruff and format check on `checks/home_case_browser_check.py` only if that file changes | static |

Focused tier: no permission, workflow, dependency, deployment, SQL or security-control change. A complete gate and a blanket `--changed` run are not planned for V1. A G5 change would add a `buildingView` and `homeCaseView` rendering assertion with an Unknown case, and would be reclassified then.

## Preserved boundaries

* Unknown values stay Unknown. Adverse: an absent or null `funding_ok` currently renders as "Funding confirmed: no" (critique CR-002); the correct representation is an open decision and is not changed by this plan. No invented building data. A shared building ID never transfers a home's evidence or approval.
* Human, AT, hosted CI and SQL Server acceptance stay separate and unchecked.
* Earlier artifacts (1406 matrices, 1409, 2300) are read-only.

## Critique and Review

* Critique: [critique](issue-74-building-separation-0400-critique.md) (one independent execution).
* Review: [review](../../reviews/2026-11-13/issue-74-building-separation-0400-review.md) (planning-only).
