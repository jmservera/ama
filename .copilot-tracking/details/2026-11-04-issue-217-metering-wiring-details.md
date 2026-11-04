---
title: Issue 217 metering wiring details
date: 2026-11-04
---

* Phase 1: add `usage_metering(usage, record_id)` to `src/core/src/zava_forward/core/regulatory_usage.py`, mapping task to surface chat or check.
* Phase 2: call it in `summarize` after the existing exact-shape check.
* Phase 3: tests in `src/core/tests/test_regulatory_usage.py` for both surfaces, content-free output and rejection of non-identifier versions.
* Phase 4: log entry in docs/reference/log.md.
