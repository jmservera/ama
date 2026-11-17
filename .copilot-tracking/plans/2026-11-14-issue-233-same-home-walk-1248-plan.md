# Plan: #233 same-home walk hardening

Tier: Focused (role-screen unit tests, accessibility baseline, mypy, ruff).

1. [x] Add a `Same home: case <id>` badge and a never-relabel sentence to the selected-home panel in `role-screens.js`.
2. [x] Withhold a record whose id differs from the requested home with an alert, owner and next action.
3. [x] Add `tests/test_role_screens_same_home_identity.py` (five roles, deep links, mismatch).
4. [x] Validate; commit locally, no push.

Critique: one pass. Compatible: reuse the shared render path rather than per-screen edits. No conflicts.
