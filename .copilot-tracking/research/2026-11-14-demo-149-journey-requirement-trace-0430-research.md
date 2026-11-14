---
title: Epic 149 journey and requirement traceability research
ms.date: 2026-11-14
---

Task: `demo-149-journey-requirement-trace-0430` (Refs #149). Stacked child of `test/demo-149-manual-fallback-continuity-0338`. Research disposition: executed. Planning Readiness: Ready. Tier: focused (docs and web source read-only; one new test).

## Evidence

* `docs/reference/research/ux/` holds 30 Markdown artefacts. `design-system.md` has a journey to requirement to design to test matrix; existing `test_ux_design_traceability.py` checks only that matrix.
* All FR/NFR/AC/SA/OD IDs cited in the artefacts resolve in the BRD or PRDs.
* 5 artefacts have neither their own requirement ID plus journey nor a matrix row: briefing-hax-design-note, map-tile-provider-options, regulatory-literacy-for-journeys, regulatory-ux-acceptance-protocol, resident-chat-learning-record. Two more lack a journey reference: prototype-learnings-and-simplicity-review, supported-devices-proposal.
* Test modules named in the docs: `test_hazard_referral`, `test_atlas_screen_trace`, `test_needs_inventory` and `test_scenario_manifest` live in `src/core/tests/`, not `src/api/tests/`; the documented PYTHONPATH exposes both.
* Some cited modules use conditional `skipTest` for prerequisites; only unconditional skips are disqualifying.

## Boundaries

Source-level engineering evidence. Not WCAG conformance, assistive-technology acceptance or comprehension evidence.
