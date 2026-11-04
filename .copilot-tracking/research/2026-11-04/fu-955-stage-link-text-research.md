# Research: issue 955 stages 3 and 7 share link text

Date: 2026-11-04. Disposition: executed. Planning Readiness: Ready.

## Prior delivery check

* PR for #935 ("same-home journey stage map on programme queue", Refs #233) merged and introduced the map. No PR addresses #955.

## Findings

* `src/api/src/zava_forward/api/web/role-screens.js` `journeyStageMap`: each list item shows `"<stage>: "` as plain text followed by a link whose text is the target screen title. Stages 3 and 7 both target `resident-choice`, so two links read "Resident choice and update queue" in a screen-reader link list; the stage prefix is outside the link (WCAG 2.4.4 Link Purpose in Context is arguably met by the list item, but the issue asks for distinct link text).
* Visible text matching the accessible name keeps WCAG 2.5.3 satisfied, so the stage name goes into the visible link text, not an aria-label.
* Existing test `test_same_home_stage_map_links_by_role_and_states_deferral` in `tests/test_programme_screen.py` checks hrefs and deferral text, which remain valid.

## Acceptance criteria status before work

* Distinct accessible text per stage link: unmet. Test or manual check: unmet.
