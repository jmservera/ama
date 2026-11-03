---
title: "Research: #432 resident topic adapter discards provider usage"
ms.date: 2026-11-03
---

Disposition: reused (2026-11-02 owner-gate and 2026-11-03 re-check research) plus a direct read of provider call sites on main d5ff35f16. Planning Readiness: Ready for one source-only slice.

* Merged for #432: #602, #660, #709, #765, #790, #832. Open PRs #911 and #915 are other issues and do not touch the resident adapter.
* Call sites reading provider usage: `core/ai.py` (validated and metered), `agents/chat.py` and `dispatch.py` (validated), `api/resident_demo/aoai.py` (validated and accounted). One call site discards usage: `AzureTopicProvider.select` in `api/resident_demo/assistant.py` parses the reply and never reads `usage`. This matches the issue statement that some paths discard provider usage (criterion 1).
* The adapter is disabled by default and expires 2026-11-01 (owner-controlled constant); it has no ledger by design. A slice therefore adds an optional counts-only sink, not a ledger, price, budget or activation.
* Still blocked and unchanged: criteria 2 (live clause), 3, 5, 6, 8, 9 (OD-51, spend authority, attributable Azure billing, live identity admission, protected slide 52). Criteria 4 and 7 stay ticked.
* The slice touches no security, infrastructure, SQL or deployment code: focused tier applies.
