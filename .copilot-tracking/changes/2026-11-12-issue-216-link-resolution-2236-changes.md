---
title: Changes for #216 citation and card link resolution regression
ms.date: 2026-11-12
---

* Plan: ../plans/2026-11-12-issue-216-link-resolution-2236-plan.md
* Changed: `src/api/tests/test_regulatory_chat_api.py` (+67 lines, test-only): `resolve_links`, `ask_and_resolve`, `negative_controls` helpers and three tests (base with forgery controls, truncated excerpt, conflict with two provision versions).
* No production, gate, scorer, README, threshold, price or authority change. Zero provider calls; synthetic loopback only.
* Plan markers P01, P02 complete; P03 is this record plus one Review.
* Validation run locally (venv with pip editable installs of this worktree): `test_regulatory_chat_api` 12 tests OK; ruff check and format check clean; mypy on the file clean. Baseline before change: `test_regulatory_gates test_regulatory_answers test_eval_registry` 33 tests OK.
* Not run: blanket full gate, hosted CI, browser harness. Classification: focused tier (test-only, no gate semantics, workflow, dependency or security-control change).
* Amendments/divergences: critique PC-001 to PC-003 applied directly (see details). The first draft of the loop-based test was restructured into three tests because subtests share one fixture.
* Limitation: coverage is for the staff principal sam@example.test; not an authorisation matrix.
* Follow-ups: none admitted; AC1, AC4 and tokenomics criteria remain unmet and human/live-owned. No criterion is ticked.
