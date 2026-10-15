---
title: Issue 199 M5 phase details
ms.date: 2026-10-15
---

* Phase 1: destinations are `src/api/src/zava_forward/api`, `src/core/.../core` (lawstore, `law/`), `src/orchestrator/.../orchestrator`, `src/api/checks`, `src/api/tests`, `src/orchestrator/tests`.
* Phase 2: `WEB` and `REGISTER` resolve beside the module; tests use `parents[3]` for the repository root; package data `web/*`, `web/vendor/*`, `web/vendor/images/*` and `law/*.json`.
* Phase 3: lock regenerated with `--generate-hashes`; only the transitive `pycparser` 3.1 to 3.11 changed; Dockerfile adds `chmod -R a+rX` on web, `ZF_AI_GOLDEN`, healthcheck, `CMD python -m zava_forward.api.server`.
* Phase 4: workflows `mvp-ci`, `mvp-validation`, `src-ci` keep names; `src-ci` passes `pythonpath` per matrix entry.
* Success: totals at least 747, lint and mypy clean, wheels carry assets, smoke test of the installed server.
