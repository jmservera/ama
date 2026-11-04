---
title: "Research: #432 resident adapter ledger join"
ms.date: 2026-11-04
---

Disposition: reused (2026-11-04 call-site inventory research and review) plus a direct read of main fc92d53c4 and merged PR list. Planning Readiness: Ready.

* Merged for #432: #602, #660, #709, #765, #790, #832, #936, #977, #1051. Nothing is open for the issue. The inventory test (#1051) names `resident_demo/assistant.py` as counts-only and `aoai.py` as own accounting, so criterion 1 ("each model call is joined") is unmet for them.
* The resident adapter has host callbacks `reserve` (bool) and `record_usage` (success only, counts only). It has no callback for failure outcomes, the returned model, or a post-credential dispatch recheck, which the ledger needs (`reserve`, `dispatch_check`, `complete`).
* Ledger behaviour to reuse: unknown authority, price, liability or exhausted budget raises `DispatchHeld` and an owned `workflow-only` alert; completion without a cached-token count holds as `liability-unknown` and is never estimated.
* Smallest coherent slice: an opt-in bridge that wires the adapter to the ledger, plus one outcome hook on the adapter. `aoai.py` stays on its own accounting (separate slice).
* Unchanged blockers: OD-51, spend authority, attributable Azure billing and tolerance, live identity admission, pitch placement (slide 52 protected).
* Focused tier applies: no security, infrastructure, SQL or deployment change; the adapter stays disabled by default and expired (2026-11-01).
