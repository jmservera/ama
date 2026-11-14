# Review: demo-149-role-workbench-heading-hierarchy-0442

* Date: 2026-11-14
* Review execution: executed once, self-review of the diff against the brief
* Outcome: conformant with one disclosed divergence and open follow-ups
* Tier: Focused. Independent exact-head review, human approval and hosted CI remain required and are not claimed.

## Checks

* Every role (7 staff plus contractor) and every primary view: asserted. Exactly one `h1`, monotonic non-skipping levels, no empty headings, tables named and `th` scoped, links and buttons named.
* Gap mechanism is two-way: the first run failed when the gap was too broad (Contractor `#/`), proving the check fails on mismatch.
* Hidden elements are excluded, so the hidden empty `h3` and hidden button are not counted.
* No `Closes`, `Fixes` or `Resolves` for #149.

## Divergence

* Real browser instead of `TestClient` (none exists). Skips if Playwright or Chromium is missing, so a CI without them would not exercise it: state this when reading hosted results.

## Follow-ups (ranked)

1. Move the staff list `h1` before the filter and briefing headings in `app.js`, then empty `H1_NOT_FIRST`.
2. Fix the pre-existing mypy error in `test_epic149_landmarks_skip_link_focus_order.py`.
3. Assistive-technology and human heading-navigation testing (not replaced by this check).
