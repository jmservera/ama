# Details: issue 230 programme overview withheld panel

* `src/api/src/zava_forward/api/web/role-screens.js`: programme-queue `overview` appends `screenWithheld([...])` listing resident contact and access history, household and vulnerability detail beyond a queue row, and funding amounts. Native section, heading and list; no new CSS class, no script behaviour.
* `src/api/tests/test_programme_screen.py`: `test_overview_lists_withheld_items_as_text` for Programme Manager, Coordinator and coordinator-down.
* `src/api/tests/test_role_screens_conformance.py`: the withheld guard now also covers the programme-queue overview.
* Docs: `docs/reference/research/ux/atlas-screen-trace.md`, `docs/reference/log.md`.
