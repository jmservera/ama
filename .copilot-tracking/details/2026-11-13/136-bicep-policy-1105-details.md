---
title: Issue 136 details
ms.date: 2026-11-13
---

## Commands

* `python3 -m venv --system-site-packages /tmp/venv-136pol-1105`
* `/tmp/venv-136pol-1105/bin/pip install --no-deps -e src/<pkg>` for each of core, agents, api, orchestrator, importer (offline; if build isolation needs the network use `--no-build-isolation`).
* Path check: python -c printing `zava_forward.<pkg>.__path__[0]`.
* From infra/tests: `python -m unittest <module> -v > /tmp/out-<module>.txt 2>&1; echo $? > /tmp/rc-<module>`; test_bicep_policy under `timeout 240`.
* Cleanup: remove the venv, /tmp outputs after summarising, any `*.egg-info` created in src/ (check `git status --short --ignored`).

## Success

All four exit 0, or every failure classified with evidence. Hashes (sha256) of raw outputs retained in the changes log.

## Revisions after critique

* Environment for all runs: PYTHONDONTWRITEBYTECODE=1, REQUIRE_AZ_BICEP=1, AZURE_BICEP_USE_BINARY_FROM_PATH=true, AZURE_BICEP_CHECK_VERSION=false.
* Upgrade setuptools and wheel in the venv only (authorised), then `pip install --no-deps --no-build-isolation -e`.
* Delete only egg-info created by this run; confirm with `git status --short --ignored`.
