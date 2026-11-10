# Details: Registry wave current-main observation (2026-11-10, Refs #440 #185)

## Section outline (pack)

* Heading `## Registry wave current-main checkpoint (2026-11-10, Refs #440 #185 #110 #109 #184 #111 #1288)`, intro paragraph with record links, dependency statement.
* `### Identities, scope and exclusions` table: pin, trigger, source blobs, documents, hosted state, issue states, excluded items.
* `### Consumed evidence (Root local runs, not re-run here)` table plus bullets: component-subtree equivalence, adverse items.
* `### Requirement trace (Registry contract)` table: BRD FR-048, AC-090, OD-43; PRD FR-050, AC-066 to AC-068; ADR 0003 decision 6; source behaviours; class per row.
* `### Evidence classes`, `### Findings, owners and gates`, `### Recommendation`, `### Process record and limits`.

## Facts to use (all read 2026-11-10)

* Main `6cc59776`, tree `eaf44bcd`; blobs listed in research; documents BRD 0.21.0 draft, PRD 0.21.0 in-review, ADR 0003 accepted with amendment.
* Evidence: Root handoff numbers (89 tests, 2 reproductions, Ruff 237 files, mypy 290 files, SDK 2.7.0, six 1.17.0), independent functional approve 0, verdict limits.
* Statuses of issues and PRs read live; PR 1395 and local 109 preparation excluded.

## Index and log

* README: one paragraph linking to the new anchor, saying pins, source-qualified, Azure none, gates unmet, separate from NomUX, Bicep and CSV records.
* log: one `## [2026-11-10] update | Registry wave current-main checkpoint (Refs #440 #185)` entry, appended last.

## Edit method

`apply_patch`-style append edits only (end-of-file appends), then `git diff --stat` and `git diff` checked for insertions only.
