# Details: issue 955

## Phase 1

* `src/api/src/zava_forward/api/web/role-screens.js` `journeyStageMap`: an installed-for-role stage renders `<a href>` with text `"<stage>: <title>"` followed by the boundary sentence; deferred or not-installed stages render `"<stage>: <message>"` plain text as before.

## Phase 2

* `src/api/tests/test_programme_screen.py`: helper `link_texts`; `test_every_stage_link_has_distinct_accessible_text` checks uniqueness of all case-linked texts for the manager and coordinator roles, and that the two resident-choice links start with "3. " and "7. ".
* Test confirmed failing against the previous `role-screens.js`.
