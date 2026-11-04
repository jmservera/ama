---
title: "Plan: #432 provider call-site inventory"
ms.date: 2026-11-04
---

Details: [details](../details/2026-11-04-issue-432-call-site-inventory-details.md)

* [x] 1. Add `src/api/tests/test_ai_call_site_inventory.py`: scan `src/*/src` for the chat-completions endpoint, require each site to be classified with a join status, and name the two sites that are not ledger-joined.
* [x] 2. Focused test, ruff, mypy (cache /tmp/mypy-432).
* [x] 3. Commit, push, PR with Refs #432.

Stacked follow-ups need owner scope: wire the adapter sink or aoai accounting to the ledger (adapter expired and disabled), then OD-51, spend authority, billing, live admission, pitch.

## Critique (single pass)

* Risk: test claims coverage it does not prove. Applied: it asserts classification only; the criterion stays unticked.
* Risk: brittle text scan. Accepted: a new site failing until classified is the intent.
* Rejected: wiring the ledger into the resident adapter now; needs owner decision.
