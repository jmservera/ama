---
title: Review for #188 slice 1
ms.date: 2026-11-05
---

* Review executed once inline. Outcome: conformant for the slice; issue incomplete.
* Checked: replay returns the prior receipt; same-slot value change is `IDENTITY_CONFLICT`; older slot is `OUT_OF_ORDER`; every reject creates an Open data-quality exception with the manual route; consent, window, mapping and calibration controls still gate live rows; backfill rows unchanged (existing tests pass).
* Residual risks routed to later work: SQL Server path untested here (the `schema_version` ALTER widens to 19 characters); sunlight is not in a queryable column; `OUT_OF_ORDER` rejects a late live slot rather than back-filling it (existing policy).
* Acceptance criteria: (1) queryable together per home: partly proven on SQLite via `observed_series`, not on live Azure; (2) no discontinuity beyond tolerance: unmet; (3) re-running a window is idempotent: proven for live rows on SQLite, not on SQL Server. Use Refs #188.
* [ ] Human approval left unchecked.
