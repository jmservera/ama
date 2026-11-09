---
title: Visible-demo integration checkpoint 440 C2 changes
ms.date: 2026-11-08
---

## Changes

* `docs/architecture/cutover-evidence-pack.md` line 3243: stored route now "can call `ChatModel` ... at most once per turn and only after `chat_admission`" (R1).
* Same file line 3266: the trace row now points to the one observed generic model answer and states that case-grounded provider behavior and human acceptance are not shown (R2).
* Same file, new "C2 provenance note" subsection before the recommendation: records the C1 wall-clock conflict, unknown cause, no witness, C1 preserved (R3).
* `docs/reference/log.md`: one appended entry; earlier bytes identical.

## Validation (actual)

* `git diff --check`: exit 0.
* Non-ASCII in added lines: none.
* Log prefix byte comparison (`cmp -n`): exit 0.
* Pack diff hunks only at lines 3243, 3266 and 3277; text before 3243 untouched.
* `git fetch origin main`: `6354b13f7abf1441a815e92f2b01dc184ce0b0ac`, unchanged.
* C2 research/plan commit `cd3050b01` (2026-11-08T20:13:09Z) precedes the edits.
* Not run: tests, SQL, browser, model, Azure, hosted checks. No repository-wide documentation check exists.
