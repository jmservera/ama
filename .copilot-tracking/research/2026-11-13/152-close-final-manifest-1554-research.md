---
title: Issue 152 cross-profile manifest research
ms.date: 2026-11-13
---

Research disposition: executed. Planning Readiness: Ready.

## Findings

* Issue #152 has one unchecked criterion: cross-profile checks follow the PRD AC-034 and AC-043 manifest.
* PRD source: `docs/prds/proper-warm-retrofit-programme-demonstrator.md` (AC-034 line 1156, AC-043 line 1165, FR-032, FR-035, check rows 1201 and 1207). `docs/requirements/prd.md` does not exist.
* Manifest `supported_devices` (desktop 1280, tablet 768, mobile 360, checked-only 1024, reflow-only 390 and 320) matches `design-system.md` and `test_owner_decided_device_widths_match_checked_widths`. No width drift found.
* Existing tests cover profile and workflow counts, partial/deferred shape, default IDs/count/order/selection and empty reason. Gaps: no assertion of the active slice declaration, unavailable-behaviour non-claim, endpoint format, scope/reset/empty checks, workflow fixture links, or that counts follow the PRD (eleven profiles, nine workflows).

## Decision

Add focused AC-034 and AC-043 tests to `src/api/tests/test_workbench.py`; no manifest change expected. Tier: Focused. No full AC acceptance claim (AC rows stay Not run).
