<!-- markdownlint-disable-file -->
# Plan: issue 1292 extension E1 (2026-11-09)

Research: [research](../research/2026-11-09-priority-order-1292-e1-research.md). Details: [details](../details/2026-11-09-priority-order-1292-e1-details.md). Critique: [critique](2026-11-09-priority-order-1292-e1-critique.md). Owner-selected demo-targeted tier (modified and impacted tests, no blanket full gate); hosted CI and independent exact-head review remain mandatory. Extension cycle E1 of five owner-approved new cycles E1-E5 (after spent C5); four remain after this.

* [x] Phase 0: local ordinary `git merge origin/main` (no rebase, no force), recording the merged head and tree.
* [x] Phase 1: `_suspect_ranges` strict `rec_order_legacy` validation (absent vs present; object with positive integer `rows`; anything else returns the whole range).
* [x] Phase 2: `priorityPanel.ask` uses `mutationNeedsHistory` and a latched `checkHistory`/`pending`; no enabled creation control after a committed, uncertain or transport outcome.
* [x] Phase 3: regressions: C0 metadata matrix (SQLite and owned SQL Server); real HTTP committed outcome fed to the shipped `app.js` in the existing Node DOM harness; real lock-timeout `BEGIN` on SQL Server with a second connection and `@@TRANCOUNT`; affected C2/C4 edge classes admitted on SQL Server.
* [ ] Phase 4 (PARTIAL: local unit, API, ruff, mypy pass; owned SQL Server run BLOCKED by another lane's lock holder, not run): targeted validation on an owned disposable SQL Server (nonqueued flock), ruff and mypy as configured, API node harness tests, import provenance.
* [x] Phase 5: README sentence, records, one review, local commit, handoff.

Stop conditions: any failing selected test (not waivable); assertion weakened or broad catch added; SQL or lock unavailable (record blocked, keep visible); production cause outside this scope (return a separate draft). No push, PR, issue, board or merge.
