---
title: Exception register plan (#135)
ms.date: 2026-11-04
---

## Stacked slices

1. [x] This slice: read-only register and endpoint (core mixin, route, tests, README).
2. [ ] Staff screen on `/api/exceptions` (Fluent 2, WCAG, plain language).
3. [ ] Persistence of the queue and an audited recovery request endpoint.
4. [ ] Importer producer for failed imports; health check for the outage banner.
5. [ ] Owner approval of operator and steward roles and runbooks (human step).

## Slice 1 phases

Details: [details](../details/2026-11-04-exception-register-135-details.md).

* [x] Phase 1: `exception_register.py` mixin and `Store` wiring.
* [x] Phase 2: `GET /api/exceptions`, role inventory entry.
* [x] Phase 3: tests, ruff, mypy, README.

## Critique (one pass, self-applied)

* Access must not fall back to manager roles when staff are named: applied (named staff only; managers only see the empty roles_not_named state).
* One unreadable case must not break the register: applied (reported in `unrouted`).
* No fabricated health: banner stays unknown: applied.
