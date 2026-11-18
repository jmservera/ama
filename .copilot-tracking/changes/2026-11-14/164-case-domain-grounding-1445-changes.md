# Changes: case-domain chat grounding

* `src/core/src/zava_forward/core/chat_case_answers.py`: new facts, intents (`claim`, `pas2035`, `sensor`), answers, `DOMAIN_BOUNDARY` rule, `RULES_FIRST`.
* `src/core/src/zava_forward/core/chat_panel.py`: rules-first routing uses `RULES_FIRST`.
* `src/agents/tests/test_regulatory_chat_case_domain_grounding.py`: 6 focused tests.
* Validation: new tests OK; core `test_chat*.py` 155 OK; api `test_chat_panel` and `test_accessibility_baseline` OK; ruff check and format clean and mypy clean in `src/core` and `src/agents` (`/tmp` caches, no cache dirs left).
* Not run: full local RPI gate, hosted CI, browser harness, Docker. Tier: focused. No push or PR.
* No HTML or `aria-invalid` change.
