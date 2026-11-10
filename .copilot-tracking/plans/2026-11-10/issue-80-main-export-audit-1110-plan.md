<!-- markdownlint-disable-file -->
# Plan: issue #80 current-main export acceptance and inventory audit

Task `issue-80-main-export-audit-1110`. Research: `.copilot-tracking/research/2026-11-10/issue-80-main-export-audit-1110-research.md`. Details: `.copilot-tracking/details/2026-11-10/issue-80-main-export-audit-1110-details.md`. Critique: `.copilot-tracking/plans/2026-11-10/issue-80-main-export-audit-1110-critique.md`.

## Objective

Produce a source-qualified inventory and acceptance matrix for criterion C2 on current main `c66370042`, backed by the smallest maintained targeted API and browser checks on synthetic fixtures. No source, test, fixture or endpoint change; no tick, closure, threshold choice or publication.

## Phases

* [ ] Phase 1: owned environment and cwd verification
  * Create an owned venv `/tmp/ama-80-audit-venv-1110` only if the existing interpreter does not import this worktree (it does not: system `zava_forward` resolves to a different checkout).
  * Install `src/core`, `src/agents`, `src/api` editable from this worktree and `playwright==1.64.0` (declared pin), then verify import origins all sit under this worktree.
* [ ] Phase 2: targeted API checks (raw logs outside the worktree)
  * `test_list_export_api`, `test_role_endpoint_inventory`, `test_form_staging_api` from `src/api` with the declared `PYTHONPATH`, synthetic fixtures only.
* [ ] Phase 3: targeted browser checks, one non-queued heavy `flock -n` each
  * `checks.schema_download_browser_check`, then `checks.progress_browser_check` with the pinned axe asset. Fetch and read the current web guidelines and the local Fluent 2, WCAG baseline and plain-language precedence before any UI review; no design changes and no site audit.
  * BUSY or failure stops that check; no queue, wait, spin or kill.
* [ ] Phase 4: write the acceptance matrix (`.copilot-tracking/audits/2026-11-10/issue-80-main-export-audit-1110-matrix.md`) from the research tables plus check results, with unknown kept unknown and the exact owner decision stated.
* [ ] Phase 5: independent-style Review (one pass), handoff, local commit.

## Dependencies and constraints

* No private or default dataset, workbook, cloud, provider, model, SQL, image, full gate or new agents.
* Dependencies only after an actual missing or failed import; no shared installs.
* Raw evidence goes to the Root evidence folder `checks-80-main-export-audit-1110/`, outside the worktree.
* Only `.copilot-tracking/` files are committed.

## Success criteria

* The matrix names every route class with role, source, filter, order, paging, visibility, export and one-way boundary, and marks blob proof as not applicable or unknown.
* Distinct missing scope is documented for Root, without implementation.
* Seven genuine witness records, final `verify` run, clean worktree after the local commit.
