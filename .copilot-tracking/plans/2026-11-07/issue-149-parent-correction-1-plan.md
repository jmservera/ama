---
title: Issue 149 parent corrective cycle 1, plan and critique
ms.date: 2026-11-07
---

## Plan (before any source edit)

* Reproduce red first: a Python counterexample replaying the current substring selection over cell rows containing the two correct rows plus a third failed-AI row with the sentence "Model result delivered."; it must show the old logic passes. Keep the output.
* Fix: in data_operator_ai_state.py add the Kind label constant, `failed_ai_rows(rows)` selecting by the Kind cell (exact label), and `says_failure_outcome(cell)`. In the browser check collect cell texts from the Items region rows with evaluate_all, select by Kind, require each synthetic ID exactly once, allow extra legitimate rows, validate each What happened cell.
* Tests in test_data_operator_ai_state.py: (a) kind label equals the label the real renderer prints in Kind column of the rendered rows; (b) third failed row with wrong or missing sentence is rejected while both synthetic rows pass; (c) a legitimate extra fallback row is accepted and total rows are not forced to 2; (d) a non-failed kind row is not selected.
* Validate from a fresh git-archive of the committed candidate with a new external venv or verified-identical reuse: unit (api modules), ruff and mypy from component cwd (checks/*.py format exclusion reported, not claimed), Node render via existing test. No browser, axe, SQL, Docker or runner.
* Commit source and tests, then the Review and state; later results external. Browser and axe on the final source stay pending for coordinator admission.

## Critique (once, prospective)

* Risk: test depends on the same rendered text. Applied: select by Kind label only; validate the other cell separately.
* Risk: scope creep. Applied: only the checker, helper and tests.
* Verdict: proceed.
