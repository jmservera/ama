---
title: Research for issue 2164 live r10
ms.date: 2026-11-23
---

Disposition: reused plus one new source read. Prior notes in `docs/reference/research/issue-2164-*.md` prove the inheritance decision, `view_only` denial and scope bypass in assistants. The issue body has no checklist, so its three asks are the criteria.

New finding: `Assistants.authorize` and `sensor_review_draft._gate` accept a roster row without a `tid` for any tenant (`tid in (None, "", user.tid)`), whereas `identity.matches`, which created the binding, accepts a tenant-less row only when the store's legacy tenant equals the principal's tenant. A principal whose bound pointer was forged or went stale could therefore inherit a tenant-less row from another tenant. No test covers a forged bound pointer, row tenant mismatch, or positive `areas` scope on this base (commit ab7d029065 is not an ancestor).

Planning Readiness: Ready. No Azure action: the restricted-row live proof needs a live roster edit, excluded for the demo.
