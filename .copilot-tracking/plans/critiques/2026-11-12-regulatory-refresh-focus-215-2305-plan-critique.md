---
title: Plan critique - restore keyboard focus after Refresh alerts (#215-R1)
description: Single independent pre-edit critique and dispositions
ms.date: 2026-11-12
ms.topic: reference
---

## Execution

Executed once before any source edit by an independent read-only rubber-duck agent that read the research, plan, details, `chat.js`, `async-action.js` and the harness. Not rerun. Verdict: Revise. No conflict with a confirmed user decision; no user decision needed.

## Findings and dispositions

1. Blocking: the click handler is wrapped by `AsyncAction.run` (via `h()` in `app.js`). In the synchronous law-store-unloaded branch `load()` re-enables the button, then the wrapper sees an enabled button and disables it again, blurring a restored focus. Accepted: the branch yields one microtask while still disabled before the shared finish, so the wrapper never owns the disabled state; the test checks focus after the wrapper settles.
2. Blocking: setting `fixture.app.law = None` exercises the API error, not the cached `me.services.law_alerts === false` branch. Accepted: test both separately and restore capability and fixture in `finally`.
3. Blocking: a blocking `page.route` handler can deadlock the sync API and an unchanged status can satisfy an assertion early. Accepted: capture the route without continuing it, assert the request and loading state, move focus, then continue the captured route and wait for the completed status; unroute in `finally`; loopback only.
4. Non-blocking: no-stealing coverage incomplete. Accepted: also test a pointer press on non-focusable content, and assert the initial `load()` never takes focus.

No WCAG conformance and no AC5 claim; confirmed.
