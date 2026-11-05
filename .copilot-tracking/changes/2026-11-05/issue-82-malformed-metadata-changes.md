---
title: Issue 82 malformed quality metadata changes (2026-11-05, correction)
ms.date: 2026-11-05
---

Prior commits (8cdb1f676, 776502686, e4bc3266d, merge 9c48d0b44) and the original full receipt `/tmp/g82-ar1-1105/receipt.json` (SHA256 c3c51a40...) are preserved and now historical for this correction.

* `quality.py` `evidence_gaps`: every item must be a dict with a string label and `checklist` must be absent or a string; otherwise the record is unreadable (None, so the existing Unknown gate and the approved audited replacement apply). Unrecognised checklist strings keep the existing measure fallback. No broad catch.
* `test_quality_procurement.py` `Flows` (inherited by `JsonFlows`, `SqlFlows` and, in the maintained SQL group, `MssqlProcurement`): `corrupt_stored` persists and reopens corruption; tests for unhashable label, unhashable checklist (GateError, record unchanged, replacement supersedes with originals kept, independent acceptance) and the unrecognised-checklist control.

## RED then GREEN

* RED (before source change), `unittest -k unhashable -k unrecognised_checklist` on `JsonFlows` and `SqlFlows` (SQLite): 6 tests, 4 errors (`TypeError: unhashable type: 'list'` and `'dict'`), control passed.
* GREEN: `test_gates`, `JsonFlows`, `SqlFlows`, `HandoverBlockersTest`, `JsonHazardReferral`, `SqlHazardReferral`: 177 tests OK, 1 skipped; exit 0.
* `ruff check --no-cache .` clean; `ruff format --no-cache --check .` 213 files already formatted; mypy (cache /tmp/ama82-metadata-mypy) no issues in 266 files. Bytecode disabled; worktree had no ignored files.
* Not run: SQL Server (`MssqlProcurement`), full gate, browser. SQLite is not a SQL Server observation.
* Full gate, new receipt and independent exact-head assessment pending. Refs #82 only.
