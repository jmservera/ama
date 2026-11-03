---
title: Issue 216 round 3 details
ms.date: 2026-11-03
---

* Agreement fields: owner, independent_grader (different person), agreed_on, case_set_sha256, min_graded_cases, min_adversarial_cases, min_rates per gate.
* Outcomes per gate: `unset_pending_owner_agreement`, `owner_threshold_met`, `owner_threshold_not_met`; `overall_pass` is always None.
* Manual path: staff keep the card and provision-link route; nothing here uses a model.
