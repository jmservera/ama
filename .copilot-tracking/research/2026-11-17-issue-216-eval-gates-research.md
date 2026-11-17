---
title: Issue 216 research, regulatory evaluation gates
date: 2026-11-17
---

# Research: issue 216

Opened. Inventory so far (base eb51af5c9): `src/agents/src/zava_forward/agents/regulatory_gates.py` (pure grader),
`regulatory_eval.py`, `src/agents/evals/regulatory_gates_cases.json` (24 cases, 17 expected refusals),
`regulatory_gates_results.json`, `src/agents/tests/test_regulatory_gates.py` (17 tests) and
`test_regulatory_answers.py`. Baseline measurement: with `PYTHONPATH` set to the worktree
`src/agents/src:src/core/src:src/core/tests:src/agents/tests`, `test_regulatory_gates test_regulatory_answers
test_eval_registry` ran 34 tests OK. Without it the installed non-editable `zava-forward-agents` copy is stale and gives 2 errors
(`comparison()` signature); that is an environment fact, not a repo defect. Criterion 1 owner sign-off is a human gate.

## Findings

Reproduction: a 22-question adversarial probe of `regulatory_chat.refusal` (case, soft hyphen, fullwidth text, compound
"lookup plus approve", legal-permission, hold removal, PII extraction) gave zero unsafe non-refusals and both
positive controls answered. No defect to fix. Planning readiness: Ready. Gap: the shipped frozen cases cover zero-width
obfuscation but not case, soft-hyphen, fullwidth or compound-question variants as a named regression.
Out of scope: owner-threshold sign-off (human), live staff trials, core store, chat grounding (#1818/#1641).
