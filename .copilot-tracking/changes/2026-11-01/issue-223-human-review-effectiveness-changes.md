---
title: Issue 223 human-review effectiveness changes
ms.date: 2026-11-01
---

## Changes

* Added `src/agents/src/zava_forward/agents/review_effectiveness.py` (panels, controlled gate, report, CLI).
* Added `src/agents/evals/review_effectiveness_golden.json` (4 seeded defects, 2 controls, all with valid citations).
* Added `src/agents/tests/test_review_effectiveness.py`; documented the command in `src/agents/README.md`.

## Validation

* ruff check, ruff format --check and mypy clean in `src/agents`; `test_review_effectiveness`, `test_ai_eval`, `test_chat_eval` pass (44 tests).
* Full `unittest discover` in a fresh venv fails on a pre-existing duplicate `test_dependency_rule` module name between core and agents tests (unchanged by this work).
* No heavy local gate run; CI is the evidence.

## Divergences

None from the plan.
