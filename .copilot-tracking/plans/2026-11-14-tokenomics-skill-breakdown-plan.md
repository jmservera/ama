# Plan: per-skill tokenomics breakdown

1. [x] `usage()`: parse `reasoning_tokens` (direct or `completion_tokens_details`), bounded by completion tokens; omit the key when absent so stored shape is unchanged.
2. [x] Add `token_breakdown()` (input, cached, uncached, completion, reasoning; Unknown when any call lacks a field) and `tariff_basis()` (offline-demo / live-unverified / mixed / Unknown).
3. [x] Add `token_breakdown` and `tariff_basis` to each `by_capability` row; add `tariff_basis` to the report.
4. [x] Tests in `src/core/tests/test_ai_consumption_skill_breakdown.py`; adjust one exact-dict assertion in `test_ai_consumption.py`.
5. [x] Validate: unittest, ruff check and format; API consumption tests.
Critique: single pass, no conflicts with confirmed decisions.
