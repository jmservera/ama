---
title: Rubric publication CAS and PR score-edit detection plan
date: 2026-11-01
---

* [x] Phase 1: make refresh publication compare-and-swap (observe lease first, skip when main or pending refresh is newer, lease push, recheck main before merge); recompile lock file.
* [x] Phase 2: detect PR score and badge edits against merge-base; include badge edits in `should_score`.
* [x] Phase 3: regression tests (reverse completion order, lease race, newer main before merge, stale-fork PR, badge-only PR) and README update.
* [x] Phase 4: local gate, commit, push, PR with `Refs #748`.

Critique: executed once, inline. Verdict: proceed; closing the post-push main race required the pre-merge recheck, added. Tier: full (workflow change).
