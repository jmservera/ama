---
title: Issue 104 criterion 5 details
ms.date: 2026-11-14
---

* Signature: `authorize(..., alert: str | None = None, alert_owner: str | None = None)`; synthetic prices stay unchanged and store no alert fields.
* `OPTIONAL = {"authority": {"alert", "alert_owner"}}` lets `_read` accept both shapes without invalidating the ledger.
* Alert id and owner are stored as `reference()` digests like the owner.
* Unknown (unrecorded) prices skip the authorize check because `reserve` already holds `price-unknown`.
* Alert `route` stays `workflow-only` so the workbook query and existing assertions hold.
