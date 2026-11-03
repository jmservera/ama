---
title: Issue 217 metering record details
date: 2026-11-03
---

* Phase 1: `src/core/src/zava_forward/core/regulatory_privacy.py` gains `METERING_FIELDS` and `metering_record`. Unknown keys, free text, bad counts, naive times and non chat/check surfaces raise ValueError. No storage, no model call, no cost.
* Phase 2: tests in `src/core/tests/test_regulatory_privacy.py`.
