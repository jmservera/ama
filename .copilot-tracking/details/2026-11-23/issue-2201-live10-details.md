---
title: Issue 2201 live10 details
ms.date: 2026-11-23
---

Phase 1: in the generic `except Exception` of `main`, emit `error_type=` with the class name only. Phase 2: extend `ReceiverStartupTests.run_main` usage with a persistence that raises `RuntimeError("secret-sentinel")`.
