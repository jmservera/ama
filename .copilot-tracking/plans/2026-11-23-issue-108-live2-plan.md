---
title: Issue 108 live plan, second 2026-11-23 round
ms.date: 2026-11-23
---

Refs #108. Tier: focused. The change touches `src/agents/tests` only (no runtime source); basis, basis: offline test, no permissions, packages, deployment or control change.

Critique (executed once): verdict accepted. Reading `aoai.py` as text from the agents test avoids a cross-project import. Pin only names, not live Azure state.

Steps: add `test_resident_deployment_name_matches_record` ; run `tests.test_ai_eval`, ruff; write changes record with the per-criterion table.
