---
title: Issue 149 parent preparation for child 229, plan and critique
ms.date: 2026-11-07
---

## Plan (written before any merge or edit)

* Phase 1: normal merge of origin/test/ux-evidence-149 (dbeab436) into the local topic. Expected fast-forward; keep ancestry, no rebase, reset, amend or force.
* Phase 2: normal merge of origin/main (f0afa8d7) into the topic with a merge commit. Resolve only conflicts that provably preserve both intents; otherwise stop and record the exact unresolved intent. No speculative cleanup.
* Phase 3: compare main-relative source (`git diff origin/main...HEAD`, not the inverse) and verify the file list matches the 233/153 delta and that `doc_controls.py` differs only in message text.
* Phase 4: light checks only: own-source unit tests for atlas checker, content standard, document controls and role screens conformance, plus ruff and mypy over touched projects, with imports resolved to this worktree, PYTHONDONTWRITEBYTECODE and external caches. No browser, axe, SQL, containers, images, scans, `--changed`, `--all` or heavy lock.
* Phase 5: commit dated artifacts (changes, review, state) on this topic; no push, PR, tick or closing keyword.

## Critique (once, prospective)

* Risk: stale-ancestor local ref could tempt a rebase. Applied: normal merges only.
* Risk: the doc_controls change touches a deletion control. Applied: FOCUSED only if the main-relative diff is message-only, otherwise record FULL and stop.
* Risk: light tests could be read as acceptance. Applied: record they are engineering checks, not browser, WCAG, AT or user evidence.
* Risk: touching the heavy-lock holder (776680). Applied: no gate, no lock, no shared runtime.
* Verdict: proceed unchanged. No conflict with confirmed owner decisions.
