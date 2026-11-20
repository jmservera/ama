---
title: Details, issue 1204 live pass 2
date: 2026-11-19
task_slug: issue-1204-live-2
---

Phase 1: in `check_agent_instructions` (tools/check-coordinator-handoff.py), after the live-token loop, loop over required clauses (regex, label) and append `{display}:1: missing-tick-liveness-rule: ...` when absent from `unfenced_body`.

Clauses: `up to five[^\n]{0,80}unassessed`; `closure_review`; `tick_log`; `approved_actions`; `expired approval`; `never[^\n]{0,80}global stop|never a success claim or a global stop`.

Phase 2: add six mutation cases replacing each token with a neutral word.
Phase 3: `python3 tools/check-coordinator-handoff.py`; `python3 -m unittest discover -s tools -p test_check_coordinator_handoff.py -q`; `python3 -m ruff check` and `ruff format --isolated --line-length 100 --check` on the two tools files.
Phase 4: docs and records.
