---
title: Issue 82 round 1 details
ms.date: 2026-11-03
---

* `gates.check` passes only on boolean True; None or non-boolean evidence is unknown; a rule not yet effective is unknown.
* `transition_allowed` is false for an empty gate list or any non-pass.
* `safety_release_gate` compares the actor role to the hold's `accountable_role` (case-insensitive), fails on wrong role, returns unknown if the role or the actor identity is absent.
* `release_hazard` applies the role check only when the hold has an accountable role and is not legacy.
* Manual path and AI-unavailable behaviour: no AI involved; the release stays a recorded human decision.
