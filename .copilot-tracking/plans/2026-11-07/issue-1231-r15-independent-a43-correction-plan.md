# Plan: issue 1231 independent correction cycle 1

Date: 2026-11-07. Research: .copilot-tracking/research/2026-11-07/issue-1231-r15-independent-a43-correction-research.md. Critique: none run.

1. Stage mode 0o600 (ranking_publication.py).
2. Attach stage_retained to the primary exception; runner publish_failed message and next action name the file; Store logs the warning and adds a path-free sentence to the 503.
3. Regressions: umask 0022 and 0002 on retained-stage and final modes with reliable umask restore (try/finally); helper exception carries the retained name; runner and manager route with simultaneous link and unlink failure, foreign file preserved, no path in responses.
4. Light checks only: core and API wiring tests, Ruff, format, mypy, diff check.
5. Commit; freeze; return. Parent alignment waits for the coordinator's frozen parent.
