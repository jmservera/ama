---
title: Issue 920 phase details
description: Step details for the expected-denial slice
ms.date: 2026-11-03
---

## Phase 1

* `server.py` `/api/me`: add `services = {photo: token present, law_alerts: law store loaded}`.

## Phase 2

* `web/app.js` `loadPhoto`: when `services.photo` is false, show the plain note, no request.
* `web/chat.js`: alerts panel shows the human-route note when `services.law_alerts` is false; the proposal panel treats contractors like administrators; regulatory chat status is treated as role-denied for a trusted-proxy user without `regulatory_chat`. Manual routes remain in each message.

## Phase 3

* `tests/test_expected_denials.py` and `checks/expected_denials_browser_check.py`.

## Out of scope

* Accessibility acceptance, live deployment evidence.
