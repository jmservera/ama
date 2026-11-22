---
title: Issue 2255 review
date: 2026-11-22
---

# Review (executed once)

Outcome: conformant for the stated scope, with open items routed to later work. Boundary: the working tree against origin/main, the live demo SQL state read through the API.

* Tool behaviour matches the tests and the live counts (23 written, 0 on re-inspect, 23 reverted once).
* The tool writes a synthetic `response_due_at`. The hazard service stays the real authority, but the seeded value would block a later real `observe_hazard_times` on those 23 hazards until reverted; acceptable for the demo, stated in the note.
* The `store._case` and `store.lock` usage depends on SqlStore internals; fine for a one-off private tool.
* Safeguarding items are skipped; none were seeded.

Routed follow-ups: independent exact-head review and hosted CI; a decision whether the dataset generator should emit `aware_at` so a re-seed keeps the clock (a src change, full tier).

## Post-rebase check (2026-11-22)

Review executed once on the rebased tree: no collision with main artifacts remains, 4 targeted tests and ruff pass, no `src` change. Outcome unchanged: conformant for the demo; independent exact-head review, hosted CI and the full gate remain open.
