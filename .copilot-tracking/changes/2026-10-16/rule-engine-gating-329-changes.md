---
title: RPI Changes - Rule engine gating regressions
description: Implementation evidence for issue 329
ms.date: 2026-10-16
---

## Task and Scope

Task ID: 329. Slug: rule-engine-gating-329. Full plan P01:
.copilot-tracking/plans/2026-10-16/rule-engine-gating-329-plan.md.
Details: .copilot-tracking/details/2026-10-16/rule-engine-gating-329-phase-details.md.
One independent critique passed with no findings.

## P01-T01: Regression Coverage

Complete. Original rule-engine suite: 17 tests passed. Initial
fresh-venv import failed because core was not installed; installed src/core[dev]
editable with pip and reran successfully. No dependency manifest changed.
Added three focused methods and tightened the existing source-gating method.
The existing engine passes all 20 tests; no production defect was demonstrated
and rule_engine.py is unchanged. Fixture card IDs are optional to exercise
independent card keys; a raw publication helper avoids filtered-view proxies.

* Exact consultation/historical/future not-applicable versus unknown results,
  citation metadata, no evaluator invocation and no persisted publication.
* Distinct-case and changed-due-time episodes on the same home, before and at
  the 24-hour boundary; every attempted check and checkpoint remains stored.
* Positive independent home/card/step/item keys and immediate cross-case breach
  escalation with acknowledgement/outcome requirements.

An initial new-fixture run exposed subtest reuse of the same episode across
different home IDs and time ranges. Isolated first-case IDs per scenario fixed
the test fixture; this was not a demonstrated production defect.

## P01-T02: Validation and Delivery

Local implementation, validation and documentation complete. Exactly one Review
executed, outcome Conformant, no findings:
.copilot-tracking/reviews/logs/2026-10-16/rule-engine-gating-329-review.md.
Branch/PR publication remains.

Validation uses a Python 3.12 pip venv in the session workspace, with
src/core[dev] installed editable. Commands executed from src/core:

```bash
python -m unittest discover -s tests -p test_rule_engine.py -q
python -m unittest discover -s tests -q
ruff check .
ruff format --check .
mypy
```

* Targeted: 20 tests passed.
* Full core: 466 tests run in 134.295 seconds, OK with one skip. The skipped
  AzureResidentDecisions test explicitly requires an isolated synthetic Azure
  SQL database and opt-in environment variable. No Azure accessed.
* Ruff lint passed; format check: 36 files already formatted.
* Mypy: no issues in 89 source files.
* Existing sensor-backfill ResourceWarnings were emitted; no unrelated edits.
* README contract/coverage, reference routing and append-only log updated.

### Mutation Evidence

Executed nine in-memory mutations against the installed module. Loaded source
into a separate module and temporarily patched citation_eligibility or
RuleEngine._publish. Each mutation required at least one AssertionError in
the targeted regression and zero unittest errors. No mutation was written to
package files. Test constants and fixture clocks were not altered.

| Mutation | Target regression | Assertion failures |
| --- | --- | --- |
| Remove consultation from the not-applicable status tuple | test_future_consulted_historical_partial_stale_and_missing_sources | 1 |
| Remove historical from the not-applicable status tuple | test_future_consulted_historical_partial_stale_and_missing_sources | 1 |
| Remove future-effective eligibility guard | test_future_consulted_historical_partial_stale_and_missing_sources | 4, including exact-result failure and retained-publication follow-ons |
| Disable shared attention throttle but retain episode deduplication | test_attention_limit_across_cases_and_due_time_episodes | 2 |
| Change shared throttle comparison from less-than to less-than-or-equal | test_attention_limit_across_cases_and_due_time_episodes | 2 |
| Omit home_id from shared throttle key | test_attention_throttle_keeps_home_card_step_and_item_independent | 1 |
| Omit card_id from shared throttle key | test_attention_throttle_keeps_home_card_step_and_item_independent | 1 |
| Omit step from shared throttle key | test_attention_throttle_keeps_home_card_step_and_item_independent | 1 |
| Omit item from shared throttle key | test_attention_throttle_keeps_home_card_step_and_item_independent | 1 |

The package implementation is already correct, so there is no genuine defect
to restore for a red/green fix. These removed-guard mutations demonstrate the
specific missing-test sensitivities requested by issue 329 rather than inventing
a production change to manufacture a red test.

## Amendments and Divergences

No material divergence. Added only three methods, below the six-method maximum.
Research reused from issue/source/test evidence; no external research needed.

## Blockers and Follow-Ups

None.
