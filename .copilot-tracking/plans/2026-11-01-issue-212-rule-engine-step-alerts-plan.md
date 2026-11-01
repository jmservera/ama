---
title: "Issue 212 plan: prove grouped, ranked, fatigue-tracked alerts over HTTP"
ms.date: 2026-11-01
---

* Research: .copilot-tracking/research/2026-11-01-issue-212-rule-engine-step-alerts-research.md
* Critique (single pass, inline): scope is test-only, no production change unless the test exposes a defect; no conflict with confirmed decisions; no resident messaging, model calls or clock changes. Verdict: proceed.

## Steps

* [x] Add `test_alerts_endpoint_returns_home_groups_ranked_with_precision` to `src/api/tests/test_rule_alerts.py`: report two hazards on one home via the API, read `/api/law/alerts`, assert one home group, ranking by due time then harm, `precision` keys with unclassified equal to total and null rate, and `usage.model_calls == 0`.
* [x] Run `test_rule_alerts`, `test_rule_engine`; ruff check, ruff format --check and mypy for touched projects.
* [x] Commit, push, open PR (no log entry: knowledge base unchanged).

## Non-goals

* No engine change, UI change, new dependency or mvp/prototype code.
