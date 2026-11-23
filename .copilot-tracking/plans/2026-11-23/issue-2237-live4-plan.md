---
title: Plan issue 2237 live4
ms.date: 2026-11-23
---

* Phase 1: in `retention_due`, wrap trigger parsing per document; on `ValueError` or `TypeError` emit a row with `trigger=None`, `due=None`, status `needs review: trigger date unreadable`; continue.
* Phase 2: add a regression test in `src/api/tests/test_document_controls.py` (one case with `retention_trigger="not-a-date"` plus a normal due case; the listing returns both, nothing deleted).
* Phase 3: run test_document_controls, mypy, ruff. Tier FULL boundary noted: src change, but the gate is run by the coordinator.

## Critique (one pass, verdict proceed)

* Skipping unreadable records silently would hide retention duty: rejected; surface as needs-review row.
* Sorting uses `r["due"]`; None breaks the sort. Apply: sort key uses `r["due"] or ""`.
* Approval of such a row must still fail closed: `approve_retention_deletion` already uses `_trigger` and would raise; out of scope, row is not approvable and noted.
