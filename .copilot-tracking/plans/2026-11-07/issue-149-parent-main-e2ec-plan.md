---
title: Issue 149 parent main e2ec integration plan
ms.date: 2026-11-08
---

## Plan

* One normal merge of fetched origin/main e2ecee25 into the parent. No rebase, force, amend or reset. Resolve only conflicts whose both intents are provable (append-only log keeps both entry sets; README index keeps both rows); otherwise stop with the exact question.
* Compare the main-relative parent delta after the merge to confirm no main intent is lost and no product, SQL, auth or Core change comes from the parent.
* Focused validation (CI-first, light before heavy): own installed core, agents and api from a fresh archive of the merged head with all production bytes compared; AI-state, exception-register screen, atlas checker, content-standard, document-controls and role-screens unit tests; ruff, canonical format, mypy strict from `src/api` and `src/core` with tests; core needs-inventory and scenario-manifest tests. Then maintained atlas and data-operator Chromium checks with required axe 4.10.3 under `flock -n`, no queue. Historical results are reused only where bytes are proven equal.
* Source freezes at the merge plus the records commit; browser evidence stays external.

## Critique (single pass)

A normal merge preserves ancestry and all RPI records. Incoming server.py and store.py changes could alter the data-operator register served to the browser check, so unit equality does not replace a current browser run. No FULL tier is needed because the parent adds no SQL, auth or deletion logic. Scope expansion would stop the integration.
