---
title: Issue 1373 independent-record metadata continuation plan
ms.date: 2026-11-10
task_id: 1373-independent-record-1110
---

## Plan (authored 2026-11-10 before any new record besides research)

Objective: persist the independent Functional assessment of `3d89f63` as new tracking records with explicit provenance.

* [ ] Phase 1: Plan, details and one critique.
* [ ] Phase 2: Create the changes record and the new independent-review record (findings, read ledger, provenance, carried checks, unconfirmed residual).
* [ ] Phase 3: Verify: HEAD still `3d89f63`; `git diff 3d89f63 HEAD -- src docs` empty; only new paths under `.copilot-tracking` added; no earlier tracking file modified; no token fragments; `git diff --check`.
* [ ] Phase 4: One Review, state, freeze commit, witness commit-complete with the actual HEAD, verify exit and hash, handoff.

Out of scope: source or docs edits, re-running tests, installs, GitHub, publication, source repair or issue for the residual, allowance extension, earlier evidence edits.
