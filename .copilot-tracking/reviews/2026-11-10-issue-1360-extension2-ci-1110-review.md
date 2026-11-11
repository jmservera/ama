---
title: Issue 1360 extension 2 CI regression review
ms.date: 2026-11-10
task_id: 1360-extension2-ci-1110
---

Self-run review, executed once, not independent. Boundary: the E2 source, tests and evidence.

* Outcome: conformant for the reported hosted Core regression; MSSQL unverified.
* Resolved: shared `save` error contract (original `OSError`/`ValueError`/chaining for hazard, quality, resident callers) restored; Importer committed truth and idempotence retained; marker leak guarded.
* Open and routed: MSSQL affected selectors blocked (no owned fixture), hosted CI rerun and Root independent exact-head review pending. Core `sqlstore.py` format failure is pre-existing. Other callers of `save` with OSError at the post-commit refresh stay uncommitted-ambiguous by their established contracts; not altered.
* No E3 required.
