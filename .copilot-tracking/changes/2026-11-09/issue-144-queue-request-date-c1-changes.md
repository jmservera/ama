# Changes: issue 144 queue request-date correction C1 (2026-11-09)

Plan: [plan](../../plans/2026-11-09/issue-144-queue-request-date-c1-plan.md).

* `src/agents/src/zava_forward/agents/queue_azure.py`: `_call` adds a fresh `x-ms-date` (RFC 1123 UTC via `email.utils.formatdate(usegmt=True)`) on every request.
* `src/agents/tests/test_queue_azure.py`: `DateContractTransport` returns 403 without a parseable GMT date within 60 seconds of now; `RequestDateTests` cover receive, poison POST, ack and release (accepted), the transport refusing missing or stale dates, and a receive with the date stripped failing. Negative check: with the header stripped, the all-operations test errors (403 -> QueueError); with the fix 24 queue tests pass.
* Operation order: originals persisted, research, plan/details, then source/test edits, then checks.
