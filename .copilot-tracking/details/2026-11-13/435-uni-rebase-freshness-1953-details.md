---
title: 435 unified rebase details
ms.date: 2026-11-13
---

## Phase details

* Rebase onto `dab0b0893`, then cherry-pick `e1834dfc6`, `142824c30`, `6124aee61` in order.
* `python3 src/core/src/zava_forward/core/synthetic/cutover_audit.py --write`, then no-flag check.
* Verifier run writes `...-report.json`; report result honestly.
* Validation: `test_cutover_audit`, `docs/capstone/source/validation.json` hash, relative links, secret scrub.
