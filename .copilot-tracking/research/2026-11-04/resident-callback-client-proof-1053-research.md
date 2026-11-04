---
title: Research - client-side proof for hidden callback form (#1053)
ms.date: 2026-11-04
---

* Disposition: reused. PR #1070 (merged 2026-11-04) delivered slice 1: the server reports `callbacks_available`, the page hides the form, booking link and lede when no agenda is set; the 503 stays by design.
* Gap (issue comment): no test executes `web/demo.js`, so the client hiding was unproven.
* Not pursued: connecting a cloud agenda. `__main__.py` reads `ZF_DEMO_AGENDA_PATH`; wiring it needs infra/deployment changes and the coordinator's gate.
* Planning readiness: Ready for a test-only slice.
