# Plan 2026-11-23 issue 198 live r5

Tier: FULL not triggered; change is a test file under .github/rubric/scripts only (no src, workflow, registry or gate semantics). Focused tier.

Critique (executed once): a "every glob matches a tracked file" test is wrong, since format globs (vtt, pptx, docs/planning/adrs) legitimately match 0 files; capstone-deck is skipped by size without its per-artifact override. Accepted: assert (a) no registry pattern targets retired roots mvp/prototype(s); (b) solution-code and infrastructure match tracked files and none under retired roots.

Phases: add 2 tests to test_prepare.py; run pytest and ruff; review.
Details: .copilot-tracking/details/2026-11-23-issue-198-live-r5-details.md
