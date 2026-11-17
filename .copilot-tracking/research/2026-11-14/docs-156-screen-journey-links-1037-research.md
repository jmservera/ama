<!-- markdownlint-disable-file -->
# Research: issue 156 screen to journey, task flow and design artefact links (docs-156-screen-journey-links-1037)

* Task ID `docs-156-screen-journey-links-1037`; base `61e1917dd` on `docs/demo-156-screen-journey-links-1037`; research disposition `executed`; Planning Readiness `Ready`.

## Evidence

* `gh issue view 156 --comments`: AC1 (each backlog feature with a screen links to its journey, task flow and design artefact) is the only unticked criterion. Owner comments (#400, #401, 2026-10-31 closure audit) say AC1 stays unmet because all 74 current designs are Not supplied, some detailed flows are gaps, and no named human review exists.
* Canonical synthesis: `docs/reference/research/ux/zava-forward-prototype-profile-review.md` holds the 74-row issue register, two deltas and the 2026-11-12 IoT update. `tools/check-design-trace.py` reports blocked, 74 screens, 0 supplied designs.
* Delivered screens are registered in `src/api/src/zava_forward/api/web/role-screens.js` (twelve ids) plus case workspace, briefing, resident demo, chat widgets and `#/simulator`.
* Nearest written design records exist for asset, programme technical/quality, safety, finance, data (delivery-status sections), resident task designs J1 to J6, case workspace, briefing HAX, resident demo redesign and chat learning record. None is a versioned reviewable design.

## Findings

* A screen-keyed map is missing; the issue-keyed register cannot be navigated from a screen.
* A map can honestly supply links but cannot supply the missing versioned designs, so AC1 cannot be proven whole.

## Planning Readiness

Ready: additive documentation map, no gate change.
