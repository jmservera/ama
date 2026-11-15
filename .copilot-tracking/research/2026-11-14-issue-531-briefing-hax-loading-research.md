# Research: issue 531 Today's briefing loading feedback and HAX provenance

* Disposition: executed. Planning Readiness: Ready.
* Surface: `src/api/src/zava_forward/api/web/` (`app.js` `aiBox()`, `style.css`); the task named `static/` and `styles.css`, which do not exist here.
* Existing: `content` already had `aria-busy` and a polite `role=status` line ("Reading case summaries..."); ranking text and "Not an instruction" label already present.
* Gaps: busy not on the section; terse loading text; status line height not reserved; no explicit split of rule-driven priority versus AI wording; no per-item "why listed".
* Constraints: keep `test_accessibility_baseline`, `test_connected_home_check`, `test_role_screens_conformance`, and `ownedNotice` patterns in `test_app_js_notices_content`.
* Scope: local deliverable only; stacked on #1639; no push.
