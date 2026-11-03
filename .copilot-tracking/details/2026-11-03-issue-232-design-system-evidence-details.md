# Details: issue #232 design-system and no-simulator evidence

* Phase 1: `tests/test_role_screens.py::test_screens_use_only_documented_design_system_classes_and_no_simulator` parses the inventory section of design-system.md.
* Phase 2: `checks/role_screens_browser_check.py::check_design_system_use`, called from `check_readonly_accessibility` for `STORY_RESIDENT`.
* Phase 3: paragraph after the 232/232s story description in `src/api/README.md`.
* Phase 4: commands recorded in the changes file.
