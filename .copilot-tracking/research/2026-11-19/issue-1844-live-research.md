# Research: issue 1844 (2026-11-19)

Task: issue-1844-live. Refs #1844. Disposition: executed (source read plus prior audit reuse).

## Scope decision

Owner decision 2026-11-18: synthetic demo, desktop only. All six acceptance criteria are defined at 320x568, 320x900, 390x568 and 390x900 viewports.

## Evidence

* Checkout 910adb0a1. `src/api/src/zava_forward/api/web/style.css` sets `.map-home-card` to `position:absolute` (top/right inset, width min(22rem, 100% - 2 * sp-3)); the expanded dialog layout uses a separate grid. The narrow-width defect described in the issue is still present in source.
* Prior audit `docs/reference/research/issue-1844-live-20261119-2026-11-19.md` reached the same conclusion.

## Re-run 2 (branch test/code-live-20261119T135807Z, base 309635e29)

Disposition: reused. The issue body was re-read: all six criteria are written for 320x568, 320x900, 390x568 and 390x900 viewports or for delivery gates (independent exact-head assessment, hosted CI) that the owner decision of 2026-11-18 excludes for the demo. `style.css` still has no narrow-width rule for `.map-home-card` outside the expanded dialog (`@media(max-width:600px)` at line 308 only changes `.map-dialog`). The owner decision limits the demo to desktop, and criterion 3 already requires desktop behavior to stay unchanged. No Azure resource was touched and no browser run was made.

## Planning readiness

Ready: no criterion is unmet for the desktop-only demo, so the goal clause "if none is unmet say so and stop" applies. No source change.
