---
title: Issue 110 device identity hardening plan
ms.date: 2026-11-14
---

Task: `110-device-identity-1848`. Critique executed once: compatible, no conflicts.

* [x] Phase 1: require canonical `YYYY-MM-DDTHH:MM:SSZ` ASCII `observed_at` in `verify_envelope` before slot parsing.
* [x] Phase 2: add unit cases for non-canonical timestamps and a null schema version in `test_iot_device_identity_schema.py`.
* [x] Phase 3: run ruff check, ruff format (line length 100) and focused tests; commit locally, no push.

Tier: focused (small non-gate change). No live Hub or SQL work.
