---
title: Issue 1251 explicit-inactive promotion root cause research
description: Evidence-based root cause for backlog-sync promoting an explicitly inactive issue to In Progress
ms.date: 2026-11-07
ms.topic: reference
---

## Scope

* Issue [#1251](https://github.com/jmservera/ama/issues/1251); task `backlog-inactive-conflict-1251`; branch `fix/backlog-inactive-conflict-1251`; clean `main` 8af3aea6b042f5dfb3305e18334439717f7c5649; helper blob 8c82130c5fdb649e23bdd005723134f1f3ccbf01.
* Files in scope: `tools/backlog-sync.py`, `tools/test_backlog_sync.py`, dated RPI records.
* Disclosure: the backlog-planning skill's shared reference was missing, so no complete validation against it is claimed. No generic issue template exists.
* Research disposition: executed. Planning Readiness: Ready.

## Inputs (read-only, external)

* `/mnt/ama-gates/r1251-repro-inputs-1107/open-prs.json` (8 open PRs), `issue-80.json`, `board-before-manual-correction.json` (500 items, state after the promotion).
* Only the fields the reconciliation consumes are copied into the test fixture: PR number, title, head branch and the single sentence mentioning #80. The board, raw PR bodies and other captures are not committed.
* Invocation: `--active 79,81,86,1231,107 --inactive 80,108`.

## Findings

* `refs()` in `main()` records every `#N` or `issue-N` token in an open PR's title, body or head branch as evidence for N. A reference is treated as an open implementation.
* `desired_status` returns In Progress when `has_open_pr` is true, before consulting `confirmed_inactive`. Inactive evidence is therefore never compared to PR evidence.
* Open PR #1239 (`feat(ranking): publication runner (#79)`, branch `feat/ranking-publication-runner-79`) references #79 and #1231 as intended, and its body says "Parent of the #1231 and #80 stacks". That sentence is the only mention of #80 in any open PR. #80 has no PR of its own (no `issue-80` branch, no `#80` title).
* #80 was Todo and inactive, so the apply wrote Todo to In Progress, matching `#80 open: board Todo -> In Progress`.
* #108 is Todo, inactive and unreferenced by any open PR: unaffected.
* Worktree theory: the helper never inspects worktrees (no `git worktree`, filesystem or branch calls). Not a trigger; no worktree pathway is reproduced.

## Offline reproduction (baseline)

* Harness: `tools/test_backlog_sync.py` `run()` with mocked `gh`; no board write. Log: `/mnt/ama-gates/g1251-focused-1107/repro-baseline.log`.
* Result: one write, `project item-edit i80 -> o-prog`; output `#80 open: board Todo -> In Progress`.

## Reference versus implementation

* A mention in prose, such as a parent-stack description, is a PR reference, not proof of an unmerged implementation of that issue. Distinguishing intent by parsing text is heuristic and out of scope for the smallest fix.
* The issue's decided behaviour: explicit inactive input versus current open-PR evidence is a conflict. Report it and leave the affected status unchanged from either starting status.

## Existing behaviour to preserve

* `test_open_pr_outranks_inactive` currently passes by silently keeping In Progress; the new requirement is an explicit diagnostic.
* Closed-issue checkbox edits and Done status, missing-item additions, unknown In Progress kept and reported, merged-reference review list, audit zero writes, active/inactive overlap and non-open evidence rejection before writes.

## Follow-ups

* Optional later work: classify PR references by closing keyword or title/branch versus prose, to reduce repeated conflict diagnostics. Not required and not in this change.
