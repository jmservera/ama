---
title: Issue 1251 explicit-inactive conflict phase details
description: Phase details for the backlog-sync inactive versus open-PR conflict fix
ms.date: 2026-11-07
ms.topic: reference
---

## Phase 1: tests first

* Add a sanitized fixture of PR #1239 (title, branch, the one sentence) and the observed argument set; regression: #80 Todo, inactive, referenced only by that PR, must produce no write and a conflict diagnostic. Fails on baseline with `o-prog`.
* Parametrize the conflict over Todo and In Progress starts; update `test_open_pr_outranks_inactive` to assert the diagnostic.
* Cover: inactive without PR evidence stays Todo and In Progress goes to Todo; active with PR protected; conflict for a missing board item adds nothing; audit zero writes; conflicting issue does not block other writes (closed ticks, missing adds, other statuses); merged reference does not create a conflict.
* Existing overlap and unknown tests stay unchanged.

## Phase 2: fix

* In the `main()` loop, for an open issue with `n in inactive and n in open_ref`, print `#N conflict: --inactive contradicts open PR(s) [..]; status X left unchanged`, collect it, set `want = current` so no write occurs. Keep `desired_status` unchanged.
* Update the module docstring rule list.

## Phase 3: validation and record

* Run the focused commands on the frozen HEAD with external logs. Write changes and review records; commit once with implementation and evidence.
