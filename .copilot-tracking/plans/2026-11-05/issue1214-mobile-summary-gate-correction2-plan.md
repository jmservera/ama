---
title: Issue 1214 correction cycle 2 plan
description: Bounded plan for a rebased, exact-final-head maintained runner execution
ms.date: 2026-11-05
ms.topic: reference
---

## Executive Summary

Rebase onto main 180dcf3e2 (done), commit cycle 2 records first, then run the maintained focused runner once on that final head with the heavy lock nonblocking, verify the partial receipt, and hand off without another commit. No source change beyond the existing CSS rule. The original plan, critique and reviews stand; no second critique is run because plan scope is unchanged (execution-evidence correction only).

## Goals and Scope

* Goal: exact-final-head evidence from the real runner (preflight, project-api with 72 relevant units inside the API suite, namespace, static, browser with 407 assertions, image-api, logo-0600) on a clean head.
* Non-goals: source/tool changes, full matrix, hosted claims, cleanup, publication.

## Phase Checklist

### [x] P01 Rebase and pin
* [x] P01-T01 Verify #1217 merged; fetch and pin origin/main 180dcf3e2; rebase.
### [ ] P02 Records and freeze
* [x] P02-T01 Write cycle 2 research, plan, changes, review before gating.
* [ ] P02-T02 Commit; confirm clean tree and ignored status.
### [ ] P03 Runner execution on the frozen head
* [ ] P03-T01 Run `python3 -B tools/rpi-checks.py --changed --jobs 3 --lock-timeout 0 --base 180dcf3e2 --out <short external dir>`.
* [ ] P03-T02 Verify with `--verify-receipt --required-scope partial`.
* Stop rule: a real failure stops this lane; preserve evidence; do not retry in a loop.

## Critique Disposition

Not re-run: one critique already executed for this task; plan content is unchanged. Original verdict Revise and its dispositions stay in the original plan.

## Follow-Up Items

* Results of P03 are external (receipt path/hash in the handoff) because a post-gate commit would invalidate them.
