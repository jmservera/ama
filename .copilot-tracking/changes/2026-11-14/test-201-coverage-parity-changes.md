---
title: Issue 201 coverage baseline parity changes
ms.date: 2026-11-14
---

Refs #201.

* Added `tools/test_src_coverage_baseline_parity.py` (11 tests).
* `docs/architecture/cutover-evidence-pack.md` unchanged (PR #1618 stays conflict-free).
* Validation: `python3 -m unittest tools.test_src_coverage_baseline_parity -v` OK (11 tests); `ruff check` and `ruff format --check` pass.
* No divergences from plan. Hosted CI not observed.

## Correction Cycle 1

* Replaced the vacuous `>= 0` threshold check with a `> 0` guard and removed the unrelated rubric `>= 48` check.
* Added `ExecutableDiscoveryParity`: per-project `unittest.TestLoader` discovery (no execution) across core, agents, api, orchestrator and importer. Measured 5,570 discovered and 4,783 non-skipped tests; asserts discovered > 7x and non-skipped > 6x the v0.21.0 719-test baseline (719 includes 92 skips; non-skipped is 6.65x, so 7x is not claimed for it).
* Validation: `python3 -m unittest tools.test_src_coverage_baseline_parity -v` OK (11 tests, ~13s); `ruff check` and `ruff format --check` pass.
* Scope stays `Refs #201`: measured line/branch coverage and hosted CI comparison remain open.
