---
title: Epic 73 criterion audit and local clock proof (2026-11-19, demo)
description: Per-criterion proven/unproven audit of epic 73 and a new HTTP test for hazard and safeguarding clocks on list rows
ms.date: 2026-11-19
---

Refs #73. Synthetic demo, desktop only; no Azure resource was created or changed and no demo data was written.

## Method

The issue and its six children were read with `gh`. Open children: #76, #79, #80. The first unmet child criterion is #76 "Hazard and safeguarding items show a clock and named owner". Earlier live passes ([third pass](./issue-76-live-r3-2026-11-18.md)) found 1 of 16 live cases with a hazard clock of unknown value and none with a safeguarding item; seeding would write demo data, so the live half stays unproven.

New local evidence: [test_list_clocks_over_http_76.py](../../../src/api/tests/test_list_clocks_over_http_76.py) starts the real `App` over HTTP on a constructed synthetic store (one hazard with `aware_at`, one overdue safeguarding item) and asserts, for every role that sees the case, a named owner, elapsed hours, response state and due date in both `/api/cases` rows and `/api/cases/{id}`. Earlier tests covered only detail, Node rendering and the core evaluator. Result: 1 test, OK.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Epic: scoped stabilization checkpoint (#440) | Unproven | Needs an owner-recorded checkpoint; merged children alone do not satisfy it |
| Epic: all children closed or deferred | Unproven | #76, #79 and #80 are open; no owner deferral recorded |
| Epic: each requirement traces to a passing check or deferral | Unproven | Traceability not re-derived in this run |
| #76 hazard and safeguarding clock and owner | Partly proven | Local HTTP proof for both kinds; live demo has unknown hazard value and no safeguarding item |
| #79 named policy owner signs first rule order | Unproven | Needs a named human signature |
| #79 snapshot publication scheduled and retained | Unproven | Code exists; scheduled live publication not shown here |
| #80 owners set staged transition thresholds | Unproven | Owner decision, not code |
