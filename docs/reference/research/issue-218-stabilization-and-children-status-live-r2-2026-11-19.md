---
title: Epic 218 stabilization and child status, live demo r2
description: Per-criterion proven or unproven status for epic 218 on 2026-11-19, with the reason no source change is supported
ms.date: 2026-11-19
ms.topic: reference
---

Refs #218. Scope: synthetic desktop demo under the owner decisions of 2026-11-18. No source, Azure or issue state was changed.

## Observations (2026-11-19)

* `gh issue view`: #440 OPEN; #219 CLOSED; #220, #221, #222, #223, #224 OPEN.
* `az containerapp show -g ama -n ca-cutover-test-demo-api`: revision `ca-cutover-test-demo-api--0000033`, image digest `sha256:5368f4e4...`, unchanged since the [r1 note](./issue-218-first-unmet-demo-criterion-2026-11-19.md).
* The [440 triage note](./stabilization-checkpoint-triage-440-live-2026-11-18.md) holds the latest checkpoint verdicts.

## Result

The first unticked criterion, the #440 stabilization checkpoint, has two unticked items of its own (owner-approved triage and deferrals; PR-delivered artifacts with independent review). Both need the owner or a pull request, and merged children cannot satisfy it. The second, "children closed or deferred by the owner", needs an owner deferral comment per child. Neither is deliverable as code, so no source change is made. A redeploy to observe the #220 staff write live would be a deployment change (FULL tier) and was not attempted.

| Criterion | Demo status | Basis |
| --- | --- | --- |
| Stabilization checkpoint (#440) | Unproven | #440 open; owner gates remain |
| Children closed or deferred | Unproven | #220 to #224 open; no issue-level owner deferral |
| No live AI activation without named approval | Already ticked | Not re-tested |
| Requirements trace to a check or deferral | Already ticked | Not re-tested |
| RAI checks reported separately from the real-AI gate | Already ticked | Not re-tested |
