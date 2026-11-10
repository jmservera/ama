---
title: Issue 96 independent record details
description: Phase details
ms.date: 2026-11-10
---

## Phase 1

The record states reviewer, exact head and tree, scope, verdict, limits, guard wording, validation as observed, and what is not claimed. It does not edit earlier records.

## Phase 2

`git diff --name-only 612d7604 HEAD` must list only `.copilot-tracking/` paths and `git diff 612d7604 HEAD -- src` must be empty.
