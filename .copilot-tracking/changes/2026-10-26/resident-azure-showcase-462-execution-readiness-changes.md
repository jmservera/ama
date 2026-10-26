---
title: Resident showcase 462 execution-readiness local source stage changes
ms.date: 2026-10-26
---

Written 2026-10-26 after the plan and critique dispositions in
`.copilot-tracking/plans/2026-10-26/resident-azure-showcase-462-execution-readiness-plan.md`.
Local source only. No cloud call, secret, password or session key was generated or read.

## Changes

* Expiry cutoff is now the exclusive UTC instant `2026-11-01T00:00:00Z` (through 31 October) in
  `resident_showcase.AUTHORITY_END`, `infra/sql/resident-showcase.sql`,
  `infra/scripts/resident_demo_secrets.py`, both READMEs and the tests that held the old 12:00Z literal.
  New test pins the exclusive boundary.
* New `infra/resident-demo.bicep`: identity, one Consumption app (min 0, max 1, digest image), two
  secret-scoped Key Vault Secrets User assignments, AcrPull on the registry, full runtime contract,
  ingress toggle, `ama` scope guard. No jobs, schedules, environment or vault role at vault scope.
  `ZF_STORE` is deliberately absent because the service refuses it as a forbidden prefix.
* New `infra/scripts/resident_demo_deploy.py`: what-if default, deny guard for any change outside the
  five resident-owned resources, typed-phrase apply, scale read-back, `--no-ingress` rollback.
* New `infra/tests/test_resident_demo_deploy.py` (12 tests, compiled template and command).
* `infra/README.md`: template, command, stop conditions, rollback, corrected statement that no extra
  Key Vault writer role is proposed (the Owner ARM write path is unproven against the private vault).

## Validation (venv /mnt/ama-rpi-gates/issue462-helper-correction1/venv)

* core showcase 37 tests, SQL 18 (13 skipped, no SQL Server), API demo 34, infra secrets 15,
  infra deploy 12, `test_bicep_policy` 48: all OK. Runner-style ruff check and format: clean.
* Not run: SQL Server, browser, image, mypy, full gate (heavy lock held by another session).

## Docker hygiene

Images created: none. Containers created: none. Nothing to dispose or retain.

## Open

G1 headroom, G2 live synthetic email provenance, G3 SQL principal/view, G4 private-vault write path,
hosted checks and coordinator assessment. The earlier gate receipt is stale for any new head.

## Correction 2026-10-26T13:45Z (coordinator-confirmed defect, implemented after the prospective brief in the plan)

* Defect: the compiled template contains the nested guard deployment `resident-demo-scope`, which
  `check_changes` refused, so a real what-if could not pass; my fake OWNED list omitted it.
* Fix: `check_changes` allows exactly that one deployment id; no other deployment is allowed. New
  regression `test_compiled_inventory_including_guard_passes_and_unknown_nested_is_refused`
  derives the compiled deployment resource, requires it in the owned set and refuses other nested
  deployments. OWNED fixtures now include the guard (6 resources).
* Docs: first operational stage must use `--no-ingress`; nothing is validated live; nested what-if
  shapes beyond this id are refused (official nested expansion format unverified).
* Tests: 29 infra resident tests OK; ruff check and format clean. The original review and its Low
  finding are unchanged; no new review was run (coordinator accepted this route).
* Docker: images and containers created: none.
