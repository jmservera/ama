---
title: Issue 202 live r2 plan and critique, 2026-11-19
---

Plan: prove each unticked criterion or state why not; record in a research note; no source, workflow or protection change.

## Critique (executed once)

Verdict: proceed with evidence-only scope. Deleting the two workflows edits `tools/rpi-checks.py` (SHA pins, job map), `src-ci.yml` and `src/core` code, which is gate-semantics and src change (FULL tier). The brief bars `rpi-checks.py --all` and tells the worker to stop and report FULL tier instead. Changing rulesets is a shared-system change and unnecessary because `mainprotect` requires no checks. Applied directly.

## Phases

* [x] Re-probe repo, tag, workflows, rulesets
* [ ] Write research note with per-criterion table, index and log entries
* [ ] Changes record, review, commit
