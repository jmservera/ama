# Research: #233 tensions and same-home walk (2026-11-14)

Disposition: executed. Planning Readiness: Ready.

* Existing: `role-screens.js` already had the "Not shown for this role" panel, "Choice comes before offered capacity" and a `journeyStages` map; `atlas-screen-trace.md` and `core/atlas_screen_trace.py` trace both tensions and the eight-stage walk (EX-HOME-901, design-level).
* Gap: no explicit plain-language tension callout labelled as atlas hypothesis; no render test that all stage links carry one home.
* Constraints: Fluent design system classes only (`screenPanel`), no role simulator, no `aria-invalid` (accessibility baseline counts), non-colour status text, hypotheses pending #155.
