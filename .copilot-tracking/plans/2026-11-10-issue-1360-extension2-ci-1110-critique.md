---
title: Issue 1360 extension 2 CI regression critique
ms.date: 2026-11-10
task_id: 1360-extension2-ci-1110
---

One independent critique pass (rubber-duck agent, read-only, executed once). Verdict: approve with changes. No blocking finding; the approach is sound and smallest.

* Non-blocking: a leaked marker would silently restore the shared-contract regression. Disposition accepted directly: save and restore the previous marker value in `finally`, and add controls that a plain `save()` on the same store and thread raises the original error after both a successful and a failed refusal write.
* Confirmed by the reviewer: existing importer tests exercise real pre- and post-commit failures; JSON behaviour is unaffected.
