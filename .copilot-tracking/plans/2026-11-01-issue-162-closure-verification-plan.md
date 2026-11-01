---
title: Issue 162 remaining slice plan
ms.date: 2026-11-01
---

Scope: verify the merged slice on current main and record the blocker. No source change.

* Phase 1: run `test_chat_isolation` (core, api, agents installed with pip into a venv), ruff check, ruff format --check, mypy for touched projects.
* Phase 2: record research, plan, changes and review artifacts.
* Phase 3: open a PR using `Refs #162` naming the unmet criterion.

Critique (single pass, executed): verdict proceed. Adding new code or deciding OD-46 here would exceed scope and authority, so both are rejected.
