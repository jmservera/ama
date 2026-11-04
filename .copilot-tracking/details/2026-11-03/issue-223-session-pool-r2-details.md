---
title: Issue 223 session pool details
date: 2026-11-03
---

Phase 1: add pool_human_sessions in src/agents/src/zava_forward/agents/review_effectiveness.py; CLI accepts several sheet paths (single sheet output unchanged).
Phase 2: tests in src/agents/tests/test_review_effectiveness.py (pooled effort, failed session and repeat reviewer, unauthorised reviewer, CLI exit code).
Phase 3: README note in src/agents/README.md.
Validation: ruff check and format, mypy --cache-dir=/tmp/mypy-223, test_review_effectiveness only.
