---
title: Issue 146 live plan critique (single pass)
ms.date: 2026-11-25
---

Execution: one pass on the final candidate plan. Verdict: proceed with changes applied directly.

* Do not enable disabled alerts or redeploy the workbook: needs named-human approval and is an estate change outside the goal. Applied: plan is read-only plus throwaway resources.
* Do not weaken storage network or key policy to force the poison test. Applied: attempt stops at the policy block and is recorded as unproven.
* Claims must separate executed-query proof from Portal render. Applied in the note.
* Throwaway resources must be deleted and the deletion checked. Applied.
* No src change, so the focused tier applies; never run rpi-checks.py --all. Applied.
