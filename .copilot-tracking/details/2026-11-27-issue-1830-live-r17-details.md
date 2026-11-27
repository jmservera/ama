---
title: Issue 1830 live r17 details (2026-11-27)
ms.date: 2026-11-27
---

Phase 1: after the schema check in `load_receipt`, raise `TimingError(EXIT_INPUT, ...)` when `jobs` is not a positive int, `image_cache` is not a string, or `sealed` is not an aware ISO timestamp (use `aware_timestamp`). Phase 2: add a test that mutates each field of a valid fixture, re-seals the hash and expects exit 2 without a traceback.
