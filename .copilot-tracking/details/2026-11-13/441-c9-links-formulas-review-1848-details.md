<!-- markdownlint-disable-file -->
# Details: issue 441 criterion 9 verification

## Phase 1 checks (verifier)

* Freshness: HEAD equals `origin/main` after fetch, clean tree.
* Hash: SHA-256 and byte counts of BRD, PRD, addendum, proposal, three figures, custody JSON; re-hash the 30 custody files against `source-evidence/` copies and report matches, missing and mismatches honestly.
* Traceability: BRD FR-053 to FR-064 and AC-104 to AC-132 present once as definitions; PRD FR-062 to FR-073 and AC-111 to AC-140 present; base FR preserved vs commit 140d8f49; PRD resident traceability references to BRD IDs resolve.
* Formulas: parse BRD input table (13 inputs x 3) and recompute W,B,G,H,J,N,O,F,I and the 12-row derived table x 3; compare with the published values at table rounding; PRD -1.594/14.74/94.333; F(U)=35.4U-2.96, break-even 8.36%, V 29.90%, 25/50/75% uptake values.
* Links and anchors: every relative link and heading anchor in the five docs, GitHub slug algorithm; targeted check of PRD line 609 and addendum line 1510; compare against the 2026-11-01 inherited broken-link list.
* Policy: FR-044, RULE-028, OD-52 to OD-55, no `Closes #441`.
* ADR: unregistered proposal wording, docs/adrs registry listing (0001 to 0007, no resident ID).

## Critique amendments (see plan critique)

Pin `origin/main` SHA and report clean source inputs separately from tracking artifacts; the proposed ADR is the unregistered proposal; custody reports matched, mismatched and not-archived; re-run link/anchor method on the historical pre-#1519 blobs and label new-method-only findings unclassified; compare normalized individual lint diagnostics, else unproven; review prompt names exact hashes of BRD, PRD, proposal and changes file; add fixtures in `441-c9-links-formulas-review-1848-verify-test.py`; formula table is 12 rows x 3.

## Phase 2

`npx --yes markdownlint-cli2` with repository config if present, on the three docs; compare counts against the same run on `140d8f49` blobs only if cheap.

## Phase 3 and 4

Changes file lists each check with command, result and evidence. Review: `code-review-readiness` agent over the changes file and verifier.
