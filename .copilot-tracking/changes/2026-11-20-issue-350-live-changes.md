# Changes: issue 350 live (2026-11-20)

Refs #350. Tier FULL (src/core change), local commit only; no push, no redeploy, no `rpi-checks.py --all`.

Files
* `src/core/src/zava_forward/core/sqlstore.py`: `_repair_identity_columns`, called from `_migrate` when columns exist but are not otherwise stale; rebuilds the derived row of any case whose stage, area, wave, owner_code, closed or contractor column disagrees with its body.
* `src/core/tests/test_sqlreads.py`: `test_identity_columns_that_disagree_with_the_case_body_are_repaired` (failed first: own queue 0 against 12; passes now).
* `docs/reference/research/issue-350-live-r4-2026-11-20.md` and its `raw/` and `scripts/`; index line in `docs/reference/README.md`; entry in `docs/reference/log.md`.

Divergence: none from the plan. Why: live GET probes showed own-queue list 16 against CSV 133 (SQL `owner_code` column drifted from bodies for 8 of 9 owners); deploy of the fix is not authorised for the demo, so the live disagreement persists.

Validation (FULL for the touched module, not the whole gate)
* `unittest tests.test_sqlreads`: 16 tests OK.
* `src/core` full discover: 4104 run, 35 failures and 22 errors, all in `test_device_registry_azure`, `test_telemetry`, `test_diagnostic_logging` and `test_discovery_assistant_demo` (missing Azure/OpenTelemetry stubs or installed-command setup in this environment, none touch SqlStore); every SQL test passes.
* `mypy` in src/core: 23 errors, all in telemetry.py, tests/telemetry_support.py, tests/test_telemetry.py and synthetic/device_provision.py (missing opentelemetry stubs, pre-existing); none in changed files. `ruff check` on changed files: clean. `src/api` suite not run (no api file changed). MssqlStore path not run live.

Per-criterion table (live 2026-11-20, revision 0000037)

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Anonymous browser API 401, page redirect kept | Unproven, failing (curl 401, browser 302); edge change outside demo authorisation |
| 2 | Staff prerequisite, all rows, 16 assets | Partly proven (one staff role, assets not re-hashed); role-specific rows unproven |
| 3 | Continuing synthetic baseline | Partly proven (980 cases, 30 visits, 167 funding); authorisation record and sensor/contractor cases unproven |
| 4 | Models, five assistants, release | Partly proven (5 assistants, 9 tasks, gate blocked, no release, SUS-1 active); live model draft unproven |
| 5 | Map provider and agreement | Partly proven (443 agrees; OSM public tiles; sensors 403); own-queue 16 vs 133 defect fixed locally, not deployed |
| 6 | Photo tokens | Unproven (503; consent and token store) |
| 7 | Law store | Unproven (503; human-owned seeding) |
| 8 | Ledger, document, digest, jobs | Partly proven (orch job every 5 min succeeding; audit job no run yet; digest 403) |
| 9 | Time capture gated | Proven for the gate (status 200, switched off, explanation); approvals human-owned |
| 10 | Per-role results | Partly proven (one staff role, resident anonymous only); other roles unproven |
