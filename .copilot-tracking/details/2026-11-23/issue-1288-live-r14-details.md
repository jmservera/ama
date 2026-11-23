---
title: Issue 1288 r14 details
date: 2026-11-23
---

* P1 test in `src/api/tests/test_quality_sensor_grounding.py`: run `ready()`, `scan()`, execute the proactive task, then `UPDATE sensor_reading` on one cited row to humidity 250, and read `service.detail`; expect `review_flag.status == "implausible-readings"` and `autonomous` false.
* P2 in `src/core/src/zava_forward/core/assistants.py` `review_flag`: when `observed` and no capture-time implausible entries, take `sensor_view.implausible` over the current capture's citation rows, keep entries whose `citation_key` is a cited key (`known`). Reuse the existing `implausible-readings` status, effect text and output fields. Limit: new impossible rows that are not cited stay covered by `newer_readings`.
* Risk: low; only downgrades an L4 flag, never upgrades. No gate, permission or release semantics change.
