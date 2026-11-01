# Changes: issue 164 claim-level grounding check (2026-11-01)

* src/core/.../chat_panel.py: `unsupported_claim` withholds answers asserting an assurance word or number absent from cited text.
* src/agents/evals/chat_golden.json: `known_gap` removed; added supported-claim control scenario.
* src/core/tests/test_chat_panel.py, src/agents/tests/test_chat_eval.py: new unit test; gap-dependent expectations updated (golden now passes, enablement `insufficient`, disabled).
* src/agents/README.md: gap closure documented.

Validation: core chat, regulatory_chat (25), assistant tests; agents chat tests (47); api test_ai_tasks (67), assistant_release (45), continuity (16); ruff check/format, mypy core+agents. Full core suite exceeded the local time box; CI is the gate evidence.
