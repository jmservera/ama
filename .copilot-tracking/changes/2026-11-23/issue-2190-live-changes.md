# Issue 2190 live changes, 2026-11-23

Classification: Tier FULL (src code changed); the coordinator owns the complete gate, which was not run here (`rpi-checks.py --all` never run).

## Files

| File | Change |
| --- | --- |
| `tools/rpi-checks.py` | `_region_passed` accepts a result only as a line equal to `ok` or `ok` glued to an unterminated log fragment |
| `tools/test_rpi_checks.py` | Three rejected log shapes; the flake 2 AST test now pins `settle_route` before the baseline snapshot |
| `src/api/tests/test_rai_release_readiness_api_218.py` | Constant-pinning test replaced by a slow-server behavioural test |
| `src/api/checks/employee_chat_browser_check.py` | `settle_route` waits for the list status then `networkidle` |
| `src/api/tests/test_employee_chat_settle.py` | New deterministic ordering and predicate tests |
| `docs/reference/research/issue-2190-live-20261123-note.md` and evidence folder, `docs/reference/README.md`, `docs/reference/log.md` | Research note, index line and log entry |

## Validation

* `tools.test_rpi_checks`: 129 OK (new rejected shapes failed before the fix: 2 subtest failures).
* `src/api`: settle and 218 tests, 7 OK; mypy clean; ruff check and format pass on changed files; `tools` ruff findings unchanged at 20.
* `checks.employee_chat_browser_check` under 14 busy loops: 6 of 6 passed. Manifest recipe does not list the script.
* Not run: complete local gate, hosted CI.

## Per-criterion table (issue 2190)

| Criterion | Proven / unproven | Basis |
| --- | --- | --- |
| Each flake reproduced or explained | Proven | Earlier notes and evidence |
| Flake 1 fixed with regression test | Proven | Accepting and rejecting tests; stricter rule |
| Flake 2 fixed with regression test | Unproven as a deterministic race reproduction; fix ordering proven | Client-side gap cannot be injected deterministically; ordering and predicate tests plus 6 of 6 loaded runs |
| Flake 3 fixed with regression test | Proven | Slow-server test fails if the budget is not honoured |
| No check relaxed | Proven | `_region_passed` stricter; failing patterns and snapshot comparison unchanged |
| Azure, billing, DPO, AT testing | Not applicable | Demo scope; no Azure resource touched |
