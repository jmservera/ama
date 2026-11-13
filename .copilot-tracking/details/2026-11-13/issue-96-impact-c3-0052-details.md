---
title: Issue 96 impact correction C3 details
description: Phase details for the role-screen POST and timer contract corrections
ms.date: 2026-11-13
---

## Critique amendment (CR-1 to CR-3, see the critique artifact)

The guards below are strengthened before implementation: exact full `path` assignment and exact full `fetch(...)` call text, single `fetch` and `method` tokens, no other transports, all `api(` sites with `undefined` options, balanced-parenthesis `setTimeout` call extraction with exact allowed calls, `if (hadFocus)` prefix and alias rejection, each with negative fixtures. The substring rules in the sections below are superseded where stricter.

## Phase 3 details

### test_role_screens.py

Replace `assertNotIn('"POST"', source)` in `test_host_reads_existing_scoped_endpoints_without_post` (renamed `test_host_reads_scoped_endpoints_and_posts_only_the_read_only_saved_copy_check`) with:

* exactly one `fetch(` call, whose target is `path`; exactly one `method: "POST"`; no PUT, PATCH or DELETE method literal;
* that POST lies inside `function fundingSavedCopyCheck(`, whose `path` ends in `/held-export/freshness`, with the `X-ZF-CSRF` header and raw `body: text`;
* every `api(` call site passes `undefined` options (so the shared helper is never used to mutate);
* keep the existing endpoint and `innerHTML` assertions.

Add a small regression test over a pure helper `_mutating_sites(source)` showing a second POST, a PUT, a `fetch` to another path and an `api(path, {method...})` call are each reported while the real source reports only the one allowed site.

### test_role_screens_conformance.py

Replace the single-timer equality with the exact allowed list: the revoke timer and the exact focus-restoration timer (guarded by `button.isConnected`, `!button.disabled` and `document.activeElement === document.body`, delay `0`), and require it to sit under `if (hadFocus)`. Existing bans on `setInterval`, `requestAnimationFrame`, `.animate(`, and `animation` or `transition` in screen CSS stay. Add a regression test over helper `_unexpected_timers(source)` showing a delayed class toggle, an unguarded focus timer and a 300 ms animation timer are rejected.
