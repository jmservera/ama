---
title: Issue 96 impact correction C3 independent critique
description: Single independent critique of the C3 plan with direct dispositions
ms.date: 2026-11-13
---

## Execution

* Independent read-only rubber-duck context, executed once on plan commit `876fd74a8`. Verdict: Revise (3 blocking findings, all compatible with confirmed decisions, no user decision required, none rejected, no repeat critique).

## Findings and dispositions

* CR-1 Mutation detection underspecified (single quotes, variable method, helper aliases, other transports): accepted. The guard now counts the bare tokens `fetch` (exactly 1) and `method` (exactly 1), rejects `XMLHttpRequest`, `sendBeacon`, `WebSocket`, `EventSource`, requires every `api(` site to pass `undefined` options, and fails closed. Negative fixtures cover each form.
* CR-2 Allowed POST insufficiently bound: accepted. The guard requires the exact full `path` assignment, exactly one assignment of `path` and the exact full `fetch(path, { method: "POST", headers: {...}, body: text, signal })` call text, so a changed prefix, reassignment or options spread fails. Negative fixtures cover each.
* CR-3 Timer matching needs complete calls: accepted. A balanced-parenthesis scanner extracts each complete `setTimeout(...)` call; the set must equal the two exact allowed calls, the focus call must sit under `if (hadFocus) `, and the bare `setTimeout` token count must equal the parsed calls (rejecting aliases). Fixtures cover motion after `button.focus()`, string callbacks, non-literal and long delays, unguarded focus and a third timer.
