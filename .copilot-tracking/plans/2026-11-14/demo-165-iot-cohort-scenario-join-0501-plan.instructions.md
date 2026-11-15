<!-- markdownlint-disable-file -->
# Plan: Epic 165 IoT, cohort and scenario join parity (2026-11-14)

Refs #165. Research: [research](../../research/2026-11-14-demo-165-iot-cohort-scenario-join-0501-research.md). Details: [details](../../details/2026-11-14/demo-165-iot-cohort-scenario-join-0501-details.md).

* [x] Phase 1: add `src/core/tests/test_epic165_iot_cohort_scenario_join_parity.py`
* [x] Phase 2: run scenario manifest, needs inventory, synthetic and epic165 suites in core and importer, ruff check, ruff format --check, mypy
* [x] Phase 3: commit on the stacked child branch without pushing

Critique: one pass, final candidate. Verdict: no blocking findings. Direct dispositions: do not invent a stock-to-case mapping (applied: namespaces asserted disjoint); tolerate the register's deliberately messy EPC casing and spacing by normalising before comparing (applied); keep cohorts small for speed (applied). No conflict with confirmed decisions.
