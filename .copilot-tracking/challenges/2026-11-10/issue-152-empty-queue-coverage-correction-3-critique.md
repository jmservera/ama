<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-152-empty-queue-coverage-correction-3

## Metadata

* Task ID: issue-152-empty-queue-coverage-correction-3
* Critique date: 2026-11-10 (executed once, before the merge)
* Plan: .copilot-tracking/plans/2026-11-10/issue-152-empty-queue-coverage-correction-3-plan.md
* Details: .copilot-tracking/details/2026-11-10/issue-152-empty-queue-coverage-correction-3-phase-details.md
* Critique execution status: Complete
* Assessment boundary: plan and caller requirements; no source or hosted evidence assessed.

## Coverage Assessment

| Requirement | Coverage | Evidence or concern |
|---|---|---|
| Ordinary merge, no history rewrite | Covered | P01-T01 |
| Both intents preserved | Partial | Needs a durable check that main's other app.js changes survive (PC-002) |
| Original-before-change records | Partial | Records exist only as untracked files; a merge could blur them (PC-001) |
| Recipe hash via existing mechanism | Covered | P01-T03 reads the code first |
| Real rendered proof | Covered | Served harness; Node helper alone is not claimed |
| Strict API typing | Partial | Exact mypy config and scope not named (PC-003) |

## Verdict

* Verdict: Revise (three small direct corrections; no user decision needed)

## Findings

### PC-001 [Medium]: pre-change evidence is not committed

* Concern: research, plan, details, critique and state are untracked when the merge runs, so "original before changes" rests on file mtimes only.
* Smallest change: commit the C3 pre-merge records and state as their own commit before `git merge`, so Git order proves they preceded the integration.
* Route: direct planner correction.

### PC-002 [Low]: no stated way to prove main's behaviour survives

* Smallest change: after the merge, diff `app.js` against `origin/main` and require only the slice hunks; also grep for main's account label, simulator navigation and priority history controls; run the whole workbench test module.
* Route: direct planner correction.

### PC-003 [Low]: strict typing scope unspecified

* Smallest change: read `src/api/pyproject.toml` (and the README command) for the mypy configuration and run it over the whole API project with the matching installed distribution, not a single file.
* Route: direct planner correction.
