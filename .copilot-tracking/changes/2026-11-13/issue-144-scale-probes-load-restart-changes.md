# Changes: Issue #144 scale, probes, load and restart (local slices)

* Plan: [plan](../../plans/2026-11-13/issue-144-scale-probes-load-restart-plan.md)

## Added

* `infra/tests/test_container_hosting_completeness.py`: 11 source-contract tests over every declared Container App and job.
* `src/api/tests/test_scale_fixture_load_and_restart.py`: 4 tests plus a CLI benchmark (separate API process, concurrent load, SIGKILL restart, audit chain check).
* `docs/architecture/scale-restart-2026-11-13.json`: unedited benchmark output (60,000 homes, 20 clients, 62 s).

## Modified

* `infra/README.md`: hosting table rows for criteria 2, 4 and 5 and a dated "Separate-process load and restart run" section.
* `src/api/README.md`: Tests section paragraph.
* `docs/reference/log.md`: appended entry.

## Not changed

`infra/main.bicep`, `infra/modules/operationalMonitoring.bicep`, `infra/modules/storage.bicep`, `infra/modules/containerapps.bicep` (frozen #79/#146 candidates).

## Divergences

None from the plan. No criterion ticked.
