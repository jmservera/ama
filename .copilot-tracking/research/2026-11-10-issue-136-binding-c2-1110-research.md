---
title: Issue 136 binding C2 research
description: Research for one bounded C2 fixing initial-candidate lint, format and typing regressions in the policy test
ms.date: 2026-11-10
---

## Execution and boundary

Research disposition: `executed`, 2026-11-10. Frozen C1 input `c6310ea91d2e32258b792b98f1bfdbe2e57ee511` (tree `4e37d5649942e0a373622246e107454b7b14162b`), base and target `d52f20a5198de7269f39daf794911545aee01ced`. Refs #136 and #1288 only. This consumes the second of five whole-issue cycles; no reset, no automatic C3. All earlier original and C1 artifacts are preserved unchanged.

## Independent disposition (input, not C2 approval)

The same independent reviewer approved the frozen C1 delta functionally (no open Functional finding; F1 and F2 closed; four startup tests pass) but publication stays blocked by the policy-test lint, format and two typing diagnostics that originate in the initial candidate.

## Evidence

* Pinned `ruff==0.17.1` isolated check on `infra/tests/test_bicep_policy.py` reports FOUR E501 (lines 2192, 2234, 2244 and 2294; 102, 102, 103 and 109 columns), reproduced on the C1 head and read from raw output. The earlier C1 summary said three; that count was inaccurate and is corrected here. `git blame` attributes all four lines to `53fcf666c` (the initial candidate); the base file passes check and format.
* `ruff format --diff` shows exactly four hunks at the same places.
* Workflow `src-ci.yml` lines 243-244 and README lines 1191-1193 define the Ruff commands. No workflow runs mypy on `test_bicep_policy.py`; the README line 1216 gives `mypy --check-untyped-defs` for local type checking. That is a configured local diagnostic, and the three base diagnostics (`Match[str] | None` twice and a bool-to-str assignment) are a baseline that this cycle does not repair.
* Two introduced mypy diagnostics at the `refusals` dict: `{**valid, **override}` where `override` is inferred `object`. A concrete annotation `dict[str, tuple[dict[str, object], str]]` removes both.
* Process disclosure: before this research was recorded I ran an exploratory fix and saved it as `proof/premature-exploratory-fix.patch`, then reverted my own uncommitted edits with `git apply -R` (no stash, reset or hooks override). The red reproductions were captured in `proof/red-*`; the fix is re-applied after implement-start.

## Planning Readiness

`Ready`. Product scope only `infra/tests/test_bicep_policy.py`.
