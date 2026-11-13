# Research: #441 ADR 0007 numbering and PRD:609 anchor provenance

Task: 441-adr-anchor-trace-1143. Date: 2026-11-13. Base 3b05143. Mode: read-only trace, tracking-only writes.
Start-of-research reads: case study original and addendum, knowledge base index, memory (skimmed headers; trace needs git evidence only).

## Questions

* Q1: Which PR/branch/ADR did the 2026-11-04 comment "PR opened accepting the ADR as ADR 0007" refer to?
* Q2: When was PRD line 609 anchor broken, what heading replaced it, and what is documented correction-cycle spend?

## Findings

Research disposition: executed. Planning Readiness: Ready.

### Q1 ADR 0007 numbering

* Comment on #441 (2026-11-04, "PR opened accepting the ADR as ADR 0007") refers to PR #1059, head branch `docs/accept-resident-portal-adr`, title "docs(adr): accept resident portal architecture as ADR 0007 (Refs #441)".
* PR #1059 was CLOSED unmerged at 2026-11-04T12:43:28Z (mergedAt null). Commits 2cad28376 (2026-11-04 12:21, ADR file `docs/adrs/0007-optional-resident-service-over-shared-case-authority.md`, 157 lines) and 4f80b611b (RPI evidence) exist only on `origin/docs/accept-resident-portal-adr`; `git merge-base --is-ancestor 2cad28376 origin/main` is false.
* On main, ADR 0007 is `docs/adrs/0007-contractor-intake-staff-mediated-proposal.md` (Proposed): added by 844346329 (2026-11-04, PR #1150, Refs #132), last changed by b7d66e425 (2026-11-11, PR #1440). PR #1059 closed at 12:43 UTC; #1150 was created 18:27 UTC and merged 18:51 UTC the same day, so 0007 was taken by the contractor intake proposal after #1059 closed unmerged; the resident ADR was never merged and holds no number on main.
* Not verified from the local view: the exact reason #1059 was closed (no closing comment was retrieved).

### Q2 PRD line 609 anchor

* `docs/prds/zava-forward-retrofit-programme-demonstrator.md:609` links `../capstone/README.md#agents-in-the-retrofit-process-2026-10-13`. Same stale anchor at `docs/case_study_48_addendum.md:1510` and `docs/reference/log.md:2124` (historical log entry).
* Link introduced by 5973c8eb0 (2026-10-13, PRD line 529 at that commit). The target heading "Agents in the Retrofit Process (2026-10-13)" was added to `docs/capstone/README.md` by 0af4a9b48 (2026-10-13).
* Broken by a75bbdffa (2026-10-31, "Add Microsoft Fabric Fit Assessment documentation (#558)"), which rewrote `docs/capstone/README.md` (416 lines changed) and created `docs/capstone/history/storage-map-before-reorganization.md`.
* Replacement location: `docs/capstone/history/storage-map-before-reorganization.md:223`, heading `## Agents in the Retrofit Process (2026-10-13)` (same slug). It is a relocation to a history file, not a rename; current `docs/capstone/README.md` has no such heading. `docs/reference/README.md:977` and `:1038` already use the history path.
* Candidate fix (not applied; out of scope): retarget PRD:609 to `../capstone/history/storage-map-before-reorganization.md#agents-in-the-retrofit-process-2026-10-13` and addendum:1510 to `./capstone/history/storage-map-before-reorganization.md#agents-in-the-retrofit-process-2026-10-13`. Parent of a75bbdffa had the heading at `docs/capstone/README.md:196`; PR #558 merged 2026-10-31T10:43:53Z.

### Correction-cycle spend for #441 (scoped inventory, no total)

* 2026-10-23/24 lifecycle `resident-portal-requirements-441` (PR #442): correction1 (plan, review, critique under 2026-10-23), correction2 and correction3 (plans and states under 2026-10-24).
* 2026-10-25 lifecycle `resident-prd-backlog-readiness-441` (PR #454): correction cycle 1 and 2 (state JSON, review log; commits 10d446dde, 255fa0de6, 4f989d683), plus a later "PR 454 correction" (2026-10-27) in the same review log.
* At least five numbered correction cycles are identified; the inventory is not proven exhaustive for #441 and no total is claimed. No monetary, token or time spend figure is recorded in the artifacts found, so "spend" is a cycle inventory only.
