---
title: Issue 1292 startup lock diagnostic plan critique
ms.date: 2026-11-09
---

## Verdict

Revise. One critique pass by an independent read-only reviewer (`rubber-duck`), executed once on the final candidate plan; no second critique runs. Findings were returned inline. None conflicts with a confirmed user decision and none needs a user decision.

## Findings and dispositions

* PC-001 Blocking. Editable installs and bytecode could write into the source tree, and the planned diff would not see ignored files. Disposition: applied. No editable install; worktree `src/*/src` on `PYTHONPATH`, bytecode writing disabled, and `git status --short --ignored` before and after.
* PC-002 Blocking. Method timing is not write-lock hold time. Disposition: applied. Hold time is derived only from `set_trace_callback` BEGIN IMMEDIATE and COMMIT/ROLLBACK events and labelled an inference; otherwise reported unknown.
* PC-003 Blocking. Synchronous logging or traceback formatting could perturb or mask. Disposition: applied. Buffered tuples, post-run formatting, guarded recorder, original exception re-raised, observer runs treated as perturbed evidence.
* PC-004 Non-blocking. A 3 s head start does not prove overlap with the opener threads. Disposition: applied. Actual intervals recorded; no overlap is inconclusive and still counts against the cap.
* PC-005 Non-blocking. H4 contradicted the assertion and the connect default timeout was missing. Disposition: applied in research.
