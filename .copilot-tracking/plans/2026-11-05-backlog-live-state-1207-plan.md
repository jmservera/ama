# Plan: preserve confirmed active delivery in backlog sync (Refs #1207)

* Phase 1: add `parse_active`, `validate_active`, `desired_status` and `--active`; remove worktree-as-activity; report unverified activity; update docstring.
* Phase 2: add offline mocked regressions (reproduction, preservation, promotion, explicit none, invalid input, unchanged closed/open-PR/review-needed rules).
* Phase 3: knowledge-base log entry; focused validation; self-review; local commit. Never push.

Critique: executed once, self-critique; compatible. Considered keeping the worktree heuristic (rejected: issue forbids equating worktrees with activity) and blanket demotion suppression (rejected: unverified-only suppression keeps other rules). Tooling only: no app, SQL, infrastructure, deployment or authentication change; focused tier. Details: [details](../details/2026-11-05-backlog-live-state-1207-details.md).
