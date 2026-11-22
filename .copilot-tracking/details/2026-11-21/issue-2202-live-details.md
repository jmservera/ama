---
title: Issue 2202 plan details
ms.date: 2026-11-21
---

Phase 2: in `_sensor_consent`, on exception print `sensor consent write failed: <class>: <code>` to stderr (class name and the first exception argument only when it is a short code string). Test: FakePort raising ConsumerError("SENSOR_SQL_UNAVAILABLE") yields 503 and stderr contains the code. Tier: full (src change); targeted tests, mypy, ruff only here.
