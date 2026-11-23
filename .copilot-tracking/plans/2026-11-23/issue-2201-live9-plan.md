---
title: Issue 2201 live9 plan
ms.date: 2026-11-23
---

Full tier (src change). Details: `.copilot-tracking/details/2026-11-23/issue-2201-live9-details.md`.

* [ ] Add `receive_error_type` to `HubReceiver`; set in `on_error` (first wins) and the outer handler.
* [ ] Print it in `live_receiver.run_window`.
* [ ] Tests in `test_iot_stream.py` and `test_live_receiver_sql.py`; run unittest, mypy, ruff.
