---
title: "Issue 212 research: deterministic rule engine and proactive step alerts"
ms.date: 2026-11-01
---

* Disposition: executed (repo evidence review). Planning Readiness: Ready.
* Task: 212 / rule-engine-step-alerts. Dependency #211 (rule cards) is closed.
* Delivered and merged: #328 (engine and scoped alerts), #334 (gating regressions), #630 (per-home grouping across cases).
* Code: `src/core/src/zava_forward/core/rule_engine.py` (`RuleEngine.run`, `alerts`, `disposition`); API routes in `src/api/src/zava_forward/api/server.py` (`_rule_alerts`).
* Criteria 1-6, 8, 9 are checked in the issue and covered by `src/core/tests/test_rule_engine.py` (27 tests, green) and `src/api/tests/test_rule_alerts.py` (6 tests, green).
* Criterion 7 (group per home, rank by clock and harm, rate-limit attention, track false positives) is implemented and proven at core level: `test_home_group_ranking_and_default_deny_roles`, `test_attention_limit_across_cases_and_due_time_episodes`, `test_attention_throttle_keeps_home_card_step_and_item_independent`, `test_breach_owner_ack_outcome_false_positive_history_no_suppression`.
* Gap: no HTTP-level proof that the shipped endpoint returns the grouped, ranked home list and the `precision` block (false-positive tracking). The API disposition route cannot record `false_positive` for Entra identities (documented roster-email limit), so the API test asserts the read contract only.
* Follow-ups: (1) UI surfacing of `precision` on the alerts panel; (2) human Compliance approval of rule cards remains outside code.
