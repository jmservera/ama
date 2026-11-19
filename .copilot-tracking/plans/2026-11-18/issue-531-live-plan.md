---
title: Issue 531 live verification plan
description: Plan to record live demo evidence for the unticked criterion of issue 531 without source changes
ms.date: 2026-11-18
---

## Objective

Prove or bound criterion 7 of #531 on the live demo and keep the evidence in the knowledge base. Focused tier; no source change; Refs #531 only.

## Phases

* [x] Phase 1: add `docs/reference/research/issue-531-live-demo-evidence-2026-11-18.md` with the per-criterion table, method, adverse observations and limits.
* [x] Phase 2: update `docs/reference/README.md` index and append the `docs/reference/log.md` entry.
* [x] Phase 3: retain probe, JSON and screenshots under `.copilot-tracking/evidence/2026-11-18/issue-531-live/`.
* [x] Phase 4: validate links and diff, record changes and review, commit locally with trailers.

## Validation

Markdown link and diff review; secret scan of retained files; no unit tests apply because no executable changed. Critique: [issue-531-live-critique](../../critique/2026-11-18-issue-531-live-critique.md).
