---
title: Issue 2255 plan
date: 2026-11-22
---

# Plan

* Phase 1: add `infra/scripts/seed_demo_hazard_clock.py` (inspect and apply modes, counts-only output) and focused unit tests in `infra/tests/test_seed_demo_hazard_clock.py` using a SQLite SqlStore.
* Phase 2: run lint (ruff check and format) and the new tests.
* Phase 3: live, through exec into `ca-cutover-test-demo-api`: inspect, apply with N=6, inspect again (expect 0), then verify the queue through the API with Playwright and a staff session read at runtime.
* Phase 4: research note with a per-criterion table, changes record, review, local commit. No push, no deploy.

Tier: FULL (live SQL write); no src change; rpi-checks --all not run here.
