---
title: Plan, issue 133 concern pack
ms.date: 2026-11-04
---
## Plan

* [x] Phase 1: add `propose_pack` and `review_pack` to `aftercare.py`; register `aftercare-concern-pack` in `ai_registry.py`.
* [x] Phase 2: add `ConcernPackTests`; run focused tests, registry-dependent API tests, ruff and mypy.
* [x] Phase 3: README paragraph and log entry.

Details: [details](../details/2026-11-04-issue-133-concern-pack-details.md).

## Critique (one pass)

Executed once. Verdict: proceed. Applied directly: the pack is template-first so it works with AI unavailable; an AI summary passes `neutral_text`; only the named owner reviews; neither review action touches the concern; the registry entry is disabled with a manual route because no model route exists; no approval is claimed. The slice does not touch security, infrastructure, SQL or deployment, so the focused tier applies. Use Refs #133.
