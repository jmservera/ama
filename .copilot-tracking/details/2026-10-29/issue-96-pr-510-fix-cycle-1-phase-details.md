---
title: Issue 96 PR 510 fix cycle 1 phase details
description: Bounded cache and regression execution details
ms.date: 2026-10-29
---

## Metadata

Task ID and slug: `issue-96-pr-510-fix-cycle-1`.
Plan: `.copilot-tracking/plans/2026-10-29/issue-96-pr-510-fix-cycle-1-plan.md`.
Research: `.copilot-tracking/research/2026-10-29/issue-96-pr-510-fix-cycle-1-research.md`.

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Implement and validate report-local reuse | Complete | P01-T01, P01-T02 |

<!-- rpi:phase id=P01 -->
## P01: Implement and validate report-local reuse

C1-C4 establish the duplicate read/hash path and existing fixtures. Only the
report freshness decision changes; candidate verification and visibility are
preserved. No unresolved implementation decision.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add cache and regression coverage

In `_report`, allocate a tuple-to-bool dictionary beside report-local state.
Under `schema_current` and non-null evidence, construct the exact source key.
Check membership before `_current` so false results are reusable. Use the
cached result for effective state. Keep schema-stale reports short-circuited.

Create shared-source fixture evidence through actual registration, upload,
staging and review, not by manufacturing the primary performance test.
Two fields can use the same staged source text while the numeric field uses
an explicit typed correction. Patch `docstore.get` only after preparation.
Parameterize view and diagnose over JSON/SQLite, count actual reads in each
report and change the returned bytes for the next report without metadata
changes. Assert both bound fields stale after the later check.

Use narrow copied-draft tests under the store lock to exercise exact-key
differences for ID/version/hash/kind and shared metadata-stale negative
results. Spy on `_current` to avoid mistaking metadata short circuits for
cache hits. Existing source/schema and permission tests remain active.
Maximum additions: three test methods, one helper. No removals or package tests.

Completion evidence: original-code red regression, fixed-code green regression,
correct output states and exact invocation/read counts.
Completed: two new methods and one helper, both backends and both public report
paths, true/false reuse and four exact identity dimensions. Original code failed
all four shared-source subtests; fixed code passes.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Validate and document

Run the four validation commands in the plan with `/tmp/mv`, record exit codes,
test counts and optional skips. Review the diff/links and confirm no unrelated
files or `latest.json` changes. Add a short core README statement for the
new cache lifetime and exact key.

Completion evidence belongs in
`.copilot-tracking/changes/2026-10-29/issue-96-pr-510-fix-cycle-1-changes.md`.
Completion: all requested checks pass; 201 tests with 54 existing optional SQL
skips, Ruff clean, 112 files formatted, mypy clean across 165 source files.
The core README documents the cache identity/lifetime. An independent Review
owns acceptance of this bounded fix; do not equate it with financial or
publication approval. The full gate is required before any later publication.
