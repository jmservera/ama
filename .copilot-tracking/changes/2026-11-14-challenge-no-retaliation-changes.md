# Changes: issue #220 assurance flags

* `src/core/.../challenges.py`: ASSURANCE_TEXT, `assurance()`, `stamp_assurance()`, `view()["assurance"]`.
* `src/core/.../resident_decisions.py`: stamp on challenge open, resolve, nomination correction.
* `src/core/.../store.py`: `challenge_assurance` in detail for permitted readers only.
* `src/api/.../web/panels.js`: plain-language `#challenge-assurance` note.
* Tests: three new cases in `test_challenge_non_retaliation_hazard_guard.py`.
* Validation: guard, resident_api, nomination_screen, content_standard, design_system, accessibility_baseline, dependency_rule (api); test_challenges (core); ruff and mypy in core and api all pass. No `discover`. Hosted CI and browser harness not run.
