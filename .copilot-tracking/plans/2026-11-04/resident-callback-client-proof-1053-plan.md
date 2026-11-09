---
title: Plan - client-side proof for hidden callback form (#1053)
ms.date: 2026-11-04
---

* Add `src/api/tests/test_resident_callbacks_page.py`: run the unchanged `demo.js` in Node with a fake DOM, using a real `/demo/view` payload from the demo test server.
* Assert hidden state (no mount, no callback section, no booking link, read-only lede, explanatory help text) and the connected state (form mounted, lede offers it).
* Critique: executed once by the author; no conflicts. Validation tier: focused.

Details: [details](../details/2026-11-04-resident-callback-client-proof-1053-details.md)
