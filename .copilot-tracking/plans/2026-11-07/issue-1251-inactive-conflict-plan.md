---
title: Issue 1251 explicit-inactive conflict plan
description: Plan to report inactive versus open-PR conflicts in backlog-sync without writing the affected status
ms.date: 2026-11-07
ms.topic: reference
---

## Objective

Make `tools/backlog-sync.py` report, and not write, the status of an open issue named `--inactive` that a current open PR references, from either Todo or In Progress. Keep all other behaviour.

## Context

* [Research](../../research/2026-11-07/issue-1251-inactive-conflict-research.md), [details](../../details/2026-11-07/issue-1251-inactive-conflict-details.md), [critique](../../challenges/2026-11-07/issue-1251-inactive-conflict-critique.md).
* Tier: FOCUSED small tooling. No FULL gate, services, SQL, browser, scanners, images or lock waiting.

## Phases

* [ ] Phase 1: regression tests; capture RED on the unmodified baseline
* [ ] Phase 2: smallest source fix and docstring update; capture GREEN
* [ ] Phase 3: focused checks on the final exact HEAD, changes record, single Review

## Hand-off

* Main-targeting PR and independent exact-head assessment are coordinator work after this session, with hosted CI; no push or PR here. Critique disposition: see the critique record.

## Validation

* `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_backlog_sync.py' -v`
* `python3 -m py_compile` equivalent via compile in scratch, repository-configured formatter/linter check if present (ruff), `git diff --check`.
* Scratch and caches under `/mnt/ama-gates/g1251-focused-1107`. `rpi-checks.py --changed` only if safely non-queued; otherwise record non-applicability.
