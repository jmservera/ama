---
title: Zava Forward MVP has moved
description: Pointer to the src projects that replaced the mvp folder under ADR 0006
author: AMA programme
ms.date: 2026-10-15
ms.topic: reference
---

All code, tests, web assets, policies, evals, the image build and the documentation that lived in `mvp/` moved to [`src/`](../src/README.md) in issue #199 (M1 to M6). This folder holds only this pointer until the cut-over gate (#201), when `mvp/` is deleted after the archive tag (ADR 0006, phase 5). Nothing is imported from here and no module or copy is left behind.

| Former content | Now in |
| --- | --- |
| Staff features, configuration, sign-in, local run, honest limits, container checks | [src/api/README.md](../src/api/README.md) |
| Stores, ledger, law store, rule cards, governance, continuity, chat storage, synthetic tools | [src/core/README.md](../src/core/README.md) |
| Five assistants, AI evaluation harness, dated validation record | [src/agents/README.md](../src/agents/README.md) |
| Ledger digest publish and verification jobs | [src/orchestrator/README.md](../src/orchestrator/README.md) |
| Document import | [src/importer/README.md](../src/importer/README.md) |

`mvp/data/` is git-ignored local working data and is never committed.
