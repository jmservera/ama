---
title: Research - status check for callback 503 (#1053)
ms.date: 2026-11-04
---

* Disposition: reused. Merged PRs already delivered both code slices: #1070 (server reports `callbacks_available`; page hides form, booking link and lede; 503 stays by design) and #1186 (Node/fake-DOM test proving `demo.js` hiding and connected state).
* Re-run at origin/main c45be7e19: `test_resident_callbacks_page.py` 2 OK.
* Remaining: connect a synthetic agenda in the cloud composition. `__main__.py` reads `ZF_DEMO_AGENDA_PATH`; wiring it is infra/deployment work needing the coordinator's gate. Live confirmation on ca-resident-demo needs a deploy and a signed-in walkthrough.
* Planning readiness: no ungated code slice remains.
