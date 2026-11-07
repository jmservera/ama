---
title: Issue 1251 explicit-inactive conflict review
description: Original single post-implementation review with acceptance-criteria mapping
ms.date: 2026-11-07
ms.topic: reference
---

## Execution and outcome

* Executed once after implementation, on the uncommitted candidate on base 8af3aea6b042f5dfb3305e18334439717f7c5649; review boundary: `tools/backlog-sync.py`, `tools/test_backlog_sync.py`, dated RPI records.
* Outcome: Conformant for the tooling change with the open items below. This is an author-session review; independent exact-head assessment and hosted CI remain required and are not claimed.

## Acceptance criteria

* Regression from the observed inputs fails on baseline: proven (`red.log` exit 1, 5 failures; `repro-baseline.log` writes In Progress). No worktree pathway invented.
* Inactive with no PR evidence stays or returns Todo: covered (`test_explicit_inactive_demotes_only_named_issue`, missing-unreferenced test, merged-reference-only test).
* Active protected; inactive versus open PR gives diagnostic and no write from Todo and In Progress; overlap rejected before writes: covered (conflict, active-protected, existing invalid-evidence tests). "Frozen" is the same `--active` input.
* Unknown, closed checkbox, missing additions, merged review, audit zero write unchanged: existing tests unmodified and passing, plus new harness coverage of `item-add`.
* Full RPI loop and original Review: this record. Main-targeting PR and independent exact-head review: coordinator work, not done here.

## Findings

* Low: a prose-only mention (the #1239 parent-stack sentence) still yields a conflict diagnostic on every run until that PR merges, and an inactive In Progress issue referenced that way stays In Progress. This follows the issue's decided no-silent-choice rule; reference classification is a later optional follow-up.
* Low: the `--changed` runner was not run; the sole heavy lock belongs to #107 and the focused unit suite is the planned check. No receipt is claimed.
* Disclosure: the backlog-planning skill's shared reference was missing, so no complete validation against it is claimed.

## Routing

* Optional follow-up: classify PR references (closing keyword, title or branch versus prose). Not required for #1251 acceptance; no further work in this task.
* Issue closure: `Closes #1251` only if the coordinator's independent assessment proves every criterion including the PR/review criterion; otherwise `Refs #1251`.
