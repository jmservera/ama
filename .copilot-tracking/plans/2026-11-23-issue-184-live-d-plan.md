---
title: Issue 184 live plan d (2026-11-23)
description: Plan and one-pass critique for a wire-body secret allow-list regression
ms.date: 2026-11-23
---

Tier: focused (test-only, no src change). Plan: add one test in `src/api/tests/test_iot_credential_hygiene.py` asserting every published body is a JSON object with no secret-named key and no repository secret pattern in any field. Run that module, ruff format and check.

Critique (executed once): the key-name regex could false-positive on legitimate fields; the test runs on actual payloads, so a failure is informative. Proceed. No live Azure change; live body proof stays unproven (network blocked, see bodyread note).
