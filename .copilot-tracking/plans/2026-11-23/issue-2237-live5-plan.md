---
title: Plan issue 2237 live5
ms.date: 2026-11-23
---

* Phase 1: in `approve_retention_deletion`, catch `ValueError` and `TypeError` from `_trigger` and raise a plain ValueError (HTTP 400) saying nothing was deleted.
* Phase 2: regression test in `src/api/tests/test_document_controls.py` (memory and SQL stores).
* Phase 3: run test_document_controls, ruff, mypy. Tier FULL (src change); coordinator runs the gate.
* Deploy and live re-proof are out of scope (registry has no public access).
