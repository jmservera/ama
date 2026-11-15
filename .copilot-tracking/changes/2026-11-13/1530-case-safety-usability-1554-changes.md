<!-- markdownlint-disable-file -->
# Changes: Issue 1530 case safety usability

Status: implemented (Option A1, client only, no backend rule change).

## Files

* `src/api/src/zava_forward/api/web/app.js`: new `hazardState` wording and `safetyPanel`. Every control has a label, deterministic id and hint. One form, fieldset and legend per action with its own evidence field. `What humans need to do next` callout. Restart form only for an independent reviewer with the accountable role (mirrors the server, including history fallback). Legacy rows get the job pre-filled, plain wording and no restart trap. Facts list, details and optional timing disclosures. Raise form with guidance, markers, examples and a default of Significant.
* `src/api/src/zava_forward/api/web/style.css`: safety card, facts, step, details and hint styles using existing tokens.
* `docs/reference/research/ux/design-system.md`: Safety issue card component row.
* `docs/reference/log.md`: log entry.
* `src/api/tests/test_safety_panel_ux.py`: 7 DOM tests on the shipped code.

## Validation

* Passed (113 tests): test_safety_panel_ux, test_hazard_api, test_content_standard, test_accessibility_baseline, test_design_system, test_case_journey, test_cutover_audit, test_scenario_manifest, test_needs_inventory. The cutover inventory needed no regeneration.
* Passed: `checks.workbench_browser_check`; `checks.case_view_ux_browser_check` (pinned axe 4.10.3, SHA-256 verified).
* `checks.case_journey_browser_check` fails at "320x800 summary within one viewport scroll (1636.4 > 1600)". The same value fails on unmodified HEAD web files, so it is pre-existing. With a temporary threshold of 1700 in a throwaway copy, the whole journey check passes, including axe.
* `ruff check`, `ruff format --check` and `mypy` (238 files) pass.
* A bug found while testing was fixed: a nested timing array in `step` children rendered as text.
* Not run: the full `src/api` suite (exceeded time budget) and the complete local RPI gate. Hosted CI is not observed.
