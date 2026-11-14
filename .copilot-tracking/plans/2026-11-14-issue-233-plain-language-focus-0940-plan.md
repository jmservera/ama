# Plan: #233 stage-map focus and announcements

Tier: Focused (api accessibility baseline, content standard, design system, role-screen tests, ruff).

1. [x] Name the stage list and add `aria-current="step"` once on the current stage; text cue kept.
2. [x] Add `tests/test_role_screens_stage_map_focus.py` (list name, single current step, no tab stops or nested headings, tension status line).
3. [x] Log update, validate, commit locally; no push, no PR.

Critique: one pass. Compatible: no browser check script touched, so the scenario manifest is unchanged.
