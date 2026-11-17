---
title: Issue 155 research
---
# Research: demo-first desktop-only usability slice (#155)

Disposition: executed. Planning Readiness: Ready. Tier: FOCUSED (docs plus one doc-contract test).

## Measurements

* `docs/reference/research/ux/usability-test-programme-plan.md` (363 lines, `ms.date: 2026-11-15`) holds the full programme (21 scripts, 13 cohorts, SA-010 gate).
* Gap measured by regex count in that file: `resident_demo` 0, `Demo-first` 0, `desktop-only` 0, `1280` 0, `demo` 1 (an unrelated demonstration phrase in `R-J5`).
* The plan therefore never says which built surface a first session would use, nor the viewport. Existing surfaces: employee workbench `src/api/src/zava_forward/api/web/` and synthetic resident showcase `src/api/src/zava_forward/api/resident_demo/web/` (`Synthetic showcase - not a live resident service`).
* Desktop 1280 CSS px is the owner-decided primary class (`supported-devices-proposal.md`, #152); tablet and mobile are supported classes but out of this first slice.
* Existing regression `test_markdown_specification_matches_contract_and_keeps_human_sessions_not_run` checks the spec text but not any demo-first scope.

## Constraints

* No participant data, no human result, no SA-010 agreement is created; criterion 3 stays unmet; `Refs #155`.
* Out of scope: #1818, #1641 (core mssqlstore, chat grounding).
