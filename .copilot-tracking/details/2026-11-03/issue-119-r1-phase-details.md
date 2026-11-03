---
title: Issue 119 r1 phase details
ms.date: 2026-11-03
---

## Phase 1

* File: `src/api/src/zava_forward/api/web/app.js`. A `tileNote` paragraph with `role="status"` and `aria-live="polite"` sits after the existing status paragraph; `tileerror` on the tile layer sets plain-language text with a next step. No colour-only signal, no new motion, native elements only.
* The note appears only when a configured tile provider is set; with no tile URL nothing changes.

## Phase 2

* `src/api/tests/test_ui_support.py`: `test_tile_load_failure_is_announced_and_points_to_the_list`.
* Protocol in `docs/reference/research/ux/wcag-conformance-baseline.md` updated; log entry appended.
