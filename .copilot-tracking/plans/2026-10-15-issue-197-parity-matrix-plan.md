---
title: Issue 197 parity matrix plan
ms.date: 2026-10-15
---

* [x] Phase 1: inventory and import graph
* [x] Phase 2: review PRs 235 to 287 against issues; derive reopen list
* [x] Phase 3: author the matrix with layout, outcomes, migration order
* [x] Phase 4: index row, log entry, scripted file-coverage check, link review
* Critique: executed once on the final candidate (self-critique); applied directly: skip-reason wording corrected to match test guards; M1 line estimate and M2 test count corrected. No conflict with confirmed decisions.
* Details: `.copilot-tracking/details/2026-10-15-issue-197-parity-matrix-details.md`

## Fix iteration (PR #291 review)

* [x] Phase 5: merge `origin/main`, keep both log entries
* [x] Phase 6: rebase PR 287 wording, add three rows, recount, drop the hold action, map the 450 sandbox files as retire (S1)
* [x] Phase 7: align targets with ADR 0006, state deviations as amendments A1 to A5, remove draft wording and stale assumptions
* [x] Phase 8: record owner answers, rerun the coverage script, update README row and append a log entry
* Critique: executed once on the final candidate; compatible findings applied directly (browser checks to `api/checks`, `test_content_standard` to `api/tests`, `chat_fixture` to the agents test tree). No conflict with confirmed decisions.
