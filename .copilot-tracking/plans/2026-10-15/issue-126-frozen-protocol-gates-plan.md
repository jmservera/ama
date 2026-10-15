---
title: Issue 126 plan
ms.date: 2026-10-15
---

* Phase 1: `governance.py` mixin (protocol freeze/approve, BG-011 register and MDE verdict, capture gate, release decisions, breach pause and restart).
* Phase 2: wire into `Store`, generalise `SqlStore` document persistence, add API routes.
* Phase 3: `tests/test_governance.py` on both stores; run the full suite.
* Phase 4: README, knowledge index and log; explicit open items.
* Critique: standard single pass. Guard against inventing approvals; every approval needs a different named person and supplied references.
