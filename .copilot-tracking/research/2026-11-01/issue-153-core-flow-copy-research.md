---
title: Issue 153 core-flow copy and error contract research
date: 2026-11-01
task_slug: issue-153-core-flow-copy
---

Research disposition: executed (reused prior 2026-10-18 and 2026-10-27 audit evidence). Planning Readiness: Ready.

## Evidence

* `docs/reference/research/ux/content-standard.md` "Open message findings" lists residual gaps. AC1 and AC4 are already ticked in the issue.
* `src/api/tests/test_content_standard.py` guards eight web files lexically. `role-screens.js`, `law.js`, `law.html` are inventoried but unguarded.
* `role-screens.js` lines 129, 177, 178 show "gate" in visible copy.
* `app.js` `api()` falls back to "Something went wrong." with no reason, owner or next action. `ops.js` line 253 compares to that literal.
* `store.py` `ranking_snapshot()` shows "ranking snapshot" in a visible manager-only error.
* `law.js` `fail()` forwards the raw message.

## Scope decision (tight slice)

* Remove "gate" from role-screens copy and add role-screens.js, law.js, law.html to the guard.
* Replace the generic fallback with a reason, owner, next action message (read failure vs unknown write outcome stays distinct: check recorded history before repeating).
* Plain wording for the ranking error with owner and next action.

## Out of scope (stays unmet)

* Universal coverage of every dynamic or server error.
* Named human review of resident wording (Juan Manuel Servera appointed; review not run).
* Comprehension and accessibility acceptance testing.
* "Keep on hold" stored finance value.
