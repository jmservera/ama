# Changes: issue #232 choice queue projection

* New `GET /api/resident/choice-queue` and `Store.resident_choice_queue` (Resident Liaison Officer, Retrofit Coordinator, Retrofit Programme Manager, Programme Support Officer only).
* `resident-choice` screen now shows the open-home queue from the server (portfolio scope, "N of total"), Unknown when unavailable.
* Tests added or updated; browser check 232 and 232s scroll panels into view because the larger queue pushes evidence below the fold.

## Validation (focused tier, security-sensitive: new authorised read route)

* Run: new core test (4 OK); api unittest test_ai_tasks, test_role_endpoint_inventory, test_role_screens, test_role_screens_conformance, test_resident_choice_screen, test_role_matrix (124 OK); browser check 232 and 232s (PASS, axe skipped, no pinned axe file); ruff check and format on touched files; core mypy strict clean; api mypy: 4 errors in tests/test_ai_consumption_api.py, identical on baseline (agents stubs not on path).
* Not run: local gate (required for security-sensitive change; coordinator runs it), rpi-checks, benchmarks, full suites, axe, assistive-technology or human testing.
* Unmet acceptance criteria: 4 (WCAG 2.2 conformance and AT testing, #151/#155) and 5 (Fluent component adoption, #150). Criterion 1 now has server-side projection evidence but is not ticked pending independent review and the criterion 4 and 5 gaps. Refs #232, not Closes.
