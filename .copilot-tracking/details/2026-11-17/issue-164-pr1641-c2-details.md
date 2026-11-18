---
title: Issue 164 PR 1641 c2 details
ms.date: 2026-11-17
---

Phase 2 commands: from src/core, src/agents, src/api run unittest discover with PYTHONPATH per .github/copilot-instructions.md; bare `python3 -m mypy` per project (api with PYTHONPATH=../core/src:../agents/src); `python3 -m ruff check` and `ruff format --isolated --line-length 100 --check` on changed files.
