# Review: Issue #144 scale, probes, load and restart (local slices)

* Review execution: executed once, after implementation. Critique: one final-candidate critique, executed inline (no Bicep edits, so frozen candidates are not touched; text-based Bicep parsing is the main fragility).
* Outcome: conformant for the stated local slices; hosted criteria remain unmet by design.
* Tier: focused (no workflow, Dockerfile, dependency, permission, secret, deployment, security-control or Bicep change).
* Plan: [plan](../../plans/2026-11-13/issue-144-scale-probes-load-restart-plan.md); changes: [changes](../../changes/2026-11-13/issue-144-scale-probes-load-restart-changes.md).

## Validation actually run (pip venv `/tmp/venv-144-2315`, removed afterwards; no `uv`)

| Check | Result |
| --- | --- |
| `infra/tests` full discovery | 527 tests, 2 errors from missing `zava_forward.orchestrator` and `yaml` in the fresh venv (environment, not code); after installing both, `test_bicep_policy`, `test_pipeline`, `test_container_contract`, `test_container_hosting_completeness`: 111 OK |
| `src/api` `test_scale_fixture_load_and_restart`, `test_scale_load`, `test_restart_audit` | 12 tests OK |
| `src/core` `test_scenario_manifest`, `test_needs_inventory` | 19 tests OK |
| `ruff check .` and `ruff format --check .` in `src/api` | passed; 156 files formatted |
| `mypy` in `src/api` | 66 playwright import errors until the `playwright` dev extra was installed; then "no issues found in 240 source files" |
| New infra test file | `ruff check` and `ruff format` clean (root default config) |

## Benchmark (local loopback, one process, not production scale)

60,000 homes, 53,821 events (declared 600,000 not met), 20 closed-loop clients, 62 s: 236 requests, error rate 0, p50 4.8 s, p95 9.5 s (over NFR-002 thresholds), RSS 614 MiB (high-water 622 MiB, limit 1 GiB), cold start 5.6 s. SIGKILL restart: 3 audit entries kept, chain intact, new write accepted, chain intact at 4 entries. Record: `docs/architecture/scale-restart-2026-11-13.json`.

## Findings routed to later work (none open in this task)

1. Hosted load, rollback and restart receipts need authorised Azure and the #138 pipeline.
2. Dashboard and list p95 far exceed NFR-002 at 60,000 homes in one process.
3. Infra Bicep parsing is text-based; a Bicep build/what-if check would be stronger but needs tooling.

## Not claimed

No Azure, hosted replica, autoscaling, production scale, deployed rollback, or criterion tick. Human and hosted CI review remain required; not pushed.
