# Plan: issue 227 building safety lead and repairs hazard screens (2026-11-01)

1. Append `safety-lead` and `hazard-triage` registrations to `role-screens.js` using a shared `hazardRows` renderer (no new server code).
2. Add node-vm tests `src/api/tests/test_safety_screens.py`: sent/received/accepted distinct, awareness and source, pending follow-up owner, release decision evidence, legacy release without evidence, released items not hidden, no controls, role scoping.
3. Validate: new + role_screens + design_system + accessibility_baseline tests, ruff check, ruff format --check, mypy for src/api.
4. Commit, push, PR (Refs #227 unless all criteria proven).

Critique (single pass, self): screen must not infer receipt or acceptance from sent; must not show a computed clock or classification; released items stay visible; a released hold without recorded decision is flagged, not trusted. Accepted. Rejected: adding action buttons (read-only boundary).
