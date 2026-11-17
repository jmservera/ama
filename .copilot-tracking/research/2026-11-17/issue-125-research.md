---
title: Issue 125 research - optional discovery assistant
ms.date: 2026-11-17
---

## Scope

Assess issue 125 against main eb51af5c9 (evidence only, desktop demo-first). Reproduce first, then the smallest fix plus regression test. Out of scope: 1818/1641 (core mssqlstore, chat grounding).

## Opening state

* Delivered on main: discovery_assistant_boundary, _drafting, _evaluation, _demo modules in src/core and the discovery-demo CLI entry.
* Issue comments (2026-11-16 closure correction) restore all three criteria to unticked.

## Measurements (2026-11-17, main eb51af5c9)

* `/tmp/venv125/bin/python -m unittest tests.test_discovery_assistant_boundary tests.test_discovery_assistant_demo tests.test_discovery_assistant_drafting tests.test_discovery_assistant_evaluation` from `src/core`: 41 tests OK.
* First run used PYTHONPATH only and failed 1 of 41 (`test_demo_runs_from_this_worktree_without_inputs`): that test spawns a subprocess with a scrubbed environment and needs the package pip-installed (`pip install -e src/core`), as the repository instructions require. Environment cause, not a code defect; adverse first result preserved.
* `python -m zava_forward.core discovery-demo` reproduces: `query_approved_analytical_store` allowed read-only; `write_source_system`, `contact_resident`, `rank_properties` denied; `read_company_dataset` not on the allowlist; no tool dispatched.

## Assessment

* C1 readiness before company data: synthetic helpers keep connection false; needs accountable discovery owner, privacy and access approvals. Unmet, human-gated.
* C2 no operational write access: policy-level denial is reproduced on synthetic fixtures only; no observed access denial against a real operational system. Unmet.
* C3 manual and conventional comparison: the demo comparison is constructed arithmetic, not an actual human or BI comparison. Unmet.
* No reproducible defect found, so no source fix or regression test is justified (a test with no failing behaviour would restate existing coverage).

Planning readiness: Ready (evidence-only outcome).
