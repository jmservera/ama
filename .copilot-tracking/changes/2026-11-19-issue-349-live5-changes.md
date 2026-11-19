---
title: Issue 349 live5 changes
ms.date: 2026-11-19
---

## Changes

Docs and evidence only; no src change. Tier: FOCUSED (documentation, no SQL, security
control, infrastructure or deployment change; Azure calls were reads).

* Added the round 5 research note, an index row in docs/reference/README.md and a log entry.
* Added evidence files under .copilot-tracking/evidence/2026-11-19/issue-349-live5/.

## Per-criterion table

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Tenant owner provisions app, roles, credential | Partly proven (Graph denied for provisioner and role definitions) |
| 2 | Credential in private vault, not weakened | Proven for the demo |
| 3 | API auth/audience on registration; callbacks preserved | Partly proven (callback list unreadable) |
| 4 | Private roster reconciled | Unproven, not applicable to the demo |
| 5 | Real-user sign-in, logout, switching, wrong-role/unknown-staff denial | Sign-in, logout, picker proven; denial unproven (resident probe failed at sign-in) |
| 6 | Anonymous 401, forged-header denial, positive request | Proven with a qualification |

## Validation

* Link and diff review of the touched Markdown.
* mypy, ruff and unit tests: not applicable, no source changed.
