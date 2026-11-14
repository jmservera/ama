# Plan: recommendation origin provenance (Refs #104, #164)

Date: 2026-11-14. Critique: executed once inline; no conflicting findings.

1. Add `ai_tasks.origin_of(source)`: `generative_model` only for `ai`, else `decision_rule`.
2. In `_rec_view` add card `origin`, `ordering_origin` (always `decision_rule`), per-item `reason_origin`, and `origin` on `deterministic` rows.
3. Add `src/agents/tests/test_recommendation_origin_provenance.py`: mapping, model card, template, fallback and workflow-only cards.
4. Validate: targeted unittest, ruff check, ruff format --check, mypy from `src/agents`.

Cycle 1 correction: fix `origin_of` placement and typing; re-run focused tests, ruff and mypy in core and agents from an isolated worktree install.
