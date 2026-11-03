---
title: Chat Administrator and Break-Glass Demo-Only Disclaimer
description: Owner decision of 2026-11-03 that sets a demo-only administrator and break-glass policy for chat and memory, recorded as unreviewed by the DPO and Legal
author: AMA programme
ms.date: 2026-11-03
ms.topic: reference
---

## Decision

On 2026-11-03 the owner approved a demo-only disclaimer in place of the DPO and
Legal decision for criterion 6 of #162 (BRD OD-46). This is the owner's decision
as relayed to the agent. It is not a legal opinion, and no agent has decided
that a legal duty is met.

## Disclaimer

Demo-only policy for synthetic data, approved by the owner on 2026-11-03. It
has not been reviewed by the DPO or Legal and is not approval for real personal
data or production use.

## Policy

Option A in the [proposed policy](./chat-memory-dpia.md#proposed-administrator-and-break-glass-policy-brd-od-46-not-decided)
applies to the demo only.

* Administrators and break-glass users see counts for a named user, never message or memory text.
* A written purpose of 10 or more characters and a named role in `CHAT_BREAKGLASS_ROLES` are required.
* Access stays refused until `CHAT_BREAKGLASS_REF` points to this record.
* Granted and refused attempts are audited with actor, target, redacted purpose and `basis` of `demo-only`.
* The response carries the disclaimer above.
* Content access (option B) is not permitted and needs a separate DPO and Legal decision.

## Not decided

* DPO and Legal review of this policy: unreviewed.
* Which Entra app role is the administrator, user notification after access, and audit retention period.
* Any production or real-data use.
