---
title: Issue 157 memory-as-evidence boundary review
ms.date: 2026-11-12
task_id: memory-evidence-boundary-157-1112
---

## Execution and outcome

One independent post-implementation Review (code-review agent, claude-sonnet-5.5, read-only) of commit `8ca313b15`, executed once. Original outcome: Findings (1 Low). It ran the new test twice (pass, no flake), confirmed boundary compliance (only `test_assistants.py` and the changes record changed), correct isolation (`patch.object` restores the provider attribute) and no overclaiming: the record states simulated provider and no human review, and the criterion stays unticked. The research conclusion matches the test. The reviewer did not rerun the other suites, lint, type checks or mutation checks; those results rest on the changes record.

## Original findings and routing

* RF-001 (Low): `assertNotIn(memory_id, canonical(refused["output"]))` evaluates `canonical(None)` after `output is None` is already asserted, so it cannot fail; the refusal proof rests on `state == "failed"` and `output is None`. The recorded mutation (removing the snapshot-citation check) does fail the step, so the proof holds in practice. Routed as a later optional tidy (drop the line or assert the failure reason names the unsupported citation), not applied here: the one Review is not repeated and no loop back to Implement occurs in this task.

## Assessed boundary

Local candidate only. Not assessed: hosted CI, MSSQL variant, any real provider or model, human review or production acceptance. Independent exact-head assessment by the coordinator remains required.
