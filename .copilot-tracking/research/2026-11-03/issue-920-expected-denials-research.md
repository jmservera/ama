---
title: Issue 920 research, expected 503/403 denials in the employee UI
description: Prior delivery check, response classification and slice choice for issue 920
ms.date: 2026-11-03
---

## Prior delivery

* PR #694 (Refs #691) worded expected 403/503 plainly and logs 5xx on the server.
  It did not stop the browser logging the failed requests.
* No merged PR claims #920. Research disposition: executed (local code read).

## Classification (criterion 1)

| Response | Class | Reason |
| --- | --- | --- |
| 503 `/api/account/photo` | Expected | No `X-MS-TOKEN-AAD-ACCESS-TOKEN`; token store off (`core/profile.py`). |
| 503 `/api/law/alerts` | Expected | `App.law` is `None`; rule checks unknown (`server.py` `rule_engine`). A raised engine fault also answers 503 and stays defective, logged by the server. |
| 403 `/api/assistants` | Expected | Role is not a staff role (Application Administrator, Contractor). |
| 403 `/api/chat/regulatory/status` | Expected | Trusted-proxy user lacks the separate `regulatory_chat` capability. |

## Finding

The browser prints "Failed to load resource" for any non-2xx fetch and
JavaScript cannot suppress it. The only way to keep the console quiet is not to
send a request whose denial the client can already predict. `/api/me` already
carries `auth_provider`, `rule_roles` and `contractor`; it lacked the photo and
law-store state.

## Planning readiness

Ready. Slice: add `services` to `/api/me`, skip predictable requests, show the
existing plain-language text, add a browser check. Not security, infrastructure,
SQL or deployment work (read-only status flags, no authorisation change; the
server still enforces every denial).
