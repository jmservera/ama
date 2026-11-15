---
applyTo: '.copilot-tracking/changes/2026-11-13/issue-203-verify-cleanup-references-changes.md'
---
<!-- markdownlint-disable-file -->
# Plan: Issue #203 criteria 1 and 2

* Research: [../../research/2026-11-13/issue-203-verify-cleanup-references-research.md](../../research/2026-11-13/issue-203-verify-cleanup-references-research.md)
* Details: [../../details/2026-11-13/issue-203-verify-cleanup-references-details.md](../../details/2026-11-13/issue-203-verify-cleanup-references-details.md)
* Validation tier: Focused (documentation and non-gate tooling; no workflow, dependency, Dockerfile, security or deployment change)

## Phases

* [x] Phase 1: Add `tools/check-legacy-references.py` and unit tests (file-class policy, archive-tag proximity, dated-package rule, changed-file relative-link resolution)
* [x] Phase 2: Repoint stale live tooling data (excalidraw `sources`) to migrated `src/` paths
* [x] Phase 3: Name archive tag `v0.21.0` beside retained `mvp/` and `prototype/` mentions in live documents and comments
* [x] Phase 4: Knowledge base bookkeeping (`docs/reference/README.md` row, one appended log entry)
* [x] Phase 5: Validate (`rename-zava-tests.py`, new tests, checker, `ruff check tools`, link check, diff review)

## Out of scope

Immutable regulatory snapshots, `log.md` earlier lines, historical `.copilot-tracking/` artifacts, `case_study_48_original.md`, `memory.md`, workflow check names (Issue #202), criteria 4 and 5, issue closure.
