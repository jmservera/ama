---
title: Research: C1 ruff correction (issue 144, PR 1672)
ms.date: 2026-11-14
---

* Task: correction cycle 1 of 5 for `infra/tests/test_container_hosting_completeness.py`.
* CI rule: `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` and `ruff format --isolated --line-length 100 --check`.
* Evidence: on the branch head the file passes both commands with ruff 0.17.3 and with the CI-pinned ruff 0.17.1 (venv, `--no-cache`); `ruff format --diff` is empty.
* The reported failure does not reproduce at this head; the file was already formatted by prior commit e21d4f979. Other infra files fail the isolated rules but are outside CI scope and this task.
* Environment note: `test_bicep_policy` needs `zava_forward.orchestrator` installed; used a venv with core, agents and orchestrator.
* Planning readiness: Ready (no source change needed).
