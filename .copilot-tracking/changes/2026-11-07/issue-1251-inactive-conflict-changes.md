---
title: Issue 1251 explicit-inactive conflict changes
description: Original change record for the backlog-sync inactive versus open-PR conflict fix
ms.date: 2026-11-07
ms.topic: reference
---

## Changes

* `tools/backlog-sync.py`: an open issue named `--inactive` that an open PR references is now reported as `#N conflict: --inactive contradicts open PR(s) [...]; status X left unchanged` and receives no status write, from Todo, In Progress or missing. Docstring rule added. `desired_status` is unchanged.
* `tools/test_backlog_sync.py`: harness records `project item-add`; added regression from the sanitized #1239 "Parent of the #1231 and #80 stacks" input, both-start-status conflict, active protection, no-block of other writes, missing-item (conflicting and unrelated), audit zero writes and merged-reference-only cases; replaced the silent `test_open_pr_outranks_inactive`.
* `.copilot-tracking/`: issue metadata, research, plan, details, critique, this record and the review.

## Evidence

* Root cause: PR mention treated as open-PR evidence and `has_open_pr` ranked above inactive evidence; see [research](../../research/2026-11-07/issue-1251-inactive-conflict-research.md).
* Offline baseline reproduction: `/mnt/ama-gates/g1251-focused-1107/repro-baseline.log` (one `item-edit` to In Progress).
* RED on unmodified source: `red.log`, exit 1, 5 failures in 17 tests. GREEN: `green.log`, exit 0, 17 tests OK. Final exact-HEAD results are external under the same directory.

## Amendments and divergences

* Critique finding 2 (harness lacked `item-add`) applied. Finding 1 rejected (PR and independent review are coordinator work).
* No divergence from plan. No real board write was made.

## Not done

* No FULL gate, `--changed` runner (see review for applicability), push, PR, issue ticking or closure.
