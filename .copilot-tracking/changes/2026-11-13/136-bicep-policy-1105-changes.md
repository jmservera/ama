---
title: Issue 136 changes
ms.date: 2026-11-13
---

Tracking-only change log (Refs #136, #137, #360, #110, #142). No edits to infra/, src/ or docs/. Base 3b05143179f83235c5b4e80e70aad99bdc44d83f.

## Environment

* Venv /tmp/venv-136pol-1105 with `--system-site-packages`; setuptools and wheel upgraded in the venv; `pip install --no-deps --no-build-isolation -e` for src/core, agents, api, orchestrator, importer (since removed).
* Verified `zava_forward.<pkg>.__path__[0]` for all five lies under this worktree's `src/<pkg>/src/`.
* Env: PYTHONDONTWRITEBYTECODE=1, REQUIRE_AZ_BICEP=1, AZURE_BICEP_USE_BINARY_FROM_PATH=true, AZURE_BICEP_CHECK_VERSION=false. No az login, what-if, Docker or cloud calls.

## Results (from infra/tests, `python -m unittest <module>`, producer exit code saved directly)

| Module | Tests | Skips | Duration | Exit | sha256 of raw output |
| --- | --- | --- | --- | --- | --- |
| test_staff_azure | 74 | 0 | 6.2s | 0 | 2c04e1cbc6d85f7cc7b22c5a121eb6ca47c0ecccabd15b404939666e5772facf |
| test_identity_rbac | 12 | 0 | 0.03s | 0 | 1e56d4a82a95e20708b5562efba64112ed1eff20782a4aad077508a369ab2380 |
| test_private_cutover_proof | 20 | 0 | 14.8s | 0 | 9237456ee4848cdcd44469cab3c4868f0c19793e79b551c31db6caf74807fe8b |
| test_bicep_policy | 61 | 0 | 118.9s | 0 | 58d07aa4e9690ea005ac9f723d55dcdf18ff13ae418f807f33a080adce53ed50 |

## Findings

* No genuine defects: all four Wave-1 gaps were environmental (missing system-site packages and editable installs; the policy timeout was CPU contention, 119s on an uncontended run, within the 240s allowance).
* Focused tier only; this is not a complete local gate or hosted CI result.

## Cleanup

Venv and /tmp outputs removed; no egg-info or bytecode left in the worktree.
