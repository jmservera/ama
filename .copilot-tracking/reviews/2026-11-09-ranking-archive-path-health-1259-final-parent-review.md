---
title: Issue 1259 final parent integration review
description: Single author review of the final parent integration, with routing; independent exact-head assessment remains required
ms.date: 2026-11-09
---

## Execution

One Review, executed 2026-11-09 by the author agent after implementation; it is not an independent assessment. Boundary: merge commit `13381ea25a24bd1b1ea72e2ed282d550009e1b5c` against parent `9b1e2567c2d0a2173b562103cd27508f75181526` and frozen child `5ed86a6a7f799aa7c2bc574f8f101a56fb30fdda`. Not repeated for this task.

## Outcome: Conformant to the plan, with residual (inherited and one child-owned) findings

* Plan order held: research, plan, details and critique were committed (`04cb3159`) before the merge; validation followed the merge.
* Merge is ordinary, conflict-free, and adds exactly the parent's source delta (patch-id equal); ranking adapter, publication and runner blobs equal the frozen child; no parent source touched; no source fix made.
* Targeted tests all pass: core 146 and 398 (158 SQL/Azure opt-in skips), API 67 and 31.

## Findings

| ID | Severity | Finding | Routing |
| --- | --- | --- | --- |
| R-1 | Medium, inherited | API `ruff check` 10 errors and `ruff format --check` failure in `test_ranking_publication_wiring.py`, identical at parent; parent C5 budget zero | Parent authority; not cured or waived here; parent publication blocked until resolved |
| R-2 | Medium, inherited | Core `mypy` 84 errors (parent) in `test_ranking_archive_blob.py` and `ranking_blob_fixture.py`; API mypy 13 errors identical to parent | Parent authority |
| R-3 | Low, child-owned | Child's added test in `test_ranking_archive_blob.py` adds 2 strict-mypy errors (missing `-> None`, untyped fixture call) to the already failing file | Later scoped cycle (cycle 2 of 5, four remain) together with, or after, R-2; no source change here |
| R-4 | Low, inherited | Trailing whitespace in main's committed `server-version.txt` | Inherited from PR 1308 |
| R-5 | Info | Earlier Azurite evidence applies to unchanged adapter/runner blobs only, emulator evidence, not Azure | Any future source or transport change needs explicitly scoped new validation |
| R-6 | Info | Duplicate NextMarker remains independently classified speculative | No owner blocker invented |

No finding requires a current-task fix. A failing selected test: none. Independent exact-head review, hosted CI, SQL-service behaviour, Azure acceptance and human approval remain unmet.
