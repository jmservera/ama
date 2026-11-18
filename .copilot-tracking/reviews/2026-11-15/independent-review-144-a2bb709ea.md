---
title: Independent Exact-Head Review for Issue #144
ms.date: 2026-11-15
---

## Scope and Candidate

* Issue: `#144` (Container Apps hosting, scaling, revision management and container hardening)
* Branch: `feat/infra-144-container-hardening` (stacked onto `feat/demo-164-chat-grounding-provenance-0900`, `PR #1641`)
* Assessed Commit: `a2bb709ea21abcfa18bd4c2322cee97a8edbd329`
* Base Commit: `971cc68fc`

## Independent Verification Summary

1. **Functional & Security Review**:
   * `src/importer/src/zava_forward/importer/__main__.py` adds a deterministic `run` subcommand that enforces `enforce_from_env()`, validates `IMPORT_QUEUE`, `https` `QUEUE_ENDPOINT`/`BLOB_ENDPOINT`, `SQL_SERVER`/`SQL_DATABASE` under `ZF_STORE=mssql`, and fails closed if `ZF_IMPORT_DISPATCH` is set outside standby/off.
   * All 6 `src/` Dockerfiles (`api`, `agents`, `orchestrator`, `importer`, `resident-demo`, `live-simulator`) declare `TMPDIR=/tmp`, `PYTHONDONTWRITEBYTECODE=1`, and `USER 10001:10001` with `/app` remaining root-owned.
   * `infra/modules/containerapps.bicep` wires `importJob` with `command: ['python', '-m', 'zava_forward.importer']`, `args: ['run']`, and `ZF_STORE: 'mssql'`, and adds `@minLength(1)` on all four workload image parameters while preserving stage-1 bootstrap defaults in `infra/main.bicep`.
   * `infra/scripts/pipeline.py` builds and verifies `release-manifest.json` binding all 4 project images and 7 hosted workloads to immutable `@sha256:` digests and `HARDENING_CONTRACT`, and `infra/scripts/deploy.py` blocks `--apply` with placeholder or `:latest` image overrides.
   * `infra/scripts/staff_azure.py` and `infra/scripts/staff-azure-worker.py` enforce `ZF_CONTAINER_HARDENING=enforced` and `/tmp` + `/state` `EmptyDir` mounts on dynamic staff jobs.
2. **Validation Executed**:
   * `python3 -m ruff check` and `python3 -m ruff format --isolated --line-length 100 --check` on all 12 modified Python files: passed (`0` issues).
   * `mypy` on `src/importer` (`16` source files) and `mypy --strict infra/scripts/pipeline.py`: passed (`0` issues).
   * `TMPDIR=/dev/shm PYTHONPATH=src/core/src:src/importer/src:infra/scripts python3 -m unittest src/importer/tests/test_cli_run.py infra/tests/test_container_hosting_144.py infra/tests/test_pipeline.py infra/tests/test_deploy.py infra/tests/test_staff_azure.py -q`: `Ran 150 tests in 42.556s — OK`.
   * `python3 infra/scripts/bicep_inventory.py --check`: passed.

## Verdict

* **Verdict**: `PASS`
* **Blocking Findings**: `0`
