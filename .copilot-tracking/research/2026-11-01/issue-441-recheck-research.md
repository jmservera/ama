<!-- markdownlint-disable-file -->
# Research: issue 441 fresh-main recheck (2026-11-01)

Task: `issue-441-recheck`. Branch `docs/resident-portal-brd-prd`, worktree `~/source/ama-wt/issue-441`, base `81cf0c9e2b34affbe98cb75eb13734529700c369` (equals `origin/main` at fetch). Research disposition: `executed`. Planning Readiness: `Ready`.

## Finding 1: the integration the issue describes is already merged

* PR #442 (`df3e9643c`) integrated the BRD, PRD, addendum, UX statements, index, log and an unregistered Option B proposal with figures. PR #454 (`ffde36315`) corrected PRD target precedence and added the draft backlog. Both used `Refs #441`.
* Current main holds BRD FR-053 to FR-064, AC-104 to AC-132, RULE-027/028, and PRD FR-062 to FR-073 with AC-111 to AC-140 references. No original FR definition was lost (checked against base `140d8f4`).
* The pinned draft patches no longer apply to main (`git apply --check` fails on both), so re-applying them is wrong. Main drifted 254 files in `docs/` since the pinned base.

## Finding 2: custody and identifiers

* All 30 files in the 2026-10-23 custody record match their recorded SHA-256 against the coordinator session directory (`verify-441-recheck.py`, report `recheck-report.json`).
* BRD has 64 unique FR definitions and 132 unique AC definitions. PRD has 73 unique FR definitions. No duplicates once matrix and mapping rows are excluded.

## Finding 3: overlaps (issue and PR inspection at 2026-11-01)

| Item | State | Relevance |
| --- | --- | --- |
| #426 (`docs/map-provider-options-119`) | merged | No open overlap. |
| #424 (`docs/fictional-form-review-97`) | merged | No open overlap. |
| #439 (`docs/demo-cost-headroom-126`) | merged | No open overlap. |
| #722 `599d5cb6`, #690 `bbe2374d`, #704 `cbd2adc9`, #698 `4fd0f1f1`, #640 `3faa4f77` | open | Edit only `docs/reference/log.md`. Append-only entries; resolve by rebase ordering, no blanket dependency. |
| #692 `aa3bd381`, #648 `91c08923` | open | Edit `docs/reference/README.md` and `log.md`. |
| #668 `f7094d50` | open | Edits `log.md` and `research/ux/content-standard.md`. |

None touch BRD, PRD, `docs/adrs/` or the addendum. This slice edits only `log.md` (append) so any conflict is a trivial rebase.

## Finding 4: ADR registry convention

* `docs/adrs/` holds 0001 to 0006 (the repository-native registry). No `.adr-config.yml` and no `docs/planning/adrs` exist, so the plugin default allocator is not adopted here.
* Allocating `0007` would be a guessed ID without an owner or allocator decision; #442 deliberately left the proposal unregistered. Resolution: keep unregistered, do not create a competing registry, do not edit 0001 to 0006. Editable Excalidraw, SVG, PNG and text proposal are linked from the proposal; it describes the PNG as Chrome-rendered from the same model.

## Finding 5: human gate and workload figures

* FR-044 and RULE-028 on main make named per-message review the default; the exception applies only when explicitly enabled under RULE-028/OD-53, which is OFF. OD-52 to OD-55 remain visible in BRD and PRD.
* Net staff hours/week -1.594, 14.74 and 94.333 are present as author-judgement assumptions.
* Criterion 5 needs a human requirements-owner disposition. An agent cannot record it. Issue closure audit (2026-10-31) agrees.

## Link diagnostics (inherited)

Four broken relative links exist in `docs/case_study_48_addendum.md` (2) and `docs/reference/README.md` (2, the mentor deck). They are unrelated to resident work and pre-existing; recorded, not repaired.

## Recommended slice

No requirement or ADR text change. Deliver fresh exact-head verification evidence, an explicit owner-disposition request with the exact proposed wording check, a KB log entry, and independent review. `Refs #441`, not `Closes`.
