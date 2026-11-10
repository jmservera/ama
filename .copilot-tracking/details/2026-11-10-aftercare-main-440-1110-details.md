# Details: aftercare integration current-main checkpoint (2026-11-10)

Plan: [plan](../plans/2026-11-10-aftercare-main-440-1110-plan.md). Research: [research](../research/2026-11-10-aftercare-main-440-1110-research.md).

## P1 evidence pack section

* File: `docs/architecture/cutover-evidence-pack.md`, append after the Registry wave section; heading level two, same table style.
* Contents: banner (draft, local only, not approved, focused tier, no run); identities table; direct tree comparison table; consumed evidence table with original commands attributed to `b7e46b3be`; adverse and qualified items; requirement trace table (document-qualified); boundary review; inherited findings #1401 and #1402; evidence classes; exclusions; owners and gates; recommendation; process limits.
* Source facts come from the research record, `gh` reads and `git rev-parse` comparisons only.

## P2 index

* File: `docs/reference/README.md`, one paragraph after the Registry wave paragraph, linking `../architecture/cutover-evidence-pack.md#aftercare-integration-current-main-checkpoint-2026-11-10-refs-440-89-133-134-1401-1402`.

## P3 log

* File: `docs/reference/log.md`, append `## [2026-11-10] update | Aftercare integration current-main checkpoint (Refs #440 #89 #133 #134 #1401 #1402)` with a short bullet list.

## P4 verification

* `git diff --stat` shows only the three documentation files plus new tracking records; `git diff` of documentation files has zero deleted lines; extract the new anchor and compare it with the heading; grep for non-ASCII and em dashes in added lines; `git status` clean after commit.
