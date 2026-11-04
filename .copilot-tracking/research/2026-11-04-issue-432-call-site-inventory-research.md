---
title: "Research: #432 provider call-site inventory"
ms.date: 2026-11-04
---

Disposition: reused (2026-11-02 owner-gate, 2026-11-03 re-check and resident-usage research) plus a direct read of main cb2394ebd. Planning Readiness: Ready for one source-only test slice.

* Merged for #432: #602, #660, #709, #765, #790, #832, #936, #977. Nothing is open for this issue.
* Source has exactly three chat-completions call sites: `core/ai.py` (ledger: admission, call context, counts, outcome), `api/resident_demo/aoai.py` (own reserved and closed token accounting, not the ledger) and `api/resident_demo/assistant.py` (optional counts-only sink from #936, no ledger). The legacy draft and image paths named in the issue no longer exist in `src/`. `documents.py` urlopen is blob storage, not a model call.
* No test classifies call sites, so "each model call" cannot be checked and a new site could be added unmetered.
* Unchanged blockers: OD-51, spend authority, attributable Azure billing and tolerance, live identity admission, pitch placement (slide 52 protected).
* Focused tier applies: test only, no security, infrastructure, SQL or deployment code.
