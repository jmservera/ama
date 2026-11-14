# Research: Issue #231 assessor/coordinator screens WCAG 1.4.1 state clarity

* Date: 2026-11-14
* Disposition: executed. Planning Readiness: Ready.
* Finding: `role-screens.js` has no dedicated "Retrofit Assessor" screen. The PAS 2035 assessment/design/building/coordination sign-offs render in `technical-queue` (Retrofit Coordinator, Quality Inspector, Building Safety Liaison, managers); per-check evidence renders in `quality-queue`. No lodgement screen exists, so none was changed.
* Constraint: classes must come from the design-system component inventory (`test_role_screens.py` enforces it). `.screen-links`, `.card`, `.screen-record` are documented, so the jump nav uses `.screen-links`.
* Constraint: test harnesses mock `h()` as plain objects, so helpers must not use DOM methods.
* Environment note: the installed `zava_forward.core` resolves to another checkout, so validation uses `PYTHONPATH` pointing at this worktree's `src/*/src`.
