---
title: Research for issue 2245 (2026-11-26 live run)
---

Opening: issue has no checkboxes; criteria are read from the Expected paragraph (thread create no 500; model-answerable question shows Model calls 1; plain banner when rule-based; which skills call the model and why none did). Prior notes 2026-11-22 to 2026-11-25 exist; the 2026-11-25 wording fix sits on unmerged local branch test/code-live-20261125T231506Z (baf5d17491).

## Findings

Disposition: executed (reuse of prior notes plus live re-probe). Planning Readiness: Ready.

* Live revision 0000079: creates 8/8 200; widget "Model calls: 1"; evidence in docs/reference/research/issue-2245-live-2026-11-26.md.
* Cause of 2026-11-25 stops: day-wide synthetic budget plus fail-closed liability-unknown after a slow settlement (ai_consumption.py, 40 s window).
* Fix candidates: hourly meter slot (branch 550175089f) and spend-held wording (baf5d17491), both unmerged and absent from this base.
