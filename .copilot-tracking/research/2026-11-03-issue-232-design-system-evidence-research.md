# Research: issue #232 design-system and no-simulator evidence

* Disposition: executed (prior #232 artifacts reused, merged PRs inspected). Planning Readiness: Ready.

## Already delivered (merged)

* #652, #715: resident choice and update queue screen with page-level summary.
* #777: resident service issue screen with access needs and linked commitment.
* #856: browser keyboard, text-only state, no-controls and optional axe evidence for stories 232 and 232s.
* Closed unmerged: #487 (superseded by the above).

## Unmet acceptance criteria before this slice

* Criterion 1: page-level (20 homes) only; server-side cross-home projection unmet.
* Criterion 4: engineering evidence only; assistive-technology validation (#155) unmet.
* Criterion 5: no evidence that the screens use the #150 inventory; no-simulator evidence existed only for other stories.

## Slice chosen

Test and documentation only: prove criterion 5 as far as the repository can (native inventory classes, no custom elements, no role simulator). Smallest slice; no product code, no resident contact, no AI feature.

## Evidence

* docs/reference/research/ux/design-system.md: component inventory; states it is a native extension, not Fluent adoption.
* src/api/src/zava_forward/api/web/role-screens.js: class literals all in inventory.
* Finding: shell-owned `.work-context` panel uses undocumented classes (`muted`, `next-action`, `safety-clock`, `work-context`); excluded from the check and routed as follow-up.

## Follow-ups

1. Server-side cross-home resident queue projection (criterion 1).
2. Assistive-technology and people validation in #155.
3. Document or retire the undocumented work-context classes (#150).
