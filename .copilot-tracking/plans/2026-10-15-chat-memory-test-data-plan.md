---
title: Plan for #172 chat and memory test data
ms.date: 2026-10-15
---

* [x] Add `mvp/zavaforward_mvp/chat_fixture.py`, a seeded generator reusing stock case IDs and role names.
* [x] Add `mvp/tests/test_chat_fixture.py` covering AC: eleven perspectives, expiry, deletion, isolation, no real content.
* [x] Register dataset (provenance register, data dictionary, eval registry, mvp README, index, log).
* [x] Run full `mvp` suite.

Critique (single pass): keep expectations as fixture targets, label retention illustrative, no SQL DDL since no store exists yet. Applied directly.
