---
title: Issue 233 record recovery details
description: Phase details for the single metadata recovery
ms.date: 2026-11-10
---

## Phase 1

Create `.copilot-tracking/changes/2026-11-10/issue-233-record-recovery-1110-changes.md` as a pending-implementation stub; confirm it is non-empty and that the state lists it and the plan and critique paths; then call implement-start.

## Phase 2

`.copilot-tracking/github-issues/issue-1362.md`: URL, open state, generic template with no labels, type or assignee, Refs #233 and #149, the Medium finding with file and lines, static-counterexample wording, suggested direction, explicit no-fix and balance UNKNOWN.

## Phase 3

Changes record lists the new files, the qualification (coverage PARTIAL), provenance qualification, Root diagnostics 1394 to 1397, producer-only observations, the stopped first attempt (4 events, refusal) and the three witness dispositions. Append one dated entry to `docs/reference/log.md`; no earlier entry is rewritten and no index row is needed.

## Phase 4

Single review of the diff; state updated; implement-done then review-done.

## Phase 5

Checks: `git diff --stat 6725 -- src infra tools .github` empty; changed paths limited to new `.copilot-tracking` files and the log; relative links resolve; privacy-safe identity; required trailer; message `Refs #233, #149, #1362`.
