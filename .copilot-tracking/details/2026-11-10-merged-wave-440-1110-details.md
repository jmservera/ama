<!-- markdownlint-disable-file -->
# Merged-wave 440 checkpoint details (2026-11-10)

Prospective matrix written before running. Each run is its own process, `env -i` with `PATH` (venv bin, node, system), `HOME`, `TMPDIR`, `LANG`, `ZF_DATA` (inside the owned scratch directory) and `PYTHONPATH`. No `ZF_*` SQL, Azure, model or benchmark variable is set. Scratch directory is recorded in `/tmp/i440-1110-scratch.txt`; venv at `<scratch>/venv`.

| Id | Dir | Selection | Purpose |
| --- | --- | --- | --- |
| P | repo | import-origin and version proof | Packages and test modules come from this worktree |
| R1 | `src/core`, `PYTHONPATH=tests` | `test_form_dependencies test_form_review test_form_review_pack test_form_export test_form_staging` | Finance held report, dependency, retained history, legacy Invalid-and-regenerate (PR 1345) |
| R2 | `src/api`, `PYTHONPATH=../core/tests:../agents/tests:tests` | `test_form_staging_api` | Complete current finance API form and CSV regressions |
| R3 | `src/core`, `PYTHONPATH=tests` | `test_resident_decisions` | Default-unconfigured DENY, approval evidence and binding mutation rejection, JSON and SQLite; SQL Server class skipped by design (PR 1346) |
| R4 | `src/orchestrator`, `PYTHONPATH=../core/tests` | `discover -s tests` | Four-image fake build, tag, verification, explicit mapping, failure and resume, no-I/O dry run (PR 1348) and the other orchestrator tests |
| R5 | `src/api`, same as R2 | `test_timecapture test_timecapture_copy` | Time capture default off, DPIA, notice, manual boundary and copy (PR 1343); browser class skipped without opt-in |
| R6 | `src/api`, same, `ZF_BROWSER_TESTS=1` | `test_timecapture_copy.StaffTimeGuidanceBrowser` | Opt-in loopback Chromium copy journey, external routes aborted |
| R7 | `src/api`, same | `test_case_journey test_role_matrix test_workbench` | Synthetic served staff boot, roles, error and manual paths |
| R8 | `src/core`, `PYTHONPATH=tests` | `test_scenario_manifest test_needs_inventory test_version test_dependency_rule` | Public manifest and needs inventory integrity, core boundary |
| R9 | each of api, agents, orchestrator, importer | `test_version test_dependency_rule` (api); `test_dependency_rule test_version` elsewhere | Package boundary and version identity, exact per project |

Counts are taken from the unittest `Ran N`, `OK`, `skipped=` summary and `-v` lines. SKIP reasons are read from `-v`. Each log is hashed. Exit codes are recorded from the producer.

Stop conditions: a product failure stops widening for that area and is preserved; no rerun to obtain a pass. An environment fault (missing tool, path) is corrected once and the first log is kept.

Allowed writes after the runs: cutover-evidence-pack (append), reference README (index sentence), reference log (append), and own RPI records.
