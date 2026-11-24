---
title: Issue 2304 live r64 details
ms.date: 2026-11-24
---

Phase 1: `probe_r64.py <label> <count> <gap> [others-first]` under `docs/reference/research/issue-2304-live-r64-2026-11-24/`; reads sign-in at run time; records status and seconds only.
Phase 2: from `src/api`, `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests.test_assistants.ForecastStatements`.
Phase 3: note `docs/reference/research/issue-2304-live-r64-2026-11-24.md`; issue edit through `gh api` (GraphQL is rate limited).
