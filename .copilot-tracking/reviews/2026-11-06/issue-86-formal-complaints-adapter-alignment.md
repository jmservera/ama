---
title: Issue 86 formal-complaints adapter parent alignment record (2026-11-06)
ms.date: 2026-11-06
---

Scope: issue86 only. Supplements, and leaves intact, the original research, plan, critique, changes and author Review (now commits `dc585f7a4`, `e71ffa746`, `116ccd7ec`).

## Adverse evidence retained

* R1 full gate refused at preflight: `BLOCKED: Candidate does not descend from the reviewed main base` (exit 1, base `56eec736`, old head `67f043c4`). No group ran, no receipt exists. Evidence: `/mnt/ama-gates/e86-r1-1106/`.

## Alignment

* Pre-alignment identity kept as local branch `issue86-pre-align-67f043c` (HEAD `67f043c487d90c871d819f37d959ee8f0784b4f0`, tree `367e9df6`).
* Authorised local rebase: `git rebase --onto c5edb320ad10d3d73bb985bfb82b2d0bee94381a af891a5cccf730ccf61e670f312b7674218dbe4b`. Parent local head `c5edb320` (tree `4f2a712c`) has fresh `origin/main` `56eec736906774ef56d8c9a66ed7f3f9c1e520c6` as ancestor. No conflicts; parent branch and remote untouched; nothing published.
* Equivalence: `git range-diff` shows all 3 child commits `=` identical patches. Child diff against its parent is 11 files, 588 insertions, 2 deletions both before (against `af891a5c`) and after (against `c5edb320`).

## Author alignment review

Checked: only the three issue86 commits were replayed; no parent patch duplicated; tree is clean; ancestry of main and parent holds. Not checked: no test has been run at the new head by this record; earlier test results apply to the old head only and are not claimed here. The final full gate is the validation for the new tip. This is not independent assessment.
