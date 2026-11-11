# Changes: #134 extension E1

Starting candidate 468bdd3 (tree e1b5e5bf), unchanged ancestry; origin/main e691255ff7 not integrated.

* `src/api/checks/connected_home_browser_check.py`: `RECORD_PANELS`, `is_record_panel`; `sibling_failures` scans them; `run_record_leak` injects a marker into each sibling's real record panel on every screen and requires rejection by the same predicate.
* `src/api/tests/test_connected_home_check.py`: two new tests (escaped record panels rejected; portfolio panels with other homes' data not rejected).

## Validation (private HOME/TMPDIR under /tmp/z134, existing venv)

| Command | Raw exit |
| --- | --- |
| `python -m unittest tests.test_connected_home_check` (src/api) | 0, 8 tests OK |
| `ruff check .`, `ruff format --check .` | pass, pass |
| `mypy` (234 files) | no issues |
| `flock -n -E99 /tmp/ama-rpi-heavy.lock timeout 900 python -m checks.connected_home_browser_check` (one run) | 0; 138 PASS lines; 6 record-panel leak controls rejected; log /tmp/z134/browser-e1.log |

No browser rerun, no axe, no full gate, no SQL, no install. Legitimate sibling evidence and portfolio panels remained accepted in the real run (no failure).

## Limits

Unchanged from C5: six screens, five logins, Asset proxy, no rows 6/7/8/11, intake/aftercare, event order, AT, approvals. Original C1-C5 artifacts untouched. Correction balance: E1 of 3 used; E2 and E3 not started.
