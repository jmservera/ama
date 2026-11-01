<!-- markdownlint-disable-file -->
# RPI Plan: Issue 440 second stabilization checkpoint

## Task Metadata

* Task ID: 440; parent #123 (hierarchy only). Slug: issue-440-second-checkpoint. Plan date: 2026-11-01.
* Research: .copilot-tracking/research/2026-11-01-issue-440-second-checkpoint-research.md
* Details: .copilot-tracking/details/2026-11-01/issue-440-second-checkpoint-phase-details.md
* Critique: one execution, recorded in the details file (compatible findings applied directly).
* Tier: Focused (owner-selected; documentation and evidence only, no source change, no heavy gate).

## Objective

Execute a second bounded local checkpoint on origin/main 36a1d0da, record it in the existing evidence pack, and file a scoped issue for the unattributed PERF-440 benchmark risk (criterion 7). Do not claim criteria 7 or 8 beyond the evidence.

## Phases

* [x] P01 Environment: pip venv outside the repo, install the five `src/` distributions.
* [x] P02 Focused checks: affected-package suites for the feedback-first journey (API auth, assistants failure paths, resident API, core store, orchestrator, importer, agents), the PERF-440 selector repeated, ruff check, ruff format --check and mypy per project.
* [x] P03 Triage: re-search open issues, file one deduplicated issue for PERF-440 with severity, reproduction, requirement/ADR links, acceptance criteria and dependencies.
* [x] P04 Evidence: append the second checkpoint to docs/architecture/cutover-evidence-pack.md and one new entry to docs/reference/log.md; write the changes record.
* [x] P05 Independent review, commit, push, PR (Refs #440, no closing keyword).

## Success Criteria

* Actual commands, exits and skips recorded; heavy SQL/container/browser groups recorded as blocked by a foreign lock holder, not passed.
* New issue exists and is linked; criteria 7 and 8 unticked unless proven.

## Constraints

* No code change, no coordinator change, no Azure, no private data, no threshold waiver.
