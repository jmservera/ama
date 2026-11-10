---
title: Issue 136 binding C1 review
description: Single post-implementation review of the bounded C1 on the public simulation startup binding
ms.date: 2026-11-10
---

## Execution

Executed once after implementation, author-inline (no nested agent), so it is not independent. Root's same independent reviewer assesses the full C1 delta and the raw evidence before any publication. The earlier independent `approve_with_comments` disposition is recorded as input, not as C1 approval.

## Outcome: conformant for the two bounded findings, with disclosed residuals

* F1 resolved: the import is inside the existing `try`; red run 3 shows the old recipe exits on an unimportable module and the new recipe starts the ordinary API with `public simulation lane unavailable: ImportError` and no `/state/public-simulation` created. The error report prints only the code or type name. Paths, validation and `execv` are unchanged; policy test (60 tests) still pins the recipe tokens.
* F2 resolved: both probes share one pinned slot-aligned clock; store identity, readback digest and `added == 0` hold across restart; the slot-crossing negative control shows the old real-clock assertion is invalid (added 1 with the same store and no reset). The startup command is the compiled recipe, unmodified by the harness.
* Evidence retention: raw stdout, stderr, command and real exit per check are in the external proof directory; adverse runs are preserved.

## Residuals (routed, not fixed here)

* `infra/tests/test_bicep_policy.py` fails the workflow-pinned isolated `ruff check` (3 E501) and `ruff format --check`, and has 2 introduced `mypy` errors over a 3 error baseline. These come from the frozen original candidate; C1 scope forbids that file. Routed to a later user-selected change or Root decision.
* The shadow `sitecustomize` harness simulates a missing module, not a genuinely older image.
* Local container checks use the default JSON working store; no MSSQL, browser-auth, Azure or model evidence. Whole #136, #1288, live, human and production criteria stay unmet.
* Original `core.hooksPath` override disclosure remains; none in C1.
