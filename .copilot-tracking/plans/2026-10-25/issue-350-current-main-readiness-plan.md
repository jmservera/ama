<!-- markdownlint-disable-file -->
---
title: Issue 350 current-main readiness plan
description: Prospective plan for a non-rewriting main merge and focused checks; written before critique and merge
ms.date: 2026-10-25
---

Prospective. Written after the research and before the critique and merge.

* [ ] Phase 1: one independent critique of this plan.
* [ ] Phase 2: merge `origin/main` (`ea5577b2`) into the branch with a merge commit (no rebase, amend, reset or force). Preserve branch history, both logs and current-main rubric scores as main has them. Resolve conflicts, if any, only by keeping main's content for main-owned files.
* [ ] Phase 3: focused checks from a throwaway venv built from `git archive` of the merged tree under `/tmp` and deleted afterwards, only if the existing `/tmp/c1-350/v` venv is stale: checker tests (`tools.test_check_demo_feedback`, expect at least 80), plus `src/core` seed-merge tests only if cheap and self-contained. No Docker, no SQL service, no gate. Available lint or type tools only if already installed.
* [ ] Phase 4: no source edit unless a focused check fails for a concrete, surgical reason; then a failing regression first and one correction cycle.
* [ ] Phase 5: one scoped independent assessment covering the merge result, the retained RecursionError and Application Administrator contract tests, and RV-201 re-verification. Write the changes, review and state records.
* [ ] Phase 6: commit records, stop. No full gate, push, PR or issue edit.

Stop conditions: any conflict that needs behaviour choices, a failed check not attributable to this branch, or a need for a human decision, which would be reported with evidence. Gate readiness and disk needs are reported only.
