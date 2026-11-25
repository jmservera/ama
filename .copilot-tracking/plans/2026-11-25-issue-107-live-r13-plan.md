# Plan: issue 107 r13 real-AI acceptance harness (2026-11-25)

Tier: FULL (src/api code change); rpi-checks.py --all not run (coordinator runs gates).

* [ ] Phase 1: add src/api/checks/assistant_real_ai_acceptance.py (dry-run default, injected live call, caps, fail-closed).
* [ ] Phase 2: add src/api/tests/test_assistant_real_ai_acceptance.py (refusals, dry-run, caps, bad usage, denied listing).
* [ ] Phase 3: run tests, ruff, mypy; write research note docs/reference/research/issue-107-live-r13-real-ai-harness-2026-11-25.md, index and log entries.
* [ ] Phase 4: changes record with per-criterion table, review, commit.

No Azure change and no tokens spent.
