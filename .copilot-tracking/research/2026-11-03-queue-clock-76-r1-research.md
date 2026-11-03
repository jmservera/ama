---
title: Issue 76 round 1 research
ms.date: 2026-11-03
---

Research disposition: executed. Planning Readiness: Ready.

## Prior delivery checked

* Merged: #325 (role queues and shared case context), #376 (queue signals and reset scope, #77), #401, #406, #407 (blockers aligned to current stage), #438, #866 (SA-007 evidence for safety screens).
* Criteria 1 to 4, 6 and 7 are already ticked on the issue. The closure audit of 2026-10-31 left only criterion 5 unmet.

## Fresh evidence (origin/main b855aec86)

* `src/core/src/zava_forward/core/taskqueues.py` builds `hazard_clocks` only for unreleased hazards: owner, awareness, elapsed hours, response and resident update due dates.
* A missing owner is recorded as `Unknown` with no plain statement or next action, and each deadline has no plain state (open, completed, overdue, unknown).
* No safeguarding record exists in the case model or the hazard categories (Damp and mould, Structural, Electrical, Other). Adding one touches special-category data and consent boundaries, so it is out of a focused slice.

## Slice choice

Smallest coherent slice: make each hazard clock state its named-owner status and each recorded deadline state in plain words, never inventing an owner. Additive core fields plus the existing UI sentence. No auth, SQL, infrastructure or deployment change; focused tier.

## Unmet after this slice

* Criterion 5 stays unmet: safeguarding items have no data model, so no safeguarding clock or owner exists; hazard clocks remain a recorded-snapshot view, not a live statutory clock.
* Owner ratification of queue definitions, live Entra and human acceptance remain open.
