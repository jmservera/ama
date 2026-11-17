# Plan: #233 connected journey across role screens

Tier: Focused (api role-screen tests, accessibility baseline, content standard, ruff, mypy).

1. [x] `journeyStageMap(c, current)`: current-screen stage as text, note for screens outside the eight stages.
2. [x] Render the map after the evidence in `roleScreensView` for every screen except `programme-queue` (`ownsStageMap`).
3. [x] Add `tests/test_role_screens_connected_journey.py` (all roles, one home, no self-link, uninstalled stages as text).
4. [x] Update atlas trace and knowledge-base log.
5. [x] Validate and commit locally; no push, no PR.

Critique: one pass. Compatible: central render rather than per-screen edits to avoid drift; `browser_check.py` untouched. No conflicts.
