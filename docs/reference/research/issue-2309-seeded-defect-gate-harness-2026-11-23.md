---
title: Issue 2309 seeded critical-defect gate harness evidence
description: Per-criterion proof that the existing #223 core harness seeds wrong, stale, unsupported and incomplete proposals and that the gate refuses each; synthetic demo only
ms.date: 2026-11-23
ms.topic: reference
---

## Scope and result

Issue #2309 asks for a core harness that seeds critical defects with valid
citations into workflow-only synthetic scenarios and asserts a controlled gate
refuses them. The harness already exists: `human_review_gate`, `evaluate_panel`
and `run_automation_bias_harness` in
`src/core/src/zava_forward/core/human_review_effectiveness.py`, tested by
`src/core/tests/test_human_review_effectiveness_223.py`. No source change was
needed. Synthetic demo data only; no Azure call was required. Evidence class:
`synthetic_harness_not_human_oversight_evidence`.

## Evidence

Run on 2026-11-23 from `src/core` with
`PYTHONPATH=src:tests python3 -m unittest -v tests.test_human_review_effectiveness_223`:
6 tests, OK.

| Panel | Detection rate | Gate passed (of 8) | Gate leakage |
| --- | --- | --- | --- |
| competent | 1.0 | 8 | 0 |
| default_accept | 0.0 | 0 | 0 |
| automation_bias | 0.1667 | 2 | 0 |
| citation_only | 0.0 | 0 | 0 |
| unauthorised_competent | 1.0 | 0 | 0 |

Gate leakage 0 means no seeded defect passed the gate unreviewed or ineffectively reviewed.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Test seeds each critical defect class on synthetic data and the gate refuses it | Proven | `test_seeded_defects_all_carry_valid_citations_across_tasks_and_classes` (8 scenarios, four classes plus control); `test_automation_bias_default_accept_citation_only_and_unauthorised_fail_gate` (gate leakage 0); `test_adversarial_gate_bypasses_and_staleness_fail_closed` |
| Default acceptance and citation validity alone fail the gate in a test | Proven | `default_accept` and `citation_only` panels: 0 of 8 pass; reason `citation_validity_alone_insufficient` asserted |
| Reviewer, source and reason are retained and asserted | Proven | `test_competent_panel_detects_all_defects_retains_evidence_and_compares_effort` asserts reviewer, reason, source hashes, retained evidence per scenario |
| Detection, corrections and review effort are reported for the same scenarios | Proven | Same test asserts detection rate 1.0, 3 corrections, 3 rejections, workflow, AI review and net effort seconds |
| No real participant outcome is claimed; human-participant criterion stays with #223 | Proven | `human_trial_complete` is False and the evidence class is synthetic; the human-participant criterion stays with #223 |

Ticking the issue boxes stays with the owner.
