---
title: Issue 133 aftercare criteria 1, 2, 4, 5, 6 plan
task_id: 133-aftercare-criteria-2035
date: 2026-11-13
---

## Process note

Plan authored after code edits had started (process divergence recorded in the changes file); critique runs once on this plan plus the working diff.

## Phases

* [x] Phase 1 Research: audit recorded in the research file.
* [x] Phase 2 Core code: widen `PARAPHRASE_PATTERNS` (savings, household blame, retrofit causation); stop `propose_pack` writing concern history; refuse a restored `completed` or `not_needed` remedy with no outcome or evidence.
* [x] Phase 3 Core tests: closure regressions (register, restart, before-concern, after-closure actions, service level), restore refusals, guard phrasings, pack no-mutation, no pack route.
* [x] Phase 4 Evaluator rendering in `aftercare.js`: households raising with denominator, outside-scope count, unresolved-with-closure count, baseline window definitions, per-home unresolved denominator; tests in `test_aftercare_screen.py`.
* [ ] Phase 5 Validate: all `test_aftercare*`, `test_content_standard`, `test_accessibility_baseline`, ruff check and format, mypy in three projects, in `/tmp/venv-133ac-2035`.
* [ ] Phase 6 Review artifact, remove only the scratch venv, commit with `Refs #133`.

## Out of scope

Resident self-service digital portal, human assistive-technology sign-off, DPO position, evaluator role access, GitHub edits and push.
