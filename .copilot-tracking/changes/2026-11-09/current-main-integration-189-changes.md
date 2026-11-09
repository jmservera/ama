<!-- markdownlint-disable-file -->
# Issue 189 current-main integration changes (2026-11-09)

Plan: [plan](../../plans/2026-11-09/current-main-integration-189-plan.md). Refs #189 only. No source correction, grant or reset; no cycle consumed (C1 to C4 spent, one of five remains).

## Merge

* Frozen prospective records commit `8e519002e9e93450642ce3fa25a8f3341173e28c` (research, plan, details, critique) before the merge and any validation.
* Ordinary `git merge --no-ff origin/main` (`3a9767d5cf728c5e3be76813ce0bfdac4c06841e`, #1240, re-fetched and re-pinned): merge commit `0dea958760ea6727035e902a5f01e7c82858df94`, tree `141ec2719df2cc8ca524957335e2acf507186842`, parents `8e519002e` and `3a9767d5c`; no conflicts, no resolution edits. Published ancestry (C4 head `b933c2f60`) preserved.
* Source equivalence: `git diff b933c2f60 HEAD -- src/api` is empty (C4 `live_simulator.py` sha256 `5195ff4a828df67cbf1fadf9bc05aa2b11257c5c6757c38fff6b8fe4854da913`, `test_live_simulator.py` `ccf4cd0644bc8247b66b142a0c369f0434d1d70b571f1372b666f227223c9e78` unchanged). `src/core` tree `1be525fa66f701ec61e03606c05b223d125b6b7c` equals origin/main; `src/api` tree `70f2a9e1b617d559a45fbc8735c3ce1b42e7c919`; `src` `47e1df7b3aded66c5b6564fdb69c191b7ef8ec89`; `tools` `74ad3cb586dbff7f08ed3ba78301b9596a31ca86` (equals main). The delta against main under `src` and `tools` is the 14 C1 to C4 `src/api` files only.
* Composition read: no #189 module calls the #1240 Core changes (`store.py` quality-evidence, `quality.py`, `gates.py`, `resident_decisions.py`); `live_simulator` uses only `mssqlstore.connection_string`, `open_store`, `query_case_ids`, `cases`. `grep azure.iot src/core` is empty.

## Validation (owner demo-targeted tier; scratch `/tmp/i189-curmain-gt7YdQ`, outside the repository; producer exits in files; SQL/Azure variables unset)

| Check | Result |
|-------|--------|
| Reduced SDK-free venv (`pip install --no-deps` core, agents, api; `azure` namespace absent): import `simulator_admin`, `live_simulator`, `live_control`, `server` | exit 0, all import; `azure.iot.device` and `azure` absent |
| Same interpreter `test_simulator_admin` | exit 0, 27 OK |
| Same interpreter `test_live_simulator`, `test_live_control` | not runnable: the test modules import `iot_stream`/`live_receiver` (SDK) at top level; ImportError at collection, not a source defect (planned subset assumption corrected) |
| Scrubbed-server regression `test_api_install_prevents_scrubbed_server_child_writing_source_bytecode` (tools) | exit 0, 1 OK |
| `tools` `test_rpi_checks` (includes main's 1312 cases) | exit 0, 103 OK (C4 local had 102) |
| API (full venv with declared SDK) `test_live_simulator` 31, `test_simulator_admin` 27, `test_live_control` 34, `test_iot_stream` 37, `test_iot_credential_hygiene` 12, `test_sensor_consistency` 48 | each exit 0, 189 OK, 0 skipped |
| Core `test_gates` 20, `test_quality_procurement` 136, `test_resident_decisions` 308 | each exit 0; 110 skipped (actual-SQL/Azure opt-in, unverified, not passed) |
| mypy 2.4.0 (API profile, `src/api`) | exit 0, no issues in 202 source files |
| Ruff 0.17.1 `check .` and `format --check .` (`src/api`, 127 files) | exit 0, exit 0 |
| Ruff isolated check/format and `mypy --strict` on `tools/rpi-checks.py tools/test_rpi_checks.py` (CI profile) | exit 0, exit 0, exit 0 (2 files) |
| Browser `simulator_control_browser_check --axe` | NOT RUN: `/tmp/ama-rpi-heavy.lock` held (pid 3083388, issue 1292 diagnostic driver) at two checks 60 s apart; not queued. No `src/api` byte changed and controls use no changed Core path. Unverified in this merge; the last pass (11 states, 0 violations) is on the pre-merge head and is historical |

Not run: full gate, SQL services, cloud, model, private data, global installs, web-guidelines refresh (no web file changed).

## Cycle ledger

C1 to C4 spent; one of five remains. Hosted CI for the new head remains required.
