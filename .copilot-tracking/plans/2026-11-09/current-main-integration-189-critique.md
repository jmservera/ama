<!-- markdownlint-disable-file -->
# Issue 189 current-main integration critique (2026-11-09)

One critique of the final candidate plan (independent rubber-duck agent, read-only). Verdict: Revise, six findings. Not repeated for this task.

| # | Severity | Finding | Disposition |
|---|----------|---------|-------------|
| 1 | Blocking | `src/api/pyproject.toml` declares `azure-iot-device` mandatory, so a normal install is never SDK-free. | Applied: the SDK-free environment is a deliberately reduced `--no-deps` install (core, agents, api sources plus only the non-SDK runtime packages), disclosed as reduced, not as the declared base install. The packaging contradiction is recorded as a boundary and not resolved here (no source/config change authorized). |
| 2 | Blocking | The scrubbed-server regression builds its own pip-free venv with source on a `.pth`; it does not test the install. | Applied: the regression is kept as the contract, and additionally the reduced-install interpreter imports `server`/`simulator_admin`, proves `azure.iot.device` is absent, and runs the SDK-free test subset (`test_live_simulator`, `test_simulator_admin`, `test_live_control`). |
| 3 | Blocking | Ruff paths prefixed `src/api/` while run from `src/api`. | Applied: paths relative to `src/api` (`src/zava_forward/api/...`, `tests/...`, `checks/...`). |
| 4 | Non-blocking | Browser admission race. | Applied: take `flock -n` on the heavy lock and hold it until the browser process exits. |
| 5 | Non-blocking | Browser invocation lacked setup. | Applied: from `src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests`, `python -m checks.simulator_control_browser_check --axe <asset>`, Playwright 1.64.0 and `google-chrome` prerequisites; missing prerequisite is BLOCKED. |
| 6 | Non-blocking | "SDK import only lazy" claim false (`iot_stream.py`, `live_receiver.py` import the SDK at top level). | Applied: P4 checks the server's reachable import chain, and that `src/core` has no SDK import. |
