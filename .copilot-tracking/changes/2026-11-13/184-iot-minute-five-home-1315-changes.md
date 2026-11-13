# Changes: #184
* Applied candidate e904ba4c0 diff (15 files) cleanly onto dafed6a27: cadence 1/5 minutes, five-home fail-closed Quality scope, operator-triggered analysis guard, READMEs, tests.
* Critique fixes: attempt_permitted rechecks exact demo cohort; DEMO_COHORT_MISMATCH re-raised from run(); --max-homes with demo five refused; sensor_handover_verify.main accepts only literal bool passed (None/{}/1/"true" refused, exit 2); README wording ("hold", "envelope" removed from added text).
* New RED-first tests: tests/test_sensor_handover_verify_guard.py; three cases in test_live_control.DemoControlCohortTests (9 failures before code).
* c71cdd457 helper lives in untracked-to-source .copilot-tracking, not in e904ba4c0; not ported.
Validation (venv --system-site-packages, env -u ZF_DATA -u ZF_TEST_MSSQL): ruff check OK, ruff format --check OK (398 files), mypy core 142 / api 28 clean; core live_readings 24, sensor_consumer 50, device_identity 40 OK; api live_simulator+live_control+guard+demo 102 OK; assistants 138 OK (59 MSSQL skips, no MSSQL available).
