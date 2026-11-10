<!-- markdownlint-disable-file -->
# Plan details: nomination and UX integration wave checkpoint (#440, 2026-11-10)

Plan: [plan](../plans/2026-11-10-nomination-ux-main-440-1110-plan.md). Research: [research](../research/2026-11-10-nomination-ux-main-440-1110-research.md).

## Phase 1: pack section

* File: `docs/architecture/cutover-evidence-pack.md`, appended after the last section; heading `## Nomination and UX integration wave checkpoint (2026-11-10, Refs #440 #130 #149 #153 #156 #1360 #1362)`.
* Subsections: identities, scope and exclusions; consumed evidence (two Root verification records with command counts, skips and limits); tree-equivalence and qualification; requirement trace (document-qualified); source boundaries; evidence classes; findings, owners and gates; recommendation; limits and independent review needs.
* Success: every identity matches the research record; every count matches the Root handoff or raw summary; each claim carries its class; no sentence implies a command ran on `65c2ab9d9`.

## Phase 2: index and log

* `docs/reference/README.md`: append one paragraph after the last checkpoint paragraph with the anchor link to the new heading.
* `docs/reference/log.md`: append one `## [2026-11-10] update | ...` entry; do not edit earlier entries.
* Success: anchor equals the GitHub slug of the heading; only appended lines changed in each file.

## Phase 3: review and commit

* Review the full diff, scan added lines for non-ASCII, em dashes and bold-prefix lists, resolve relative links, commit with `docs(evidence): ...`, `Refs` only, Copilot trailer, repository-local noreply identity.
* Then the witness events `implement-done`, `review-done` and `commit-complete`, and `verify`.
