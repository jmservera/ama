<!-- markdownlint-disable-file -->
# Plan: issue-98-r1-manifest-freshness

Research: .copilot-tracking/research/2026-11-03/issue-98-r1-manifest-freshness-research.md
Details: .copilot-tracking/details/2026-11-03/issue-98-r1-manifest-freshness-details.md
Critique: .copilot-tracking/reviews/plans/2026-11-03/issue-98-r1-manifest-freshness-critique.md

## Slices (stacked)

* [x] S1 (this PR): saved-manifest freshness in `form_review.view`, tests, README, log.
* [ ] S2 (blocked on Finance/template owner): approved-rule validation.
* [ ] S3 (blocked on S2 and Finance authority): reviewed pack assembly and export.
* [ ] S4 (after S2/S3): stale propagation to rules, calculations and pack reviews.

## Phases

* [x] P01: implement `_freshness` and `diagnostic_freshness` in view (core only).
* [x] P02: tests (both backends), ruff, mypy, README and log.

## Validation tier

Focused. No security, infrastructure, SQL schema or deployment change, so no gate.
