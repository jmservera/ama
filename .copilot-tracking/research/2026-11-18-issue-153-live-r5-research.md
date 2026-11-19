---
title: Issue 153 live RPI research (wording defects)
ms.date: 2026-11-18
---

Refs #153. Disposition: executed. Scope: synthetic demo, desktop only. FULL tier applies because src code changes.

## Evidence in hand

* Defects recorded in docs/reference/research/content-recheck-153-live-r4-2026-11-18.md (R1, R2) and
  content-audit-live-153-2026-11-18.md (N1, N2, N3).
* R1/N3: src/core/src/zava_forward/core/exposure_limits.py:258 emits "Held" and "envelope".
* R2/N1: app.js lines 827 and 1581 show "Unassigned" for the resident update owner.
* N2: app.js lines 935-936 show "Unassigned" in chase owner and receiver cells.
* Criterion 5 (named human review) cannot be proven by an automated run.

## Planning readiness

Ready (to be refined by targeted source reading).

## Process note

An earlier draft of these artifacts overwrote the tracked files of the previous run (same names) and a source edit was
made before the changes file existed. Both were reverted with `git checkout` before any commit; this run uses the
`r5` suffix. Source selected for change: exposure_limits.py:258, panels.js exposureNotice (lines 859-868), app.js
handoff owner fallbacks (806, 826, 827, 935, 936, 1579, 1581).
