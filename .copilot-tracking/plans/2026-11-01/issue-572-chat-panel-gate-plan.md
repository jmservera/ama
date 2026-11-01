<!-- markdownlint-disable-file -->
# Plan: issue 572 chat-panel gate evidence

Research: [research](../../research/2026-11-01/issue-572-chat-panel-gate-research.md)

## Phases

* [x] Phase 1: confirm AC1-AC3 on main by reading the gate and tests.
* [x] Phase 2: run focused validation (gate unit tests, pinned ruff, mypy strict, real chat-panel case).
* [x] Phase 3: record changes and review artifacts, commit, push, open PR with `Refs #572`.

## Decisions

* No code change: criteria 1-3 already hold; widening skips or adding tokens is prohibited by AC2.
* AC4 requires a fresh complete exact-head local gate; out of scope for this tier, so the PR uses `Refs #572`.
* Critique: executed once inline; verdict accept, no findings.
