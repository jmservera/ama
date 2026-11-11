---
title: Issue 80 capacity page export controls, critique
description: One final-candidate critique of the plan and details, with direct dispositions
ms.date: 2026-11-10
---

Executed once on the final candidate plan and details, before implementation. Native author critique, not independent review. Verdict: proceed with the direct amendments below. No finding conflicts with a confirmed Root decision and none needs a user decision.

| # | Finding | Evidence | Disposition |
| --- | --- | --- | --- |
| 1 | The details claim a null child would print "null" through `replaceChildren`. Wrong: `show` filters `n && n.nodeType`, and `h` skips `null`/`false`. The real hazard is a numeric `0`, which `h` would render as text "0" if `total && link` were used. | `app.js:21-35`, `app.js:99-106` | Amend: use `pkgPage.total ? exportLink(...) : null`, no spread, no `&&`. Details corrected below. |
| 2 | The existing check's `reads` filter matches by exact path, so a CSV GET (`/api/packages.csv`) cannot be mistaken for the `/api/packages` read in `verify_route`. The `failures` listener only flags status >= 400, so a 200 download is clean. | `capacity_browser_check.py` `verify_route`, listeners | Accepted: place the download assertions after the seeded scan, before the manager-route loop, and `reads.clear()` is already done by each later route. |
| 3 | Unpaged JSON for count comparison: `GET /api/packages` without `limit` returns a bare list, not the envelope. | `server.py` handler | Amend details: compare CSV data-row count with `len(response.json())` of the unpaged call, using `context.request.get`. |
| 4 | Parsing CSV by line count is fragile if a cell holds a newline. | `list_export.to_csv` | Amend: parse with the `csv` module and count rows, not lines. |
| 5 | Seed holds one package and one work order, so the "not only this page" breadth cannot be exercised by data. | seed id `PKG-SYN-001`, `WO-SYN-0001` | Accept and disclose. The label text is asserted; breadth parity is a source-contract claim (unpaged `list_rows`), not a runtime proof here. No new fixture code. |
| 6 | The check clears the environment and builds its own tempdir store, so no `ZF_DATA` assertion applies. | `main()` | Accept. Record that the store path is the check's own `tempfile` directory and that default data is never opened. |
| 7 | The error state is not asserted in the browser. | view throws before render | Accept and disclose as a source-by-construction claim, not a runtime proof. |
| 8 | Accessible name: two links with the same text would be ambiguous. | design review | Already handled: distinct visible labels. |

## Amended details (supersedes Phase 1 and Phase 2 wording of the details file)

* Phase 1: use `pkgPage.total ? exportLink(...) : null` and `orderPage.total ? exportLink(...) : null` as plain children.
* Phase 2: CSV row count via the `csv` module against `len()` of the unpaged JSON list; download assertions go after the seeded axe scan.

Critique is not repeated for this task.
