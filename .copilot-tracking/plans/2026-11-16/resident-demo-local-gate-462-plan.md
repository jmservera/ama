---
title: "Plan: resident-demo-local-gate-462"
description: "Plan for the local engineering, threat-model, RPI artifact and full-gate criteria of Issue #462"
ms.date: 2026-11-16
---

## Overview

Task: `issue-462-local-candidate` (`resident-demo-local-gate-462`). Base `5e0c7f74432ffce73cfeaa672e4e40a605ca6274`, branch `feat/resident-demo-rpi-gate-462`. Goal: a clean, frozen, committed local candidate with a verified full receipt. No push, PR, merge or Azure mutation.

Inputs: [research](../../research/2026-11-16/resident-demo-local-gate-462-research.md), [phase details](../../details/2026-11-16/resident-demo-local-gate-462-phase-details.md), [critique](../../reviews/plans/2026-11-16/resident-demo-local-gate-462-plan-critique.md).

Validation tier: FULL (issue requires SQL Server parity, Docker non-root startup, browser journeys and the complete exact-head gate). Basis: the issue text and the repository tier rules.

## Decisions

* D1 No cloud access of any kind; criteria 6 and 7 stay unmet and unticked.
* D2 The threat model is a durable knowledge-base document, not only a tracking file, so it is reviewable and linkable.
* D3 No source code change unless a local check exposes a defect. A defect found is fixed with a failing-first test.
* D4 One critique and one review; findings become follow-ups, not repeat loops.
* D5 No credential value is generated, stored or printed. Tests use fake constants.

## Phases

* [ ] Phase 1 Threat-model document, README link, KB index row and log entry.
* [ ] Phase 2 Verify dependencies #444/#455 and local previews (read-only evidence).
* [ ] Phase 3 Local verification: lint and type, unit suites, SQL Server parity, Docker non-root image start, browser journeys.
* [ ] Phase 4 Reconcile changes evidence, then single-pass review.
* [ ] Phase 5 Commit evidence and candidate, run the full gate externally, verify the receipt, record witness `commit-complete`.

## Exit criteria

* Threat model covers public fake-email login, shared credential, session handling, cross-case access, database fields and deployment isolation.
* Every check result is recorded as passed, failed or not run, with the command.
* Receipt verifies against the base with no later commit.
* Worktree clean after the final commit.
