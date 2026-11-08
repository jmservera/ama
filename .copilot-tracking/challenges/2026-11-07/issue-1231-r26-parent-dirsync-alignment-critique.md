---
title: Issue 1231 r26 plan critique
description: Prospective one-pass author-only critique of the r26 parent dirsync alignment plan
ms.date: 2026-11-07
---

Author-run, NOT independent, before mutation. Verdict: proceed with the amendments below.

| ID | Severity | Concern | Disposition |
| --- | --- | --- | --- |
| C-01 | High | Textual auto-merge hides a semantic collision: the broad OSError to 503 translation would swallow DurabilityUnconfirmedError, dropping the audit and 409. | Specific handler first; regression through Store and API. |
| C-02 | High | Parent exception without errno would break the child's existing errno EIO assertion. | Carry cause errno; assertions unchanged. |
| C-03 | High | Copying the parent's "retry does not confirm" claim would be false for the child. | README integrated wording; the retry re-attempts the sync. |
| C-04 | Medium | A retry or race loser whose sync fails must not claim confirmation. | _confirmed raises the unconfirmed error on every path. |
| C-05 | Medium | Double sync or lost stage_retained marker. | Single sync path; error carries stage_retained. |
| C-06 | Medium | Other archive failures must stay 503 and path-free. | Handler untouched; existing tests retained. |
| C-07 | Medium | Parent appended docs/reference/log.md beyond its narrow scope. | Preserve, record as a parent scope deviation, no rewrite and no child KB edit. |
| C-08 | Low | Stale receipts. | r25 receipt valid only for old head; new FULL required. |
| C-09 | Low | Open gaps (cross-UID, real mount, real fs fault, future date; author-only critique and Review). | Not claimed closed. |
