---
title: "Critique: issue 1362 inherited one correction"
description: Single final-candidate critique of the plan and details
author: Copilot
ms.date: 2026-11-10
ms.topic: reference
---

Executed once on the final candidate plan and details, by the author (no nested agent). Verdict: APPROVE with direct applications. No finding conflicts with a confirmed Root decision and none needs a user decision.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | `Locator.evaluate` is strict; a duplicated Design version panel would raise a Playwright error rather than a clear check failure. | Applied: assert the panel count is exactly one before evaluating. |
| 2 | The panels use `content-visibility: auto`; an unscrolled panel could report skipped content. | Applied: scroll the section into view first, as `panels()` does. |
| 3 | Exactness: normalising inner whitespace could hide `1 0`. | Applied: trim only; compare to `str(expected)` exactly; whitespace-only counts as blank. |
| 4 | A `dd` containing child markup (for example `1<span>0</span>`) must not match `1`. | Applied: use rendered `innerText`, not a prefix or substring; covered by the exactness check. |
| 5 | The unit doubles cannot exercise the in-page script. | Accepted and disclosed: the D1 DOM-mutation control against the real served page is the proof of the script; the units prove the Python decision logic. |
| 6 | Scope creep to the `Recorded by` and note assertions. | Rejected: unchanged and out of the authorised scope. |
| 7 | A second correction if the candidate browser run fails. | Rejected by authority: one inherited cycle only; a failure is preserved and reported, not self-retried. |
| 8 | The baseline must precede the edit and STOP if the false positive is absent. | Retained in Phase 1. |

No second critique will run for this task.
