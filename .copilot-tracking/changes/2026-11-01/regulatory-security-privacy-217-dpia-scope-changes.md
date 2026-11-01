---
title: DPIA scope drift guard changes (issue 217)
description: Change record
ms.date: 2026-11-01
---

* Changed `src/core/tests/test_regulatory_privacy.py`: added `DpiaScope` (2 tests) tying
  `CLASSES`, `reg_chat_turn` and usage metadata to the DPIA draft; no runtime code changed.
* Validation: unittest (privacy, usage; 8 tests OK), `ruff check`, `ruff format --check`,
  `mypy` on src/core all pass. Heavy local gate not run by owner direction; CI is evidence.
* Divergence: first draft derived tokens from storage text and failed; replaced by an explicit class-to-DPIA-term map.
* Review fix: added `docs/reference/research/chat-memory-dpia.md` to the `src-ci.yml` pull-request path filter so DPIA-only changes run the guard.
