<!-- markdownlint-disable-file -->
---
title: Issue 350 RV-501 default fixture correction critique
description: Independent critique run before any source edit
ms.date: 2026-10-26
---

Independent read-only `rubber-duck` critique, 2026-10-26, after research and plan, before any source edit. Verdict as returned: Revise.

* PC-601 (blocking): the default runtime baseline for `ZF-1` has no prior contacts, so the oldest-first mutation test would lose its meaning. Build a runtime multi-contact baseline by writing prior contacts through `Store.log_call` first, capturing the tested write last.
* PC-602 (blocking): parameterize `RuntimeFixture.case_write(outcome, note, channel)` and pass to `Store.log_call`; the 120 character outcome is produced by the runtime, never patched into a cached default.
* PC-603: values such as timestamps, AI ids and ledger heads vary; the provenance regression must patch or spy the runtime factory (cache cleared) and assert the helper returns a deep copy of its output, not compare separately produced runs.
* PC-604: cached factories stay private; public `case_write()` and `ai_record()` always return `copy.deepcopy`; add a regression that mutating one fixture does not affect the next.
* PC-605: `restart=False` is a declaration change on a genuine runtime snapshot; the 40-contact cap fixture stays a named handcrafted boundary constructor, independent of the cached default; state both in comments.

Disposition: all accepted and applied prospectively; the plan's wording is superseded where it differs. Sole critique for this correction cycle.
