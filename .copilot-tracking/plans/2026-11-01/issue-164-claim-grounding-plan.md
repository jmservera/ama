# Plan: issue 164 claim-level grounding check (2026-11-01)

1. Add `unsupported_claim(answer, cited_texts)` in core chat_panel; withhold in `ask` flow.
2. Remove `known_gap` from the golden scenario; add a supported-claim control scenario.
3. Unit tests in src/core/tests/test_chat_panel.py; run agents chat_eval + core chat tests, ruff, mypy.
4. Critique (one pass, self): risk of false withholds is accepted as fail-safe; word list is narrow.
5. Review once, commit, push, PR with Refs #164.
