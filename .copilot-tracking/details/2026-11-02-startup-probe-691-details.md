---
title: Startup probe details for issue 691
description: Phase details
ms.date: 2026-11-02
---

* Phase 1 files: `infra/modules/containerapps.bicep`, `infra/resident-demo.bicep`.
* Phase 2 files: `src/api/src/zava_forward/api/web/app.js` (`fetchReadRetrying`, `startupFailure`, `SCRIPT_RETRY_DELAYS`).
* Phase 3 files: `infra/tests/test_bicep_policy.py`, `src/api/tests/test_workspace_scripts.py`.
