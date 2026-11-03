---
title: Issue 164 chat threshold checks plan
ms.date: 2026-11-03
---

Slice 2: add `threshold_checks` to chat eval enablement. Floors apply only when thresholds are approved; mismatched bindings or unmeasured rates give insufficient; below floor gives fail. Details: [details](../../details/2026-11-03/issue-164-chat-threshold-checks-details.md).

Critique (executed once, proceed): never default thresholds, never output pass for enablement, test only with constructed fixtures, no model calls.
