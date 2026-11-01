---
title: Resident chat learning review
ms.date: 2026-11-01
---

* Review execution: executed once (independent code-review agent on the uncommitted diff). Outcome: one Medium finding, fixed in this task; no open material findings.
* Finding: fallback could answer other-resident or act-for-me requests that used none of the blocked words (case ids, "see all cases", choose or reserve a slot, "is my case approved"). Fix: digits, record nouns without a first-person word, more boundary words; wording no longer says "yet". Added eight negative tests.
* Residual (follow-up): a name-only request such as "who is the officer for john smith" still gets the static fallback, which reveals nothing; consider a positive-signal allowlist if the learning summary shows misuse.
* Human review: DPO and Legal approval for real-resident use remains required (#163 deferred). Owner review of resident wording and no accessibility acceptance are claimed.
