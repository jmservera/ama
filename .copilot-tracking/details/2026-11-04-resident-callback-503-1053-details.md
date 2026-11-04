---
title: Details - resident callback 503 (#1053)
ms.date: 2026-11-04
---

* `app.py`: `CALLBACKS_OFF` text; `view["callbacks_available"] = self.agenda is not None`; chat override when `topic == "appointments"` and no agenda.
* `web/demo.js`: `callbackLede` appended only when available; form mount, "Book a synthetic callback" link and "form above" wording conditional; nav label "Help" when off; neutral signed-out lede.
* `web/index.html`: lede no longer promises booking.
* Tests: `test_resident_demo_api.py` (key set, false by default), `test_resident_chat_api.py` (true with agenda; false and no search offer without).
