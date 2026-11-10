---
title: Issue 136 binding C1 plan
description: Prospective plan for one bounded C1 fixing two independent Medium findings on the public simulation startup binding and retaining raw execution evidence
ms.date: 2026-11-10
---

## Provenance

Written after the [research](../research/2026-11-10-issue-136-binding-c1-1110-research.md) and before any source edit. Phase details: [details](../details/2026-11-10-issue-136-binding-c1-1110-details.md). The single critique, [critique](../challenges/2026-11-10-issue-136-binding-c1-1110-critique.md), is author-inline and not independent. Original artifacts are preserved unchanged.

## Scope

Refs #136 and #1288 only. Product files: `infra/modules/containerapps.bicep`, `infra/tests/test_public_simulation_startup.py`, `infra/README.md`. No other source, parameter set, Dockerfile, policy, model, budget, auth or scale change. No push, PR, rebase, merge, deployment or model call.

## Plan

* P1 Recipe (F1): move the `simulation_lane` import inside the existing `try`; paths, provision, `Lane.open` validation, error-code report and `os.execv` stay. No new fallback.
* P2 Test (F2): both `Lane.open` probes get the same explicit fixed clock; the rendered command is unchanged. Assert retained `store_id`, reading identity and readback across restart and `added == 0`. Negative control: the old real-clock style probe across a 300 second step fails the old assertion while persistence is intact. New import-failure case: the same rendered command on the actual image, with the module made unimportable through an owned harness input, still serves the ordinary API `/healthz`.
* P3 README: minimal clarification of the placeholder guard limit, the missing-module manual fallback and the test clock.
* P4 Evidence: owned venv; complete stdout, stderr and real exits under the external proof directory; image identity reuse; non-queued heavy lock; demo targeted tier checks with the repository pinned `ruff==0.17.1` isolated commands and relevant mypy.

## Acceptance

* Red before green for F1 (old recipe, import failure exits without serving) and F2 (old assertion fails when the slot crosses).
* All relevant regressions pass or adverse results are preserved.
* Whole #136, #1288, live, human and production criteria stay unmet.
