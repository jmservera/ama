---
title: Details - client-side proof for hidden callback form (#1053)
ms.date: 2026-11-04
---

* Harness: Node `vm` runs `demo.js`; `fetch` is stubbed with `/demo/session` (signed in) and `/demo/view` (real payload, `callbacks_available` toggled).
* Skips when Node is absent. No source change, no AI path, no consent change.
