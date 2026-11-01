---
title: Issue 223 human-review effectiveness changes
ms.date: 2026-11-01
---

## Changes

* Added `src/agents/src/zava_forward/agents/review_effectiveness.py` (panels, controlled gate, report, CLI).
* Added `src/agents/evals/review_effectiveness_golden.json` (4 seeded defects, 2 controls, all with valid citations).
* Added `src/agents/tests/test_review_effectiveness.py`; documented the command in `src/agents/README.md`.

* PR #638 review follow-up: edits now carry the full corrected statement (supported claims plus required topics); `replacement_effective` validates the final text and feeds the gate, detection, correction and `uncorrected_defects` metrics; reports keep per-case `source_hashes`; the workflow-only baseline runs one review per proposal with the same effort model; added negative tests for ineffective edits.
* CI fixes: registered the golden in `src/agents/evals/registry.json` and `provenance-register.json` (DS-REVIEW-EFFECTIVENESS) and labelled its description as constructed and synthetic.
* Second PR #638 follow-up: seeded runs fail when `ai_run` does not return AI output (for example `ZF_AI=off`); `replacement_effective` compares complete semicolon-delimited statements, so numeric prefixes such as `120` or `10` no longer pass; edited controls are validated against source facts in the gate; tests added for each.

* PR review round 4: `review_effectiveness.py` gate requires the reason to name the seeded discrepancy topic and its source; `_origin` keeps the original citable label for aliased topics. Two regressions added to `test_review_effectiveness.py`.

## Validation

* ruff check, ruff format --check and mypy clean in `src/agents`; `test_review_effectiveness`, `test_ai_eval`, `test_chat_eval` pass (44 tests).
* CI-equivalent agents run (`PYTHONPATH=src/core/tests`, `unittest discover`, ruff, mypy) passes: 132 tests; core provenance and form-review tests pass.
* No heavy local gate run; CI is the evidence.

## Divergences

None from the plan.
