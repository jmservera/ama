---
title: Issue 184 live run c research
ms.date: 2026-11-23
---

Research disposition: executed (opening). Planning Readiness: Ready.

* Issue #184 body (REST read; GraphQL rate-limited): all three acceptance criteria are ticked, so there is no unticked criterion. Owner-only items: none.
* Prior notes: `docs/reference/research/issue-184-live-recheck-2026-11-23.md` proves child stories, no real-device binding, source/log secret absence; the only unproven element is secret absence in live message bodies (Event Hubs is network-private, so not readable from the CLI).
* Code-satisfiable gap found: `test_iot_credential_hygiene.py` covers the publish path only. The receive path (`decode` in `src/api/src/zava_forward/api/iot_stream.py`) handles hostile or malformed bodies, and nothing asserts its refusals never echo body content (which could carry a credential) into error text.
* Planned action: add a focused test; no live Azure change is needed.
