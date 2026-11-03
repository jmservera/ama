---
title: "Issue 163 retention purge plan (2026-11-03)"
ms.date: 2026-11-03
---
Research: [research](../research/2026-11-03-issue-163-retention-purge-research.md). Details: [details](../details/2026-11-03-issue-163-retention-purge-details.md)

* [x] Add `purge_threads` to the in-memory and SQL chat repositories.
* [x] Add `ChatPrivacy.purge_retention`, a no-op without a recorded period.
* [x] Add unit tests on both stores (no period, period applied, other users).
* [x] Update the demo approval record and append a log entry.
* [x] Focused validation: chat tests, ruff check, mypy.

Later slices (stacked, not in this PR): scheduled invocation (infrastructure, own review); DPO and Legal decisions for criteria 2 and 5.
Critique: executed once; verdict compatible. Advice to leave the period policy unchanged and keep it a no-op without a recorded period applied directly.
