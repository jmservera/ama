---
title: Issue 162 live audit plan details
ms.date: 2026-11-18
---

* Phase 1: run `python3 -m unittest tests.test_chat_isolation` in src/api (PYTHONPATH per instructions); run dump script; sign in with the test user from credential files (never printed); POST break-glass twice with audit-check before and after; read env names with az containerapp show; delete the scratch cookie file.
* Phase 2: add one index row and one log entry.
* Phase 3: write changes and review records; commit without pushing.
* Constraint: no Azure change, no throwaway resource, no src edit.
