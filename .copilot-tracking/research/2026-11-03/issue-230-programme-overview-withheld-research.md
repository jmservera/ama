# Research: issue 230 programme overview withheld panel

Disposition: executed. Planning Readiness: Ready.

## Delivered so far (merged PRs)

* #662: programme-queue screen; criteria 1 to 3 (queue, separate chase and update owners, reset, five-gate view).
* #781: browser keyboard and axe proof for the programme screen (criterion 4 for programme controls).
* #815: "Not shown for this role" panel on the per-home view only; the atlas trace says the queue overview does not show it yet.
* Closed PR #489 is superseded.

## Unmet

* Criterion 4 full WCAG 2.2 and assistive-technology acceptance (#151, #155).
* Criterion 5 Fluent component adoption (#150); the no-role-simulator part is guarded by test_role_screens_conformance.
* Planner role: the journey names one "Programme Manager / planner" persona; the code has no planner role (owner decision).

## Slice choice

Smallest coherent unmet gap in #230 scope: the programme queue overview lists return reasons and owners but, unlike its per-home view, does not state what is withheld. Add the existing `screenWithheld` panel (continuity versus disclosure, proposed rule). Out of scope: Fluent library adoption (#150), portfolio endpoint, new roles.

## Tier

Focused. No security, infrastructure, SQL or deployment change. Gate not run.
