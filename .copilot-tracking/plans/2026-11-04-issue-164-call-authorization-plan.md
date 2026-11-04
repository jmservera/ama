---
title: Issue 164 call authorization plan
ms.date: 2026-11-04
---

* Slice 1 (this PR): `call_authorization` pure guard in `chat_eval`, `actual_calls` field in enablement, tests, README, log.
* Later slices: held-out freeze check once owner supplies labels; human exercise protocol after consent, accessibility and privacy approval.
* Critique (single pass, self-run): fail closed on any missing, boolean, non-positive or exhausted limit; no implied spend authority; no model call added; task stays disabled. Applied directly.
* Details: [details](../details/2026-11-04-issue-164-call-authorization-details.md).
