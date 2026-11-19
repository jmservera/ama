# Issue 344 live pass 3: changes

No source code changed. Tier: FOCUSED (documentation and evidence only).

Files: docs/reference/research/public-browser-access-live-r3-2026-11-18.md (new), docs/reference/README.md (index row), docs/reference/log.md (entry), evidence under .copilot-tracking/evidence/2026-11-18/issue-344-live-r3/.

Live actions: read-only az show/list/logs, anonymous curl, one Playwright sign-in. No Azure resource created or changed; nothing to delete.

## Per-criterion table

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Public landing; Entra sign-in; protected pages gated; anonymous API 401 not a redirect | Partly proven: non-browser 401 proven; browser-style API calls get 302, unproven |
| 2 | Edge follows #143 | Already ticked; external Container Apps environment re-observed |
| 3 | /healthz public; anonymous API 401 | Proven for non-browser clients; same 302 caveat |
| 4 | SQL private, public access Disabled, no policy bypass | Proven for the demo server (Disabled, 0 firewall rules; exemptions 0 from pass 2, not re-run) |
| 5 | Parity with matrix, gaps filed | Partly proven: reachability 22/25 API routes; time/status 500 classed ProgrammingError; defect not filed (shared-system write) |
| 6 | Browser sign-in smoke | Already ticked; refreshed with test account |

## Validation

* Secret scan of evidence and note for both credential values: no match.
* Markdown link review and git diff review. No unit tests, mypy or ruff apply (no code).

## Correction recorded honestly

The first drafts of this pass's plan, details, critique, changes, review and state files were written under the names of the pass 1 files and overwrote them in the working tree. The pass 1 files were restored from HEAD before commit and this pass's artifacts were moved to `*-r3-*` names. Phase witness events seq 2 to 6 for 344-live were recorded against the pass 1 state path (`issue-344-live-state.json`) while it held this pass's content; the committed copy of that path is the unchanged pass 1 file, and this pass's state is `issue-344-live-r3-state.json`.
