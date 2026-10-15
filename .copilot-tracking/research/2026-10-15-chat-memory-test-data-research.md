---
title: Research for #172 chat and memory test data
ms.date: 2026-10-15
---

## Scope

Issue #172 (parent #167): synthetic personas, threads, memory items, consent states, isolation and deletion cases.

## Evidence

* Eleven perspectives: PRD Users and Personas; profile review `docs/reference/research/ux/zava-forward-prototype-profile-review.md`.
* Requirements: PRD FR-056, FR-057, NFR-015, AC-094 to AC-097, AC-102; ADR 0004 isolation model (accepted 2026-10-15).
* Reuse: `mvp/zavaforward_mvp/scale_fixture.py` (60,000 homes, seed/is_synthetic conventions), `assistants.REGISTRY` tasks, `auth.DEFAULT_ROLE_MAP` roles, sibling `sensor_backfill.py` pattern.
* Research disposition: executed. Planning readiness: Ready.

## Open items

* Retention policy and legal lock (OD-45/OD-46), owner confirmation of persona-to-app-role mapping, no runtime exists yet (#160 to #164).
