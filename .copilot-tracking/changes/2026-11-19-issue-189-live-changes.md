---
title: Issue 189 live changes
ms.date: 2026-11-19
---

Tier: FOCUSED, documentation only (no `src` change). Refs #189.

Changes: add `docs/reference/research/issue-189-live-20261119-2026-11-19.md` and its `verifier-output.txt`; index line in `docs/reference/README.md`; entry in `docs/reference/log.md`.

## Per-criterion table

| Criterion | Proven | Unproven reason |
| --- | --- | --- |
| Cost estimate for N homes before any run | Proven (already ticked) | None |
| Quota headroom against the #140 tier | Proven (already ticked) | None |
| Run owner | Proven in code, tests and hub tag | No live run |
| Run time limit | Proven in code and tests | No deployed simulator job; deploying is outside the authorisation |
| Budget alert | Configuration proven live (80 percent actual, 100 percent forecast) | Both recipients unreachable; firing needs spend; owner action |

Validation: core suites 32 OK, `test_simulator_admin` 30 OK, live verifier 5 of 6 checks pass. mypy and ruff not applicable (no Python changed).
