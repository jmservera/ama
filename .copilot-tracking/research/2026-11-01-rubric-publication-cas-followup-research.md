---
title: Rubric publication CAS and PR score-edit detection research
date: 2026-11-01
---

Disposition: executed. Planning Readiness: Ready.

Source: unresolved late review threads on PR #748 (merged 2026-11-01).

## Findings

* Refresh step in `.github/workflows/rubric-score.md` read the branch lease after committing, so any head present at publication time was overwritten. Push and dispatch runs use separate concurrency groups, so older dispatches can finish after newer ones.
* `prepare.py` compared score file blobs with the current base, which flags PRs forked before a main-only refresh.
* `should_score` ignored badge-only edits, so the badge warning in `gate.baseline_notes` was never produced.
* Pull request runs check out the PR head, so merge-base comparison is valid.
* `latest.json` records the scored `commit`; refresh commits carry a `Scored commit:` trailer. `gh api compare` status `ahead` identifies a newer commit without needing local history.

## Pre-existing, out of scope

* `test_gate.py` hard-codes a 66 seed total; main baseline is 77 (6 failures before this change).
