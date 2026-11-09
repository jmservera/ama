---
title: Infrastructure integration 136 metadata correction C2 details
description: Phase details for the C2 metadata correction plan
ms.date: 2026-11-09
---

## Phase 1 Prospective records

* Files: research, plan, details (this file) under `.copilot-tracking/`, committed before any correction edit.
* Done when: the critique result is recorded and committed.

## Phase 2 Correct the state next_action

* File: `.copilot-tracking/rpi-sessions/2026-11-09/infrastructure-integration-136-pm-state.json`.
* Replace only the `next_action.action` text and append one `confirmed_decisions` entry for the dated C2 supersession. Keep valid JSON and all other fields.
* The supersession leaves the original adverse and closure history in git commits `fc6adc5c5` and earlier.

## Phase 3 Correct the critique attribution

* File: `.copilot-tracking/plans/2026-11-09-infrastructure-integration-136-pm-plan.md`.
* Append a dated correction under `## Critique result` naming the host-displayed `Rubber-duck (model: gpt-6.1-terra)` source (coordinator session log `rpi-136-postmerge-refresh.log`, line 76) and the author model. Do not edit the original sentence.

## Phase 4 Records and checks

* New C2 changes, review and state JSON records. Review is author-only; independent exact-delta closure, publication, new-head hosted checks and merge remain coordinator actions in that order.
* Checks: JSON validity, link and path existence, non-tracking tree identity versus `fc6adc5c5`, scoped diff inventory.
