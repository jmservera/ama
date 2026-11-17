---
title: Issue 121 resident hold plan
date: 2026-11-17
---

* Phase 1: in `AzureAdvisor._answer` and `_question`, before any reservation, raise `AssistantUnavailable("data_protection_hold")` when `data_protection.dispatch_hold("tenant_identity", os.environ)` returns a reason; existing fallback renders the rules answer.
* Phase 2: add the fallback reason to the allowlist if one exists; run test_resident_aoai, test_resident_assistant_*, ruff format check, mypy for src/api.
* Critique: single pass recorded in `.copilot-tracking/critique/2026-11-17-issue-121-resident-hold-critique.md`.
