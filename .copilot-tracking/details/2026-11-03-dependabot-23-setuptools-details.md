---
title: Dependabot alert 23 setuptools phase details
ms.date: 2026-11-03
---

## Phase 2: slice decision

* Keep `src/build-requirements.in` and `.txt` at setuptools 84.2.1.
* Do not edit source, hashes or pyproject floors (`>=77` is a floor, not a pin).

## Phase 3: validation

* Hash-checked install of the pinned build requirements and wheel builds of core, agents and importer. See the research file for results.
* ruff, mypy and unit tests: not run, because no Python source changed.
