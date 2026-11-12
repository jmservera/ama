---
title: Issue 116 offline provider-payload spies plan critique
ms.date: 2026-11-12
task_id: provider-payload-spies-116-1112
---

## Execution and verdict

One independent critique (rubber-duck agent, claude-sonnet-5.5) of the final candidate plan, executed once. Original verdict: Revise.

## Original findings and dispositions

* PC-001 (blocking): the assistant oracle compared wire evidence with `capture` output and checked top-level categories only. Applied: literal expected nested `sources` per capability from the constructed fixture, independent of `capture`.
* PC-002 (blocking): legacy role differences were understated (citable labels, 14-label cap, document names). Applied: literal citable suffix; the first 14 labels exclude the role-dependent ones for this fixture; both role scenarios labelled characterisation.
* PC-003 (non-blocking): optional `sensors` source and dispatch-time state. Disposition: not covered, recorded in the changes file; the no-sensors branch has a literal expected shape.
* PC-004 (non-blocking): environment isolation. Applied in `setUp`.

The critique confirmed the gap is real but partial (`test_sensor_privacy.py` already checks one legacy body against two sensor sentinels) and that the reason-role override describes current behaviour, not an OD-14/OD-19 decision. No user decision was required and the critique was not repeated.
