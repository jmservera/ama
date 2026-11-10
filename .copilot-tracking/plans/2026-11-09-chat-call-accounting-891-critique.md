---
title: Issue 891 chat call accounting critique
ms.date: 2026-11-09
task_id: issue-891-chat-call-accounting-1109
---

## Execution

* One critique, executed 2026-11-09 between 22:36Z and 22:37Z by an independent read-only `rubber-duck` subagent over the final-candidate research, plan and details, BEFORE any `src/` edit (tree clean except `.copilot-tracking/`). Never repeated for this task.
* Verdict: no blocking finding; the minimal fix is sound for the wired core `Ai` provider. Three findings, dispositioned directly below (no conflict with a confirmed user decision, no significant or divergent issue needing the owner).

## Findings and dispositions

| Severity | Finding | Disposition |
| --- | --- | --- |
| Significant | The `financial-held` and no `meter_id` rule assumes the envelope contract of the core `Ai`; `AgentWorker` accepts any provider, and another provider could return `financial-held` without `meter_id` after a transport. | Accepted. The rule is constrained and documented as the core provider envelope contract (a code comment at the function and a README sentence). Not enforceable in the adapter without a core marker; that marker is the named follow-up. Plan FR1 and FR4 amended below. |
| Significant | Details Step 4 commands used wrong working directories and the API `PYTHONPATH` omitted `tests`; `test_ai_consumption_api` starts a local HTTP stub. | Accepted. Commands corrected below to the README forms. Offline tests are preferred; a loopback-only owned stub is not the network or a provider, but if any module is excluded the exact exclusion is reported. |
| Non-blocking | `input-refused` is emitted before reserve and transport (`ai.py`, `InputRefused` docstring "no provider call is made") yet counts 1. | Accepted and folded in. `input-refused` joins `disabled` as a closed pre-call outcome with `calls=0`, with its own test case. Plan FR1 amended. |

## Amendments applied to the plan and details (22:37Z)

* FR1 now: `calls=0` for `disabled`, `input-refused`, and `financial-held` without `meter_id`; else 1. Comment and README state it is the core `Ai.evidence` envelope contract.
* Step 1 adds an `input-refused` case (adapter-level envelope). Step 4 commands corrected as in the details file.
* Conservative over-counts remain and are documented: `dispatch_check` hold with a reservation, and guard-denied `provider-unavailable` (no `meter_id`, indistinguishable from a provider exception).
