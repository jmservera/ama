# Plan: issue 2245 chat ask timeout

Details: `.copilot-tracking/details/2026-11-22-issue-2245-chattimeout-details.md`.

* [ ] Phase 1: seed the demo chat meter once per day and configuration per ledger (`src/core/src/zava_forward/core/chat_demo_meter.py`) with a regression test that counts ledger transactions across repeated admission checks and reseeds on changed settings.
* [ ] Phase 2: run the targeted core and api tests, mypy and ruff for the touched project.
* [ ] Phase 3: dated research note under `docs/reference/research/`, index and log entry, per-criterion table in the changes record.
