---
title: Issue 153 research, residual internal identifiers in demo-path copy
ms.date: 2026-11-17
---

## Disposition and readiness

Research disposition: executed. Planning Readiness: Ready. Tier: FOCUSED (web copy only, no Core, SQL, security or deployment).

## Evidence

* Issue 153 criteria 1 to 4 are ticked; criterion 5 (named human review of resident-facing wording) needs a named person and cannot be satisfied by this change.
* The existing guard `src/api/tests/test_content_standard.py` covers gate, hold, provenance, trace, snapshot and envelope in all served scripts and pages.
* Measurement: a scan of every prose-like string literal in `src/api/src/zava_forward/api/web/*.js` and `*.html` for snake_case identifiers found two person-visible leaks:
  * `app.js:2234` shows "data_steward and digital_operator are unassigned" on the operator exception queue blocked screen.
  * `role-screens.js:1353` shows "State: Action needed (roles_not_named)" on the exception register.
* The other matches were code expressions, not visible copy.
* Content standard rule violated: everyday words, no jargon, one name per thing; the glossary names "data steward" and "digital operator" with spaces in adjacent copy.

## Selected scope

Reword the two strings, add a lexical regression guard for snake_case identifiers in prose literals, record a dated audit row in the content standard and the knowledge-base log. Excluded: criterion 5, resident wording, `ok` state label, Core, chat grounding (1818/1641).
