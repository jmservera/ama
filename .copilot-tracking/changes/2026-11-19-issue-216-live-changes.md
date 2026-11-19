---
title: Issue 216 live changes, 2026-11-19
description: Changes record with per-criterion table
ms.date: 2026-11-19
---

No source change. Tier FOCUSED (no `src/` edit); mypy, ruff and `rpi-checks.py` are not applicable and were not run. Added only dated `.copilot-tracking/` artifacts. Refs #216.

Validation: `python3 -m unittest test_regulatory_gates test_regulatory_citation_card_gates test_ai_eval test_paired_trial test_gate_agreement test_regulatory_eval_gates_216` from `src/agents`, 100 tests OK. No Azure or model call today.

| Criterion | Status | Basis |
| --- | --- | --- |
| Citation validity and refusal accuracy gates set with owners and measured on a graded and adversarial set | Proven for the demo, with limits | [eval-gates-live-216-2026-11-18.md](../../docs/reference/research/eval-gates-live-216-2026-11-18.md): refusals 10 of 10, cited model answers 9 of 9 valid, adversarial 10 of 10, 30 declared prompts, raw output kept; gate tests pass today |
| Hazard misses on seeded cases are critical (ticked) | Not re-proven | Covered by gate tests in today's run |
| Rule recall baseline before thresholds (ticked) | Not re-proven | Not re-run |
| Paired comparison, cards alone if no value (ticked) | Not re-proven | `test_paired_trial` passes |
| Out-of-cadence cards labelled (ticked) | Not re-proven | Not re-run |
| Results per check (ticked) | Not re-proven | Gate tests pass |
| Tokenomics: cost per accepted check or Unknown (ticked) | Not re-proven | Not re-run |
| Tokenomics: finite owner-authorised limits (ticked) | Not re-proven | Not re-run |
| Production: named Legal and Compliance owners, independent grader, multi-case set, rule-card citation validity | Unproven, not demo-provable | Waived for the demo by owner decision 2026-11-18; regulatory chat role unavailable to test account |

Result: no unmet demo criterion.
