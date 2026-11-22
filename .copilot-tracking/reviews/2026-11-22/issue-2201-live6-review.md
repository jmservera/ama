---
title: Issue 2201 live6 review
ms.date: 2026-11-22
---

Execution: once, after implementation. Outcome: conformant with routed open work. Boundary: the evidence note, index paragraph, log entry and evidence folder.

* Claims checked against `receiver-executions.json`, `simulator-executions.json`, `failure-lines-since-10.json` and `probe-readings.json`; times and counts match.
* No secrets in the evidence; probe output holds only case ids, counts and timestamps.
* Routed: log the exception class in the `IOT_CALLBACK_FAILED` handler (`iot_stream.py`), full tier; recheck the 15:30 run.
* Witness qualification: implement-start reported a dirty tree because the note was written before the call; no source file changed.
