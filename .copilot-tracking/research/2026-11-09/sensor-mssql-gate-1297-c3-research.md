---
title: Research - #1297 correction C3 (direct shared dependencies of the sensor MSSQL suite)
date: 2026-11-09
---

## Brief

* Purpose: verify and resolve the C2 independent Revise: `changed_groups(["src/core/tests/dataset.py"], [])` selects project-core but not mssql while the sensor MSSQL suite depends on dataset.py. Posture: focused, inline, no delegation.
* Start state verified: HEAD 1cc88544284744efce20ae7a42458e15473b2768, tree fc525f97c5b3f9ad5ed1d18db92436d287e698b5, base fa7ae0c97; `git status --short --ignored` shows only retained ignored tools/__pycache__/.
* Preserved historical evidence: C2 full receipt /tmp/ama-g1297-c2-1109/receipt.json (SHA-256 e7b55e62bc5a5096a7ba662f3692914d5eaeaac3ede1d13ee561f158d094b2e2), valid for C2 only.
* Non-goals: weakening the full gate, #184 items, other worktrees.

## Findings

* C1: Direct first-party imports of test_sensor_analysis_mssql.py, test_sensor_analysis_store.py and sensor_consumer_fixture.py were enumerated by AST and each passed to `changed_groups` (tools/rpi-checks.py `changed_groups`). 15 of 17 resolve to mssql. Two do not: `src/core/tests/dataset.py` (imported by the fixture, which deep-copies `dataset.DATA` to seed the suite) and `src/core/src/zava_forward/core/synthetic/__init__.py` (imported by `from zava_forward.core.synthetic import ...` in the store test and the fixture). Both are direct dependencies missed by the C1 `sensor` keyword rule.
* C2: The transitive static first-party closure of the suite is 67 of 128 core src modules plus 7 test modules, because dataset.py imports store.py and workflows.py, which import most of core. A closure-derived rule would therefore select mssql for roughly half of core runtime changes, which is a cost/coverage policy shift, not a minimal fix.
* C3: check_skips has no selection context; receipt verification recomputes the selection from the diff via changed_groups, so a corrected selection rule is enforced at both runtime and receipt verification without receipt-format change.
* C4: Honest limit: transitive modules such as store.py are already selected by the existing store keyword; others in the closure (for example workflows.py, ai.py, ledger.py) are not selected and remain a residual.

## Alternatives

* A. Add an explicit, named tuple of the suite's direct non-sensor-named dependencies (dataset.py, synthetic/__init__.py) to the mssql selection, plus a regression test that derives the suite's direct first-party imports by AST and requires each to select mssql (so future direct-import drift fails the test). Selected: minimal, evidence-based, covers every direct dependency, makes no closure claim.
* B. Select mssql for every project-core change or for the full static closure. Not chosen: roughly half of core runtime (or all core) changes would start the SQL container in focused runs; a cost/coverage policy decision for the owner. Reported as an alternative.
* C. Make check_skips require mssql executed. Rejected: focused core runs without mssql would then always fail discovery.

## Decision state

Research disposition: executed. Planning Readiness: Ready for A; B is reported as an owner policy option, not decided.
