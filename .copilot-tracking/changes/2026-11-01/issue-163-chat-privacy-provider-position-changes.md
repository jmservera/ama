# Changes: issue 163 provider position and DPO decision pack, 2026-11-01

Plan: ../../plans/2026-11-01/issue-163-chat-privacy-provider-position-plan.md

* src/core `chat_privacy.py`: `MODEL_PROVIDER_POSITION["documented_terms"]` (vendor documentation, not DPO-accepted) and revised open items.
* src/core `tests/test_chat_privacy.py`: test that the position is documented but not accepted.
* `docs/reference/research/chat-memory-dpia.md`: sourced provider table, blank decision pack D1 to D8, refreshed open items, ms.date.
* `docs/reference/README.md` index row and `docs/reference/log.md` entry.
* Validation (src/core, venv, pip): 101 chat tests OK; ruff check, ruff format --check and mypy clean. No heavy gate; CI is the evidence.
* Divergence: none.
