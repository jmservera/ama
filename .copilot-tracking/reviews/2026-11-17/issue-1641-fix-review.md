---
title: Issue 164 / PR 1641 gate failure correction review
date: 2026-11-17
---

Review executed once. Outcome: conformant for the record-only scope; the gate failures are not resolved by code.

* Scope: only `.copilot-tracking/` files; `git diff --check` clean; no caches or private data staged.
* Open item 1 (routed to coordinator): re-run the full gate for a new receipt; browser reset assertion is intermittent (about 1 in 70 on the candidate, none observed on main) and unreproduced on demand. If it recurs, make `wait_cases` in the reset step wait on reset inputs rather than case count, as a separate reviewed change.
* Open item 2 (routed, needs owner decision): Core suite needs a timeout of at least 3600 s or sharding in `tools/rpi-checks.py` (candidate 1535 s quiet vs 1800 s limit; gate saw about 25 % slowdown). Not applied: gate semantics.
* Human review checkboxes remain unchecked.
