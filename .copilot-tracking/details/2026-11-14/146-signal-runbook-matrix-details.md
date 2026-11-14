---
title: Alert signal matrix test details (Refs #146)
ms.date: 2026-11-14
---

## Phase 1

* Discover alert and budget declarations by regex across `infra/**/*.bicep`.
* Assert exact equality with a matrix of alert name to runbook anchors, and budget notifications to anchors.
* Assert every anchor, plus the four AI limit anchors, has an owner statement (own, child or parent section).
* Assert rule descriptions carry owner and runbook link; main wires the action group and candidate flags.
