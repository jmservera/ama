---
title: "Plan: #135 controlled recovery request"
ms.date: 2026-11-14
task_slug: 135-conflict-recovery-1844
---

## Phases

* [x] 1. Extract `_build_exception_queue` from `exception_register` so the register and recovery share one build.
* [x] 2. Add `request_exception_recovery`: named staff only, in role scope, allowed action per kind, reason up to 400 characters, owner-only `resolve_by_owner`, closed items refuse further requests; writes one `exception_recovery_requested` audit entry keyed `kind:ref`.
* [x] 3. Overlay latest request onto items (`status`, `recovery`, `recovery_key`) with replayed and released false.
* [x] 4. Add `POST /api/exceptions/recovery` (403 on scope, 400 on invalid input); list it in the role inventory.
* [x] 5. Tests in `src/api/tests/test_exception_register.py`; ruff check and format; focused unit tests.

## Critique (one pass, direct dispositions)

* Audit-ledger storage over a new SQL document: accepted (no schema or merge change, tamper-evident).
* Unstable `EX-` ids: rejected as keys; `kind:ref` used. Items without a ref cannot be recovered through this route and show `recovery_key: null`.
* No UI edit: `role-screens.js` untouched by owner direction; screen wiring is a follow-up.

## Validation tier

Focused tier: no workflow, dependency, SQL schema, permission or deployment change. The route adds an authenticated, audited, request-only action; no complete local gate run, stated here as not run.
