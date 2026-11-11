---
title: Issue 131 inherited correction batch for the household inventory primitive (critique)
ms.date: 2026-11-10
task_id: 131-inherited-repair-1110
---

## Execution

One final-candidate critique, authored by the implementing session (not independent). It runs once for this task and is not repeated. Subject: the plan and details dated 2026-11-10 in `.copilot-tracking/plans/` and `.copilot-tracking/details/`, against the Root brief, the D1 handoff, the independent assessment 8f0786 and the current source.

Verdict: Proceed, with PC-001 to PC-005 applied directly. No finding conflicts with a confirmed decision and none needs a user decision.

## Findings and dispositions

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | Medium | Failing closed on the stored `identity_state` means a fully linked, current, verified inventory always lists the identity reason, because no existing action ever changes that field. A reader could take the permanent reason as a fault. | Applied: kept (it is the Root-required refusal of the supported Ambiguous path and nothing is inferred from verification text), stated in the Core README sentence and asserted in the test; no new identity action is added. |
| PC-002 | Medium | The history validator could grow into a full record schema (source, owner, dates, status). That broadens the batch and risks rejecting legitimate older records. | Applied: validate only what the findings require (position, case, rows, link and digest types). No other field, and no historical digest comparison. |
| PC-003 | Low | Refusing a present but empty history list is a new refusal; the view already reads it as Malformed, and the supported action never writes it. | Applied: deliberate, covered by an injected `[]` case, and the absent field still allows the first revision. |
| PC-004 | Low | Adopting main must not disturb the witness boundary or conflict with the README hunks. | Applied: the dry-run merge is clean; the ordinary merge happens after `implement-start`, before the source edits, and the README edit follows the merge. The composed baseline is run before the change. |
| PC-005 | Low | RV-001 (strengthening the API `scope_record` assertion) was in the D1 one-batch proposal but not in the Root brief. | Applied: left out of this batch and routed as a follow-up; the API selector is still run. |

## Confirmed constraints retained

No schema, endpoint, UI, role, shared store or adapter, authority model, roster, Legal interpretation or hold release. Reasons are counts only. The unconditional tenure hold, legacy unmanaged cases, resident negative answers and the privacy deletion behaviour are unchanged. Typing uses real types, with no `Any` casts, suppressions or ignores.
