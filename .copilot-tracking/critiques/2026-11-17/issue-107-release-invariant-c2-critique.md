---
title: Issue 107 release-invariant classifier correction critique
description: One independent critique of the C2 plan and its direct dispositions
ms.date: 2026-11-17
---

## Execution

Executed once by an independent read-only rubber-duck agent against the plan, details, probe `judge` and the test fixture. Verdict: Revise. No user decision required.

## Findings and dispositions

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | `status="ok"` is not completion; the worker can report ok after execute or reinvoke errors, giving a false violation | Applied. The mismatched-row audit requires status ok, at least one executed record, and no `error` in any executed or reinvoked record. Test added. |
| 2 | A missing bound ID hides a readable active row | Applied. Active detection and unreadability are independent; both are recorded. Test with both. |
| 3 | Malformed or missing row `status` could pass as non-active | Applied. A row whose status is not a string is unreadable (INSUFFICIENT). Test added. |
| 4 | Trigger readbacks not bound to the provisioned IDs | Applied. Revocation and mutation readbacks use only rows whose id is in the bound set. Test with an unrelated row. |
| 5 | Fixture mutated row is revoked rather than active before the worker (non-blocking) | Applied. `after_mutation` fixture row becomes active with the MUTATED version; ACCEPTED must still hold. |
