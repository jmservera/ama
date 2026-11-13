---
title: Research for issue 216 criteria 4 and 7 (paired comparison, cost, cards alone)
ms.date: 2026-11-13
---

## Scope

Issue #216 unticked criteria 4 and 7 (body and 8 comments read via `gh issue view 216`).
Disposition: `executed`. Planning Readiness: `Ready`.

## Evidence

* `src/agents/src/zava_forward/agents/paired_trial.py`: `evaluate_paired_trial` scores
  per-role gains, a separate critical chat hazard-miss check, and `cost_per_accepted_check`
  (Unknown with named missing inputs; `authorise_model_run` gate). Recommendation is
  `cards_only` unless thresholds are agreed and every role shows gain.
* `src/agents/src/zava_forward/agents/regulatory_gates.py`: `comparison()` (committed report)
  carries `economics` (core `regulatory_usage.economics`, cost Unknown, four missing inputs)
  but not beside the citation validity, refusal accuracy and hazard-miss results.
  `evaluate_answers` yields `citation_validity`, `answer_contract`, `refusal_accuracy` checks.
* `src/agents/evals/run_regulatory_gates.py`: constructed-observation consumer; no
  thresholds, no cost inputs, so always cards only.
* `src/core/tests/test_rulecards.py` and the paired fixtures cover deterministic cards with
  card and provision links (`test_regulatory_gates` asserts links on every baseline card).
* README `src/agents/README.md` 2026-10-16 audit and 2026-11-03/10 sections record both
  criteria as unmet in full.

## Gaps

1. Cost per accepted check is not reported in one block beside citation validity, refusal
   accuracy and hazard-miss results, in either `evaluate_paired_trial` or the committed
   `comparison`.
2. `evaluate_paired_trial` can recommend `chat_value_measured_owner_decision_required`
   while cost is Unknown, and without any citation validity or refusal accuracy result:
   value is not shown "at its cost" and the gates are not consulted.
3. `cost_per_accepted_check` checks only presence of price fields: an undated or future
   `as_of`, blank `id` or `currency` still yields a number. A known dated cost must be a
   dated, past, identified price.
4. No tests for: cards beat or tie chat with links, chat adds cited value at a known dated
   cost beside the gates, failed citation or refusal gate, or an undated price.

## Constraints

* No live spend authority, no price invented, no gate weakened (`test_ai_call_site_inventory`,
  `test_content_standard`, `test_accessibility_baseline` untouched).
* Report-engine output stays free of live calls; owner thresholds remain unset.

## Follow-ups (candidate)

* Owner thresholds, real staff trial, independently graded set remain external.
