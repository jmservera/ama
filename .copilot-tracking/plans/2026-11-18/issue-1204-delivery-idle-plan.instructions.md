---
applyTo: '.copilot-tracking/changes/2026-11-18/issue-1204-delivery-idle-changes.md'
---

<!-- markdownlint-disable-file -->
# Plan: issue 1204 port coordinator contract to main

Research: [research](../../research/2026-11-18/issue-1204-delivery-idle-research.md). Details: [details](../../details/2026-11-18/issue-1204-delivery-idle-details.md).

## Phases

* [x] Phase 1: three-way merge #1813 agent diff onto main (`git merge-file`), no conflicts.
* [x] Phase 2: run `tools/check-coordinator-handoff.py` and its unit tests; both must pass.
* [x] Phase 3: markdown/diff review, commit with trailers.

Critique: single post-hoc worker self-critique at [critique](../../critiques/2026-11-18-issue-1204-critique.md); the plan is mechanical (one deterministic merge verified by an existing checker).
