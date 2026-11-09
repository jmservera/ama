# Issue 81 forward preparation plan, 2026-11-09

Refs #81 only. Research: `.copilot-tracking/research/2026-11-09/issue-81-forward-preparation-research.md`. Details: `.copilot-tracking/details/2026-11-09/issue-81-forward-preparation-details.md`. Local only: no push, PR edit, board, ticks, merge, SQL, deploy, model calls or full gate.

## Scope

* P1: normal local merge of `origin/main` `9f9aacc8` into HEAD `05ec1a7e` (no reset, rebase, force, new PR). Keep both sides of the evidence document. No #1308 import.
* P2: run the unaffected lifecycle, authorisation and manual-path selectors once, worktree-bound, because main's merge changes source.
* P3: record the prospective final #1292 integration plan and exact unresolved dependencies in the handoff.
* P4: Review once; commit evidence; write the coordinator handoff.

## Correction-count

The default five TOTAL correction cycles preserve the actual history. This preparation is not a review-correction cycle, so it neither resets nor consumes one.

## Critique (author, executed once, before changes)

* Verdict: proceed. Findings applied directly:
  * Merge only the exact fetched `origin/main` SHA, not a moving ref, so the identity is reproducible.
  * Resolve the conflict as union of both appended sections; verify no line from either side is dropped by comparing against each parent.
  * Do not treat `store.py` / `test_resident_decisions.py` / core README overlap with #1308 as resolvable now; defer.
  * Test imports must come from this worktree (check `zava_forward.core.__file__`), not another checkout's editable install.
  * No test result may be inferred from the earlier recovery record; counts are recorded only from this run.
* No finding conflicts with confirmed owner decisions. No repeat critique.
