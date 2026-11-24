---
title: Issue 220 details
---

Phase 1: core tests via unittest with PYTHONPATH=src:tests (13 tests). api tests with the documented PYTHONPATH (10 tests).
Phase 2: `probe_live.py` logs in as the staff test user at runtime, calls GET /api/me and a POST to the challenge route with a nonexistent proposal and no valid revision, then stops. Nothing is created.
Phase 3: note under docs/reference/research/issue-220-no-retaliation-closure-2026-11-24/.
