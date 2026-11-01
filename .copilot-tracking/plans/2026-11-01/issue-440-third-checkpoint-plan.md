<!-- markdownlint-disable-file -->
# RPI Plan: Issue 440 third stabilization checkpoint

## Task Metadata

* Task ID: 440; parent #123 (hierarchy only). Slug: issue-440-third-checkpoint. Plan date: 2026-11-01.
* Research: .copilot-tracking/research/2026-11-01-issue-440-third-checkpoint-research.md
* Details: .copilot-tracking/details/2026-11-01/issue-440-third-checkpoint-phase-details.md
* Critique: one execution, recorded in the details file.
* Tier: Focused (owner-selected; documentation and evidence only).

## Objective

Record a third bounded local checkpoint on origin/main b18f7f98e after the 40-commit wave, re-triage open findings and keep criteria 7 and 8 unticked.

## Phases

* [x] P01 Environment: pip venv outside the repo, editable install of the five `src/` distributions.
* [x] P02 Focused checks: five package suites, ruff check, ruff format --check, mypy per project.
* [x] P03 Triage: compare findings with open issues (#687, #720, #349, #350, #360, #432, #570); no new duplicate.
* [x] P04 Evidence: append checkpoint to docs/architecture/cutover-evidence-pack.md and one entry to docs/reference/log.md; write changes record.
* [x] P05 Independent review, commit, push, PR (Refs #440).

## Success Criteria

* Actual commands, exits and skips recorded; heavy groups recorded as blocked by the foreign lock, not passed.
* Criteria 7 and 8 remain unticked.

## Constraints

No code, coordinator, Azure, private data or threshold change.
