---
title: Research, issue 2255 run 6 (live)
ms.date: 2026-11-23
---

Disposition: executed. Planning Readiness: Ready.

Earlier runs (r1 to r5) proved the live queue clock and added a core re-seed test. New angle: the private seeder `infra/scripts/seed_demo_hazard_clock.py` `revert`.

Finding: `apply N` re-dates `noticed` on a running subset and stores `noticed_was` in the marker, which is `None` when the hazard had no `noticed` value but a `recorded_at` anchor. `revert` only restores `noticed` when `noticed_was is not None`, so the invented date stays after revert. That breaks the documented "undo every change" contract. Existing tests only cover hazards that had a `noticed` date.

Live criteria status is carried from [r5 research](../../../docs/reference/research/issue-2255-live-r5-2026-11-23.md) and re-checked against the live revision in the research note for this run.
