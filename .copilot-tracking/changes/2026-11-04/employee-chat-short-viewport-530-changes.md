<!-- markdownlint-disable-file -->
# Employee chat short viewport Send: changes (2026-11-04)

Plan: [../../plans/2026-11-04/employee-chat-short-viewport-530-plan.md](../../plans/2026-11-04/employee-chat-short-viewport-530-plan.md)

## Changed

* `src/api/src/zava_forward/api/web/chat-widget.css`: sticky tools row in the composer.
* `src/api/checks/chat_widget_browser_check.py`: asserts Send stays inside the panel at 320x480 and 640x360.
* `src/api/README.md`: short note.

## Validation (focused tier)

Run, on main fab02307e plus this change:

* `test_chat_panel`, `test_chat_isolation`, `test_resident_chat_api`: 133 tests OK (1 skipped).
* `ruff check` clean; `mypy --cache-dir=/tmp/mypy-530` clean on the edited check.
* `chat_widget_browser_check` (Chromium, axe-core 4.10.3 by pinned hash): every employee leg PASS including the new viewports and axe. The resident leg still FAILS at its existing 320px focused-control assertion, as on main (routed to #520); the shared check is not green overall.

Not run: complete local gate, full suites, benchmarks, SQL Server selectors, live model, live site, screen-reader and voice testing. `ruff format --check` on the check file already reported it as unformatted on main; not reformatted here to keep the diff small.

## Unmet acceptance criteria

Criterion 8 remains unmet (live employee-site verification, owner confirmation of agent names, local SQL selectors of the gate). Criteria 1 to 7 are unchanged and were delivered earlier. Hence Refs #530, not Closes.
