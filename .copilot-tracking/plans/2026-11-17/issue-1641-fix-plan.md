---
title: Issue 164 / PR 1641 gate failure correction plan
date: 2026-11-17
---

## Plan

* [x] Phase 1: record research evidence (browser flake, Core slowness).
* [x] Phase 2: decide fixes. Browser: no app.js or check change (no reproducible regression). Core: no source fix; gate timeout or shard change is a gate-semantics change, reported only.
* [ ] Phase 3: commit the tracking records only; run focused validation (documentation diff review, `git diff --check`).
* [ ] Phase 4: one Review.

Critique (executed once, compatible): changing the browser check or app.js without a reproduction would be an
unverified guess, and raising the gate timeout without owner approval changes gate semantics. Both rejected.
Details: `.copilot-tracking/details/2026-11-17/issue-1641-fix-details.md`.
