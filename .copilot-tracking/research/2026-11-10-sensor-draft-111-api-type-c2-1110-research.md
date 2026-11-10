---
title: Issue 111 API typing C2 research
ms.date: 2026-11-10
task_id: 111-api-type-c2-1110
---

## Objective

Fix the hosted `src-api` Type check failure on frozen `2b050647bff51eef4c1b34d6434bba7eae3d5f9a` (PR 1395 run 42838218050, job 129906310911): `tests/test_sensor_review_draft_api.py:63: Call to untyped function "App" in typed context [no-untyped-call]`, one error in 220 files. The previous Core mypy run does not type the API project and is not API type success.

## Evidence

* Reproduced on unchanged `2b050647b` with the actual configured command (`mypy` from `src/api`, mypy 2.4.0 in `/tmp/zf-111-1110/venv`, external cache): exit 1, the identical single error, 220 files. Raw: `ROOT/checks-111-api-type-c2-1110/api-mypy-before.log`. The local run did not set the CI `PYTHONPATH`; result identical.
* Cause: `App.__init__` in `zava_forward.api.server` is legacy untyped (module is under a `ignore_errors` override). The new test module is strict-typed and calls it once (line 63).
* Repository convention (`src/api/pyproject.toml`): other typed API tests (`test_coordinator_api`, `test_ai_consumption_api`, `test_handoff_api` and others) use exact-module `disallow_untyped_calls = false` stanzas; `tests/scale_load.py:102` uses an exact-call `# type: ignore[no-untyped-call]`. No typed App factory or helper exists; production `App` annotation is out of scope (production change, and server is under the ignore override).
* Browser: `checks/quality_sensors_browser_check.py` is the existing maintained served check covering the sensor draft section (off, empty, seeded, no write control). This fix touches no UI file, so it is a regression check only. Chromium 1248 is cached locally; axe 4.10.3 file at `/tmp/axe-4.10.3.min.js` is optional.
* Budget: Root selects this one remaining batch; minimum 0 afterwards; no further automatic correction.

## Planning readiness

Ready. Disposition: executed.
