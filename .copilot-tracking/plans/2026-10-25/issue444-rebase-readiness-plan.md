# Issue 444 rebase and readiness plan

Date: 2026-10-25. Research: ../../research/2026-10-25/issue444-rebase-readiness-research.md. Details: ../../details/2026-10-25/issue444-rebase-readiness-details.md.

## Phases

* [x] Phase 1: One independent critique before any rebase.
* [ ] Phase 2: Rebase the run-owned branch onto fresh origin/main, resolving log.md (keep both) and latest.json (main's).
* [ ] Phase 3: No source edits. A failing merged test stops the run, preserves the failed evidence and becomes a separately authorised follow-up (critique C1).
* [ ] Phase 4: Focused and full suites, ruff, mypy, browser check on the final head.
* [ ] Phase 5: Changes artifact, one independent Review of the whole PR boundary, evidence commit.
* [ ] Phase 6: Complete gate with a new external dir, official verify, lease push, keep draft.

## Acceptance

No source change beyond conflict resolution; services untouched; draft, Refs #444 only; no receipt-only commits.
