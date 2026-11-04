---
title: Details for #943
ms.date: 2026-11-04
---

* `governance.py`: add `CAPACITY_ONLY` constant; reuse it in `value_claim_record`; raise `ValueError` in `value_claim_confirm` when `claim["status"] != CAPACITY_ONLY`.
* `tests/test_governance.py`: second confirm on a Booked claim raises `ValueError` matching "already Booked"; claim record unchanged.
