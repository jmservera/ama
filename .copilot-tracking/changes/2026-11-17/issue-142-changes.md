---
title: Issue 142 changes
ms.date: 2026-11-17
---

## Changes

* `infra/scripts/secret_lifecycle.py`: `check_secrets` now reports `uninventoried` for any listed vault secret absent from the inventory (sorted, names only).
* `infra/tests/test_secret_lifecycle.py`: `test_uninventoried_vault_secret_is_a_finding`.
* `infra/README.md`: one clause documenting the finding.

## Validation (FOCUSED)

* Before: `check` with an extra `stray-unowned-secret` printed nothing, exit 0.
* After: `stray-unowned-secret: uninventoried: ...`, exit 1.
* `cd infra && python3 -m unittest tests.test_secret_lifecycle tests.test_keyvault_secret_governance`: 29 tests, OK (28 before).
* `ruff format --isolated --line-length 100 --check` on the two Python files: reports reformatting both before and after the change (pre-existing; infra/ is not in the src-ci format step), so not a gate and not fixed here.
* mypy: not applicable, no `src/<project>` code changed. Browser harness, SQL, infrastructure, deployment: not touched.
* Heavy gate (`rpi-checks.py --all`) not run, per lock.

## Divergence

First `implement-start` witness call was refused ("missing persisted artifact evidence: changes") because the state lacked the changes pointer; fixed in state and retried successfully.
