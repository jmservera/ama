---
title: Infrastructure integration 136 post-merge refresh plan
description: Prospective plan to merge current main into the 136 recovery branch and refresh evidence only
ms.date: 2026-11-09
---

## Provenance

Written and committed before the merge, after the post-merge research. Details: `.copilot-tracking/details/2026-11-09-infrastructure-integration-136-pm-details.md`.

## Plan

* P1 Commit the research, this plan and details; then run one critique (below) and record its disposition before any merge.
* P2 Run `git merge --no-ff origin/main` normally into the same branch with a Conventional Commit message and the Copilot trailer. No rebase, reset, force push, retarget or squash.
* P3 If a conflict arises, resolve by keeping both intents; if intent cannot be reconciled, stop and record the exact blocker.
* P4 Verify the preserved evidence: the original 16 records, native logs, earlier critiques and Reviews are byte-equal to the approved candidate; both branch log entries remain (the merge adds, never rewrites).
* P5 Demonstrate that source, tests, dependency manifests and infra are unchanged relative to the approved candidate except for the main delta: `git diff 24d1cfb16 HEAD` outside `.copilot-tracking/` must equal `git diff 0f05e9aae origin/main` outside `.copilot-tracking/` (same paths and content).
* P6 Add changes, review and state records, then commit. Write the handoff in the coordinator session files directory.
* P7 Validation tier: pure documentation, owner demo tier, no local gate, no tests, services or deployment. Checks: relative-link existence in the new records, Markdown review, scoped diff inventory.
* P8 No push, PR, board or issue writes. Use `Refs #136` only; all five criteria stay open.

## Critique

One independent critique of this prospective plan runs before implementation; it is recorded in the Critique result section below and is not repeated.

## Success

Clean frozen local head; merge commit has parents `24d1cfb16` and `d4d6827fe`; P5 equality holds; no 136 criterion is claimed.

## Critique result

Pending at the time of the plan commit; appended below by the critique step.
