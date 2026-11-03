# Research: issue 230 programme check hardening

Disposition: reused (prior evidence adequate). Planning Readiness: Ready.

## Delivered already (merged)

* #496 specialist screen foundation, #662 programme manager and coordinator screens, #781 browser keyboard and axe proof, #818 withheld-items panel, #854 design-system class guard.

## Acceptance criteria status

| Criterion | Status |
| --- | --- |
| 1 Shared queue with reason, sender, owner, proposed receiver | Delivered for the loaded page (#662); portfolio-level endpoint beyond 50 rows not delivered |
| 2 Chase and update separate; reset changes no records | Browser-proven (#781); this slice hardens the evidence |
| 3 Connected same-home five-state view, missing gates blocked | Delivered (#662) and browser-checked |
| 4 WCAG 2.2 baseline, textual state, keyboard | Engineering evidence only; assistive-technology acceptance unmet (#151, #155) |
| 5 Design system components, no role simulator | Class guard (#854); Fluent component adoption (#150) not proven |

## Slice

Apply the non-blocking follow-ups from the independent review of #781 to `src/api/checks/role_screens_browser_check.py`: assert coordinator-withheld detail is absent, compare the record before and after the connected view, fail when no main landmark exists for axe, use expect() for status text, relabel the reflow check to its real scope, and label Reset as corroboration of #662. Not security, infrastructure, SQL or deployment: focused tier.
