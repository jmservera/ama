# Research: issue 230 design-system class check

Disposition: reused (prior research and merged PRs). Planning Readiness: Ready.

## Delivered so far (merged PRs)

* #662 programme screens (criteria 1 to 3), #781 browser keyboard and axe proof, #818 overview withheld panel. Closed #489 is superseded.

## Unmet

* Criterion 4: full WCAG 2.2 acceptance and assistive-technology testing (#151, #155).
* Criterion 5: Fluent library adoption (#150) is not done; no-role-simulator is guarded by test.
* Planner role remains an open owner decision.

## Slice

Programme and other role screens use classes `.list`, `.row`, `.side`, `.screen-record`, `.screen-links`, `.screen-evidence` that the design-system component inventory did not list. Document them and add a test that every class in role-screens.js is defined in style.css and listed in the inventory, with no inline styles or hard-coded colours.
