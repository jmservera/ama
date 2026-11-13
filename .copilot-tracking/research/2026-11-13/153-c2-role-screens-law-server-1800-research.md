---
title: Issue 153 C2 research, owner and next action in role-screens.js, law.js, server.py
ms.date: 2026-11-13
---

## Scope

Medium findings from the C1 independent review: notices without an `Owner:` clause at
`role-screens.js` (Screen unavailable, page load failure), `law.js` (missing-file notice)
and `server.py` (500 message). `app.js` is out of scope (open PR #1542).

## Evidence

* Research disposition: executed (direct read of the files and tests).
* Planning Readiness: Ready.
* `role-screens.js` "Screen unavailable" alert and the paging failure text lack Owner.
* `law.js` missing-file message names "contact application support" but has no `Owner:` clause.
* `server.py` 500 body has next action only.
* Substring expectations to keep: `could not be loaded` (programme_screen, programme_paging browser check),
  `not installed for your role. Your access has not changed.` (programme_screen), `not installed for your signed-in role`
  (exception_register_screen), `Screen unavailable` heading, `Required law viewer file did not load: /async-action.js`
  (workspace_scripts, loading_briefing check), `Law viewer unavailable`. No test asserts the server 500 wording.
* `test_content_standard.py` already lists both JS files in `AUDITED_FILES` for banned terms but does not assert
  Owner/Next action for these notices.

## Approach

Append plain `Owner: ... Next action: ...` clauses preserving every existing substring; add focused test
assertions for the three notices.
