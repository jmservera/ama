# Details: issue #229 slice 4

## Phase 1

* `role-screens.js` data-operator: `summarise(rows, signal)` fetches each case (failures become Unavailable rows), `summary(entries)` renders two tables with captions and scroll regions via `screenTable`.
* Reuses `operatorSide` and `operatorStatus`; advance events excluded as in the per-home view.

## Phase 2

* `tests/test_data_operator_screen.py::test_page_queue_lists_both_values_and_unavailable_homes`.

## Phase 3

* `src/api/README.md` note. Validation commands below in changes.
