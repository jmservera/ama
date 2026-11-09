---
title: Ranking archive ancestor durability 1258 review
description: Single authored post-implementation review of issue 1258 LIGHT source preparation
ms.date: 2026-11-08
---

## Execution and boundary

Review execution: Complete (author review of the working diff against the plan and the critique dispositions; run once). Outcome: Residual work. FULL receipt and verification, independent exact-head assessment, hosted checks and human acceptance are all UNPERFORMED. Issue #1258 is not proven or closable.

## Verified

* Criterion 1: ancestors are synced before confirmation; first-run results unchanged (red and green tests, plan D3 to D5).
* Criterion 2: post-link ancestor failure raises `DurabilityUnconfirmedError`, record kept and valid, runner maps to `committed_unconfirmed`.
* Criterion 3: syscall-order and ancestor-failure regressions failed before the fix (7 failures) and pass after. Mocked ordering only.
* Criterion 4 (local): the 84 core and API ranking tests pass, covering retry, concurrent private stage, audit, path-free 409 and original date.
* Critique PC-001 to PC-006 dispositions held; the critique verdict Revise is preserved.

## Residual findings (routed, not repeated in this task)

* R1 (Medium) Real crash and live filesystem durability is unproven; mocks only.
* R2 (Low) Writable-parent boundary is a heuristic, not proof; the non-writable branch and root-run behavior lack a direct test (DV-3).
* R3 (Low) No API-level ancestor-fault test (DV-2).
* R4 (Low) Steady-state extra syncs (D5) need reviewer and owner visibility.
* R5 Criterion 5 gates (FULL `--all --base <current origin/main>` receipt and `--verify-receipt`, exact-head assessment, hosted checks) remain open; any later commit invalidates a receipt.
* R6 #1259 must consume this frozen source before its own source work.
