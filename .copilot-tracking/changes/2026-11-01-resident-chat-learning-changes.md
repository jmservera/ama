---
title: Resident chat learning changes
ms.date: 2026-11-01
---

* Added `resident_demo/chat_log.py` and wired it through `app.py` and `__main__.py` (`ZF_DEMO_CHAT_LOG_PATH`, optional).
* `chat.py`: more synonyms (docs, papers, outstanding, what happens next), pause and contact topics, `is_refusal`, `suggestions`, `outcome`, `with_pause_note`; fallback replaces the flat refusal for harmless questions.
* `assistant.js`: visible synthetic-demo notice. `web/` copy checked against the banned-word list.
* Docs: `docs/reference/research/ux/resident-chat-learning-record.md`, index row, log entry, `src/api/README.md` setting.
* Tests: `tests/test_resident_chat_api.py` updated and extended (183 resident tests pass, 9 skipped).
* Validation (focused tier): resident unit tests OK; `test_content_standard.py` OK; `ruff check`, `ruff format --check` and `mypy src` for src/api clean. `rpi-checks --all` not run by instruction. Browser check script not run (needs Playwright).
* Divergence: the installed editable packages point at another worktree, so tests ran with PYTHONPATH set to this worktree's `src` folders.
