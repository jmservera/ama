---
title: Demo stabilization checkpoint 440 plan critique
ms.date: 2026-11-09
---

## Verdict

Revise (single critique; no second critique runs). Worker findings returned inline; planner recorded them here verbatim in substance and verified each anchor.

## Findings

* PC-001 Blocking. Research resume condition 5 required provider-request values, conflicting with PRD AC-067. Owner planner. No user decision. Applied.
* PC-002 Blocking. Work-package identity unexamined; image digest is not that identity. Owner planner. No user decision. Applied (unknown).
* PC-003 Blocking. Auth trusts the ingress header and does not validate token signatures (`src/api/src/zava_forward/api/auth.py:7-14`, verified). Owner planner. No user decision. Applied.
* PC-004 Non-blocking. Consent and window checks are at `sensor_consumer.py:603-611`, not `:431` (verified). Owner planner. No user decision. Applied.
* PC-005 Non-blocking. AC1 named five paths, scope names three. Owner planner. No user decision. Applied.
