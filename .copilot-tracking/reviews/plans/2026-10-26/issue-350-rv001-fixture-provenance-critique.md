<!-- markdownlint-disable-file -->
---
title: Issue 350 RV-001 fixture provenance critique
description: Independent critique of the RV-001 plan, run before any source edit
ms.date: 2026-10-26
---

Independent read-only `rubber-duck` critique, run 2026-10-26 after research, plan and details were written (still untracked at the time) and before any source edit.

Verdict as returned: Revise.

* PC-501 (blocking): scripted AI text must name exactly the owned open P1-hazard case `ZF-4` with the resolvable citation `Open safety issues: 1`; otherwise `ai_priority` falls back to a template and the checker rejects it. Assert `source == "ai"`, `validated`, no `fallback_reason` and `release_denied` False before the checker runs.
* PC-502: use `sys.path.insert(0, ...)` for `src/core/tests` and assert the imported `dataset` and `release_support` files live in that directory.
* PC-503: assert the exact offline release id and version in the evidence, and that overall stays `blocked` and acceptance `not-accepted`.
* PC-504: add runtime negatives driving `_chat` with an unresolved citation and a non-hazard `ZF-1` item at `n=1`; assert runtime template fallback and checker rejection.

Disposition: all four accepted and applied prospectively to the implementation; the plan and details above are unchanged and this critique supersedes their wording where it differs. The sole critique for this task; no second critique.
