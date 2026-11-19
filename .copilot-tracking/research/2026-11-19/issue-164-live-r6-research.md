---
title: Issue 164 live research r6 (2026-11-19)
description: Opening research record for the sixth demo re-check of issue 164
ms.date: 2026-11-19
---

Refs #164. Research disposition: executed. Scope: synthetic demo, desktop only, focused tier.

Unticked criteria (4 in RAI list plus the registration criterion): thresholds approved and chat task registered with reviewer and enable state; results bound to serving model with approved thresholds and reviewers; competent human exercises; actual-call authority.

Prior pass: `docs/reference/research/issue-164-live-20261119T0909Z-2026-11-19.md` concluded none is satisfiable by code. This pass re-tests that claim against the current code.

## Findings

* Registry (`evidence/2026-11-19/issue-164-live-r6/registry_offline.txt`): `chat-case-conversation` registered, `enabled` False, state disabled, `approval_state` unapproved, accountable function Retrofit Programme Manager, accountable individual `unknown`, thresholds `proposed`, `approved_by` and `approved_on` null.
* Offline tests: `test_chat_eval`, `test_chat_heldout`, `test_chat_eval_revocation_effort` 89 tests OK (`offline_tests.txt`).
* Read-only Azure (`az_readonly.txt`): `ca-cutover-test-demo-api` revision `--0000033`, digest prefix `sha256:5368f4e4009cc`, unchanged since pass r3.

Planning Readiness: Ready. Every remaining criterion needs an approval, named person, real-model result or competent human exercise. Setting `approved_by` or an individual in code would fabricate an approval; the code already reports `insufficient` and keeps the task disabled.
