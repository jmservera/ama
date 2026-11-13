---
title: Issue 184 mid-slot rebase plan
ms.date: 2026-11-13
---

Plan (details inline):

1. Run `git rebase --onto 8ca5685b71 e2bca0c5eb` (no push). Resolve conflicts keeping main's 1518 content plus be4013d4ec sticky mid-slot exit 2 and require_cadence checks.
2. Create /tmp/venv-184-reb-1509 with pip; install src/core, src/agents, src/api and ruff, mypy.
3. Run test_live_simulator, test_live_control, test_live_readings, ruff check, ruff format --check, mypy for api and core.
4. Write rebase verification artifacts under .copilot-tracking/*/ dated 20261113T1509Z.
5. Independent code-review; remove /tmp/venv-*; commit with trailer; record commit-complete.

Details: untracked tracking files do not block rebase; tracking artifacts are added after rebase so the replayed commit stays untouched.

Critique (rubber-duck, executed once): verdict Revise. Applied: remove only /tmp/venv-184-reb-1509. Rejected for this task: new sticky-restore test (out of rebase scope; routed as follow-up).
