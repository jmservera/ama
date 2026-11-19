# Issue 154 live round 3 research

Disposition: executed (extends rounds 1 and 2 in docs/reference/research/issue-154-live-*.md).
Open criterion (only unticked item): "No live resident contact; designs are validated through the usability programme before any use".
Known gaps from round 2: 5a had no network trace; 5b needs moderated sessions (SA-010).
Plan: Playwright network trace of the resident showcase (signed in), Azure CLI listing of messaging resources in rg ama, re-run focused local tests, retained raw outputs. Criteria 1-4 are ticked; they stay as recorded in round 2.
Planning Readiness: Ready.

## Findings (executed 2026-11-18)

* Evidence dir `.copilot-tracking/evidence/2026-11-18/issue-154-live-r3/`: azure-messaging-check-raw.txt (no Communication/Email/SendGrid/Logic/NotificationHubs resource in rg ama; resident app env var names show no messaging config), network-trace-raw.json (9 requests, single host, only non-GET is POST /demo/login), local-tests-raw.txt (53 tests OK), outbound-search-raw.txt (only the funding boundary test names such libraries).
* Correction to round 1: the signed-in resident page has one textarea, the assistant question box from `chat-widget.js`; round 1 said no free-text control. It was not submitted (no real-AI action).
* 5b unchanged: needs moderated sessions and SA-010; not provable for the demo.
