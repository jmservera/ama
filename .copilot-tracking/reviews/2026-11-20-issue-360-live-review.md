---
title: Issue 360 live review
ms.date: 2026-11-20
---

## Review (one pass)

* Outcome: conformant for the scoped defect.
* The change widens no access: REGISTRY role check precedes the lookup, `verified` rejects mismatched keys, and non-Entra users take the unchanged roster path.
* Entra principals have no case_ids/areas scope, matching the coordinator path.
* Routed later work: deploy the fix and confirm live with a browser proof (needs owner-approved deployment); other modules that read `staff` by email for Entra users should be audited.
* Residual: live proof unproven; full-tier gate owned by the coordinator.
