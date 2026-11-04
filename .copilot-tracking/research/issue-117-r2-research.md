---
title: Issue 117 round 2 research
ms.date: 2026-11-04
---

* Issue 117 comments, PRs #270, #395, #918 and the 2026-10-31 closure audit were read on main f222876a7.
* Criterion 2 is proven and ticked. Criterion 1 holds in code (pending, unknown and bad scans deny availability) but only with the synthetic scanner and a Defender tag reader over a fake transport.
* infra/modules/containerapps.bicep still sets ZF_DOC_STORE=azure-blob without ZF_SCANNER; #918 only logs a warning.
* Remaining work is Azure and human: enable Defender for Storage, set ZF_SCANNER=defender in the deployment, capture real-account evidence, hosted rescan cadence and monitoring, and DPO/Legal and record-owner approval of retention periods.
* No engineering slice is left that advances criterion 1 without infrastructure change; infrastructure and deployment work needs the coordinator gate and owner authorization.
* Planning readiness: Ready for a docs-only record.
