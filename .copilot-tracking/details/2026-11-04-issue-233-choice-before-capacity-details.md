# Details: issue 233 choice-before-capacity

* Phase 1: panel placed after "Service requests and access needs" and before the withheld list, so choice panels render first. Text states precedence of choice over offered slots, that an offer is not a booking or promise, and points to the Package queue screen. Plain language, no colour or motion, native `h("p")` inside `screenPanel`.
* Phase 2: test checks panel order after the choice and withdrawal panels, required wording, and absence of ranking words (headroom, utilisation) in the render function.
* Phase 3: trace tension row records the new text with "source-level test only"; boundaries unchanged.
* Phase 4: unit tests tests.test_role_screens_conformance, test_design_system, test_accessibility_baseline, test_content_standard; ruff check and format on touched test; mypy from `src/api`; `node --check`; offline atlas checker.
