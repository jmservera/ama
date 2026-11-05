<!-- markdownlint-disable-file -->
# Plan: coordinator idle recovery (issue 1204)

* Date: 2026-11-05
* Research: .copilot-tracking/research/2026-11-05-coordinator-idle-recovery-1204-research.md
* Details: .copilot-tracking/details/2026-11-05-coordinator-idle-recovery-1204-details.md
* Validation tier: Focused (prompt and documentation only; no infrastructure or security implementation)
* Change class: Major (decision rules, stage gates, write-authority wording)

## Objective

One coherent amendment of `.github/agents/ama-backlog-delivery-coordinator.agent.md` so recurring ticks advance real work, stop decisions rest on fresh complete classification, briefs cannot publish early, and cleanup stays finite and verified.

## Success criteria

* Idle or stop decisions require a fresh complete classification with evidence; unknown or unreviewed is research or refinement work.
* Each tick names and executes a real next action; up to five unassessed closure-review items are worked per tick with cursor and findings in session SQL.
* Two no-progress ticks with ready or unassessed work trigger a bounded recovery in that tick. A tick ending is distinct from the run ending.
* Owner questions are one at a time; approvals are persisted, reclassify affected tasks and are routed before completion is claimed; authority is never re-requested or expanded.
* Eight sessions, 20-PR drain to 10-15, stacks, batched publication, exact-head review, tiers and human boundaries are preserved; no gratuitous rebase of valid green heads.
* Overlapping schedule, stop and rebase text is reconciled; schedule replacement and prompt versioning are documented.
* Briefs are generated fresh from canonical policy with an explicit target; workers do not publish.
* Cleanup honors finite selection, active receipt or image ownership, archive/readback/restore, unknown upstream and squash-merge lifecycle.
* Frontmatter unchanged; no other source file edited.

## Phases

* [ ] Phase 1: Baseline and authoring (hve-builder improve). Details: Phase 1.
* [ ] Phase 2: Independent static review, one correction batch, targeted closure. Details: Phase 2.
* [ ] Phase 3: Contained behavior simulation through `hve-builder-tester` on the final state. Details: Phase 3.
* [ ] Phase 4: Focused validation (Markdown/link review, `git diff --check`, applicable existing checks). Details: Phase 4.
* [ ] Phase 5: Changes record, original RPI Review, commit locally. Details: Phase 5.

## Critique (single final-candidate critique)

Recorded in the changes file after Phase 1 drafting; compatible findings applied directly.
