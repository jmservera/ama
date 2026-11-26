---
title: Plan for issue 2245 (2026-11-25 live run)
ms.date: 2026-11-25
---

## Phases

* [x] Research and live probe on revision 0000076 (note: docs/reference/research/issue-2245-live-2026-11-25.md).
* [ ] Fix: any `financial-held` reason other than a budget limit (for example `liability-unknown`) must not say "assistant is not available" or "allowance used"; it says the demo spending control is holding model calls and no model was called.
* [ ] Tests: agents `test_chat_model.py` (outcome mapping) and api `test_chat_panel.py` (reply and note wording).
* [ ] After 00:00 UTC re-probe for a visible "Model calls: 1" on a fresh day budget; record result either way.
* [ ] Research note with per-criterion table, log and index entries, changes record, review, local commit.

Tier: FULL for src change (no `rpi-checks.py --all`; the coordinator runs gates). Local checks: targeted unittest, mypy and ruff in agents, core, api.
