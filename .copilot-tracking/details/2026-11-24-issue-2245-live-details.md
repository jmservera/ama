---
title: Details for issue 2245 (2026-11-24 live run)
ms.date: 2026-11-24
---

Phase 1: `src/core/src/zava_forward/core/continuity.py` `demo_owner_override` returns `directed and env.get("ZF_DEPLOYMENT_PROFILE") == "demo"`; docstring updated. Tests in `src/core/tests/test_demo_owner_override.py`: exact value plus demo profile; production env without the profile stays held; production env with the profile lifts the hold.
