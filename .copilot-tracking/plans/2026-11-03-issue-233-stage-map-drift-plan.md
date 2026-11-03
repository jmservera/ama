# Plan: issue 233 stage map drift check

Date: 2026-11-03. Tier: focused. Research: `.copilot-tracking/research/2026-11-03-issue-233-stage-map-drift-research.md`. Details: in the changes file.

* [x] Phase 1: add `stage_map_drift` to the checker and call it from `check`.
* [x] Phase 2: add two tests; update trace doc and log.
* [x] Phase 3: run core atlas tests, ruff, mypy strict; commit; open PR with Refs 233.

Critique (single pass, self-run): compatible. Offline read-only check; no role simulator, no AI feature, no human approval or consent boundary touched.
