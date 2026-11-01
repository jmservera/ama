# Plan: issue 231 technical queue and quality screens (2026-11-01)

1. Append `technical-queue` and `quality-queue` registrations to `role-screens.js` reusing the #226 helpers.
2. Add node-vm tests `src/api/tests/test_technical_quality_screens.py`: stale/missing evidence cannot show readiness, return routing to competent role, per-measure positive evidence, defect owner, reinspection, handover blocked, no controls, roles.
3. Validate: new and neighbouring unit tests, ruff check, ruff format --check, mypy src/api.
4. Commit, push, PR (Refs #231 unless every criterion proven).

Critique (single pass, self): keep read-only; do not compute approvals; treat absent data as Unknown; do not add roles; compatible findings applied. Accepted.

Correction cycle 3: merge main, restore unrelated files reverted by an earlier merge, re-run validation, push, reply and resolve threads.
