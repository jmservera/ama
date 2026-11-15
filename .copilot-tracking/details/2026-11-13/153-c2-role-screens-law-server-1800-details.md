---
title: Issue 153 C2 details
ms.date: 2026-11-13
---

## Phase 1 wording (all existing substrings kept)

* role-screens.js unavailable: "This screen is not installed for your signed-in role. Your access has not changed. Owner: your team manager. Next action: go back to specialist screens and open one that is listed for you."
* role-screens.js paging: "That page could not be loaded. The rows shown are unchanged. Owner: application support. Next action: try again, or open a case from the case list."
* law.js missing file: "Required law viewer file did not load: /async-action.js. Owner: application support. Next action: reload this page to try again, and contact application support if it continues." Test matches only the prefix up to the filename.
* server.py 500: "The service hit an unexpected error. Owner: application support. Next action: try again, and if it continues report the time of the failure to application support."

## Phase 2 tests

One test: role-screens.js and law.js notices have Owner before Next action in order, with reason before Owner; server.py 500 text likewise.

## Critique dispositions (rubber-duck, Revise, applied directly)

* PC-001: keep "Try again" capitalised in the paging text; add programme_paging_browser_check to validation if playwright runs.
* PC-002: also add Owner and Next action to role-screens.js stage-list "not installed" line (~523), finance queue unknown (~1362) and Invalid file status (~1390); keep the substring asserted in test_programme_screen.
* PC-003: law.js fail appends its own Owner and Next action only when the server message has none; test with a message that already carries them.
