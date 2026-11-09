# Details: issue 144 queue request-date correction C1 (2026-11-09)

* `src/agents/src/zava_forward/agents/queue_azure.py`: import `email.utils`; in `_call` add `"x-ms-date": email.utils.formatdate(usegmt=True)` to headers.
* `src/agents/tests/test_queue_azure.py`: add `DateContractTransport` that refuses (HTTP 400) any request lacking a parseable RFC 1123 GMT `x-ms-date` within 60 seconds of now, else replies from script. Tests: receive, poison POST, ack, release succeed with it; a transport that strips the date is refused (proves the check fails without the header); date is regenerated per call.
* Preserved untouched: token injection and per-call freshness, byte-bounded poison, pop receipts, no-redirect transport, fail-closed serve.
