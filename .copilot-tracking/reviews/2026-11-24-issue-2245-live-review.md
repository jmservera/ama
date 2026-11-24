---
title: Review for issue 2245 (2026-11-24 live run)
ms.date: 2026-11-24
---

Review executed once. Outcome: conformant with open owner-gated items.

* Scope: override predicate change, its tests, live probe evidence, note, index and log.
* Checked: the old code fails the updated test; the override needs both the dated owner token and the demo profile; the suspension record stays open; probe output holds no sign-in values (searched); no Azure change.
* Open (routed to later work): deploy a revision with the fix and re-probe for "Model calls: 1"; read the 2026-11-22 500 cause once Log Analytics access exists; map `ask` lock errors to 503 after a retry-safety review.
* Not run: `rpi-checks.py --all` (coordinator), hosted CI.
