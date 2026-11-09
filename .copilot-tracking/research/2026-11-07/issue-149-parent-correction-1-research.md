---
title: Issue 149 parent corrective cycle 1, research
ms.date: 2026-11-07
---

## Research

* Original session 978d4601-9d13-4110-ac90-aea0eac18f18. Disposition: executed. Base: HEAD e2704c2b60192dee55441adf02f909d30ca68247, tree 1843217c0eb6623f1a7b8323cd8c11d6e11d6e2b, clean ignored-inclusive; origin/main b284d0d3e8ebed24d40bf9eb1e23de1ae9101d01.
* Input: independent functional review of e2704c2b (reviewer b47093e3, approve_with_comments, 0 Critical, 0 High, 1 Medium, 0 Low), finding 1, read from the original files, which stay untouched: functional-findings.json sha256 1e741e99...8562, metadata.json fdb2117a...89bf, review.md 2384ce68...8754 (folder review-149-e270-functional in session f751a4dc). The finding is not yet dynamically reproduced.
* Finding 1: src/api/checks/data_operator_browser_check.py selects failed rows with has_text=ai.NOT_A_MODEL_RESULT, the sentence it then validates. A failed_ai_run row whose What happened cell lacks that sentence drops out of the collection, so the check passes (checker false-negative, not a production defect).
* Stable semantics found: role-screens.js maps kind failed_ai_run to the Kind column label "Requested AI help did not deliver a model result" (no period; exceptionKinds, Kind is column 2 of 8, What happened is column 5) independent of exceptionHappened.
* Coupling search: only src/api/README.md names the checker; the manifest recipe pin names workbench_browser_check.py, not this file. No literal-byte pin found; re-searched before editing.
* Scope: checker, its Playwright-free helper and test file only. No product HTML, CSS, JS, server, auth, store, model, SQL, control or deletion change. Tier FOCUSED manual.
* Planning Readiness: Ready.
