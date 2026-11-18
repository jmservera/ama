---
title: "Details: #215 provenance and audit contract test"
ms.date: 2026-11-14
---

## Phase 1

* Remove `# type: ignore[misc]` from the `roles.Matrix` subclasses in the three named tests.
* Add `sys.path.append(<tests dir>)` before `import test_role_matrix` so `python -m unittest tests.<module>` imports.

## Phase 2

* Case chat on ZF-4 for the unblock and visit questions: generative origin, decision-model origin, withheld unsupported draft, held turn; compare payload to stored message `model`/`evidence` and `chat.answer` audit outcome.
* Citation list integrity: non-empty for answers, unique, all `ZF-4/` ids.
* Receipts hold the outcome, contain no question text, the case record is unchanged and the ledger verifies.
* Regulatory chat: answered and held turns make no model call, held has empty citations, doubt receipt changes no record, two audit turn rows.

## Phase 3

Commands as given in the task; all three must exit 0.
