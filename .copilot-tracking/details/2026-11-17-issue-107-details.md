---
title: Issue 107 plan details
ms.date: 2026-11-17
---

P1 touches only `src/api/tests/test_assistant_restart_non_replenishment.py`. Provider fields are patched on the counting double (`provider`, `endpoint`, `fast`); data via `REGISTRY[CAP]["categories"]`; provenance via `assistants.PROVENANCE`. Existing assertions (denied dispatch, no calls, revoked, denied after restart, quarantined late completion, no domain write) apply unchanged. P3 is docs only and states the old-image and real-AI criteria remain unproven.
