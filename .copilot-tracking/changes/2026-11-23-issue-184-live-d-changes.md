---
title: Issue 184 live changes d
description: Changes record and per-criterion table for issue 184, 2026-11-23
ms.date: 2026-11-23
---

Change: `src/api/tests/test_iot_credential_hygiene.py` gains `test_wire_bodies_hold_only_plain_fields_and_match_no_secret_pattern`, which publishes through the fake SDK and asserts each wire body is a JSON object with no secret-named key and no repository secret pattern in any field. Test-only; no src change, so the focused tier applies. No Azure change; nothing to delete; no credential read.

Validation: `tests.test_iot_credential_hygiene` and `tests.test_iot_stream` (64 tests) OK; `ruff format --check` and `ruff check` clean on the file; `mypy` in `src/api` clean (373 files).

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| All child stories closed or deferred | Proven for the demo | #185 to #189 closed as completed (research notes of 2026-11-19 and the 2026-11-23 re-check). Not re-queried this run (API rate limit on GraphQL; REST issue read succeeded) |
| Simulator never connects to, discovers or represents installed real devices | Proven for the demo, constructed plus live | `test_iot_stream.py` passes here; live `SYN-` ids in the [2026-11-23 re-check](../../docs/reference/research/issue-184-live-recheck-2026-11-23.md). Hub identity registry not enumerable (401002) |
| No device key or connection string in source, logs or telemetry | Source and logs proven; telemetry strengthened (constructed), live bodies unproven | New regression plus existing scan. Live Event Hubs bodies unreadable: public access and local auth disabled; enabling is an estate change not authorised ([body-read note](../../docs/reference/research/issue-184-live-bodyread-2026-11-23.md)) |
