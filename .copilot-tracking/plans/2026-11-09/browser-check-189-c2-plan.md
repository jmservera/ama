<!-- markdownlint-disable-file -->
# Issue 189 C2 browser check plan (2026-11-09)

Research: [research](../../research/2026-11-09/browser-check-189-c2-research.md). Details: [details](../../details/2026-11-09/browser-check-189-c2-details.md). Critique: [critique](browser-check-189-c2-critique.md). Refs #189 only. Cycle: C1 spent, C2 authorised now, three remain.

## Objective

Replace the non-specific `get_by_text("Stopped", exact=False)` wait at `simulator_control_browser_check.py:155` with a wait on the completed Stop response notice, then assert the state, so the following file assertion is no longer racing the server write. No product change, sleep, retry, removed assertion or weakened state.

## Phases

* [ ] P1 Commit research, plan, details, critique (one) and initial state before any source edit (frozen).
* [ ] P2 Edit only `src/api/checks/simulator_control_browser_check.py`: after `stop(page)` at line 154 wait for `#simulator-control-notice` containing `Stop saved and read back`, assert the State fact reads `Stopped.`, keep the file assertion and the axe scan.
* [ ] P3 Validate: `ruff check`, `ruff format --check`, `mypy` on the file if the project configures it; browser/axe all 11 states (13 axe scans) repeated 10 times with raw files; relevant API tests; `node --check`.
* [ ] P4 Changes record, one Review, final state, evidence commit, hash manifest, handoff.

## Success criteria

* Every repeated run exits 0 with all expected state lines and the completion marker; any failure is recorded and stops (no retry-to-pass).
* Failed baseline and recapture logs are kept; manifest `sha256sum -c` passes.

## Out of scope

Product code, full matrix, SQL, Azure, model calls, deploy, push, PR, board, rebase, reset, stash.

## Stop rule

A failure with a cause outside this check is recorded and stops; it is not corrected here without authorisation.
