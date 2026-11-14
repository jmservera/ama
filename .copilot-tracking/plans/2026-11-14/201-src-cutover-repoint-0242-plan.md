---
title: Plan, src cutover repoint contract (Refs #201)
ms.date: 2026-11-14
---

## Plan

* [x] Phase 1: Add `tools/test_src_cutover_repoint.py` (workflow, Dockerfile, infra contracts).
* [x] Phase 2: Validate with ruff, unittest and `tools/rename-zava-tests.py`.
* [x] Phase 3: Commit locally with `Refs #201`, no push.

Details: [phase details](../../details/2026-11-14/201-src-cutover-repoint-0242-details.md).

## Critique (single pass)

Executed once. Verdict: proceed. Compatible findings applied directly: allow the negative `git ls-files mvp/data` guard, exclude documented cutover-proof files, parse YAML key `on` as boolean True.

## Decisions

* Focused validation tier: test-only tooling, no workflow, permission, package or gate change.
* Use `Refs #201 only`.
