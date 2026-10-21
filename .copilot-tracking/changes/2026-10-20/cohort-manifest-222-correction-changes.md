<!-- markdownlint-disable-file -->
# RPI Changes: correction continuation for the #222 cohort manifest (v0.2.0)

## Metadata

* Task ID: 222 (continuation of the original loop; no second original Review)
* Original artifacts preserved unchanged: research, plan, details, critique, changes and the single Review under `.copilot-tracking/`
* Authority: owner comment 6295248053 and PR421 comment 6295248627 (2026-10-20): correction only, return the revised manifest for owner approval before evaluator work
* Base: reviewed main 993a7b88c03f5240f1e7a4c7c7afa7c064281622; starting head 2027f7260583117a20bf8cea8b3186c2b2d1dc59 (bot score commit). The earlier ba989bb0 receipt is historical and invalid for the current head.

## Process disclosure (coordinator intervention, 2026-10-20)

The first correction edits (manifest, test, review pack, README, log, this record, state, commit 073d37de) were authored directly BEFORE the `rpi-implement` skill was activated. A coordinator audit found this. They are retained, unrewritten, as an UNVERIFIED correction draft. `rpi-implement` was then actually invoked in this continuation (plan section P05 appended) and the draft reconciled against the plan below. Gate run manifest-03 was BLOCKED by an ignored ruff cache (removed, exact path); run manifest-04 started on the draft head and is superseded by any later commit. The original research, plan, critique, changes and single Review are untouched; no second original Review exists.

## Gate history (adverse receipts retained, external)

* manifest-03: BLOCKED, ignored ruff cache from my own run (exact path removed).
* manifest-04: interrupted by the coordinator intervention (signal 15); failed receipt retained.
* manifest-05 (head 382c13fb): FAILED in project-agents strict mypy, seven type-annotation errors in the new test. Fixed with typed signatures; mypy strict, ruff and 9 tests pass locally.
* P05-T03 stays unchecked in the plan: the final receipt is external and cannot be committed after the gate, so it is reported in the handoff.

## Disposition of PR inline findings and original Review findings

| Finding | Disposition |
| --- | --- |
| PR 4326877212 fresh held-out scenarios | Fixed: manifest `held_out_split.fresh_scenario_rule` and review pack require new IDs and inputs; no CM- ID reuse; roles UNFILLED |
| PR 4326877335 review burden denominator | Fixed: share is review_required / eligible, zero eligible not computable, counts retained; test checks fractions |
| PR 4326877424 support exemption | Fixed: exemption limited to `support_state` pairs; regression proves an unrelated support change is rejected |
| RV-001 | Addressed: ranking bindings checked against unchanged `rank()` with a stated comparison basis |
| RV-002 | Addressed: CM-A03 representation_pending; CM-A04 captures adjustment-as-support |
| RV-004 | Addressed: top-k exception wording added; also corrected an over-claim that a safety case sorts first (it ranks behind older open safety cases) |
| RV-006 | Note only; persisted evidence is the fresh external gate receipt |
| RV-003, RV-005 | Not in scope; original Review text unchanged |

## Owner-directed changes

* Retained three factor families; split CM-A03 and CM-C01 (new CM-A04, CM-C02).
* PP-01 Unknown-support review priority is a POLICY PROPOSAL only; no ranking change.
* Arbitrary 30 and 0.10 replaced by SO-1 to SO-3 (29, 59, 149 from the exact zero-error bound), ED-1 to ED-3 and UM-1 to UM-3; zero critical misses stays proposed.

## Files

* src/agents/evals/cohort_manifest_draft.json, src/agents/evals/registry.json (v0.2.0)
* src/agents/tests/test_cohort_manifest_draft.py
* src/agents/README.md, docs/reference/research/evaluation/cohort-evaluation-review-pack.md, docs/reference/README.md, docs/reference/log.md (append)

## Validation

* Focused: 9 structural tests pass against core on PYTHONPATH; ruff check and format clean. Full gate receipt is external and recorded in the handoff.
* No runtime, ranking, evaluator, paid, live, participant or approval activity. All six #222 criteria remain unmet.

## Independent assessment correction (2026-10-21, P06)

Assessor f9636e1f on 93cb2bba found (1) the test conversion dropped sensor, source and appointment fields so six pairs reached `rank()` identically and an exclusion wrapper still passed, and (2) the wording "behind only older open safety cases" is wrong because policy 1.0.0 compares support before waiting days inside open safety. Both accepted; ranking and runtime unchanged. The gate receipt at /tmp/ama-followon-2240-222/receipt.json (SHA256 447cb4ea...) becomes HISTORICAL after the next commit. Details below are added as work completes.

### P06-T01 and P06-T02 completed

* Test: case conversion now carries sensor_data, source_record, appointment_history and contact_need; converted pairs are asserted to differ in the declared factor; new regression shows an exclusion wrapper (sensor or source missing or stale) and an appointment-penalty wrapper fail `check_binding` for CM-S01/S02/C01/C02 and CM-H01/H02, while the unchanged `rank()` passes. Representability limit: rank() has no sensor, source, appointment or contact input, so these bindings prove invariance of the unchanged ranker and detect wrappers; CM-A03 stays representation_pending.
* Ordering: manifest and review pack wording corrected; new test shows a supported open-safety case waiting 1 day outranks an unsupported one waiting 10 days, and rank 2 is fixture-specific.
* Validation: ruff check and format, strict mypy on the test, 24 tests (manifest and ai_eval) and the registry test pass locally. No heavy gate run (coordinator-owned).

## Dependency advisory integration (2026-10-21, P07)

* Trigger: local gate /tmp/ama-cohort-followon-0037-222 failed at 02:44:00; GHSA-6q48-6c7w-9gw2 on certifi 2026.7.22 (fixed 2026.10.19) in api, importer and orchestrator scans. Receipt and log retained.
* Reuse: only the four requirements.txt files from shared commit a3257c71 (native issue 119 correction), taken by path-limited checkout; its tracking and map edits not taken. Provisional until this issue's own full gate and independent assessment.
