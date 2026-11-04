# Plan: issue 233 choice-before-capacity

Research: ../research/2026-11-04-issue-233-choice-before-capacity-research.md. Details: ../details/2026-11-04-issue-233-choice-before-capacity-details.md.

* [x] Phase 1: add "Choice comes before offered capacity" panel to `resident-choice` render (`role-screens.js`)
* [x] Phase 2: add source-level test for ordering and wording in `test_role_screens_conformance.py`
* [x] Phase 3: update `atlas-screen-trace.md` tension row and `ms.date`; append `log.md` entry
* [x] Phase 4: focused validation (unit tests, ruff, mypy, node syntax check, atlas checker)

Critique (single pass, self-applied): compatible. The panel is text only, adds no control, keeps resident-first ordering, does not rank by utilisation and states no action is taken. No conflict with confirmed decisions.
