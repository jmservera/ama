---
title: Research for #943 value_claim_confirm re-confirm of a Booked claim
ms.date: 2026-11-04
---

* Task: fix/issue-943-followup, Refs #943 (review note from #905).
* Research disposition: executed (code read only).
* Prior delivery check: merged PR #905 introduced value claims; no merged PR addresses #943 (searched merged PRs for 943).
* Finding: `value_claim_confirm` in `src/core/src/zava_forward/core/governance.py` looked up the claim, checked only the different-person rule, then overwrote destination, reference and confirmer. A Booked claim could be rebooked to another destination and the original confirmer overwritten.
* Existing refusal path: `ValueError` with a plain-language reason (the API maps it to a 4xx message).
* Planning Readiness: Ready.
