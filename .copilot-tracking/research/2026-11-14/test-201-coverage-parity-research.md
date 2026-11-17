---
title: Issue 201 coverage baseline parity research
ms.date: 2026-11-14
---

Refs #201. Disposition: executed. Planning Readiness: Ready.

## Evidence

* `docs/architecture/cutover-evidence-pack.md` (read-only): historical matrix baseline 719 tests with 92 skips; complete suites core / API / agents / orchestrator / importer = 504 / 549 / 70 / 22 / 39 before main integration; statement that equal-or-greater measured coverage is not established; criterion 4 UNMET pending candidate-commit CI. Archive tag `v0.21.0` (`README.md`).
* `.github/workflows/src-ci.yml`: matrix runs all five projects with `python -m unittest discover -s tests -v`. No `ci-affected.yml` exists; affected selection is `tools/ci-affected.py`.
* `tools/rpi-checks.py`: `PROJECTS` lists the five projects; each gets a `project-*` group with unittest discovery.
* `src/*/pyproject.toml`: no coverage `fail_under` or branch settings in any project; `test_branch_floor` modules in agents and api are unittest fixtures, not thresholds.
* `.github/rubric/scores/latest.json`: total 79, outcome Pass with Merit (baseline snapshots 47 and 48).
* Static test-method counts now: core 2480, agents 484, api 2209, orchestrator 142, importer 116 (5431).

## Conclusion

Count and wiring parity are provable offline. Threshold parity is vacuous because no threshold exists; measured coverage equivalence cannot be proven and must stay disclosed.
