---
title: Issue 130 details
ms.date: 2026-11-17
---

* Script collects `FormData`, drops blank values, converts `expected_version` to a number, omits `assisted_channel` unless the route is staff-recorded and `representative_ref` unless raised by a representative (mirrors `panels.js` builders).
* Success reloads the page; failure shows the server error in the feedback status region and re-enables the button.
* Out of scope: representative participation human evidence, OD-41/OD-42, #1818/#1641.
