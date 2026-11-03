---
title: Issue 212 per-card precision plan
description: Add per-card false-positive counts to the alert precision block
ms.date: 2026-11-03
---

Task: 212 / issue-212-precision-by-card. Plan status: Ready. Details:
[details](../../details/2026-11-03/issue-212-precision-by-card-details.md).

## Scope

* `rule_engine.py`: `_precision_by_card` and `precision.by_card`.
* `test_rule_engine.py`: assertions in the classification test.
* `src/core/README.md`: criterion 7 audit row.

## Critique (single pass, executed)

* Risk: precision read as proof of accuracy. Disposition: counts only, rate stays `null` until
  humans classify; README keeps the trial unmet.
* Risk: classification could suppress alerts. Disposition: read-only view, no suppression path.
* Verdict: proceed.

## Validation (focused)

core test_rule_engine and test_source_monitor, api test_rule_alerts, ruff check, ruff format
--check, mypy with `--cache-dir=/tmp/mypy-212`.
