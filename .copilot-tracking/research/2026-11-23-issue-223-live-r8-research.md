# Research issue-223-live-r8 (2026-11-23)

Refs #223. Base d23b7c83e8. Disposition: executed. Prior r7 note (docs/reference/research/issue-223-live-r7-2026-11-23.md) left criterion 3 "proven as reporting; unproven as measurement" because live review effort is not recorded.
Finding: `ai_tasks.review()` stores `review_evidence` (reviewer, disposition, reason, compared, source_hashes, case_version) with no elapsed review time; the record has `created` and `resolved_at` only as separate ISO strings.
Buildable gap: retain `review_seconds` in `review_evidence` so live review effort is measured, not only scripted. Owner-only items (OQ-017 holders, human panel) skipped.
Planning Readiness: Ready.
