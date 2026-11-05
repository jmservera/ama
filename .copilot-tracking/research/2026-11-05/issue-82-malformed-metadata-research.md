---
title: Issue 82 malformed quality metadata research (2026-11-05, correction)
ms.date: 2026-11-05
---

* Disposition: `reused` plus targeted re-read. Start HEAD 9c48d0b44, tree b1c1a7fee, main bb3a3b03c, parent feat/controlled-lifecycle-integration-81 at ead177ef9. No branch moves.
* Independent exact-head finding (evidence: session 77149bdf files/82-independent-malformed-metadata-probe.log): stored `items[0]["label"] = []` makes `accept_quality` and the approved replacement raise `TypeError: unhashable type: 'list'`; `rec["checklist"] = {}` raises `unhashable type: 'dict'`. Cause: `evidence_gaps` builds a dict keyed by unchecked `label` and does `CHECKLISTS.get(rec.get("checklist"))` with an unchecked value.
* Classification: functional crash on corrupt synthetic records, not an approval bypass. The original full receipt c3c51a40... passed but is not a pass for this defect and is historical for any new commit.
* Test location: `Flows` in `src/core/tests/test_quality_procurement.py` is inherited by `JsonFlows`, `SqlFlows` (SQLite) and `api/tests/test_mssqlstore.MssqlProcurement`, so one shared regression covers all backends when the SQL Server group runs. Corruption must be persisted with `save()` under the store lock and reopened through `self.reopen()`; mutating only an in-memory cache is not stored corruption.
* Existing behaviour to keep: unknown checklist name falls back to `checklist_for(measure)` (supported fallback for absent or unrecognised string); valid records unchanged; role, safety, resident and error ordering unchanged.
* Planning Readiness: Ready. No MSSQL execution claimed in this light continuation.
