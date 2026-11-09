---
title: "Research: #432 resident advisor (aoai.py) ledger join"
ms.date: 2026-11-04
---

Disposition: reused (2026-11-04 resident ledger join research and review) plus a direct read of main 1f274ba48, issue comments and the merged PR list. Planning Readiness: Ready.

* Merged for #432: #602, #660, #709, #765, #790, #832, #936, #977, #1051, #1121. Nothing is open for the issue. #1121 joined the topic adapter (`assistant.py`) through `ledger_meter.py` and routed `aoai.py` as the next stacked slice.
* `aoai.py` (`AzureAdvisor`, guidance and free-question paths) keeps its own SQL per-resident accounting (`reserve`, `complete`) and has no ledger join, so criterion 1 ("each model call is joined") is unmet for it. The inventory test classifies it `own-accounting`.
* The SQL per-resident cap is a resident-fairness control, not the financial ledger. It stays authoritative and unchanged; the ledger is an additional, opt-in layer.
* Ledger has no release call: an open reservation becomes unknown liability after 40 seconds. Order therefore matters: SQL reserve first, ledger reserve second, so a ledger hold never leaves an open ledger reservation. A ledger hold consumes one resident SQL unit (never refunded, as the existing rule).
* Smallest coherent slice: opt-in `meters` mapping on `AzureAdvisor` (kinds `guidance` and `question`), a `Meter` protocol, `advisor_meters` helper, capabilities `resident-guidance` and `resident-question`. No host wiring.
* Unchanged blockers: OD-51, spend authority, attributable Azure billing and tolerance, live identity admission, pitch placement (slide 52 protected).
* Focused tier applies: no SQL, infrastructure, deployment or credential-path change; default behaviour (no meters) unchanged and the adapter stays disabled and expired.
