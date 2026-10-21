<!-- markdownlint-disable-file -->
# RPI Changes: Cut-over soak evidence preparation for #201

## Metadata

* Task ID: 201-soak-review
* Task slug: cutover-soak-review-201
* Plan: .copilot-tracking/plans/2026-10-21/cutover-soak-review-201-plan.md
* Phase details: .copilot-tracking/details/2026-10-21/cutover-soak-review-201-phase-details.md
* Base: 993a7b88c03f5240f1e7a4c7c7afa7c064281622 (origin/main identical on 2026-10-21; no new #201 comment, four total)
* Declared scope: full plan (P01 to P03)

## Execution Status

* Status: Complete for preparation scope; commit and Review recorded in later artifacts.

## Execution Summary

Added a dated reconciliation section to the existing cut-over evidence pack, a dated ADR note, one index row extension and an appended log entry. No soak, sign-off, duration, tag, deletion, Azure, budget, private-data or issue/PR action occurred.

## Completed Work

### P01-T01 AC map and reconciliation

* docs/architecture/cutover-evidence-pack.md: new section `Soak and Cut-Over Evidence Preparation (2026-10-21)` before `Other Cut-Over Gates`: 11-row table (all UNMET, evidenced versus unmet component, owner), dated corrections (soak contradiction, stale rubric statement, open PR refresh, PR-only CI, historical health), and an additive superseded blockquote under `Other Cut-Over Gates`.
* Evidence: research record C1 to C19, W1 to W7.

### P01-T02 Soak specification

* Same file: proposed specification table; every parameter `OPEN (owner)` or labelled a proposal; no numeric duration, cadence or tolerance.

### P01-T03 Pending decisions

* Same file: D1 to D16 table (Pending) and one unchecked checklist item. No checkbox ticked.

### P02-T01 ADR, index, log

* docs/adrs/0006-src-layout-and-cutover.md: dated note under Owner Answers; Status and gate text unchanged.
* docs/reference/README.md: one existing row extended in place.
* docs/reference/log.md: appended `query` entry; deletions in diff: 0.

### P03-T01 Validation and commit

* See Validation Record. Commit 1 holds docs and tracking; commit 2 holds Review and final state.

## Implementation-Time Plan and Detail Updates

### Critique-driven revisions before implementation

* Plan and details revised for PC-001 to PC-009 before any edit (recorded in the plan Critique Disposition). No divergence during implementation; frontmatter `ms.date` of the pack intentionally not changed to avoid the open PR #423 overlap.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `git diff --check` | four changed docs | Passed | no output |
| Relative link and anchor check (inline Python) | four changed docs, 614 links | Passed for added links | 4 anchor misses are pre-existing historical log links to `mvp/README.md` anchors, not changed |
| Scope check `git diff --name-only` | worktree | Passed | only the four in-scope docs plus dated tracking |
| Log append-only check | docs/reference/log.md | Passed | 0 removed lines |
| ASCII and invented-duration scan on added lines | diff | Passed | no non-ASCII; no `N days/hours/weeks` text |
| Checkbox check | cutover-evidence-pack.md | Passed | zero checked boxes |
| Full local RPI gate (`tools/rpi-checks.py --all`) | repository | Not performed | coordinator serializes the external gate |
| Docker, SQL, Azure, browser checks | n/a | Not performed | prohibited or out of scope |
| Live Azure state | n/a | Not performed | no Azure calls permitted |
| Candidate-commit CI, rubric rerun | n/a | Not performed | no candidate exists |

## Pre-Review Reconciliation

Plan markers P01 to P03 are checked except P03-T01 final commit evidence, which the commit step completes. Details, handoff and follow-ups agree: D1 to D16 pending, none blockers.

## Blockers

* None for preparation. Actual gate blocked by owner decisions, tenant sign-in, budget.

## Remaining Work

* Local commit; Review; coordinator full gate, independent assessment, draft PR with `Refs #201`.

## Follow-Up Items

* Owner decisions D1 to D16; fresh deployed-candidate evidence after D1.

## Return-to-Caller State

* Ready for Review.

## Integration Continuation (2026-10-21)

* Rebased the run-owned branch `docs/cutover-soak-review-201` onto `origin/main` at `ca4baf75837de57c99718f7423716d5dc0b0e244` (merged PR #420). No conflicts; no file content changed beyond the rebase. The log entry remains appended after main's last entry.
* `certifi==2026.10.19` from PR #420 is present in the `src/*/requirements.txt` files; this branch does not touch them.
* The single original Review (`.copilot-tracking/reviews/2026-10-21/cutover-soak-review-201-review.md`) is unchanged and no second Review was run; its verdict and residual items stand as recorded.
* Prior exact-head gate evidence belongs to the old base and is historical, not current acceptance. No current full gate is claimed; the coordinator serializes it after handoff.
* Validation: git status clean before rebase, rebase clean, diff scoped to the 11 issue files. No Docker, Azure or full gate.
