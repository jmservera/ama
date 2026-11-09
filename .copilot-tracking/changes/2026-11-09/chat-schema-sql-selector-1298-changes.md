<!-- markdownlint-disable-file -->
# RPI Changes: chat-schema-sql-selector-1298

* Task ID: issue-1298-fresh-demo
* Plan: .copilot-tracking/plans/2026-11-09/chat-schema-sql-selector-1298-plan.md
* Base: 9f9aacc8be6a1b0e9a10efd367d1ea8bd7520939; pre-source evidence commit 52c3ec4f507a6129372e0ce747ed176d9ed9a61a
* Scope declared: full plan (P01 to P03)
* Owned external log directory: /tmp/i1298-fresh.PsO6Ge (not committed)

## Implementation opening (recorded before the first source edit)

* Research, plan, details and critique were committed at 52c3ec4f5 before any source edit. First dependency-ready item: P01-T01.
* Reproduction on unchanged source at 52c3ec4f5 (tools unchanged from base): `changed_groups(["src/core/src/zava_forward/core/chatthreads.py"], [])` returned `mssql selected: False` with groups preflight, project-core, project-agents, project-api, project-orchestrator, project-importer, namespace, static, image-api, image-agents, image-orchestrator, image-importer, logo-0600; producer exit 0 (log repro-before.log).

## Correction budget

* Review-correction cycles consumed on #1298: 0; grants: none; five remaining under the standing default. This attempt is the initial implementation.

## Evidence by plan area

### P01-T01 regression (tools/test_rpi_checks.py)

* Added `test_sensor_store_chat_schema_dependency_selects_mssql`: AST evidence that the sensor fixture imports `MssqlStore`, that `mssqlstore.py` imports exactly `MEMORY_ADDED`, `MSSQL_DDL`, `MSSQL_INDEX` from `.chatthreads` as `CHAT_*` aliases and references them, that the path is in the explicit set and matches no path keyword, that it selects `mssql`, and that `chat_panel.py` and `chat_privacy.py` do not.
* Added the `chatthreads.py` path to the existing per-path loop, which asserts the flagged sensor command, `ZF_SENSOR_MSSQL=1` and the pinned test count.
* Edited the existing exact-set pin to include the path. No removals; receipt mutation tests untouched.
* Pre-fix run (unchanged `tools/rpi-checks.py`): `python3 -m unittest discover -s tools -p test_rpi_checks.py -k chat_schema -k changed_core_sensor -k direct_sensor` exit 1, Ran 3, failures 3: loop subtest and set-membership assertions for the path (log p01-fail.log). The AST assertions passed before the fix.

### P02-T01 selector (tools/rpi-checks.py)

* Added `src/core/src/zava_forward/core/chatthreads.py` to `SENSOR_MSSQL_DIRECT_DEPENDENCIES`; the comment now states the entries are suite imports or exercised store-initialization definitions and that the set is not exhaustive or transitive. No selector logic, SQL command, skip tuple, required-test or receipt-verification change.
* Post-fix reproduction: `mssql selected: True` (producer exit 0, repro-after.log).

### P03-T01 validation: owner demo-targeted tier

Tier and rationale: owner-selected demo-targeted validation replaces the blanket full local gate for this push (coordinator brief, demo-rpi-common). No `rpi-checks --all` or `--changed`, no receipt, no SQL skip waiver, no cloud fallback. The change is path selection only; no SQL command, sensor test or store code changed, so an actual disposable-SQL run would not exercise the changed code and no shared SQL lock was taken.

| Command (repo root, worktree-bound) | Exit | Result |
|---|---|---|
| `python3 -m unittest discover -s tools -p test_rpi_checks.py -k chat_schema -k changed_core_sensor -k direct_sensor` | 0 | Ran 3, OK |
| `python3 -m unittest discover -s tools -p test_rpi_checks.py -v` | 0 | Ran 103, OK, 0 skipped (102 before this change) |
| `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` on the two files | 0 | All checks passed |
| `ruff format --isolated --line-length 100 --check` on the two files | 0 | 2 files already formatted |
| `python3 -m mypy --strict` on the two files | 0 | no issues in 2 source files |
| `git diff --check` | 0 | clean |

Ruff 0.17.3 and mypy 2.4.1 are installed; the gate pins 0.17.1 and 2.4.0, so these use the gate's isolated arguments but unpinned versions and are not gate-equivalent. An initial non-isolated `ruff check` and `ruff format --check` run exited 1 (20 errors, 2 files) because it used a configuration the gate does not use; it is preserved here and is not a gate result. Logs are in the owned external directory /tmp/i1298-fresh.PsO6Ge and are not committed.

## Limitations carried forward

* Explicit, not exhaustive: `sqlstore.py` (imported by `mssqlstore.py`) has at least fourteen top-level sibling imports plus function-local imports that remain unselected; broader transitive coverage versus cost is an owner decision.
* Real sensor MSSQL execution at this head is unproven by this attempt; the literal issue full-gate criterion remains unproven under the demonstrator policy. Hosted CI and independent exact-head review are not run or claimed.
