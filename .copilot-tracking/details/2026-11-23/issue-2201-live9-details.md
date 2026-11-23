---
title: Issue 2201 live9 details
ms.date: 2026-11-23
---

* `iot_stream.py`: init `self.receive_error_type: str | None = None` beside `callback_error_type`; reset in `run`; `on_error` sets it from `type(error).__name__` if unset; outer `except Exception as error` sets it (if unset) before raising `IOT_RECEIVE_FAILED`.
* `live_receiver.py`: in the `except StreamError` block print `receive_error_type=` when present.
* Tests: fake `receive` calling `on_error`; `run_window` print via a fake receiver.
