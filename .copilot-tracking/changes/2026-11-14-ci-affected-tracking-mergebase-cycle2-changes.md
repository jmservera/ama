---
title: ci-affected Cycle 2 formatting correction changes
ms.date: 2026-11-14
---

## Changes

* Root cause: CI `src-namespace` runs `ruff format --line-length 100`; Cycle 1 used the default 88.
* Reformatted `tools/ci-affected.py` and `tools/test_ci_affected.py` with `ruff format --isolated --line-length 100`. `tools/rpi-checks.py` and `tools/test_rpi_checks.py` were unchanged.
* No behaviour change. Original Cycle 1 artifacts preserved.
