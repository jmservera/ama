---
title: Ranking archive metadata under concurrent writers
description: Recorded scoped bug for the inherited #79 archive helper race, separate from #79 evidence
ms.date: 2026-11-06
ms.topic: reference
---

## Created Issue

* Issue: #1231, https://github.com/jmservera/ama/issues/1231
* Title: fix(core): preserve ranking archive metadata under concurrent writers
* Created: 2026-11-06 by the coordinator with `gh` after independent duplicate searches (the backlog-manager tool was absent); readback in the coordinator session file `ranking-archive-race-created-r32.json`.
* Template: generic bug; `.github/ISSUE_TEMPLATE` has none. Label: `bug`. No assignee. The referenced plugin file `instructions/github/github-backlog-planning.instructions.md` was missing and was not loaded.
* Parent: #79 (native link confirmed by the coordinator); grandparent #73. This record is metadata only and is not permission to alter #79 evidence.

## Source and dependency

* Original diagnosis: #79 r11 session, `/tmp/79-concurrency-r11-1106/` (probe SHA-256 `f2fca2441759454644eee141b234b5214e7dc9115c9c1fbb16f6bcfe95c7017a`, exit 0, fixtures `5ee9e737...a82c08` control and `8fd0b0a1...c832e` interleave). Research and Plan 04:25:02Z predate probe creation 04:25:11Z and execution 04:25:14Z.
* Dependency: #79 runner and fixtures at frozen commit `397419724e68b24bce879512a24c7df430177f87`, tree `c728049e33a3a0e20d9a7bf16b3738fabfbc14d7`.
* Child branch `fix/ranking-archive-concurrent-writer-metadata`; eventual PR targets `feat/ranking-publication-runner-79`, not main. Use `Refs #1231` until all criteria are proven.

## Confirmed limits

One deterministic two-thread interleaving in one process on a local filesystem. No lost publication, no finished-record overwrite probe, no production, separate-process, Windows or network-filesystem measurement. Selected eventual tier FULL, pending; independent assessment and publication pending.
