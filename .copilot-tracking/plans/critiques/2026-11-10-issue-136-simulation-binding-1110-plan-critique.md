---
title: Issue 136 public simulation lane deployment binding plan critique
description: One author-inline final-candidate critique of the plan, with direct dispositions
ms.date: 2026-11-10
---

## Execution

One final-candidate critique of the [plan](../2026-11-10-issue-136-simulation-binding-1110-plan.md), performed by the author in the same session on 2026-11-10 before any source edit. No nested agent ran, so this is not an independent critique. It is not repeated. Verdict: `proceed with the dispositions below`.

## Findings and dispositions

* C1 Accounting claim must not rest on assertion. Disposition: applied directly. The tests assert `ZF_STORE=mssql`, the unchanged `AI_*` values and no sim path under `/state/mssql`, and the research records the source trace (`begin_call`, `fence_send`, `_settle` live in the working store). The remaining reliance, an operator-provisioned durable allowance in SQL, is stated as outside this template.
* C2 Command override could silently change startup for OFF. Disposition: applied. OFF renders `command: null` and the test compares the OFF container to the base contract; a one-time compile of the base template at `d52f20a5` is compared in the evidence.
* C3 A recipe that reads its paths from the environment would accept caller-supplied paths. Disposition: applied. Paths are literals in the recipe and the env values are asserted equal to them.
* C4 The recipe must not mask a state fault by reprovisioning. Disposition: applied. Provisioning runs only when neither file exists (`lexists`, so a dangling link counts as present); any other state goes to validation only.
* C5 A guard that merely names a combination can hide a missing propagation. Disposition: applied. Tests drive the guard arguments from the compiled main template (`failures(**overrides)`), not substrings.
* C6 Docker first-start ownership depends on the volume arrangement. Disposition: noted and bounded. The test uses an owned disposable named volume whose initial content and ownership come from the image `/state`; the README says Azure behaviour is not established.
* C7 Conflict with confirmed decisions: none found. Advice to add a durable mount, an init container or a CLI would conflict with the confirmed single-replica volatile selection and is rejected without re-asking.

## Significant or divergent issues requiring a user decision

None.
