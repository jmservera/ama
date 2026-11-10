---
title: Issue 1259 recovery preparation plan
description: Prospective plan for unchanged-source validation and a conditional resume point for the child path-health fix
ms.date: 2026-11-09
---

## Objective and boundary

Establish current source-equivalent regression coverage for the existing child fix `683ec2716` at seed `fab9159d9`, record the proposed Blob-contract scope, and stop at a clean local handoff. No product change, no parent integration, no push, PR, issue, board or merge. Refs 1259, 1258, 79 and 1231; never closes.

## Ordering disclosure

Research reading and the read-only validation runs preceded the writing of this plan, details and critique in the same session; the plan is therefore not strictly prior to the commands, though no source, parent or remote state was changed by them. Recorded in the Changes record.

## Tier

DEMO targeted and impacted tests (owner decision for this demo push). No `rpi-checks --all`, no SQL, browser, emulator or scanner work; the shared heavy lock belongs to 1292 and is not touched. Existing FULL, SQL and cloud criteria remain unmet and are not waived.

## Phases

* [x] 1. Research (`2026-11-09-...-recovery-research.md`).
* [x] 2. Plan, details and one critique (this file, details, critique); apply compatible findings directly.
* [x] 3. Recovery validation, unchanged source: isolated venv from `git archive HEAD`; run core `test_ranking_publication*.py`, the `UnusableArchivePathTests` class, API `test_ranking_policy test_ranking_publication_wiring test_ranking_scale` and agents `test_cohort_ranking_eval`; record exits, counts and skips. Scratch red check: the same new tests against the `6d793bc3a` pre-fix source, in an external scratch copy only.
* [x] 4. Changes record, one author Review (not independent), state, handoff.

## Conditional resume point

Do not integrate until the 1258 Blob contract is frozen (clean committed parent head with its own review outcome). Then: fetch, record parent and main SHAs, write a prospective integration plan and critique, normally merge the frozen parent (the dry run already forecasts a conflict in `ranking_publication.py`; reconcile by intent, never rebase, reset or force), re-scope the path-health tests to the Blob adapter's failure matrix, run failing-first, then targeted tests, then the tier the coordinator selects. A count of review-correction cycles for this issue must be re-established at that time from retained evidence.

## Stop rules

Stop and record a blocker on any unresolved parent state, a failing selected test (not waivable), or a need for source edits. Do not poll the parent.
