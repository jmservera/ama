<!-- markdownlint-disable-file -->
# Research: issue 441 criterion 9 re-verification (2026-11-13)

Disposition: executed. Planning Readiness: Ready. Base: `origin/main` b630279b4 (worktree HEAD identical, clean).

## Issue state

* `gh issue view 441 --comments` (12 comments): 7 of 9 criteria ticked; 5 and 9 open. Owner 2026-11-02 and 2026-11-04 comments keep both unmet; per-message review stays normative; the demo exception is not an OD-53 approval.
* Criterion 9 needs: focused Markdown/link/anchor/hash/traceability/formula checks; inherited-diagnostic comparison; exact integrated-byte independent review; publication gates. This lane only verifies and records. No tick, no push, no issue edit.

## Artifacts in scope on main

* BRD `docs/brds/agentic-retrofit-programme-brd.md` (2760 lines), PRD `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (3084 lines).
* Proposed ADR: unregistered resident-service proposal under `.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/` (`docs/adrs` holds 0001 to 0007; 0007 is the unrelated contractor-intake proposal, so no resident ADR ID exists).
* Coupled: `docs/case_study_48_addendum.md`, `docs/reference/README.md`.

## Reusable prior method and limits

* `.copilot-tracking/changes/2026-11-01/issue-441-recheck/verify-441-recheck.py` exists; its base-branch checks (custody against the original session draft dir, `registry_is_0001_to_0006`, `no_adr_change_on_branch`) are stale: the draft directory is gone and the ADR registry now has 0007.
* Original input hashes are in `.copilot-tracking/research/2026-10-23/resident-portal-requirements-441-input-custody.json` (30 files); retained copies are under `source-evidence/` of the 2026-10-23 changes folder, so custody can be re-hashed from the repository.
* BRD capacity table: 12 derived rows x 3 scenarios; inputs A,D,C,Tc,E,Te,U,V,R,Tr,Q,S,To (13 x 3). PRD states -1.594/14.74/94.333 and BRD table rounds to -1.59/14.74/94.33.
* Post-#1519 anchor repair: PRD line 609 and addendum line 1510 now point at `capstone/history/storage-map-before-reorganization.md#agents-in-the-retrofit-process-2026-10-13`.

## Approach

A new read-only verifier in the 2026-11-13 changes folder computes: freshness, hashes, registry and traceability, policy, formulas, relative links with heading anchors (GitHub slug rules) for the five docs, and ADR proposal, comparing broken links to the inherited 2026-11-01 diagnostics. Markdownlint via npx is attempted and reported if unavailable.

## Not proven

Live resident acceptance, screen-reader conformance, deployment, spending, final requirements approval, BRD Define / PRD Validate (BLOCKED, quality FAIL), hosted CI on a future publication head.
