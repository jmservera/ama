---
title: Issue 2186 plan 2026-11-26
description: Plan to treat rubric score files as receipt-inert
ms.date: 2026-11-26
---

* [x] Phase 1: add `.github/rubric/scores/` to `RECEIPT_INERT_PREFIXES`; in `moved_path_blocker` return "" for receipt-inert paths after the candidate-overlap check.
* [x] Phase 2: extend `test_full_receipt_survives_only_inert_main_moves` with the score files (allowed) and a rubric script (blocked).
* [x] Phase 3: run `tools.test_rpi_checks`, ruff, write research note, changes and review.

Details: [details](../../details/2026-11-26/issue-2186-live-details.md)
