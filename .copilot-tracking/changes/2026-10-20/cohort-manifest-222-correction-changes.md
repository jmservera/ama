<!-- markdownlint-disable-file -->
# RPI Changes: correction continuation for the #222 cohort manifest (v0.2.0)

## Metadata

* Task ID: 222 (continuation of the original loop; no second original Review)
* Original artifacts preserved unchanged: research, plan, details, critique, changes and the single Review under `.copilot-tracking/`
* Authority: owner comment 6295248053 and PR421 comment 6295248627 (2026-10-20): correction only, return the revised manifest for owner approval before evaluator work
* Base: reviewed main 993a7b88c03f5240f1e7a4c7c7afa7c064281622; starting head 2027f7260583117a20bf8cea8b3186c2b2d1dc59 (bot score commit). The earlier ba989bb0 receipt is historical and invalid for the current head.

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
