# Changes: issue-216-live2 (Refs #216)

Tier: FOCUSED. No `src/` change; documentation and evidence only.

## Files

* docs/reference/research/eval-gates-live-216-2026-11-18/unit-tests-raw-2026-11-18.txt: raw output of 101 existing gate tests (OK).
* docs/reference/research/eval-gates-live-216-2026-11-18.md: rerun section and per-criterion table.
* docs/reference/log.md: appended entry.

## Per-criterion proven/unproven (demo scope)

| Criterion | Status | Evidence |
| --- | --- | --- |
| Citation validity and refusal accuracy gates set with owners and measured on a graded and adversarial set | Partly proven | Gate logic and provisional 1.0 thresholds: 101 local tests OK (raw retained). Live case chat: refusals 10 of 10, model-path citations 7 of 7 (interval 0.646 to 1.0), 13 of 30 prompts not model-reached; container figures Observed; raw output not retained. Not shown to hold at 1.0. |
| Hazard misses on seeded cases are critical (ticked) | Not re-proven | Covered by the unit run only as gate logic (test_regulatory_gates). |
| Rule recall baseline before thresholds (ticked) | Not re-proven | Existing evidence. |
| Paired comparison, cards-alone fallback (ticked) | Not re-proven | test_paired_trial passes locally. |
| Out-of-cadence labelling (ticked) | Not re-proven | Existing evidence. |
| Results per check (ticked) | Not re-proven | test_gate_agreement passes locally (per-gate results). |
| Tokenomics criteria (ticked) | Not re-proven | Spend of earlier exercise exceeded the 45-call authorization; disclosed. |
| Named Legal/Compliance gate ownership, independent grader, larger set | Unproven, production-only | Needs named professionals; not demo-provable. |

No live Azure resource was created or changed in this task; no new model call was made.
