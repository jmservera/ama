---
title: Issue 360 live plan details
ms.date: 2026-11-20
---

## Phase 1 details

File: src/core/src/zava_forward/core/assistants.py, `authorize`. Import `identity` from the package if absent. A `verified` return of None raises the existing PermissionError "Current staff role has changed or been revoked." The remaining role, disabled, malformed-scope and case checks run unchanged on the verified copy.

## Phase 2 details

Entra fixtures via `identity.principal(tid, oid, role, ...)`. Direct `self.service.sensors` and `self.service.map_sensors` calls inside `MapSensors` (existing seed with ZF-1 readings).
