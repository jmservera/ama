---
title: "Review: #164 criterion 3 memory poisoning and prompt injection gate"
ms.date: 2026-11-13
task_slug: 164-memory-poison-injection-2035
---

Review executed once (independent `code-review` agent) on the uncommitted working tree built on `c13d077d2`. Outcome: one medium finding, routed to later work; no logic holes in the gate code.

## Findings

| # | Severity | Finding | Routing |
| --- | --- | --- | --- |
| 1 | Medium | The new `ACTION_CLAIM` clauses match the words alone, so honest conditional or negated-by-context replies ("Visit cannot proceed without consent on file", "There is no written consent on file", "Proceed only once consent is given") are withheld. The direction is fail-safe (withhold, never approve) and consistent with the existing "consent has been recorded" clause. | Follow-up: tighten with condition/negation exclusions (`without`, `if`, `once`, `until`, `required`, a wider `no`/`not` window) and add legitimate-sentence tests; owner of a later `rpi-implement` |
| 2 | Info | `criterion_three` and `enablement_decision` fail closed on missing, malformed or disagreeing fields | None |

## Boundary

Scripted, component-scope evidence only. Enablement stays `insufficient`/disabled. Criterion 3 on issue #164 is not ticked here; that and GitHub edits are owner decisions.

## Follow-ups (ranked)

1. Tighten the new `ACTION_CLAIM` clauses against conditional/negated-by-context phrasing (finding 1).
2. Integrated memory poisoning in the serving prompt remains "not covered" (the panel prompt excludes memory).
3. Actual-model adversarial evidence under a finite authorisation.
