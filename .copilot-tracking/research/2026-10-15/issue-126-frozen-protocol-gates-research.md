---
title: Issue 126 frozen protocol and release gates research
ms.date: 2026-10-15
---

* Sources: issue #126 (parent #123); BRD RULE-019 (AC-062/074-077/085), RULE-020 (AC-063), RULE-024 (AC-078), BG-011 and OD-18 text; ADR 0005 (labelled synthetic fixtures only).
* Existing code: controlled workflows use mixins on `Store`; `SqlStore` persists only cases, recommendations and one `procurement` meta document; time capture is already gated by DPIA reference env vars.
* Decision: add one `GovernanceMixin` (no new service), persist as a second checked meta document in `SqlStore`, expose manager-only API routes.
* Planning readiness: Ready. Research disposition: executed.
* Open items: real OD-18 definitions and MDE, OD-36 DPIA and lawful basis, OD-35 authority, actual approvers, and the RAI closure registers and fresh assessment (owner and evidence needed).
