---
title: Plan for issue 134 slice 5
date: 2026-11-04
task_slug: journey-contract-134-r9
---

## Slices

* Slice 5 (this PR): building hold control in the connected journey.
* Later: SQL-store journey test (needs SQL Server, gate-tier), API/screen walkthroughs and browser keyboard/announcement run (human/browser steps).

## Steps

* [x] Add src/core/tests/test_journey_building.py (behavioural, typed).
* [x] Cite it as evidence in perspective_walkthroughs and journey_acceptance (AC-043).
* [x] Run focused tests, ruff, mypy as src-ci does.

Critique (single pass): no conflicting advice; statuses stay partial because no screen or browser run exists. Tier: focused (no security, infra, SQL or deployment change).
