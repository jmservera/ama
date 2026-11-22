---
title: Issue 2205 live critique
ms.date: 2026-11-22
---

Executed once. Verdict: proceed, no source change.

* The goal asks for an `az containerapp update`; the value is already set, so a repeat is a no-op. Accepted: record, do not rewrite. Direct disposition.
* Risk: claiming authority is present. Rejected; record `false` and OQ-017.
* Risk: printing credentials. Probe reads them at runtime only.
