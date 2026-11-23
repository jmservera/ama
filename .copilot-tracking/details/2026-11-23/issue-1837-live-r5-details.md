---
title: Details issue 1837 live r5 2026-11-23
ms.date: 2026-11-23
---

Tier: focused (test file only; no workflow, dependency, Dockerfile, gate or src change). Test uses `patch.object(self.app.provider, "name", "trusted-proxy")` because the shared-password provider does not enforce `X-ZF-CSRF` (server.py).
