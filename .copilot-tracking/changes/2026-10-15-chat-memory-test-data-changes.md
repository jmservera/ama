---
title: Changes for #172
ms.date: 2026-10-15
---

* Added `mvp/zavaforward_mvp/chat_fixture.py`, `mvp/tests/test_chat_fixture.py`.
* Updated provenance register (`DS-CHAT-MEMORY-FIXTURE`), data dictionary, `mvp/evals/registry.json`, `mvp/README.md`, `docs/reference/README.md`, `docs/reference/log.md`.
* Divergence: provenance test required private location `mvp/data/`; register uses that and notes the subfolder.
* Validation: full suite 603 tests; one failure (provenance location) fixed, targeted rerun OK.
