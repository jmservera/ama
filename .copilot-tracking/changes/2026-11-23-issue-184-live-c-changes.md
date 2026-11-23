---
title: Issue 184 live run c changes
ms.date: 2026-11-23
---

Change: `src/api/tests/test_iot_credential_hygiene.py` gains `ReceiveLeakTests.test_refusals_never_echo_body_content`. Five hostile inbound bodies carrying a marker credential (truncated JSON, duplicate key, marker in a field, oversize, deep nesting) are refused by `decode` with stable codes; the marker, `SharedAccess` and `HostName=` never appear in the error string, repr or traceback. No src change; focused tier (test-only), no `rpi-checks` run.

Validation: `test_iot_credential_hygiene` and `test_iot_stream` 63 tests OK (before formatting) and 13 OK after; `ruff check` and `ruff format --isolated --line-length 100 --check` clean; `python3 -m mypy` in `src/api` clean (372 files). Hosted CI not observed (no push).

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| All child stories closed or deferred | Proven (demo) | #185 to #189 closed, see `docs/reference/research/issue-184-live-recheck-2026-11-23.md`; not re-queried this run (REST/GraphQL rate-limited at start) |
| Simulator never connects to, discovers or represents installed real devices | Proven (demo, constructed plus earlier live) | `test_iot_stream.py` binding refusals pass again; Hub identity registry not enumerable (401002) |
| No device key or connection string in source, logs or telemetry | Source and logs proven; live message bodies unproven | Publish-path and, new this run, receive-path refusal leak tests pass; Event Hubs is network-private so bodies were not read live |
