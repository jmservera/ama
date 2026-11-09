---
title: Issue 891 VM demo release review
description: Original-author review of the VM release against the plan and owner decision
ms.date: 2026-11-08
---

## Execution and outcome

Review executed once by the original author. Outcome: release criteria met; live model proof NOT met.

* Met: exact-head hosted CI success, local startup, Trivy and SBOM, digest deploy, ACR restore readback, env-name parity, health 200, anonymous 401.
* Not met: genuine model-labelled employee chat on the new revision. Blocker: expected tenant/object cannot be independently verified (Entra read denied to the Azure CLI identity), so the strict identity predicate cannot be built; no sign-in attempted and no consumed attempt slot replayed.
* Not claimed: acceptance, #891 criteria ticks, AI autonomy, Legal, DPO, Finance or RAI approval.

## Routed follow-up

An owner-held expected object id (or an Entra read grant) plus a finite fresh attempt manifest enables the guarded employee ask. A reviewed in-process credential runner is still uncommitted.
