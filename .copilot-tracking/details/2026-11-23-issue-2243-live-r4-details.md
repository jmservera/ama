---
title: Issue 2243 details r4
ms.date: 2026-11-23
---

Phase 1: with clock at `EXPIRES + 86400` and `ZF_DEMO_EXPIRES_AT=2028-01-01T00:00:00Z`, `answer_question` returns label "AI-generated" and calls transport once; with the clock at the env stamp it returns "Summary by rules" without calling the transport; with the env unset it stays closed.
