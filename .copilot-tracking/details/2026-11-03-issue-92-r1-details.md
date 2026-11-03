---
title: Issue 92 r1 details
ms.date: 2026-11-03
---

* Phase 1: method in procurement.py beside require_consultation_clear; rejects events other than let or renew; requires a registered actor; always blocked while Legal verification is unconfigured.
* Phase 2: test in test_consultation_controls.py (JSON and SQLite variants) proving blocked before and after a supplied complete record, no state change, invalid event rejected.
