---
title: API discovery dirties owned gate source snapshots
description: Issue metadata and literal acceptance criteria for gate bytecode defect 1215
ms.date: 2026-11-05
ms.topic: reference
---

## Issue

* Issue: #1215, https://github.com/jmservera/ama/issues/1215
* Title: fix(tools): prevent API discovery from dirtying owned gate source snapshots
* Created (UTC, from GitHub createdAt): 2026-11-05T11:23:34Z
* State when read: OPEN
* Template: generic; no custom template.
* Labels: none. Assignees: none.
* Related: Refs #96, #1208, #440. Separate from #1214 (CSS layout).

## Literal acceptance criteria (all unticked; this branch does not tick them)

* [ ] Reproduce and identify the actual API-discovery source-bytecode producer and source/environment/order identities, distinguishing observed evidence from inference.
* [ ] Make the smallest existing-contract correction that prevents source-tree bytecode during that real path, without weakening isolation, environment scrubbing or dirty-input/cleanup checks.
* [ ] Add a focused regression of the affected gate/child-environment integration that fails before the correction; do not merely test generic Python bytecode behavior or constants.
* [ ] Run relevant existing gate-tool unit/focused checks and the maintained real Runner UI smoke where applicable; report real process exits, skips and input identities.
* [ ] Preserve the immutable failed receipt, snapshot, original/adverse RPI and verification images; deliver genuine dated RPI artifacts, independent exact-head review and hosted checks without claiming a fresh complete full receipt from partial evidence.

## Scope

* Declared target: main. Starting reviewed main: c6d5a8f3c3a35892322300be27b9747f7b11362d.
* Proposed tier: FOCUSED (gate tooling only; no SQL, security, finance, infrastructure or deployment change).
