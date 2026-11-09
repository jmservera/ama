---
title: Issue 1259 ranking archive path health plan
description: Prospective FULL-tier plan to report unusable ranking archive paths as unknown
ms.date: 2026-11-08
---

## Objective

Make a regular-file, dangling-symlink or stat-failing archive path report as unreadable with an unknown window across schedule, verify and publish, while an absent directory keeps first-run behavior. Refs 1259, 79, 1231, 1258 while stacked; no closing keyword until all reviewed criteria reach main.

## Tier, base and target

* FULL tier, from the issue's persistence-integrity scope despite the small footprint.
* Branch fix/ranking-archive-path-health on f548b65f4 (tree 32ec). PR target while stacked: the fix/ranking-archive-ancestor-durability (1258) branch, not main.
* Prospective: this plan was written before any 1258 source freeze.

## Critique dispositions

See .copilot-tracking/plans/2026-11-08-ranking-archive-path-health-1259-critique.md. Verdict Revise; all items applied or scoped; no repeat critique.

## Required input before implementation

* Coordinator admits 1258 and freezes its source head. Then this session propagates that exact candidate (normal merge, no rebase or reset, no parent worktree write) and prospectively updates this plan and details with the exact 1258 head and tree, the conflict result in ranking_publication.py and the grep of `_names`/`verify`/`overdue` callers.
* Do not implement on the old f548b65f4 baseline and do not apply the stale 86 or 123 diffs.

## Phases

* [x] 1.1 Prospective Research, plan, details, one independent critique with dispositions (PC-001 to PC-007 applied below), state JSON; the clean planning commit is recorded in the state JSON and the response, not asserted here before it exists.
* [ ] 2.1 Propagate frozen 1258 head; record head/tree; reconcile this plan (GATE: resume only after this).
* [ ] 2.2 Add failing-first tests (red demonstrated on the propagated base before the fix) in src/core/tests/test_ranking_publication_runner.py: regular file, dangling symlink, patched stat failure and absent-directory control, each for schedule, verify and publish through `runner.run` and one CLI case; shared test_ranking_publication.py only for a direct `verify()` case if needed.
* [ ] 2.3 Implement `_names()` classification in ranking_publication.py; touch ranking_publication_runner.py only if a mapping gap is proven.
* [ ] 2.4 Green: focused core selectors, then the 1258 selectors again for interaction.
* [ ] 3.1 Changes record with red evidence, amendments and divergences.
* [ ] 3.2 One authored post-implementation Review.
* [ ] 4.1 Local FULL gate: `python3 tools/rpi-checks.py --all --base <fresh origin/main> --out <new external dir>`, receipt covering the candidate stack, external only; `--verify-receipt` against the current origin/main immediately before push.
* [ ] 4.2 Independent exact-head assessment per declared target, hosted checks, owner approval. Not performed in this session boundary.

## Acceptance mapping

| Criterion | Evidence planned |
| --- | --- |
| Absent creatable vs unusable | `_names()` stat/lstat plus nearest-existing-ancestor classification (PC-001); tests 2.2 |
| Existing unreadable shape, unknown window | schedule status problem, due None, next window None; verify problem, overdue None; publish refused archive_unreadable |
| First-run and path-free diagnostics | absent-directory control publishes; no tmp path in problem text |
| Regressions fail before fix | red run recorded in changes record |
| FULL, assessment, hosted | 4.1 and 4.2 |

## Stop conditions

1258 not frozen; unreconcilable conflict in ranking_publication.py; main moves before the gate (re-verify, no base relax); a caller depends on empty-for-missing beyond tests; any need for private data, model or cloud access; any governance decision.

## Boundaries

No write to the parent worktree, issue, board or PR; no push, merge or close; no skip tokens, cloud fallback, old receipt reuse or fabricated approval. Static finding is not production proof.

## Prospective propagation update (2026-11-08)

* Exact parent: fix/ranking-archive-ancestor-durability at 26b4ea391d6a6000e9be8fc6f78994e52a6d0f6c, tree c9c7c239d2b0872425843ad9cff97c74f277a6f8, parent 3712f107. Child planning head abc142fb, tree d088b597. Main f548b65f4 (origin/main unchanged). Ignored-inclusive clean.
* Parent source delta is disjoint from `_names`/`verify`: publish docstring, new `_ancestors`, `_confirmed` parent sync, DurabilityUnconfirmedError text, one runner message string. Dry merge (git merge-tree) is conflict-free. Phase 2.1 is executed as one normal merge, no rebase, reset, amend or parent worktree write.
* Callers outside tests: runner `_verify` (OSError mapped to unreadable) and `Store.ranking_publication_status` (OSError mapped to a problem; its overdue-vs-unknown semantics stay the recorded PC-004 residual, out of scope).
* Parent residuals R1 to R6 (writable-parent heuristic, boundary coverage, API-fault) are preserved and not resolved here.
* Scope: LIGHT source/regression preparation only; FULL, receipt, independent assessment, hosted checks and human approval remain unperformed.
