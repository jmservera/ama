---
title: Issue 360 live research, run b
ms.date: 2026-11-19
---

Refs #360. Disposition: satisfied-and-skipped. Planning Readiness: Ready.

* Issue #360 (read 2026-11-19): criteria a to f are all ticked; c, d and e carry "moved to #2121".
* Issue #2121 (open) holds the unticked c, d and e: owner approval, live verification and owner-authorised Front Door retirement.
* A run earlier on 2026-11-19 already recorded live evidence and the per-criterion result in docs/reference/research/issue-360-live-20261119-2026-11-19.md and .copilot-tracking/changes/2026-11-19/issue-360-live-changes.md (on main).
* Owner decision 2026-11-18 removes billing, DPO/Legal and person-run assistive-technology testing from demo scope.
* The one open code gap under d (browser-mode 401, `infra/modules/containerapps.bicep`) is an authentication and deployment change, so it needs the FULL tier and is not a demo-provable change here.

Conclusion: no unticked criterion in #360 can be proven or built with new code and tests in this tier. Nothing in #2121 c or e can be supplied by an agent.
