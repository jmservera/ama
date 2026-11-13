<!-- markdownlint-disable-file -->
# Details: #74 criterion 2 building separation verification (issue-74-building-separation-0400)

Plan: [plan](../../plans/2026-11-13/issue-74-building-separation-0400-plan.md). Prospective only.

## V1 verification run (future)

* Preconditions: clean worktree of fetched origin/main; local `src/*` distributions installed per the repository instruction (no `PYTHONPATH=mvp`); synthetic fixtures only (the harness starts a local loopback server on a synthetic dataset; no `ZF_DATA` or private dataset, no cloud or model). Pinned axe 4.10.3 file with SHA-256 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb (as in the check); without it the result is PARTIAL, not COMPLETE.
* Commands: core test file; API test file; `python -m checks.home_case_browser_check` from `src/api`.
* Expected from source reading, to be confirmed not assumed: core tests include the explicit-True funding case; API tests include non-finance no-amount and finance own-allocation cases; browser prints PASS lines and COMPLETE with exit 0. Compare the PASS count to the reported 24 (16 + 2 + 6, which includes the harness server PASS, so the browser portion is expected to be 23 with axe) and report any difference.
* Record: head SHA, tree SHA, counts, skips, log SHA-256, Chromium version (the check does not print it; read it from the installed browser separately and state that source), writes observed (must be zero non-safe methods), JavaScript errors (zero).
* Stop conditions: any failure is recorded as adverse evidence with the first failing assertion; do not repair product source under V1.

## V2 criterion-term mapping (future documentary)

| Criterion term | Home side evidence | Building side evidence |
| --- | --- | --- |
| dependencies, holds, works | n/a (must be absent from home panel) | building panel h3 and building screen cards |
| costs | own allocation GBP 6000.00, restricted for non-finance | GBP 12000.00 in building panel only, restricted for non-finance |
| evidence, decision, outcome | documents, decision, stage, quality in home panel only | absent from building panel |

Mark each cell as observed-in-run, observed-in-diff-only or unobserved.

## G5 (not ready) design notes for a future admitted task

Minimal change: extend `shared()` in `homeCaseView` to append the existing `Affected homes` and `Packages` line already used in `buildingView`, reusing the same null-to-Unknown rule; no API or data change because the fields already travel in the payload. Verify the payload carries `case_ids` for the roles that reach this view before relying on it. Test: add one assertion each for a scoped item and an Unknown (`null`) item in the existing browser check. Behavior for existing text must not change.

## Out of scope

Outcome field additions, criterion edits, issue or PR writes, publication, cleanup, other #74 slices.
